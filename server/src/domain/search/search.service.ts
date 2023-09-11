import { AlbumEntity, AssetEntity, AssetFaceEntity } from '@app/infra/entities';
import { Inject, Injectable, Logger } from '@nestjs/common';
import { mapAlbumWithAssets } from '../album';
import { IAlbumRepository } from '../album/album.repository';
import { AssetResponseDto, mapAsset } from '../asset';
import { IAssetRepository } from '../asset/asset.repository';
import { AuthUserDto } from '../auth';
import { usePagination } from '../domain.util';
import { AssetFaceId, IFaceRepository } from '../facial-recognition';
import { IAssetFaceJob, IBulkEntityJob, IJobRepository, JOBS_ASSET_PAGINATION_SIZE, JobName } from '../job';
import { IMachineLearningRepository } from '../smart-info';
import { FeatureFlag, ISystemConfigRepository, SystemConfigCore } from '../system-config';
import { SearchDto } from './dto';
import { SearchResponseDto } from './response-dto';
import {
  ISearchRepository,
  OwnedFaceEntity,
  SearchCollection,
  SearchExploreItem,
  SearchResult,
  SearchStrategy,
} from './search.repository';

interface SyncQueue {
  upsert: Set<string>;
  delete: Set<string>;
}

@Injectable()
export class SearchService {
  private logger = new Logger(SearchService.name);
  private configCore: SystemConfigCore;


  constructor(
    @Inject(IAssetRepository) private assetRepository: IAssetRepository,
    @Inject(ISystemConfigRepository) configRepository: ISystemConfigRepository,
    @Inject(IMachineLearningRepository) private machineLearning: IMachineLearningRepository,
  ) {
    this.configCore = new SystemConfigCore(configRepository);
  }

  async getExploreData(authUser: AuthUserDto): Promise<SearchExploreItem<AssetResponseDto>[]> {
    return []
  }

  async search(authUser: AuthUserDto, dto: SearchDto): Promise<SearchResponseDto> {
    const { machineLearning } = await this.configCore.getConfig();
    await this.configCore.requireFeature(FeatureFlag.SEARCH);

    const query = dto.q || dto.query || '*';
    const hasClip = machineLearning.enabled && machineLearning.clip.enabled;
    const strategy = dto.clip && hasClip ? SearchStrategy.CLIP : SearchStrategy.TEXT;

    let assets: AssetEntity[];
    let ids;
    switch (strategy) {
      case SearchStrategy.CLIP:
        const {
          machineLearning: { clip },
        } = await this.configCore.getConfig();
        ids = await this.machineLearning.encodeText(machineLearning.url, { text: query }, { ...clip, index_name: `${authUser.id}-${JobName.ENCODE_CLIP}`, k: 100 }) as string[];
        assets = await this.assetRepository.getByIds(ids)
        break;
      case SearchStrategy.TEXT:
      default:
        throw new Error('Not implemented');
    }

    return {
      albums: {
        total: 0,
        count: 0,
        items: [],
        facets: [],
      },
      assets: {
        total: assets.length,
        count: assets.length,
        items: assets
          .filter((asset) => !!asset)
          .map(mapAsset),
        facets: []
      }
    };
  }
}
