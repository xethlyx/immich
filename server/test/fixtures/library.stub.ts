import { LibraryEntity, LibraryType } from '@app/infra/entities';
import { dateStub } from './date.stub';
import { userStub } from './user.stub';

export const libraryStub = {
  uploadLibrary1: Object.freeze<LibraryEntity>({
    id: 'library-id',
    name: 'test_library',
    assets: [],
    owner: userStub.user1,
    ownerId: 'user-id',
    type: LibraryType.UPLOAD,
    importPaths: [],
    createdAt: dateStub.JAN_01_2021,
    updatedAt: dateStub.JAN_01_2021,
    refreshedAt: null,
    isVisible: true,
    exclusionPatterns: [],
  }),
  externalLibrary1: Object.freeze<LibraryEntity>({
    id: 'library-id',
    name: 'test_library',
    assets: [],
    owner: userStub.externalPath1,
    ownerId: 'user-id',
    type: LibraryType.EXTERNAL,
    importPaths: [],
    createdAt: dateStub.JAN_01_2023,
    updatedAt: dateStub.JAN_01_2023,
    refreshedAt: null,
    isVisible: true,
    exclusionPatterns: [],
  }),
};
