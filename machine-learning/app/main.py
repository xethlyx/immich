import asyncio
from functools import partial
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Type
from zipfile import BadZipFile

import faiss
import numpy as np
import orjson
from fastapi import Depends, FastAPI, Form, HTTPException, UploadFile
from fastapi.responses import ORJSONResponse
from onnxruntime.capi.onnxruntime_pybind11_state import InvalidProtobuf, NoSuchFile  # type: ignore
from starlette.formparsers import MultiPartParser

from app.models.base import InferenceModel

from .config import log, settings
from .models.cache import ModelCache
from .schemas import (
    MessageResponse,
    ModelType,
    TextResponse,
)

MultiPartParser.max_file_size = 2**24  # spools to disk if payload is 16 MiB or larger
app = FastAPI()
vector_stores: dict[str, faiss.IndexIDMap2] = {}


class VectorStore:
    def __init__(self, dims: int, index_cls: Type[faiss.Index] = faiss.IndexHNSWFlat, **kwargs: Any) -> None:
        self.index = index_cls(dims, **kwargs)
        self.id_to_key: dict[int, Any] = {}

    def search(self, embeddings: np.ndarray[int, np.dtype[Any]], k: int) -> list[Any]:
        ids = self.index.assign(embeddings, k)  # type: ignore
        return [self.id_to_key[idx] for row in ids.tolist() for idx in row if not idx == -1]

    def add_with_ids(self, embeddings: np.ndarray[int, np.dtype[Any]], embedding_ids: list[Any]) -> None:
        self.id_to_key |= {
            id: key for id, key in zip(embedding_ids, range(self.index.ntotal, self.index.ntotal + len(embedding_ids)))
        }
        self.index.add(embeddings)  # type: ignore


def validate_embeddings(embeddings: list[float]) -> Any:
    embeddings = np.array(embeddings)
    if len(embeddings.shape) == 1:
        embeddings = np.expand_dims(embeddings, 0)
    elif len(embeddings.shape) != 2:
        raise HTTPException(400, f"Expected one or two axes for embeddings; got {len(embeddings.shape)}")
    if embeddings.shape[1] < 10:
        raise HTTPException(400, f"Dimension size must be at least 10; got {embeddings.shape[1]}")
    return embeddings


def init_state() -> None:
    app.state.model_cache = ModelCache(ttl=settings.model_ttl, revalidate=settings.model_ttl > 0)
    log.info(
        (
            "Created in-memory cache with unloading "
            f"{f'after {settings.model_ttl}s of inactivity' if settings.model_ttl > 0 else 'disabled'}."
        )
    )
    # asyncio is a huge bottleneck for performance, so we use a thread pool to run blocking code
    app.state.thread_pool = ThreadPoolExecutor(settings.request_threads) if settings.request_threads > 0 else None
    app.state.model_locks = {model_type: threading.Lock() for model_type in ModelType}
    app.state.index_lock = threading.Lock()
    log.info(f"Initialized request thread pool with {settings.request_threads} threads.")


@app.on_event("startup")
async def startup_event() -> None:
    init_state()


@app.get("/", response_model=MessageResponse)
async def root() -> dict[str, str]:
    return {"message": "Immich ML"}


@app.get("/ping", response_model=TextResponse)
def ping() -> str:
    return "pong"


@app.post("/pipeline", response_class=ORJSONResponse)
async def pipeline(
    model_name: str = Form(alias="modelName"),
    model_type: ModelType = Form(alias="modelType"),
    options: str = Form(default="{}"),
    text: str | None = Form(default=None),
    image: UploadFile | None = None,
    index_name: str | None = Form(default=None),
    embedding_id: str | None = Form(default=None),
    k: int | None = Form(default=None),
) -> ORJSONResponse:
    if image is not None:
        inputs: str | bytes = await image.read()
    elif text is not None:
        inputs = text
    else:
        raise HTTPException(400, "Either image or text must be provided")
    try:
        kwargs = orjson.loads(options)
    except orjson.JSONDecodeError:
        raise HTTPException(400, f"Invalid options JSON: {options}")

    outputs = await _predict(model_name, model_type, inputs, **kwargs)
    if index_name is not None:
        if k is not None:
            if k < 1:
                raise HTTPException(400, f"k must be a positive integer; got {k}")
            if index_name not in vector_stores:
                raise HTTPException(404, f"Index '{index_name}' not found")
            outputs = await run(vector_stores[index_name].search, outputs, k)
        if embedding_id is not None:
            if index_name not in vector_stores:
                await create(index_name, [embedding_id], outputs)
            else:
                await run(vector_stores[index_name].add, [embedding_id], outputs)
    return ORJSONResponse(outputs)


