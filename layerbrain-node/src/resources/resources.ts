import type { ListPage } from '../core/pagination.js';
import { MachineConnection } from '../machines/connection.js';
import { MachineTransport } from '../machines/transport.js';
import { ResourceBase, type JsonObject, type ListParams } from './base.js';

export class AccountsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/accounts', params);
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(`/accounts/${encodeURIComponent(id)}`);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/accounts/${encodeURIComponent(id)}`);
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/accounts/${encodeURIComponent(id)}`, body);
  }
}

export class APIKeysResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/api-keys', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/api-keys', params);
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(`/api-keys/${encodeURIComponent(id)}`);
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/api-keys/${encodeURIComponent(id)}`, body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/api-keys/${encodeURIComponent(id)}`);
  }

  rotate(id: string): Promise<JsonObject> {
    return this.post(`/api-keys/${encodeURIComponent(id)}/rotate`, {});
  }
}

export class AudioResource extends ResourceBase {
  speech(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/audio/speech', body);
  }

  transcriptions(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/audio/transcriptions', body);
  }
}

export class BrainsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/brains', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/brains', params);
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(`/brains/${encodeURIComponent(id)}`);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/brains/${encodeURIComponent(id)}`);
  }

  archive(id: string): Promise<JsonObject> {
    return this.post(`/brains/${encodeURIComponent(id)}/archive`, {});
  }
}

export class EmbeddingsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/embeddings', body);
  }
}

export class ExportsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/exports', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/exports', params);
  }

  download(id: string): Promise<JsonObject> {
    return this.get(`/exports/${encodeURIComponent(id)}/download`);
  }
}

export class EventsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/events', params);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/events/${encodeURIComponent(id)}`);
  }
}

export class ImagesResource extends ResourceBase {
  edit(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/images/edits', body);
  }

  generate(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/images/generations', body);
  }
}

export class MachinesResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    const payload = { duration_minutes: 15, ...body };
    return this.post('/machines', payload);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/machines', params);
  }

  delete(machineId: string): Promise<JsonObject> {
    return super.delete(`/machines/${encodeURIComponent(machineId)}`);
  }

  retrieve(machineId: string): Promise<JsonObject> {
    return this.get(`/machines/${encodeURIComponent(machineId)}`);
  }

  extend(machineId: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/machines/${encodeURIComponent(machineId)}/extend`, body);
  }

  restore(machineId: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/machines/${encodeURIComponent(machineId)}/restore`, body);
  }

  snapshot(machineId: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/machines/${encodeURIComponent(machineId)}/snapshot`, body);
  }

  async connect(machineId: string): Promise<MachineConnection> {
    const baseURL = this.client.baseURL;
    let wsBaseURL: string;

    if (baseURL.startsWith('https://')) {
      wsBaseURL = `wss://${baseURL.slice('https://'.length)}`;
    } else if (baseURL.startsWith('http://')) {
      wsBaseURL = `ws://${baseURL.slice('http://'.length)}`;
    } else {
      wsBaseURL = `wss://${baseURL}`;
    }

    const url = `${wsBaseURL}/v1/machines/${encodeURIComponent(machineId)}/connect`;
    const headers: Record<string, string> = {};

    if (this.client.apiKey) {
      headers.Authorization = `Bearer ${this.client.apiKey}`;
    }

    const transport = await MachineTransport.connect(url, headers);
    return new MachineConnection(machineId, transport);
  }
}

export class MembershipsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/memberships', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/memberships', params);
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(`/memberships/${encodeURIComponent(id)}`);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/memberships/${encodeURIComponent(id)}`);
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/memberships/${encodeURIComponent(id)}`, body);
  }
}

export class ModelsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/models', params);
  }

  retrieve(modelId: string): Promise<JsonObject> {
    return this.get(`/models/${encodeURIComponent(modelId)}`);
  }
}

export class ComputeResource extends ResourceBase {
  computeDisabled(): Promise<JsonObject> {
    return this.get('/compute');
  }

  createComputeDisabled(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/compute', body);
  }

  updateComputeDisabled(body: JsonObject = {}): Promise<JsonObject> {
    return this.patch('/compute', body);
  }

  deleteComputeDisabled(): Promise<JsonObject> {
    return super.delete('/compute');
  }

