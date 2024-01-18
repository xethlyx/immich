import { albumStub, dateStub } from '@test';
import { mapAlbum } from './album-response.dto';

describe('mapAlbum', () => {
  it('should set start and end dates', () => {
    const dto = mapAlbum(albumStub.twoAssets, false);
    expect(dto.startDate).toEqual(dateStub.FEB_22_2023);
    expect(dto.endDate).toEqual(dateStub.FEB_23_2023);
  });

  it('should not set start and end dates for empty assets', () => {
    const dto = mapAlbum(albumStub.empty, false);
    expect(dto.startDate).toBeUndefined();
    expect(dto.endDate).toBeUndefined();
  });
});
