import { describe, expect, it, vi } from 'vitest';
import { Layerbrain } from '../src/index.js';

describe('models', () => {
  it('encodes model ids with slashes', async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ id: 'meta-llama/llama-3.1-8b', object: 'model' }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      }),
    );

    const client = new Layerbrain({
      apiKey: 'sk-test',
      baseURL: 'https://api.layerbrain.com',
      fetch: fetchMock,
    });

    await client.models.retrieve('meta-llama/llama-3.1-8b');

    const [url] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toContain('/v1/models/meta-llama%2Fllama-3.1-8b');
  });
});

describe('chat streaming', () => {
  it('returns async iterable chat chunks', async () => {
    const encoder = new TextEncoder();
    const streamBody = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(encoder.encode('data: {"id":"a","choices":[{"delta":{"content":"Hel"}}]}\n\n'));
        controller.enqueue(encoder.encode('data: {"id":"a","choices":[{"delta":{"content":"lo"}}]}\n\n'));
        controller.enqueue(encoder.encode('data: [DONE]\n\n'));
        controller.close();
      },
    });

    const fetchMock = vi.fn().mockResolvedValue(
      new Response(streamBody, {
        status: 200,
        headers: { 'content-type': 'text/event-stream' },
      }),
    );

    const client = new Layerbrain({
      apiKey: 'sk-test',
      baseURL: 'https://api.layerbrain.com',
      fetch: fetchMock,
    });

    const stream = await client.chat.completions.create({
      model: 'meta-llama/llama-3.1-8b',
      messages: [{ role: 'user', content: 'hello' }],
      stream: true,
    });

    const chunks: Array<Record<string, unknown>> = [];
    for await (const chunk of stream as AsyncIterable<Record<string, unknown>>) {
      chunks.push(chunk);
    }

    expect(chunks).toHaveLength(2);
    expect((chunks[0].choices as Array<{ delta: { content: string } }>)[0].delta.content).toBe('Hel');
  });
});
