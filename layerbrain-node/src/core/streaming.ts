import { ConnectionError } from './errors.js';

export async function* parseSSE(body: ReadableStream<Uint8Array>): AsyncIterable<string> {
  const reader = body.getReader();
  const decoder = new TextDecoder();

  let buffer = '';
  let eventData: string[] = [];

  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }

    buffer += decoder.decode(value, { stream: true });

    while (true) {
      const newlineIndex = buffer.indexOf('\n');
      if (newlineIndex < 0) {
        break;
      }

      const line = buffer.slice(0, newlineIndex).replace(/\r$/, '');
      buffer = buffer.slice(newlineIndex + 1);

      if (line.length === 0) {
        if (eventData.length > 0) {
          const data = eventData.join('\n');
          eventData = [];
          if (data === '[DONE]') {
            return;
          }
          yield data;
        }
        continue;
      }

      if (line.startsWith('data:')) {
        eventData.push(line.slice(5).trimStart());
      }
    }
  }
}

export function requireSSEBody(response: Response): ReadableStream<Uint8Array> {
  if (!response.body) {
    throw new ConnectionError('No response body for SSE stream');
  }
  return response.body;
}
