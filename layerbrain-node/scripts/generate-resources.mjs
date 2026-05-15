import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const NODE_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REPO_ROOT = path.resolve(NODE_ROOT, '..');
const SPEC_PATH = path.join(REPO_ROOT, 'openapi', 'openapi.json');

export const RESOURCE_DEFINITIONS = {
  accounts: { className: 'AccountsResource', property: 'accounts', title: 'Accounts' },
  apiKeys: { className: 'APIKeysResource', property: 'apiKeys', title: 'API Keys' },
  audio: { className: 'AudioResource', property: 'audio', title: 'Audio' },
  brains: { className: 'BrainsResource', property: 'brains', title: 'Brains' },
  chat: { className: 'ChatResource', property: 'chat', title: 'Chat', manual: true },
  compute: { className: 'ComputeResource', property: 'compute', title: 'Compute' },
  embeddings: { className: 'EmbeddingsResource', property: 'embeddings', title: 'Embeddings' },
  events: { className: 'EventsResource', property: 'events', title: 'Events' },
  exports: { className: 'ExportsResource', property: 'exports', title: 'Exports' },
  images: { className: 'ImagesResource', property: 'images', title: 'Images' },
  logs: { className: 'LogsResource', property: 'logs', title: 'Logs' },
  machines: { className: 'MachinesResource', property: 'machines', title: 'Machines' },
  memberships: { className: 'MembershipsResource', property: 'memberships', title: 'Memberships' },
  models: { className: 'ModelsResource', property: 'models', title: 'Models' },
  networkFlows: { className: 'NetworkFlowsResource', property: 'networkFlows', title: 'Network Flows' },
  networkRules: { className: 'NetworkRulesResource', property: 'networkRules', title: 'Network Rules' },
  networks: { className: 'NetworksResource', property: 'networks', title: 'Networks' },
  organizations: { className: 'OrganizationsResource', property: 'organizations', title: 'Organizations' },
  resources: { className: 'ResourcesResource', property: 'resources', title: 'Resources' },
  secrets: { className: 'SecretsResource', property: 'secrets', title: 'Secrets' },
  snapshots: { className: 'SnapshotsResource', property: 'snapshots', title: 'Snapshots' },
  statements: { className: 'StatementsResource', property: 'statements', title: 'Statements' },
  storage: { className: 'StorageResource', property: 'storage', title: 'Storage' },
  subscriptions: { className: 'SubscriptionsResource', property: 'subscriptions', title: 'Subscriptions' },
  threeD: { className: 'ThreeDResource', property: 'threeD', title: '3D' },
  tools: { className: 'ToolsResource', property: 'tools', title: 'Tools' },
  videos: { className: 'VideosResource', property: 'videos', title: 'Videos' },
  webhooks: { className: 'WebhooksResource', property: 'webhooks', title: 'Webhooks' },
};

