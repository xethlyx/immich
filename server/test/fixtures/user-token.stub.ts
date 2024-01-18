import { UserTokenEntity } from '@app/infra/entities';
import { dateStub } from './date.stub';
import { userStub } from './user.stub';

export const userTokenStub = {
  userToken: Object.freeze<UserTokenEntity>({
    id: 'token-id',
    token: 'auth_token',
    userId: userStub.user1.id,
    user: userStub.user1,
    createdAt: dateStub.JAN_01_2021,
    updatedAt: dateStub.NOW,
    deviceType: '',
    deviceOS: '',
  }),
  inactiveToken: Object.freeze<UserTokenEntity>({
    id: 'not_active',
    token: 'auth_token',
    userId: userStub.user1.id,
    user: userStub.user1,
    createdAt: dateStub.JAN_01_2021,
    updatedAt: dateStub.JAN_01_2021,
    deviceType: 'Mobile',
    deviceOS: 'Android',
  }),
};
