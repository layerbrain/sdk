import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const NODE_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REPO_ROOT = path.resolve(NODE_ROOT, '..');
const SPEC_PATH = path.join(REPO_ROOT, 'openapi', 'openapi.json');

const HTTP_METHODS = new Set(['get', 'post', 'patch', 'put', 'delete']);
const SKIP_TAGS = new Set(['Health', 'Username']);

const RESOURCE_OVERRIDES = {
  '3D': { key: 'threeD', className: 'ThreeDResource', property: 'threeD', title: '3D' },
  'Api-Keys': { key: 'apiKeys', className: 'APIKeysResource', property: 'apiKeys', title: 'API Keys' },
};

const MANUAL_RESOURCES = {
  chat: { key: 'chat', className: 'ChatResource', property: 'chat', title: 'Chat', manual: true },
};

const METHOD_OVERRIDES = {
  '3d_create_generation_post': { method: 'generate' },
  '3d_retrieve_generation_get': { method: 'retrieve' },
  'audio_create_speech_post': { method: 'speech' },
  'audio_create_transcription_post': { method: 'transcriptions' },
  'images_create_edit_post': { method: 'edit' },
  'images_create_generation_post': { method: 'generate' },
  'videos_create_generation_post': { method: 'generate' },
  'videos_retrieve_generation_get': { method: 'retrieve' },
};

const EMPTY_BODY_ACTIONS = new Set(['archive', 'rotate', 'validate']);

const ACTION_PREFIXES = [
  'list',
  'create',
  'retrieve',
  'patch',
  'put',
  'replace',
  'delete',
  'destroy',
  'archive',
  'restore',
  'extend',
  'snapshot',
  'download',
  'rotate',
  'validate',
  'presign',
  'reveal',
  'claim',
  'cancel',
  'start',
  'resume',
  'add',
  'search',
  'copy',
  'head',
  'move',
  'signing',
  'delivery',
  'deliveries',
  'test',
];

const ACTION_METHOD_NAMES = {
  destroy: 'delete',
  patch: 'update',
  put: 'replace',
};

export function loadSpec() {
  return JSON.parse(fs.readFileSync(SPEC_PATH, 'utf8'));
}

function splitWords(value) {
  return value
    .replace(/([a-z0-9])([A-Z])/g, '$1 $2')
    .replace(/[^a-zA-Z0-9]+/g, ' ')
    .trim()
    .split(/\s+/)
    .filter(Boolean);
}

function titleCase(word) {
  return `${word.slice(0, 1).toUpperCase()}${word.slice(1)}`;
}

function toPascal(value) {
  return splitWords(value).map(titleCase).join('');
}

function toCamel(value) {
  const pascal = toPascal(value);
  return `${pascal.slice(0, 1).toLowerCase()}${pascal.slice(1)}`;
}

function lowerToken(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');
}

function singularize(value) {
  if (value.endsWith('ies') && value.length > 3) {
    return `${value.slice(0, -3)}y`;
  }
  if (value.endsWith('ses') && value.length > 3) {
    return value.slice(0, -2);
  }
  if (value.endsWith('s') && !value.endsWith('ss') && value.length > 2) {
    return value.slice(0, -1);
  }
  return value;
}

function stripV1(openapiPath) {
  const stripped = openapiPath.replace(/^\/v1/, '') || '/';
  return stripped.length > 1 ? stripped.replace(/\/$/, '') : stripped;
}

function firstPathSegment(openapiPath) {
  return stripV1(openapiPath).split('/').filter(Boolean)[0] ?? '';
}

function resourceDefinition(tag) {
  if (RESOURCE_OVERRIDES[tag]) {
    return RESOURCE_OVERRIDES[tag];
  }

  const property = toCamel(tag);
  return {
    key: property,
    className: `${toPascal(tag)}Resource`,
    property,
    title: tag,
  };
}

function operationSuffix(httpMethod) {
  return httpMethod === 'x-layerbrain-websocket' ? 'websocket' : httpMethod;
}

