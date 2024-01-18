import { PartnerEntity } from '@app/infra/entities';
import { dateStub } from './date.stub';
import { userStub } from './user.stub';

export const partnerStub = {
  adminToUser1: Object.freeze<PartnerEntity>({
    createdAt: dateStub.FEB_23_2023,
    updatedAt: dateStub.FEB_23_2023,
    sharedById: userStub.admin.id,
    sharedBy: userStub.admin,
    sharedWith: userStub.user1,
    sharedWithId: userStub.user1.id,
    inTimeline: true,
  }),
  user1ToAdmin1: Object.freeze<PartnerEntity>({
    createdAt: dateStub.FEB_23_2023,
    updatedAt: dateStub.FEB_23_2023,
    sharedBy: userStub.user1,
    sharedById: userStub.user1.id,
    sharedWithId: userStub.admin.id,
    sharedWith: userStub.admin,
    inTimeline: true,
  }),
};