const OPERATION_DEFINITIONS = {
  'accounts_list_get': { resource: 'accounts', method: 'list', kind: 'list' },
  'accounts_destroy_delete': { resource: 'accounts', method: 'delete', kind: 'delete' },
  'accounts_retrieve_get': { resource: 'accounts', method: 'retrieve', kind: 'get' },
  'accounts_patch_patch': { resource: 'accounts', method: 'update', kind: 'patch' },

  'api-keys_create_post': { resource: 'apiKeys', method: 'create', kind: 'post' },
  'api-keys_list_get': { resource: 'apiKeys', method: 'list', kind: 'list' },
  'api-keys_destroy_delete': { resource: 'apiKeys', method: 'delete', kind: 'delete' },
  'api-keys_patch_patch': { resource: 'apiKeys', method: 'update', kind: 'patch' },
  'api-keys_retrieve_get': { resource: 'apiKeys', method: 'retrieve', kind: 'get' },
  'api-keys_rotate_post': { resource: 'apiKeys', method: 'rotate', kind: 'post', emptyBody: true },

  'audio_create_speech_post': { resource: 'audio', method: 'speech', kind: 'post' },
  'audio_create_transcription_post': { resource: 'audio', method: 'transcriptions', kind: 'post' },
  'chat_create_completion_post': { resource: 'chat', method: 'completions.create', kind: 'manual' },

  'brains_create_brain_post': { resource: 'brains', method: 'create', kind: 'post' },
  'brains_delete_brain_delete': { resource: 'brains', method: 'delete', kind: 'delete' },
  'brains_retrieve_brain_get': { resource: 'brains', method: 'retrieve', kind: 'get' },
  'brains_archive_brain_post': { resource: 'brains', method: 'archive', kind: 'post', emptyBody: true },

  'compute_retrieve_compute_availability_get': { resource: 'compute', method: 'availability', kind: 'query' },
  'embeddings_create_embedding_post': { resource: 'embeddings', method: 'create', kind: 'post' },

  'events_create_post': { resource: 'events', method: 'create', kind: 'post' },
  'events_list_get': { resource: 'events', method: 'list', kind: 'list' },
  'events_types_get': { resource: 'events', method: 'types', kind: 'get' },
  'events_retrieve_get': { resource: 'events', method: 'retrieve', kind: 'get' },

  'exports_create_post': { resource: 'exports', method: 'create', kind: 'post' },
  'exports_list_get': { resource: 'exports', method: 'list', kind: 'list' },
  'exports_download_get': { resource: 'exports', method: 'download', kind: 'get' },

  'images_create_edit_post': { resource: 'images', method: 'edit', kind: 'post' },
  'images_create_generation_post': { resource: 'images', method: 'generate', kind: 'post' },

  'logs_list_get': { resource: 'logs', method: 'list', kind: 'list' },
  'logs_retrieve_get': { resource: 'logs', method: 'retrieve', kind: 'get' },

  'machines_create_machine_post': { resource: 'machines', method: 'create', kind: 'post', machineCreate: true },
  'machines_list_machines_get': { resource: 'machines', method: 'list', kind: 'list' },
  'machines_delete_machine_delete': { resource: 'machines', method: 'delete', kind: 'delete' },
  'machines_retrieve_machine_get': { resource: 'machines', method: 'retrieve', kind: 'get' },
  'machines_connect_websocket': { resource: 'machines', method: 'connect', kind: 'custom' },
  'machines_extend_machine_post': { resource: 'machines', method: 'extend', kind: 'post' },
  'machines_restore_machine_post': { resource: 'machines', method: 'restore', kind: 'post' },
  'machines_snapshot_machine_post': { resource: 'machines', method: 'snapshot', kind: 'post' },

  'memberships_create_post': { resource: 'memberships', method: 'create', kind: 'post' },
  'memberships_list_get': { resource: 'memberships', method: 'list', kind: 'list' },
  'memberships_retrieve_get': { resource: 'memberships', method: 'retrieve', kind: 'get' },
  'memberships_destroy_delete': { resource: 'memberships', method: 'delete', kind: 'delete' },
  'memberships_patch_patch': { resource: 'memberships', method: 'update', kind: 'patch' },

  'models_list_models_get': { resource: 'models', method: 'list', kind: 'list' },
  'models_retrieve_model_get': { resource: 'models', method: 'retrieve', kind: 'get' },

  'networks_list_networks_get': { resource: 'networks', method: 'list', kind: 'list' },
  'networks_patch_network_patch': { resource: 'networks', method: 'update', kind: 'patch' },
  'networks_retrieve_network_get': { resource: 'networks', method: 'retrieve', kind: 'get' },

  'network_rules_create_network_rule_post': { resource: 'networkRules', method: 'create', kind: 'post' },
  'network_rules_list_network_rules_get': { resource: 'networkRules', method: 'list', kind: 'list' },
  'network_rules_delete_network_rule_delete': { resource: 'networkRules', method: 'delete', kind: 'delete' },
  'network_rules_patch_network_rule_patch': { resource: 'networkRules', method: 'update', kind: 'patch' },
  'network_rules_retrieve_network_rule_get': { resource: 'networkRules', method: 'retrieve', kind: 'get' },

  'network_flows_list_network_flows_get': { resource: 'networkFlows', method: 'list', kind: 'list' },
  'network_flows_retrieve_network_flow_get': { resource: 'networkFlows', method: 'retrieve', kind: 'get' },

  'organizations_create_post': { resource: 'organizations', method: 'create', kind: 'post' },
  'organizations_list_get': { resource: 'organizations', method: 'list', kind: 'list' },
  'organizations_destroy_delete': { resource: 'organizations', method: 'delete', kind: 'delete' },
  'organizations_retrieve_get': { resource: 'organizations', method: 'retrieve', kind: 'get' },
  'organizations_patch_patch': { resource: 'organizations', method: 'update', kind: 'patch' },

  'resources_list_get': { resource: 'resources', method: 'list', kind: 'list' },

  'secrets_create_post': { resource: 'secrets', method: 'create', kind: 'post' },
  'secrets_list_get': { resource: 'secrets', method: 'list', kind: 'list' },
  'secrets_destroy_delete': { resource: 'secrets', method: 'delete', kind: 'delete' },
  'secrets_patch_patch': { resource: 'secrets', method: 'update', kind: 'patch' },
  'secrets_retrieve_get': { resource: 'secrets', method: 'retrieve', kind: 'get' },
  'secrets_reveal_get': { resource: 'secrets', method: 'reveal', kind: 'get' },

  'snapshots_create_post': { resource: 'snapshots', method: 'create', kind: 'post' },
  'snapshots_list_get': { resource: 'snapshots', method: 'list', kind: 'list' },
  'snapshots_retrieve_get': { resource: 'snapshots', method: 'retrieve', kind: 'get' },
  'snapshots_download_get': { resource: 'snapshots', method: 'download', kind: 'get' },
  'snapshots_restore_post': { resource: 'snapshots', method: 'restore', kind: 'post' },

  'statements_statements_list_get': { resource: 'statements', method: 'list', kind: 'list' },
  'statements_statement_retrieve_get': { resource: 'statements', method: 'retrieve', kind: 'get' },

  'buckets_create_bucket_post': { resource: 'storage', method: 'createBucket', kind: 'post' },
  'buckets_list_buckets_get': { resource: 'storage', method: 'listBuckets', kind: 'list' },
  'buckets_search_storage_objects_get': { resource: 'storage', method: 'searchObjects', kind: 'query' },
  'buckets_delete_bucket_delete': { resource: 'storage', method: 'deleteBucket', kind: 'delete' },
  'buckets_patch_bucket_patch': { resource: 'storage', method: 'updateBucket', kind: 'patch' },
  'buckets_retrieve_bucket_get': { resource: 'storage', method: 'retrieveBucket', kind: 'get' },
  'buckets_create_bucket_folder_post': { resource: 'storage', method: 'createBucketFolder', kind: 'post' },
  'buckets_list_bucket_objects_get': { resource: 'storage', method: 'listBucketObjects', kind: 'query' },
  'buckets_presign_bucket_post': { resource: 'storage', method: 'presignBucket', kind: 'post' },
  'buckets_copy_bucket_object_post': { resource: 'storage', method: 'copyBucketObject', kind: 'post' },
  'buckets_delete_bucket_object_post': { resource: 'storage', method: 'deleteBucketObject', kind: 'post' },
  'buckets_head_bucket_object_get': { resource: 'storage', method: 'headBucketObject', kind: 'query' },
  'buckets_move_bucket_object_post': { resource: 'storage', method: 'moveBucketObject', kind: 'post' },
  'buckets_create_bucket_credential_post': { resource: 'storage', method: 'createBucketCredential', kind: 'post' },
  'buckets_list_bucket_credentials_get': { resource: 'storage', method: 'listBucketCredentials', kind: 'list' },
  'buckets_delete_bucket_credential_delete': { resource: 'storage', method: 'deleteBucketCredential', kind: 'delete' },
  'buckets_update_bucket_credential_patch': { resource: 'storage', method: 'updateBucketCredential', kind: 'patch' },

  'subscriptions_create_post': { resource: 'subscriptions', method: 'create', kind: 'post' },
  'subscriptions_list_get': { resource: 'subscriptions', method: 'list', kind: 'list' },
  'subscriptions_retrieve_get': { resource: 'subscriptions', method: 'retrieve', kind: 'get' },
  'subscriptions_balance_post': { resource: 'subscriptions', method: 'balance', kind: 'post' },
  'subscriptions_downgrade_post': { resource: 'subscriptions', method: 'downgrade', kind: 'post' },
  'subscriptions_portal_post': { resource: 'subscriptions', method: 'portal', kind: 'post', emptyBody: true },
  'subscriptions_upgrade_post': { resource: 'subscriptions', method: 'upgrade', kind: 'post' },

  '3d_create_generation_post': { resource: 'threeD', method: 'generate', kind: 'post' },
  '3d_retrieve_generation_get': { resource: 'threeD', method: 'retrieve', kind: 'get' },

  'tools_web_search_post': { resource: 'tools', method: 'webSearch', kind: 'post' },

  'videos_create_generation_post': { resource: 'videos', method: 'generate', kind: 'post' },
  'videos_retrieve_generation_get': { resource: 'videos', method: 'retrieve', kind: 'get' },

  'webhooks_create_post': { resource: 'webhooks', method: 'create', kind: 'post' },
  'webhooks_list_get': { resource: 'webhooks', method: 'list', kind: 'list' },
  'webhooks_listen_websocket': { resource: 'webhooks', method: 'listenRequest', kind: 'custom' },
  'webhooks_destroy_delete': { resource: 'webhooks', method: 'delete', kind: 'delete' },
  'webhooks_patch_patch': { resource: 'webhooks', method: 'update', kind: 'patch' },
  'webhooks_retrieve_get': { resource: 'webhooks', method: 'retrieve', kind: 'get' },
  'webhooks_rotate_secret_post': { resource: 'webhooks', method: 'rotateSecret', kind: 'post', emptyBody: true },
  'webhooks_deliveries_get': { resource: 'webhooks', method: 'listDeliveries', kind: 'list' },
  'webhooks_signing_secret_get': { resource: 'webhooks', method: 'signingSecret', kind: 'get' },
  'webhooks_test_post': { resource: 'webhooks', method: 'test', kind: 'post', emptyBody: true },
  'webhooks_delivery_get': { resource: 'webhooks', method: 'retrieveDelivery', kind: 'get' },
};

