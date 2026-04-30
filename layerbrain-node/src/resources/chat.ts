import { ResourceBase, type JsonObject } from './base.js';

export interface ChatCompletionsCreateParams extends JsonObject {
  model: string;
  messages: unknown[];
  stream?: boolean;
}

export class ChatCompletionsResource extends ResourceBase {
  async create(params: ChatCompletionsCreateParams): Promise<JsonObject | AsyncIterable<JsonObject>> {
    if (params.stream) {
      const stream = await this.client.streamSSE('/chat/completions', params);
      return this.parseStream(stream);
    }

    return this.post('/chat/completions', params);
  }

  private async *parseStream(stream: AsyncIterable<string>): AsyncIterable<JsonObject> {
    for await (const chunk of stream) {
      const parsed = JSON.parse(chunk) as JsonObject;
      yield parsed;
    }
  }
}

export class ChatResource {
  readonly completions: ChatCompletionsResource;

  constructor(client: ResourceBase['client']) {
    this.completions = new ChatCompletionsResource(client);
  }
}