  computePathDisabled(path: string): Promise<JsonObject> {
    return this.get(`/compute/${encodeURIComponent(path)}`);
  }

  createComputePathDisabled(path: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/compute/${encodeURIComponent(path)}`, body);
  }

  updateComputePathDisabled(path: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/compute/${encodeURIComponent(path)}`, body);
  }

  deleteComputePathDisabled(path: string): Promise<JsonObject> {
    return super.delete(`/compute/${encodeURIComponent(path)}`);
  }
}

export class OrganizationsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/organizations', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/organizations', params);
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(`/organizations/${encodeURIComponent(id)}`);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/organizations/${encodeURIComponent(id)}`);
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/organizations/${encodeURIComponent(id)}`, body);
  }
}

export class PlansResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/plans', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/plans', params);
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/plans/${encodeURIComponent(id)}`, body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/plans/${encodeURIComponent(id)}`);
  }

  addItems(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/plans/${encodeURIComponent(id)}/items`, body);
  }

  deleteItems(id: string): Promise<JsonObject> {
    return super.delete(`/plans/${encodeURIComponent(id)}/items`);
  }

  updateItems(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/plans/${encodeURIComponent(id)}/items`, body);
  }

  cancel(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/plans/${encodeURIComponent(id)}/cancel`, body);
  }

  createComment(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/plans/${encodeURIComponent(id)}/comments`, body);
  }

  listComments(id: string, params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource(`/plans/${encodeURIComponent(id)}/comments`, params);
  }

  listActivity(id: string, params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource(`/plans/${encodeURIComponent(id)}/activity`, params);
  }

  resume(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/plans/${encodeURIComponent(id)}/resume`, body);
  }

  start(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/plans/${encodeURIComponent(id)}/start`, body);
  }

  createItemComment(id: string, item: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/plans/${encodeURIComponent(id)}/items/${encodeURIComponent(item)}/comments`, body);
  }

  listItemComments(id: string, item: string, params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource(`/plans/${encodeURIComponent(id)}/items/${encodeURIComponent(item)}/comments`, params);
  }

  listItemActivity(id: string, item: string, params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource(`/plans/${encodeURIComponent(id)}/items/${encodeURIComponent(item)}/activity`, params);
  }
}

export class WorkResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/work', params);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/work/${encodeURIComponent(id)}`);
  }
}

export class SecretsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/secrets', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/secrets', params);
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(`/secrets/${encodeURIComponent(id)}`);
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/secrets/${encodeURIComponent(id)}`, body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/secrets/${encodeURIComponent(id)}`);
  }

  reveal(id: string): Promise<JsonObject> {
    return this.get(`/secrets/${encodeURIComponent(id)}/reveal`);
  }
}

export class StatementsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/statements', params);
  }

  retrieve(statementId: string): Promise<JsonObject> {
    return this.get(`/statements/${encodeURIComponent(statementId)}`);
  }
}

export class StorageResource extends ResourceBase {
  createBucket(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/storage/buckets', body);
  }

  listBuckets(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/storage/buckets', params);
  }

  searchStorageObjects(): Promise<JsonObject> {
    return this.get('/storage/objects/search');
  }

  deleteBucket(id: string): Promise<JsonObject> {
    return super.delete(`/storage/buckets/${encodeURIComponent(id)}`);
  }