const HTTP_METHODS = new Set(['get', 'post', 'patch', 'put', 'delete']);

const ADDITIONAL_SDK_RESOURCE_CLASSES = {
  audio: `export class AudioResource extends ResourceBase {
  speech(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/audio/speech', body);
  }

  transcriptions(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/audio/transcriptions', body);
  }
}`,
  embeddings: `export class EmbeddingsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/embeddings', body);
  }
}`,
  images: `export class ImagesResource extends ResourceBase {
  edit(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/images/edits', body);
  }

  generate(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/images/generations', body);
  }
}`,
  models: `export class ModelsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/models', { page: 1, pageSize: 10, ...params });
  }

  retrieve(model: string): Promise<JsonObject> {
    return this.get(\`/models/\${encodeURIComponent(model)}\`);
  }
}`,
  networkFlows: `export class NetworkFlowsResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/network-flows', { page: 1, pageSize: 10, ...params });
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(\`/network-flows/\${encodeURIComponent(id)}\`);
  }
}`,
  networkRules: `export class NetworkRulesResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/network-rules', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/network-rules', { page: 1, pageSize: 10, ...params });
  }

  delete(id: string): Promise<JsonObject> {
    return super.delete(\`/network-rules/\${encodeURIComponent(id)}\`);
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(\`/network-rules/\${encodeURIComponent(id)}\`, body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(\`/network-rules/\${encodeURIComponent(id)}\`);
  }
}`,
  networks: `export class NetworksResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/networks', { page: 1, pageSize: 10, ...params });
  }

  update(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.patch(\`/networks/\${encodeURIComponent(id)}\`, body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(\`/networks/\${encodeURIComponent(id)}\`);
  }
}`,
  resources: `export class ResourcesResource extends ResourceBase {
  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/resources', { page: 1, pageSize: 10, ...params });
  }
}`,
  snapshots: `export class SnapshotsResource extends ResourceBase {
  create(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/snapshots', body);
  }

  list(params: ListParams = {}): Promise<ListPage<JsonObject>> {
    return this.listResource('/snapshots', { page: 1, pageSize: 10, ...params });
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(\`/snapshots/\${encodeURIComponent(id)}\`);
  }

  download(id: string): Promise<JsonObject> {
    return this.get(\`/snapshots/\${encodeURIComponent(id)}/download\`);
  }

  restore(id: string, body: JsonObject = {}): Promise<JsonObject> {
    return this.post(\`/snapshots/\${encodeURIComponent(id)}/restore\`, body);
  }
}`,
  threeD: `export class ThreeDResource extends ResourceBase {
  generate(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/3d/generations', body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(\`/3d/generations/\${encodeURIComponent(id)}\`);
  }
}`,
  tools: `export class ToolsResource extends ResourceBase {
  webSearch(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/tools/web-search', body);
  }
}`,
  videos: `export class VideosResource extends ResourceBase {
  generate(body: JsonObject = {}): Promise<JsonObject> {
    return this.post('/videos/generations', body);
  }

  retrieve(id: string): Promise<JsonObject> {
    return this.get(\`/videos/generations/\${encodeURIComponent(id)}\`);
  }
}`,
};

