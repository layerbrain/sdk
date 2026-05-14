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

export class ExportsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/exports', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/exports', { page: 1, pageSize: 10, ...params });
  }

  download(id: string): Promise<JsonObject> {
    return this.get(`/exports/${encodeURIComponent(id)}/download`);
  }
}

export class EventsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/events', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/events', { page: 1, pageSize: 10, ...params });
  }

  types(): Promise<JsonObject> {
    return this.get('/events/types');
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/events/${encodeURIComponent(id)}`);
  }
}

export class MachinesResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/machines', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/machines', { page: 1, pageSize: 10, ...params });
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(`/machines/${encodeURIComponent(id)}`);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/machines/${encodeURIComponent(id)}`);
  }

  extend(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/machines/${encodeURIComponent(id)}/extend`, body);
  }

  private websocketURL(path: string): string {
    const baseURL = this.client.baseURL;
    let wsBaseURL: string;

    if (baseURL.startsWith('https://')) {
      wsBaseURL = `wss://${baseURL.slice('https://'.length)}`;
    } else if (baseURL.startsWith('http://')) {
      wsBaseURL = `ws://${baseURL.slice('http://'.length)}`;
    } else {
      wsBaseURL = `wss://${baseURL}`;
    }

    return `${wsBaseURL}/v1${path}`;
  }

  private websocketHeaders(): Record<string, string> {
    if (!this.client.apiKey) {
      throw new Error('No API key provided. Set LAYERBRAIN_API_KEY or pass apiKey to the client.');
    }

    return {
      Authorization: `Bearer ${this.client.apiKey}`,
      'x-layerbrain-source': 'api',
    };
  }

  async connect(machineId: string): Promise<MachineConnection> {
    const url = this.websocketURL(`/machines/${encodeURIComponent(machineId)}`);
    const transport = await MachineTransport.connect(url, this.websocketHeaders());
    return new MachineConnection(machineId, transport);
  }

  async createConnection(body: JsonObject = {}): Promise<MachineConnection> {
    const transport = await MachineTransport.connect(
      this.websocketURL('/machines'),
      this.websocketHeaders(),
    );
    try {
      const machine = await transport.send('machine.create', {
        body,
        timeout: 30_000,
      }) as JsonObject;
      const machineId = typeof machine.id === 'string' ? machine.id : '';
      if (!machineId) {
        await transport.close();
        throw new Error('Machine create response did not include an id.');
      }
      return new MachineConnection(machineId, transport);
    } catch (error) {
      await transport.close();
      throw error;
    }
  }

  async run(body: JsonObject = {}, params: JsonObject = {}): Promise<JsonObject> {
    const transport = await MachineTransport.connect(
      this.websocketURL('/machines'),
      this.websocketHeaders(),
    );
    try {
      return (await transport.send('machine.run', {
        body: {
          ...body,
          command: params,
        },
        timeout: 30_000,
      }) as JsonObject) ?? {};
    } finally {
      await transport.close();
    }
  }
}

