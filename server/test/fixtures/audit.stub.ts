import { AuditEntity, DatabaseAction, EntityType } from '@app/infra/entities';
import { authStub } from './auth.stub';
import { dateStub } from './date.stub';

export const auditStub = {
  create: Object.freeze<AuditEntity>({
    id: 1,
    entityId: 'asset-created',
    action: DatabaseAction.CREATE,
    entityType: EntityType.ASSET,
    ownerId: authStub.admin.user.id,
    createdAt: dateStub.NOW,
  }),
  update: Object.freeze<AuditEntity>({
    id: 2,
    entityId: 'asset-updated',
    action: DatabaseAction.UPDATE,
    entityType: EntityType.ASSET,
    ownerId: authStub.admin.user.id,
    createdAt: dateStub.NOW,
  }),
  delete: Object.freeze<AuditEntity>({
    id: 3,
    entityId: 'asset-deleted',
    action: DatabaseAction.DELETE,
    entityType: EntityType.ASSET,
    ownerId: authStub.admin.user.id,
    createdAt: dateStub.NOW,
  }),
};