export function loadSpec() {
  return JSON.parse(fs.readFileSync(SPEC_PATH, 'utf8'));
}

function toCamel(name) {
  return name.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

function stripV1(openapiPath) {
  const stripped = openapiPath.replace(/^\/v1/, '') || '/';
  return stripped.length > 1 ? stripped.replace(/\/$/, '') : stripped;
}

function pathParams(openapiPath) {
  return [...openapiPath.matchAll(/\{([^}]+)\}/g)].map((match) => ({
    raw: match[1],
    name: toCamel(match[1]),
  }));
}

function pathExpression(openapiPath) {
  const pathTemplate = stripV1(openapiPath);
  if (!pathTemplate.includes('{')) {
    return `'${pathTemplate}'`;
  }
  const template = pathTemplate.replace(/\{([^}]+)\}/g, (_, raw) => `\${encodeURIComponent(${toCamel(raw)})}`);
  return `\`${template}\``;
}

export function collectOperations(spec = loadSpec()) {
  const resources = new Map();

  for (const [openapiPath, pathItem] of Object.entries(spec.paths ?? {})) {
    for (const [method, operation] of Object.entries(pathItem)) {
      if (!HTTP_METHODS.has(method) && method !== 'x-layerbrain-websocket') {
        continue;
      }
      const operationId = operation.operationId;
      const definition = OPERATION_DEFINITIONS[operationId];
      if (!definition) {
        throw new Error(`No Node SDK mapping for OpenAPI operation ${operationId}`);
      }
      const resourceDefinition = RESOURCE_DEFINITIONS[definition.resource];
      if (!resourceDefinition) {
        throw new Error(`No resource definition for ${definition.resource}`);
      }
      const entry = {
        ...definition,
        httpMethod: method,
        operationId,
        openapiPath,
        sdkPath: stripV1(openapiPath),
        pathParams: pathParams(openapiPath),
        summary: operation.summary,
      };
      if (!resources.has(definition.resource)) {
        resources.set(definition.resource, {
          key: definition.resource,
          ...resourceDefinition,
          operations: [],
        });
      }
      resources.get(definition.resource).operations.push(entry);
    }
  }

  return [...resources.values()];
}

