import { HTTPClient, type HTTPClientOptions } from './core/http.js';
import { ChatResource } from './resources/chat.js';
import {
  APIKeysResource,
  AccountsResource,
  AudioResource,
  ComputeResource,
  EmbeddingsResource,
  EventsResource,
  ExportsResource,
  ImagesResource,
  MachinesResource,
  MembershipsResource,
  ModelsResource,
  NetworkFlowsResource,
  NetworkRulesResource,
  NetworksResource,
  OrganizationsResource,
  ResourcesResource,
  SecretsResource,
  SnapshotsResource,
  StatementsResource,
  StorageResource,
  SubscriptionsResource,
  ThreeDResource,
  ToolsResource,
  VideosResource,
  WebhooksResource,
} from './resources/resources.js';

export interface ClientOptions extends HTTPClientOptions {}

export class Layerbrain {
  readonly accounts: AccountsResource;
  readonly apiKeys: APIKeysResource;
  readonly audio: AudioResource;
  readonly chat: ChatResource;
  readonly compute: ComputeResource;
  readonly embeddings: EmbeddingsResource;
  readonly events: EventsResource;
  readonly exports: ExportsResource;
  readonly images: ImagesResource;
  readonly machines: MachinesResource;
  readonly memberships: MembershipsResource;
  readonly models: ModelsResource;
  readonly networkFlows: NetworkFlowsResource;
  readonly networkRules: NetworkRulesResource;
  readonly networks: NetworksResource;
  readonly organizations: OrganizationsResource;
  readonly resources: ResourcesResource;
  readonly secrets: SecretsResource;
  readonly snapshots: SnapshotsResource;
  readonly statements: StatementsResource;
  readonly storage: StorageResource;
  readonly subscriptions: SubscriptionsResource;
  readonly threeD: ThreeDResource;
  readonly tools: ToolsResource;
  readonly videos: VideosResource;
  readonly webhooks: WebhooksResource;

  private readonly httpClient: HTTPClient;

  constructor(options: ClientOptions = {}) {
    this.httpClient = new HTTPClient(options);

    this.accounts = new AccountsResource(this.httpClient);
    this.apiKeys = new APIKeysResource(this.httpClient);
    this.audio = new AudioResource(this.httpClient);
    this.chat = new ChatResource(this.httpClient);
    this.compute = new ComputeResource(this.httpClient);
    this.embeddings = new EmbeddingsResource(this.httpClient);
    this.events = new EventsResource(this.httpClient);
    this.exports = new ExportsResource(this.httpClient);
    this.images = new ImagesResource(this.httpClient);
    this.machines = new MachinesResource(this.httpClient);
    this.memberships = new MembershipsResource(this.httpClient);
    this.models = new ModelsResource(this.httpClient);
    this.networkFlows = new NetworkFlowsResource(this.httpClient);
    this.networkRules = new NetworkRulesResource(this.httpClient);
    this.networks = new NetworksResource(this.httpClient);
    this.organizations = new OrganizationsResource(this.httpClient);
    this.resources = new ResourcesResource(this.httpClient);
    this.secrets = new SecretsResource(this.httpClient);
    this.snapshots = new SnapshotsResource(this.httpClient);
    this.statements = new StatementsResource(this.httpClient);
    this.storage = new StorageResource(this.httpClient);
    this.subscriptions = new SubscriptionsResource(this.httpClient);
    this.threeD = new ThreeDResource(this.httpClient);
    this.tools = new ToolsResource(this.httpClient);
    this.videos = new VideosResource(this.httpClient);
    this.webhooks = new WebhooksResource(this.httpClient);
  }

  get apiKey(): string | undefined {
    return this.httpClient.apiKey;
  }

  get baseURL(): string {
    return this.httpClient.baseURL;
  }
}
