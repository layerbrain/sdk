import { describe, expect, it } from 'vitest';
import { ListPage } from '../src/core/pagination.js';
import { parseSSE } from '../src/core/streaming.js';

describe('pagination', () => {
  it('auto pages across next pages', async () => {
    const secondPage = new ListPage({
      data: [{ id: 'c' }],
      hasMore: false,
      page: 2,
      getNextPage: async () => {
        throw new Error('no more pages');
      },
    });

    const firstPage = new ListPage({
      data: [{ id: 'a' }, { id: 'b' }],
      hasMore: true,
      page: 1,
      getNextPage: async () => secondPage,
    });

    const ids: string[] = [];
    for await (const item of firstPage) {
      ids.push((item as { id: string }).id);
    }

    expect(ids).toEqual(['a', 'b', 'c']);
  });
});

describe('sse parser', () => {
  it('parses data frames and stops on done', async () => {
    const encoder = new TextEncoder();
    const body = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(encoder.encode('data: {"id":"1"}\n\n'));
        controller.enqueue(encoder.encode('data: {"id":"2"}\n\n'));
        controller.enqueue(encoder.encode('data: [DONE]\n\n'));
        controller.close();
      },
    });

    const chunks: string[] = [];
    for await (const chunk of parseSSE(body)) {
      chunks.push(chunk);
    }

    expect(chunks).toEqual(['{"id":"1"}', '{"id":"2"}']);
  });
});