function methodSignature(operation) {
  const params = operation.pathParams.map((param) => `${param.name}: string`);
  if (operation.kind === 'list') {
    params.push('params: ListParams = {}');
  } else if (operation.kind === 'query') {
    params.push('params: JsonObject = {}');
  } else if (['post', 'patch', 'put'].includes(operation.kind) && !operation.emptyBody) {
    params.push('body: JsonObject = {}');
  }
  return params.join(', ');
}

function methodBody(operation) {
  const requestPath = pathExpression(operation.openapiPath);
  if (operation.kind === 'list') {
    return `return this.listResource(${requestPath}, { page: 1, pageSize: 10, ...params });`;
  }
  if (operation.kind === 'get') {
    return `return this.get(${requestPath});`;
  }
  if (operation.kind === 'query') {
    return `return this.get(${requestPath}, params);`;
  }
  if (operation.kind === 'delete') {
    return `return super.delete(${requestPath});`;
  }
  if (operation.kind === 'patch') {
    return `return this.patch(${requestPath}, body);`;
  }
  if (operation.machineCreate) {
    return `return this.post(${requestPath}, body);`;
  }
  if (operation.emptyBody) {
    return `return this.post(${requestPath}, {});`;
  }
  if (operation.kind === 'post') {
    return `return this.post(${requestPath}, body);`;
  }
  throw new Error(`Unsupported operation kind ${operation.kind}`);
}

