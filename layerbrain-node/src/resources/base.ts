import { HTTPClient } from '../core/http.js';
import { ListPage } from '../core/pagination.js';

export interface ListParams {
  page?: number;
  pageSize?: number;
  ordering?: string;
}

export type JsonObject = Record<string, unknown>;

function asObject(value: unknown): JsonObject {
  if (typeof value === 'object' && value !== null) {
    return value as JsonObject;
  }
  return {};
}

function asObjectArray(value: unknown): JsonObject[] {
  if (!Array.isArray(value)) {
    return [];
  }
  return value.map((item) => asObject(item));
}

export class ResourceBase {
  constructor(protected readonly client: HTTPClient) {}

  protected async get(path: string, query?: Record<string, unknown>): Promise<JsonObject> {
    return this.client.get(path, { query });
  }

  protected async post(path: string, body?: Record<string, unknown>): Promise<JsonObject> {
    return this.client.post(path, { body });
  }

  protected async patch(path: string, body?: Record<string, unknown>): Promise<JsonObject> {
    return this.client.patch(path, { body });
  }

  protected async put(path: string, body?: Record<string, unknown>): Promise<JsonObject> {
    return this.client.put(path, { body });
  }

  protected async delete(path: string): Promise<JsonObject> {
    return this.client.delete(path);
  }

  protected listQuery(params: ListParams = {}): Record<string, unknown> | undefined {
    const query: Record<string, unknown> = {};

    if (params.page !== undefined) {
      query.page = params.page;
    }

    if (params.pageSize !== undefined) {
      query.page_size = params.pageSize;
    }

    if (params.ordering !== undefined) {
      query.ordering = params.ordering;
    }

    return Object.keys(query).length > 0 ? query : undefined;
  }

  protected async listResource(path: string, params: ListParams = {}): Promise<ListPage<JsonObject>> {
    const response = await this.get(path, this.listQuery(params));
    return this.toListPage(path, response, params);
  }

  protected toListPage(path: string, response: JsonObject, params: ListParams = {}): ListPage<JsonObject> {
    const data = asObjectArray(response.data);
    const hasMore = Boolean(response.has_more);
    const currentPage = typeof params.page === 'number' ? params.page : 1;

    return new ListPage<JsonObject>({
      data,
      hasMore,
      page: currentPage,
      getNextPage: async (page) => {
        const nextParams: ListParams = { ...params, page };
        const nextResponse = await this.get(path, this.listQuery(nextParams));
        return this.toListPage(path, nextResponse, nextParams);
      },
    });
  }
}
