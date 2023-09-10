import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any
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


def validate_embeddings(embeddings: list[float] | np.ndarray[int, np.dtype[Any]]) -> np.ndarray[int, np.dtype[Any]]:
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


@app.post("/predict")
async def predict(
    model_name: str = Form(alias="modelName"),
    model_type: ModelType = Form(alias="modelType"),
    options: str = Form(default="{}"),
    text: str | None = Form(default=None),
    image: UploadFile | None = None,
) -> Any:
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

    model = await load(await app.state.model_cache.get(model_name, model_type, **kwargs))
    model.configure(**kwargs)
    outputs = await run(model, inputs)
    return ORJSONResponse(outputs)


@app.post("/index/{index_name}/search")
async def search(
    index_name: str, embeddings: np.ndarray[int, np.dtype[np.float32]] = Depends(validate_embeddings), k: int = 10
) -> None:
    if index_name not in vector_stores or vector_stores[index_name].d != embeddings.shape[1]:
        raise HTTPException(404, f"Index '{index_name}' not found")
    return vector_stores[index_name].search(embeddings, k)[1]  # type: ignore


@app.patch("/index/{index_name}/add")
async def add(
    index_name: str,
    embedding_ids: list[str],
    embeddings: np.ndarray[int, np.dtype[np.float32]] = Depends(validate_embeddings),
) -> None:
    if index_name not in vector_stores or vector_stores[index_name].d != embeddings.shape[1]:
        await create(index_name, embedding_ids, embeddings)
    else:
        vector_stores[index_name].add_with_ids(embeddings, embedding_ids)  # type: ignore


@app.post("/index/{index_name}/create")
async def create(
    index_name: str,
    embedding_ids: list[str],
    embeddings: np.ndarray[int, np.dtype[np.float32]] = Depends(validate_embeddings),
) -> None:
    if embeddings.shape[0] != len(embedding_ids):
        raise HTTPException(400, "Number of embedding IDs must match number of embeddings")
    if index_name in vector_stores:
        log.warn(f"Index '{index_name}' already exists. Overwriting.")

    hnsw_index = faiss.IndexHNSWFlat(embeddings.shape[1])
    mapped_index = faiss.IndexIDMap2(hnsw_index)

    def _create() -> faiss.IndexIDMap2:
        with app.state.index_lock:
            mapped_index.add_with_ids(embeddings, embedding_ids)  # type: ignore
        return mapped_index

    vector_stores[index_name] = await asyncio.get_running_loop().run_in_executor(app.state.thread_pool, _create)


async def run(model: InferenceModel, inputs: Any) -> Any:
    if app.state.thread_pool is None:
        return model.predict(inputs)

    return await asyncio.get_running_loop().run_in_executor(app.state.thread_pool, model.predict, inputs)


async def load(model: InferenceModel) -> InferenceModel:
    if model.loaded:
        return model

    def _load() -> None:
        with app.state.locks[model.model_type]:
            model.load()

    loop = asyncio.get_running_loop()
    try:
        if app.state.thread_pool is None:
            model.load()
        else:
            await loop.run_in_executor(app.state.thread_pool, _load)
        return model
    except (OSError, InvalidProtobuf, BadZipFile, NoSuchFile):
        log.warn(
            (
                f"Failed to load {model.model_type.replace('_', ' ')} model '{model.model_name}'."
                "Clearing cache and retrying."
            )
        )
        model.clear_cache()
        if app.state.thread_pool is None:
            model.load()
        else:
            await loop.run_in_executor(app.state.thread_pool, _load)
        return model