export class LogsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/logs', { page: 1, pageSize: 10, ...params });
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/logs/${encodeURIComponent(id)}`);
  }
}

export class MembershipsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/memberships', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/memberships', { page: 1, pageSize: 10, ...params });
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

export class ComputeResource extends ResourceBase {
  availability(params: JsonObject = {}): Promise<JsonObject> {
    return this.get('/compute', params);
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

export class SubscriptionsResource extends ResourceBase {
  balance(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/subscriptions/balance', body);
  }

  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/subscriptions', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/subscriptions', { page: 1, pageSize: 10, ...params });
  }

  downgrade(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/subscriptions/downgrade', body);
  }

  portal(): Promise<JsonObject> {
    return this.post('/subscriptions/portal', {});
  }

  upgrade(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/subscriptions/upgrade', body);
  }

  retrieve(subscriptionId: string): Promise<JsonObject> {
    return this.get(`/subscriptions/${encodeURIComponent(subscriptionId)}`);
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

  listDeliveries(id: string, params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource(`/webhooks/${encodeURIComponent(id)}/deliveries`, { page: 1, pageSize: 10, ...params });
  }

  rotateSecret(id: string): Promise<JsonObject> {
    return this.post(`/webhooks/${encodeURIComponent(id)}/rotate-secret`, {});
  }

  signingSecret(id: string): Promise<JsonObject> {
    return this.get(`/webhooks/${encodeURIComponent(id)}/signing-secret`);
  }

  test(id: string): Promise<JsonObject> {
    return this.post(`/webhooks/${encodeURIComponent(id)}/test`, {});
  }

  retrieveDelivery(id: string, deliveryId: string): Promise<JsonObject> {
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
    const headers: Record<string, string> = { 'x-layerbrain-source': 'api' };

    if (this.client.apiKey) {
      headers.Authorization = `Bearer ${this.client.apiKey}`;
    }

    return { url: `${wsBaseURL}/v1/webhooks${query}`, headers };
  }
}

export class StorageResource extends ResourceBase {
  createBucket(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/buckets', body);
  }

  listBuckets(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/buckets', { page: 1, pageSize: 10, ...params });
  }

  searchObjects(params: JsonObject = {}): Promise<JsonObject> {
    return this.get('/objects/search', params);
  }

  deleteBucket(id: string): Promise<JsonObject> {
    return super.delete(`/buckets/${encodeURIComponent(id)}`);
  }

  updateBucket(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/buckets/${encodeURIComponent(id)}`, body);
  }

  retrieveBucket(id: string): Promise<JsonObject> {
    return this.get(`/buckets/${encodeURIComponent(id)}`);
  }

  createBucketCredential(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/buckets/${encodeURIComponent(id)}/credentials`, body);
  }

  listBucketCredentials(id: string, params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource(`/buckets/${encodeURIComponent(id)}/credentials`, { page: 1, pageSize: 10, ...params });
  }

  createBucketFolder(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/buckets/${encodeURIComponent(id)}/folders`, body);
  }

  listBucketObjects(id: string, params: JsonObject = {}): Promise<JsonObject> {
    return this.get(`/buckets/${encodeURIComponent(id)}/objects`, params);
  }

  presignBucket(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/buckets/${encodeURIComponent(id)}/presign`, body);
  }

  copyBucketObject(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/buckets/${encodeURIComponent(id)}/objects/copy`, body);
  }

  deleteBucketObject(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/buckets/${encodeURIComponent(id)}/objects/delete`, body);
  }

  headBucketObject(id: string, params: JsonObject = {}): Promise<JsonObject> {
    return this.get(`/buckets/${encodeURIComponent(id)}/objects/head`, params);
  }

  moveBucketObject(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(`/buckets/${encodeURIComponent(id)}/objects/move`, body);
  }

  deleteBucketCredential(id: string, accessKeyId: string): Promise<JsonObject> {
    return super.delete(`/buckets/${encodeURIComponent(id)}/credentials/${encodeURIComponent(accessKeyId)}`);
  }

  updateBucketCredential(id: string, accessKeyId: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/buckets/${encodeURIComponent(id)}/credentials/${encodeURIComponent(accessKeyId)}`, body);
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

export class ModelsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/models', { page: 1, pageSize: 10, ...params });
  }

  retrieve(model: string): Promise<JsonObject> {
    return this.get(`/models/${encodeURIComponent(model)}`);
  }
}

export class NetworkFlowsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/network-flows', { page: 1, pageSize: 10, ...params });
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/network-flows/${encodeURIComponent(id)}`);
  }
}

export class NetworkRulesResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/network-rules', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/network-rules', { page: 1, pageSize: 10, ...params });
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(`/network-rules/${encodeURIComponent(id)}`);
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(`/network-rules/${encodeURIComponent(id)}`, body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/network-rules/${encodeURIComponent(id)}`);
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

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/3d/generations/${encodeURIComponent(id)}`);
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

  retrieve(id: string): Promise<JsonObject> {
    return this.get(`/videos/generations/${encodeURIComponent(id)}`);
  }
}
