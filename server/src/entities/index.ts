import { ActivityEntity } from 'src/entities/activity.entity';
import { AlbumEntity } from 'src/entities/album.entity';
import { APIKeyEntity } from 'src/entities/api-key.entity';
import { AssetFaceEntity } from 'src/entities/asset-face.entity';
import { AssetJobStatusEntity } from 'src/entities/asset-job-status.entity';
import { AssetStackEntity } from 'src/entities/asset-stack.entity';
import { AssetEntity } from 'src/entities/asset.entity';
import { AuditEntity } from 'src/entities/audit.entity';
import { ExifEntity } from 'src/entities/exif.entity';
import { GeodataPlacesEntity } from 'src/entities/geodata-places.entity';
import { LibraryEntity } from 'src/entities/library.entity';
import { MemoryEntity } from 'src/entities/memory.entity';
import { MoveEntity } from 'src/entities/move.entity';
import { PartnerEntity } from 'src/entities/partner.entity';
import { PersonEntity } from 'src/entities/person.entity';
import { SharedLinkEntity } from 'src/entities/shared-link.entity';
import { SmartInfoEntity } from 'src/entities/smart-info.entity';
import { SmartSearchEntity } from 'src/entities/smart-search.entity';
import { SystemConfigEntity } from 'src/entities/system-config.entity';
import { SystemMetadataEntity } from 'src/entities/system-metadata.entity';
import { TagEntity } from 'src/entities/tag.entity';
import { UserTokenEntity } from 'src/entities/user-token.entity';
import { UserEntity } from 'src/entities/user.entity';

export const databaseEntities = [
  ActivityEntity,
  AlbumEntity,
  APIKeyEntity,
  AssetEntity,
  AssetStackEntity,
  AssetFaceEntity,
  AssetJobStatusEntity,
  AuditEntity,
  ExifEntity,
  GeodataPlacesEntity,
  MemoryEntity,
  MoveEntity,
  PartnerEntity,
  PersonEntity,
  SharedLinkEntity,
  SmartInfoEntity,
  SmartSearchEntity,
  SystemConfigEntity,
  SystemMetadataEntity,
  TagEntity,
  UserEntity,
  UserTokenEntity,
  LibraryEntity,
];
