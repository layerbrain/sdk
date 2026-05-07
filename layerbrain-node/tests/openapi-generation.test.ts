import { describe, expect, it } from 'vitest';
import { Layerbrain } from '../src/index.js';
import { collectOperations } from '../scripts/generate-resources.mjs';

describe('OpenAPI generated resources', () => {
  it('maps every public OpenAPI operation to the SDK surface', () => {
    const client = new Layerbrain({ apiKey: 'sk_test' }) as Record<string, Record<string, unknown>>;
    const resources = collectOperations();

    for (const resource of resources) {
      if (resource.manual) continue;

      const api = client[resource.property];
      expect(api, resource.property).toBeTruthy();

      for (const operation of resource.operations) {
        if (operation.kind === 'manual' || operation.kind === 'custom') continue;
        expect(typeof api[operation.method], `${resource.property}.${operation.method}`).toBe('function');
      }
    }
  });
});