function operationCore(operationId, openapiPath, httpMethod, tag) {
  const suffix = `_${operationSuffix(httpMethod)}`;
  let core = operationId.endsWith(suffix) ? operationId.slice(0, -suffix.length) : operationId;
  const prefixes = [
    firstPathSegment(openapiPath),
    lowerToken(tag).replace(/_/g, '-'),
    lowerToken(tag),
  ]
    .filter(Boolean)
    .sort((left, right) => right.length - left.length);

  for (const prefix of prefixes) {
    if (core === prefix) {
      return '';
    }
    if (core.startsWith(`${prefix}_`)) {
      return core.slice(prefix.length + 1);
    }
  }

  return core;
}

function parseAction(core) {
  for (const action of ACTION_PREFIXES) {
    if (core === action) {
      return { action, entity: '' };
    }
    if (core.startsWith(`${action}_`)) {
      return { action, entity: core.slice(action.length + 1) };
    }
    if (core.endsWith(`_${action}`)) {
      return { action, entity: core.slice(0, -action.length - 1) };
    }
  }

  return null;
}

function entityMatchesResource(entity, tag, openapiPath) {
  if (!entity) {
    return true;
  }

  const entityToken = singularize(lowerToken(entity));
  const resourceTokens = [
    tag,
    firstPathSegment(openapiPath),
    toCamel(tag),
    toPascal(tag),
  ]
    .map(lowerToken)
    .filter(Boolean);

  return resourceTokens.some((token) => entityToken === singularize(token));
}

function actionMethodName(action) {
  return ACTION_METHOD_NAMES[action] ?? action;
}

function methodFromCore(core, openapiPath, httpMethod, tag) {
  const parsed = parseAction(core);
  if (parsed) {
    const methodAction = actionMethodName(parsed.action);
    if (entityMatchesResource(parsed.entity, tag, openapiPath)) {
      return methodAction;
    }
    return toCamel(`${methodAction}_${parsed.entity}`);
  }

  const baseName = toCamel(core);
  if (httpMethod === 'post') {
    return `create${titleCase(baseName)}`;
  }
  if (httpMethod === 'patch') {
    return `update${titleCase(baseName)}`;
  }
  if (httpMethod === 'put') {
    return `replace${titleCase(baseName)}`;
  }
  if (httpMethod === 'delete') {
    return `delete${titleCase(baseName)}`;
  }
  return baseName;
}

function operationKind(httpMethod, core) {
  const parsed = parseAction(core);
  if (httpMethod === 'x-layerbrain-websocket') {
    return 'custom';
  }
  if (httpMethod === 'get' && parsed?.action === 'list') {
    return 'list';
  }
  if (httpMethod === 'get') {
    return 'get';
  }
  if (httpMethod === 'delete') {
    return 'delete';
  }
  return httpMethod;
}

function pathParams(openapiPath) {
  return [...openapiPath.matchAll(/\{([^}]+)\}/g)].map((match) => ({
    raw: match[1],
    name: toCamel(match[1]),
  }));
}

function queryParams(operation) {
  return (operation.parameters ?? [])
    .filter((parameter) => parameter.in === 'query')
    .map((parameter) => parameter.name);
}

function pathExpression(openapiPath) {
  const pathTemplate = stripV1(openapiPath);
  if (!pathTemplate.includes('{')) {
    return `'${pathTemplate}'`;
  }
  const template = pathTemplate.replace(/\{([^}]+)\}/g, (_, raw) => `\${encodeURIComponent(${toCamel(raw)})}`);
  return `\`${template}\``;
}

function deriveOperation(openapiPath, httpMethod, operation) {
  const tag = (operation.tags ?? ['Untagged'])[0];
  const resource = resourceDefinition(tag);
  const operationId = operation.operationId;

  if (operationId === 'chat_create_completion_post') {
    return {
      resource: 'chat',
      method: 'completions.create',
      kind: 'manual',
      resourceDefinition: MANUAL_RESOURCES.chat,
    };
  }

  if (operationId === 'machines_connect_websocket') {
    return { resource: 'machines', method: 'connect', kind: 'custom', resourceDefinition: resource };
  }

  if (operationId === 'webhooks_listen_websocket') {
    return { resource: 'webhooks', method: 'listenRequest', kind: 'custom', resourceDefinition: resource };
  }

  const core = operationCore(operationId, openapiPath, httpMethod, tag);
  const override = METHOD_OVERRIDES[operationId] ?? {};
  const parsed = parseAction(core);
  return {
    resource: resource.key,
    method: override.method ?? methodFromCore(core, openapiPath, httpMethod, tag),
    kind: operationKind(httpMethod, core),
    emptyBody: EMPTY_BODY_ACTIONS.has(parsed?.action ?? ''),
    machineCreate: operationId === 'machines_create_machine_post',
    resourceDefinition: resource,
  };
}

