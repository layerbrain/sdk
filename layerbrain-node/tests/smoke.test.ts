import { describe, expect, it } from 'vitest';
import { Layerbrain } from '../src/index.js';

describe('smoke', () => {
  it('constructs client', () => {
    const client = new Layerbrain();
    expect(client).toBeTruthy();
  });

  it('exposes only the public OpenAPI resource surface', () => {
    const client = new Layerbrain();

    expect('auth' in client).toBe(false);
    expect('engrams' in client).toBe(false);
    expect('environments' in client).toBe(false);
    expect('tools' in client).toBe(false);
    expect(client.events).toBeTruthy();
    expect(client.exports).toBeTruthy();
    expect(client.plans).toBeTruthy();
    expect(client.storage).toBeTruthy();
    expect(client.webhooks).toBeTruthy();
    expect(client.work).toBeTruthy();
  });
});
