import { VERSION } from '../version.js';
import { normalizeBaseURL, resolveConfig } from './config.js';
import {
  AuthenticationError,
  ConnectionError,
  TimeoutError,
  raiseForStatus,
} from './errors.js';
import { parseSSE, requireSSEBody } from './streaming.js';

export interface RequestOptions {
  query?: Record<string, unknown>;
  body?: unknown;
  headers?: Record<string, string>;
  timeout?: number;
  maxRetries?: number;
}

export interface HTTPClientOptions {
  apiKey?: string;
  baseURL?: string;
  timeout?: number;
  maxRetries?: number;
  fetch?: typeof fetch;
  headers?: Record<string, string>;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function withQuery(url: string, query?: Record<string, unknown>): string {
  if (!query) {
    return url;
  }

  const entries = Object.entries(query).filter(([, value]) => value !== undefined && value !== null);
  if (entries.length === 0) {
    return url;
  }

  const parsed = new URL(url);
  for (const [key, value] of entries) {
    parsed.searchParams.set(key, String(value));
  }

  return parsed.toString();
}

function retryableStatus(statusCode: number): boolean {
  return statusCode === 408 || statusCode === 409 || statusCode === 429 || statusCode >= 500;
}

function retryableError(error: unknown): boolean {
  return error instanceof TimeoutError || error instanceof ConnectionError;
}

function toJSONBody(body: unknown): string | undefined {
  if (body === undefined) {
    return undefined;
  }
  return JSON.stringify(body);
}

function parseBody(text: string): unknown {
  if (!text) {
    return {};
  }
  try {
    return JSON.parse(text);
  } catch {
    return { error: { message: text } };
  }
}

export class HTTPClient {
  readonly apiKey?: string;
  readonly baseURL: string;
  readonly timeout: number;
  readonly maxRetries: number;

  private readonly fetchImpl: typeof fetch;
  private readonly extraHeaders: Record<string, string>;

  constructor(options: HTTPClientOptions = {}) {
    const resolved = resolveConfig({ apiKey: options.apiKey, baseURL: options.baseURL });
    this.apiKey = resolved.apiKey;
    this.baseURL = normalizeBaseURL(resolved.baseURL);
    this.timeout = options.timeout ?? 30_000;
    this.maxRetries = options.maxRetries ?? 0;
    this.fetchImpl = options.fetch ?? fetch;
    this.extraHeaders = options.headers ?? {};
  }

  fullURL(path: string): string {
    const normalizedPath = path.startsWith('/') ? path : `/${path}`;
    return `${this.baseURL}/v1${normalizedPath}`;
  }

  requireAuth(): void {
    if (!this.apiKey) {
      throw new AuthenticationError(
        'No API key provided. Set LAYERBRAIN_API_KEY or pass apiKey to the client.',
      );
    }
  }

  private buildHeaders(extraHeaders?: Record<string, string>): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'User-Agent': `layerbrain-node/${VERSION} node/${process.versions.node}`,
      ...this.extraHeaders,
      ...(extraHeaders ?? {}),
    };

    if (this.apiKey) {
      headers.Authorization = `Bearer ${this.apiKey}`;
    }

    return headers;
  }

  private async requestResponse(method: string, path: string, options: RequestOptions = {}): Promise<Response> {
    this.requireAuth();

    const maxRetries = options.maxRetries ?? this.maxRetries;
    const timeout = options.timeout ?? this.timeout;
    const url = withQuery(this.fullURL(path), options.query);

    for (let attempt = 0; ; attempt += 1) {
      const controller = new AbortController();
      const timeoutHandle = setTimeout(() => controller.abort(), timeout);

      try {
        const response = await this.fetchImpl(url, {
          method,
          headers: this.buildHeaders(options.headers),
          body: toJSONBody(options.body),
          signal: controller.signal,
        });

        if (retryableStatus(response.status) && attempt < maxRetries) {
          await sleep(Math.min(250 * 2 ** attempt, 2_000));
          continue;
        }

        return response;
      } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
          const timeoutError = new TimeoutError(`Request timed out after ${timeout}ms`);
          if (attempt < maxRetries) {
            await sleep(Math.min(250 * 2 ** attempt, 2_000));
            continue;
          }
          throw timeoutError;
        }

        const connectionError =
          error instanceof ConnectionError
            ? error
            : new ConnectionError(
                error instanceof Error ? `Connection failed: ${error.message}` : 'Connection failed',
              );

        if (retryableError(connectionError) && attempt < maxRetries) {
          await sleep(Math.min(250 * 2 ** attempt, 2_000));
          continue;
        }

        throw connectionError;
      } finally {
        clearTimeout(timeoutHandle);
      }
    }
  }

  private async requestJSON(method: string, path: string, options: RequestOptions = {}): Promise<Record<string, unknown>> {
    const response = await this.requestResponse(method, path, options);
    const text = await response.text();
    const parsed = parseBody(text);
    raiseForStatus(response.status, parsed);

    if (typeof parsed === 'object' && parsed !== null) {
      return parsed as Record<string, unknown>;
    }

    return {};
  }

  async get(path: string, options: RequestOptions = {}): Promise<Record<string, unknown>> {
    return this.requestJSON('GET', path, options);
  }

  async post(path: string, options: RequestOptions = {}): Promise<Record<string, unknown>> {
    return this.requestJSON('POST', path, options);
  }

  async patch(path: string, options: RequestOptions = {}): Promise<Record<string, unknown>> {
    return this.requestJSON('PATCH', path, options);
  }

  async put(path: string, options: RequestOptions = {}): Promise<Record<string, unknown>> {
    return this.requestJSON('PUT', path, options);
  }

  async delete(path: string, options: RequestOptions = {}): Promise<Record<string, unknown>> {
    return this.requestJSON('DELETE', path, options);
  }

  async streamSSE(path: string, body: Record<string, unknown>, options: RequestOptions = {}): Promise<AsyncIterable<string>> {
    const response = await this.requestResponse('POST', path, {
      ...options,
      body,
      headers: {
        Accept: 'text/event-stream',
        ...(options.headers ?? {}),
      },
    });

    if (!response.ok) {
      const text = await response.text();
      raiseForStatus(response.status, parseBody(text));
    }

    return parseSSE(requireSSEBody(response));
  }
}
