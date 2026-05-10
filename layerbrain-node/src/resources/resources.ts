import type { ListPage } from '../core/pagination.js';
import { MachineConnection } from '../machines/connection.js';
import { MachineTransport } from '../machines/transport.js';
import { ResourceBase, type JsonObject, type ListParams } from './base.js';

export class AccountsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/accounts', { page: 1, pageSize: 10, ...params });
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
    return this.listResource('/api-keys', { page: 1, pageSize: 10, ...params });
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

export class ComputeResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/compute', { page: 1, pageSize: 10, ...params });
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/compute/${encodeURIComponent(id)}`);
  }
}

export class EmbeddingsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/embeddings', body);
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
    return this.listResource('/machines', { page: 1, pageSize: 10, ...params });
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
    const headers: Record<string, string> = { 'x-layerbrain-source': 'api' };

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
    return this.listResource('/memberships', { page: 1, pageSize: 10, ...params });
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/memberships/${encodeURIComponent(id)}`);
  }
}

export class ModelsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/models', { page: 1, pageSize: 10, ...params });
  }

  retrieve(modelId: string): Promise<JsonObject> {
    return this.get(`/models/${encodeURIComponent(modelId)}`);
  }
}

export class NetworksResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/networks', { page: 1, pageSize: 10, ...params });
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/networks/${encodeURIComponent(id)}`, body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/networks/${encodeURIComponent(id)}`);
  }
}

export class NetworkRulesResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/network/rules', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/network/rules', { page: 1, pageSize: 10, ...params });
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(`/network/rules/${encodeURIComponent(id)}`);
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/network/rules/${encodeURIComponent(id)}`, body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/network/rules/${encodeURIComponent(id)}`);
  }
}

export class NetworkFlowsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/network/flows', { page: 1, pageSize: 10, ...params });
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/network/flows/${encodeURIComponent(id)}`);
  }
}

export class OrganizationsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/organizations', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/organizations', { page: 1, pageSize: 10, ...params });
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

export class SecretsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/secrets', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/secrets', { page: 1, pageSize: 10, ...params });
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
    return this.listResource('/statements', { page: 1, pageSize: 10, ...params });
  }

  retrieve(statementId: string): Promise<JsonObject> {
    return this.get(`/statements/${encodeURIComponent(statementId)}`);
  }
}

export class StorageResource extends ResourceBase {
  createBackend(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/storage/backends', body);
  }

  listBackends(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/storage/backends', { page: 1, pageSize: 10, ...params });
  }

  createBucket(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/storage/buckets', body);
  }

  listBuckets(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/storage/buckets', { page: 1, pageSize: 10, ...params });
  }

  deleteBackend(id: string): Promise<JsonObject> {
    return super.delete(`/storage/backends/${encodeURIComponent(id)}`);
  }

  updateBackend(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/storage/backends/${encodeURIComponent(id)}`, body);
  }

  retrieveBackend(id: string): Promise<JsonObject> {
    return this.get(`/storage/backends/${encodeURIComponent(id)}`);
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

  presignBucket(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/storage/buckets/${encodeURIComponent(id)}/presign`, body);
  }

  validateBackend(id: string): Promise<JsonObject> {
    return this.post(`/storage/backends/${encodeURIComponent(id)}/validate`, {});
  }
}

export class SubscriptionsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/subscriptions', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/subscriptions', { page: 1, pageSize: 10, ...params });
  }

  retrieve(subscriptionId: string): Promise<JsonObject> {
    return this.get(`/subscriptions/${encodeURIComponent(subscriptionId)}`);
  }
}

export class SnapshotsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/snapshots', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/snapshots', { page: 1, pageSize: 10, ...params });
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/snapshots/${encodeURIComponent(id)}`);
  }

  download(id: string): Promise<JsonObject> {
    return this.get(`/snapshots/${encodeURIComponent(id)}/download`);
  }

  restore(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/snapshots/${encodeURIComponent(id)}/restore`, body);
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

export class ToolsResource extends ResourceBase {
  webSearch(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/tools/web-search', body);
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
    return this.listResource('/webhooks', { page: 1, pageSize: 10, ...params });
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

  rotateSecret(id: string): Promise<JsonObject> {
    return this.post(`/webhooks/${encodeURIComponent(id)}/rotate-secret`, {});
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
    const headers: Record<string, string> = { 'x-layerbrain-source': 'api' };

    if (this.client.apiKey) {
      headers.Authorization = `Bearer ${this.client.apiKey}`;
    }

    return { url: `${wsBaseURL}/v1/webhooks${query}`, headers };
  }
}