function returnType(operation) {
  if (operation.kind === 'list') {
    return 'Promise<ListPage<JsonObject>>';
  }
  return 'Promise<JsonObject>';
}

function generateOperation(operation) {
  const body = methodBody(operation)
    .split('\n')
    .map((line) => `    ${line}`)
    .join('\n');

  return `  ${operation.method}(${methodSignature(operation)}): ${returnType(operation)} {\n${body}\n  }`;
}

function customMachinesMethods() {
  return `  private websocketURL(path: string): string {
    const baseURL = this.client.baseURL;
    let wsBaseURL: string;

    if (baseURL.startsWith('https://')) {
      wsBaseURL = \`wss://\${baseURL.slice('https://'.length)}\`;
    } else if (baseURL.startsWith('http://')) {
      wsBaseURL = \`ws://\${baseURL.slice('http://'.length)}\`;
    } else {
      wsBaseURL = \`wss://\${baseURL}\`;
    }

    return \`\${wsBaseURL}/v1\${path}\`;
  }

  private websocketHeaders(): Record<string, string> {
    if (!this.client.apiKey) {
      throw new Error('No API key provided. Set LAYERBRAIN_API_KEY or pass apiKey to the client.');
    }

    return {
      Authorization: \`Bearer \${this.client.apiKey}\`,
      'x-layerbrain-source': 'api',
    };
  }

  async connect(machineId: string): Promise<MachineConnection> {
    const url = this.websocketURL(\`/machines/\${encodeURIComponent(machineId)}\`);
    const transport = await MachineTransport.connect(url, this.websocketHeaders());
    return new MachineConnection(machineId, transport);
  }`;
}

