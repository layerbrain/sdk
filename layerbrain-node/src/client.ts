import { HTTPClient, type HTTPClientOptions } from './core/http.js';
import { ChatResource } from './resources/chat.js';
import {
  APIKeysResource,
  AccountsResource,
  AudioResource,
  BrainsResource,
  ComputeResource,
  EmbeddingsResource,
  EventsResource,
  ExportsResource,
  ImagesResource,
  MachinesResource,
  MembershipsResource,
  ModelsResource,
  OrganizationsResource,
  PlansResource,
  SecretsResource,
  SnapshotsResource,
  StatementsResource,
  StorageResource,
  SubscriptionsResource,
  ThreeDResource,
  VideosResource,
  WebhooksResource,
  WorkResource,
} from './resources/resources.js';

export interface ClientOptions extends HTTPClientOptions {}

export class Layerbrain {
  readonly accounts: AccountsResource;
  readonly apiKeys: APIKeysResource;
  readonly audio: AudioResource;
  readonly brains: BrainsResource;
  readonly chat: ChatResource;
  readonly compute: ComputeResource;
  readonly embeddings: EmbeddingsResource;
  readonly events: EventsResource;
  readonly exports: ExportsResource;
  readonly images: ImagesResource;
  readonly machines: MachinesResource;
  readonly memberships: MembershipsResource;
  readonly models: ModelsResource;
  readonly organizations: OrganizationsResource;
  readonly plans: PlansResource;
  readonly secrets: SecretsResource;
  readonly snapshots: SnapshotsResource;
  readonly statements: StatementsResource;
  readonly storage: StorageResource;
  readonly subscriptions: SubscriptionsResource;
  readonly threeD: ThreeDResource;
  readonly videos: VideosResource;
  readonly webhooks: WebhooksResource;
  readonly work: WorkResource;

  private readonly httpClient: HTTPClient;

  constructor(options: ClientOptions = {}) {
    this.httpClient = new HTTPClient(options);

    this.accounts = new AccountsResource(this.httpClient);
    this.apiKeys = new APIKeysResource(this.httpClient);
    this.audio = new AudioResource(this.httpClient);
    this.brains = new BrainsResource(this.httpClient);
    this.chat = new ChatResource(this.httpClient);
    this.compute = new ComputeResource(this.httpClient);
    this.embeddings = new EmbeddingsResource(this.httpClient);
    this.events = new EventsResource(this.httpClient);
    this.exports = new ExportsResource(this.httpClient);
    this.images = new ImagesResource(this.httpClient);
    this.machines = new MachinesResource(this.httpClient);
    this.memberships = new MembershipsResource(this.httpClient);
    this.models = new ModelsResource(this.httpClient);
    this.organizations = new OrganizationsResource(this.httpClient);
    this.plans = new PlansResource(this.httpClient);
    this.secrets = new SecretsResource(this.httpClient);
    this.snapshots = new SnapshotsResource(this.httpClient);
    this.statements = new StatementsResource(this.httpClient);
    this.storage = new StorageResource(this.httpClient);
    this.subscriptions = new SubscriptionsResource(this.httpClient);
    this.threeD = new ThreeDResource(this.httpClient);
    this.videos = new VideosResource(this.httpClient);
    this.webhooks = new WebhooksResource(this.httpClient);
    this.work = new WorkResource(this.httpClient);
  }

  get apiKey(): string | undefined {
    return this.httpClient.apiKey;
  }

  get baseURL(): string {
    return this.httpClient.baseURL;
  }
}