@app.post("/predict", response_class=ORJSONResponse)
async def predict(
    model_name: str = Form(alias="modelName"),
    model_type: ModelType = Form(alias="modelType"),
    options: str = Form(default="{}"),
    text: str | None = Form(default=None),
    image: UploadFile | None = None,
) -> ORJSONResponse:
    if image is not None:
        inputs: str | bytes = await image.read()
    elif text is not None:
        inputs = text
    else:
        raise HTTPException(400, "Either image or text must be provided")
    try:
        kwargs = orjson.loads(options)
    except orjson.JSONDecodeError:
        raise HTTPException(400, f"Invalid options JSON: {options}")

    outputs = await _predict(model_name, model_type, inputs, **kwargs)
    return ORJSONResponse(outputs)


@app.post("/index/{index_name}/search", response_class=ORJSONResponse)
async def search(index_name: str, embeddings: Any = Depends(validate_embeddings), k: int = 10) -> ORJSONResponse:
    if index_name not in vector_stores or vector_stores[index_name].d != embeddings.shape[1]:
        raise HTTPException(404, f"Index '{index_name}' not found")
    outputs: np.ndarray[int, np.dtype[Any]] = await run(vector_stores[index_name].search, embeddings, k)
    return ORJSONResponse(outputs)


@app.post("/index/{index_name}/add")
async def add(
    index_name: str,
    embedding_ids: list[str],
    embeddings: Any = Depends(validate_embeddings),
) -> None:
    if index_name not in vector_stores or vector_stores[index_name].d != embeddings.shape[1]:
        await create(index_name, embedding_ids, embeddings)
    else:
        await run(vector_stores[index_name].add_with_ids, embeddings, embedding_ids)


@app.post("/index/{index_name}/create")
async def create(
    index_name: str,
    embedding_ids: list[str],
    embeddings: Any = Depends(validate_embeddings),
) -> None:
    if embeddings.shape[0] != len(embedding_ids):
        raise HTTPException(400, "Number of embedding IDs must match number of embeddings")
    if index_name in vector_stores:
        log.warn(f"Index '{index_name}' already exists. Overwriting.")

    vector_stores[index_name] = await run(_create)


async def run(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    if app.state.thread_pool is None:
        return func(*args, **kwargs)
    if kwargs:
        func = partial(func, **kwargs)
    return await asyncio.get_running_loop().run_in_executor(app.state.thread_pool, func, *args)


def _load(model: InferenceModel) -> InferenceModel:
    if model.loaded:
        return model

    try:
        with app.state.model_locks[model.model_type]:
            if not model.loaded:
                model.load()
    except (OSError, InvalidProtobuf, BadZipFile, NoSuchFile):
        log.warn(
            (
                f"Failed to load {model.model_type.replace('_', ' ')} model '{model.model_name}'."
                "Clearing cache and retrying."
            )
        )
        model.clear_cache()
        model.load()
    return model


async def _predict(
    model_name: str, model_type: ModelType, inputs: Any, **options: Any
) -> np.ndarray[int, np.dtype[np.float32]]:
    model = await app.state.model_cache.get(model_name, model_type, **options)
    if not model.loaded:
        await run(_load, model)
    model.configure(**options)
    return await run(model.predict, inputs)


def _create(
    embedding_ids: list[str],
    embeddings: np.ndarray[int, np.dtype[np.float32]],
) -> VectorStore:
    index = VectorStore(embeddings.shape[1])

    with app.state.index_lock:
        index.add_with_ids(embeddings, embedding_ids)  # type: ignore
    return index