function customWebhooksMethods() {
  return `  listenRequest(options: { events?: string | string[] } = {}): { url: string; headers: Record<string, string> } {
    const baseURL = this.client.baseURL;
    let wsBaseURL: string;

    if (baseURL.startsWith('https://')) {
      wsBaseURL = \`wss://\${baseURL.slice('https://'.length)}\`;
    } else if (baseURL.startsWith('http://')) {
      wsBaseURL = \`ws://\${baseURL.slice('http://'.length)}\`;
    } else {
      wsBaseURL = \`wss://\${baseURL}\`;
    }

    const rawEvents = Array.isArray(options.events)
      ? options.events.map((event) => event.trim()).filter(Boolean).join(',')
      : options.events?.trim();
    const query = rawEvents ? \`?events=\${encodeURIComponent(rawEvents)}\` : '';
    const headers: Record<string, string> = { 'x-layerbrain-source': 'api' };

    if (this.client.apiKey) {
      headers.Authorization = \`Bearer \${this.client.apiKey}\`;
    }

    return { url: \`\${wsBaseURL}/v1/webhooks\${query}\`, headers };
  }`;
}

function generateClass(resource) {
  if (resource.manual) {
    return '';
  }

  const operations = resource.operations.filter((operation) => operation.kind !== 'manual' && operation.kind !== 'custom');
  const methods = operations.map(generateOperation);
  if (resource.key === 'machines') {
    methods.push(customMachinesMethods());
  }
  if (resource.key === 'webhooks') {
    methods.push(customWebhooksMethods());
  }

  return `export class ${resource.className} extends ResourceBase {\n${methods.join('\n\n')}\n}`;
}

function generateResourcesFile(resources) {
  const generatedKeys = new Set(resources.map((resource) => resource.key));
  const generatedClasses = resources.filter((resource) => !resource.manual).map(generateClass);
  const additionalClasses = Object.entries(ADDITIONAL_SDK_RESOURCE_CLASSES)
    .filter(([key]) => !generatedKeys.has(key))
    .map(([, source]) => source);
  const classes = [...generatedClasses, ...additionalClasses].join('\n\n');
  return `import type { ListPage } from '../core/pagination.js';
import { MachineConnection } from '../machines/connection.js';
import { MachineTransport } from '../machines/transport.js';
import { ResourceBase, type JsonObject, type ListParams } from './base.js';

${classes}
`;
}

function generateClientFile(resources) {
  const generatedResources = resources.filter((resource) => !resource.manual);
  const generatedKeys = new Set(generatedResources.map((resource) => resource.key));
  const additionalResources = Object.keys(ADDITIONAL_SDK_RESOURCE_CLASSES)
    .filter((key) => !generatedKeys.has(key))
    .map((key) => RESOURCE_DEFINITIONS[key]);
  const classNames = [...generatedResources, ...additionalResources].map((resource) => resource.className).sort();
  const allResources = [...generatedResources, ...additionalResources, RESOURCE_DEFINITIONS.chat]
    .sort((left, right) => left.property.localeCompare(right.property));

  return `import { HTTPClient, type HTTPClientOptions } from './core/http.js';
import { ChatResource } from './resources/chat.js';
import {
  ${classNames.join(',\n  ')},
} from './resources/resources.js';

export interface ClientOptions extends HTTPClientOptions {}

export class Layerbrain {
${allResources.map((resource) => `  readonly ${resource.property}: ${resource.className};`).join('\n')}

  private readonly httpClient: HTTPClient;

  constructor(options: ClientOptions = {}) {
    this.httpClient = new HTTPClient(options);

${allResources.map((resource) => `    this.${resource.property} = new ${resource.className}(this.httpClient);`).join('\n')}
  }

  get apiKey(): string | undefined {
    return this.httpClient.apiKey;
  }

  get baseURL(): string {
    return this.httpClient.baseURL;
  }
}
`;
}

export function generateResources() {
  const resources = collectOperations();
  fs.writeFileSync(path.join(NODE_ROOT, 'src', 'resources', 'resources.ts'), generateResourcesFile(resources));
  fs.writeFileSync(path.join(NODE_ROOT, 'src', 'client.ts'), generateClientFile(resources));
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  generateResources();
}
