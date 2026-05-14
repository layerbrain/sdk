import { describe, expect, it, vi } from 'vitest';
import { HTTPClient } from '../src/core/http.js';
import { AuthenticationError, InternalServerError } from '../src/core/errors.js';

describe('http client', () => {
  it('requires auth by default for all requests', async () => {
    const client = new HTTPClient({
      apiKey: '',
      baseURL: 'https://api.layerbrain.com',
      fetch: vi.fn(),
    });

    await expect(client.get('/machines')).rejects.toBeInstanceOf(AuthenticationError);
  });

  it('normalizes base url and full urls', () => {
    const client = new HTTPClient({
      apiKey: 'sk-test',
      baseURL: 'https://test.api.com/v1/',
      fetch: vi.fn(),
    });

    expect(client.baseURL).toBe('https://test.api.com');
    expect(client.fullURL('/machines')).toBe('https://test.api.com/v1/machines');
    expect(client.fullURL('machines')).toBe('https://test.api.com/v1/machines');
  });

  it('does not retry by default', async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ error: { type: 'internal_error', message: 'boom' } }), {
        status: 500,
        headers: { 'content-type': 'application/json' },
      }),
    );

    const client = new HTTPClient({
      apiKey: 'sk-test',
      baseURL: 'https://api.layerbrain.com',
      fetch: fetchMock,
    });

    await expect(client.get('/models')).rejects.toBeInstanceOf(InternalServerError);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0][1]?.headers).toMatchObject({ 'x-layerbrain-source': 'api' });
  });

  it('retries when maxRetries is configured', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ error: { type: 'internal_error', message: 'boom' } }), {
          status: 500,
          headers: { 'content-type': 'application/json' },
        }),
      )
      .mockResolvedValueOnce(
        new Response(JSON.stringify({ object: 'list', data: [], has_more: false }), {
          status: 200,
          headers: { 'content-type': 'application/json' },
        }),
      );

    const client = new HTTPClient({
      apiKey: 'sk-test',
      baseURL: 'https://api.layerbrain.com',
      fetch: fetchMock,
      maxRetries: 1,
    });

    const result = await client.get('/models');
    expect(result.object).toBe('list');
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});