export function collectOperations(spec = loadSpec()) {
  const resources = new Map();

  for (const [openapiPath, pathItem] of Object.entries(spec.paths ?? {})) {
    for (const [httpMethod, operation] of Object.entries(pathItem)) {
      if (!HTTP_METHODS.has(httpMethod) && httpMethod !== 'x-layerbrain-websocket') {
        continue;
      }
      if (!operation.operationId) {
        continue;
      }

      const tag = (operation.tags ?? ['Untagged'])[0];
      if (SKIP_TAGS.has(tag)) {
        continue;
      }

      const definition = deriveOperation(openapiPath, httpMethod, operation);
      const entry = {
        ...definition,
        httpMethod,
        operationId: operation.operationId,
        openapiPath,
        sdkPath: stripV1(openapiPath),
        pathParams: pathParams(openapiPath),
        queryParams: queryParams(operation),
        summary: operation.summary,
      };

      if (!resources.has(definition.resource)) {
        resources.set(definition.resource, {
          ...definition.resourceDefinition,
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
  } else if (operation.kind === 'get' && operation.queryParams.length > 0) {
    params.push('params: JsonObject = {}');
  } else if (['post', 'patch', 'put'].includes(operation.kind) && !operation.emptyBody) {
    params.push('body: JsonObject = {}');
  }
  return params.join(', ');
}

function methodBody(operation) {
  const requestPath = pathExpression(operation.openapiPath);
  if (operation.kind === 'list') {
    return `return this.listResource(${requestPath}, params);`;
  }
  if (operation.kind === 'get') {
    return operation.queryParams.length > 0
      ? `return this.get(${requestPath}, params);`
      : `return this.get(${requestPath});`;
  }
  if (operation.kind === 'delete') {
    return `return super.delete(${requestPath});`;
  }
  if (operation.emptyBody && operation.kind === 'patch') {
    return `return this.patch(${requestPath}, {});`;
  }
  if (operation.kind === 'patch') {
    return `return this.patch(${requestPath}, body);`;
  }
  if (operation.emptyBody && operation.kind === 'put') {
    return `return this.put(${requestPath}, {});`;
  }
  if (operation.kind === 'put') {
    return `return this.put(${requestPath}, body);`;
  }
  if (operation.machineCreate) {
    return `const payload = { duration_minutes: 15, ...body };\nreturn this.post(${requestPath}, payload);`;
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
  return `  async connect(machineId: string): Promise<MachineConnection> {
    const baseURL = this.client.baseURL;
    let wsBaseURL: string;

    if (baseURL.startsWith('https://')) {
      wsBaseURL = \`wss://\${baseURL.slice('https://'.length)}\`;
    } else if (baseURL.startsWith('http://')) {
      wsBaseURL = \`ws://\${baseURL.slice('http://'.length)}\`;
    } else {
      wsBaseURL = \`wss://\${baseURL}\`;
    }

    const url = \`\${wsBaseURL}/v1/machines/\${encodeURIComponent(machineId)}/connect\`;
    const headers: Record<string, string> = {};

    if (this.client.apiKey) {
      headers.Authorization = \`Bearer \${this.client.apiKey}\`;
    }

    const transport = await MachineTransport.connect(url, headers);
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
    const headers: Record<string, string> = {};

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
  const classes = resources.filter((resource) => !resource.manual).map(generateClass).join('\n\n');
  return `import type { ListPage } from '../core/pagination.js';
import { MachineConnection } from '../machines/connection.js';
import { MachineTransport } from '../machines/transport.js';
import { ResourceBase, type JsonObject, type ListParams } from './base.js';

${classes}
`;
}

function generateClientFile(resources) {
  const generatedResources = resources.filter((resource) => !resource.manual);
  const classNames = generatedResources.map((resource) => resource.className).sort();
  const allResources = [...generatedResources, MANUAL_RESOURCES.chat]
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