  updateBucket(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/storage/buckets/${encodeURIComponent(id)}`, body);
  }

  retrieveBucket(id: string): Promise<JsonObject> {
    return this.get(`/storage/buckets/${encodeURIComponent(id)}`);
  }

  deleteBucketKey(id: string): Promise<JsonObject> {
    return super.delete(`/storage/keys/${encodeURIComponent(id)}`);
  }

  createBucketFolder(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/storage/buckets/${encodeURIComponent(id)}/folders`, body);
  }

  createBucketKey(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/storage/buckets/${encodeURIComponent(id)}/keys`, body);
  }

  listBucketKeys(id: string, params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource(`/storage/buckets/${encodeURIComponent(id)}/keys`, params);
  }

  listBucketObjects(id: string, params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource(`/storage/buckets/${encodeURIComponent(id)}/objects`, params);
  }

  presignBucket(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/storage/buckets/${encodeURIComponent(id)}/presign`, body);
  }

  copyBucketObject(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/storage/buckets/${encodeURIComponent(id)}/objects/copy`, body);
  }

  deleteBucketObject(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/storage/buckets/${encodeURIComponent(id)}/objects/delete`, body);
  }

  headBucketObject(id: string): Promise<JsonObject> {
    return this.get(`/storage/buckets/${encodeURIComponent(id)}/objects/head`);
  }

  moveBucketObject(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/storage/buckets/${encodeURIComponent(id)}/objects/move`, body);
  }
}

export class SubscriptionsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/subscriptions', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/subscriptions', params);
  }

  retrieve(subscriptionId: string): Promise<JsonObject> {
    return this.get(`/subscriptions/${encodeURIComponent(subscriptionId)}`);
  }
}

export class SnapshotsResource extends ResourceBase {
  snapshotsDisabled(): Promise<JsonObject> {
    return this.get('/snapshots');
  }

  createSnapshotsDisabled(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/snapshots', body);
  }

  updateSnapshotsDisabled(body: JsonObject = {}): Promise<JsonObject> {
    return this.patch('/snapshots', body);
  }

  deleteSnapshotsDisabled(): Promise<JsonObject> {
    return super.delete('/snapshots');
  }

  snapshotsPathDisabled(path: string): Promise<JsonObject> {
    return this.get(`/snapshots/${encodeURIComponent(path)}`);
  }

  createSnapshotsPathDisabled(path: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/snapshots/${encodeURIComponent(path)}`, body);
  }

  updateSnapshotsPathDisabled(path: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/snapshots/${encodeURIComponent(path)}`, body);
  }

  deleteSnapshotsPathDisabled(path: string): Promise<JsonObject> {
    return super.delete(`/snapshots/${encodeURIComponent(path)}`);
  }
}

export class ThreeDResource extends ResourceBase {
  generate(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/3d/generations', body);
  }

  retrieve(generationId: string): Promise<JsonObject> {
    return this.get(`/3d/generations/${encodeURIComponent(generationId)}`);
  }
}

export class VideosResource extends ResourceBase {
  generate(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/videos/generations', body);
  }

  retrieve(generationId: string): Promise<JsonObject> {
    return this.get(`/videos/generations/${encodeURIComponent(generationId)}`);
  }
}

export class WebhooksResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/webhooks', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/webhooks', params);
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(`/webhooks/${encodeURIComponent(id)}`);
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/webhooks/${encodeURIComponent(id)}`, body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/webhooks/${encodeURIComponent(id)}`);
  }

  deliveries(id: string): Promise<JsonObject> {
    return this.get(`/webhooks/${encodeURIComponent(id)}/deliveries`);
  }

  rotateSecret(id: string): Promise<JsonObject> {
    return this.post(`/webhooks/${encodeURIComponent(id)}/rotate-secret`, {});
  }

  signingSecret(id: string): Promise<JsonObject> {
    return this.get(`/webhooks/${encodeURIComponent(id)}/signing-secret`);
  }

  test(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/webhooks/${encodeURIComponent(id)}/test`, body);
  }

  delivery(id: string, deliveryId: string): Promise<JsonObject> {
    return this.get(`/webhooks/${encodeURIComponent(id)}/deliveries/${encodeURIComponent(deliveryId)}`);
  }

  listenRequest(options: { events?: string | string[] } = {}): { url: string; headers: Record<string, string> } {
    const baseURL = this.client.baseURL;
    let wsBaseURL: string;

    if (baseURL.startsWith('https://')) {
      wsBaseURL = `wss://${baseURL.slice('https://'.length)}`;
    } else if (baseURL.startsWith('http://')) {
      wsBaseURL = `ws://${baseURL.slice('http://'.length)}`;
    } else {
      wsBaseURL = `wss://${baseURL}`;
    }

    const rawEvents = Array.isArray(options.events)
      ? options.events.map((event) => event.trim()).filter(Boolean).join(',')
      : options.events?.trim();
    const query = rawEvents ? `?events=${encodeURIComponent(rawEvents)}` : '';
    const headers: Record<string, string> = {};

    if (this.client.apiKey) {
      headers.Authorization = `Bearer ${this.client.apiKey}`;
    }

    return { url: `${wsBaseURL}/v1/webhooks${query}`, headers };
  }
}
