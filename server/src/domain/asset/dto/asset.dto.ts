import { IsBoolean, IsString } from 'class-validator';
import { Optional, ValidateUUID } from '../../domain.util';
import { BulkIdsDto } from '../response-dto';

export class AssetBulkUpdateDto extends BulkIdsDto {
  @Optional()
  @IsBoolean()
  isFavorite?: boolean;

  @Optional()
  @IsBoolean()
  isArchived?: boolean;
}

export class UpdateAssetDto {
  @Optional()
  @IsBoolean()
  isFavorite?: boolean;

  @Optional()
  @IsBoolean()
  isArchived?: boolean;

  @Optional()
  @IsString()
  description?: string;
}

export class DeviceIdDto {
  @ValidateUUID()
  deviceId!: string;
}
