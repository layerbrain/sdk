import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';

async function loadConfigModule(homeDir: string) {
  vi.stubEnv('HOME', homeDir);
  vi.stubEnv('USERPROFILE', homeDir);
  vi.resetModules();
  return import('../src/core/config.ts');
}

afterEach(() => {
  vi.unstubAllEnvs();
});

describe('config resolution', () => {
  it('uses default base url when nothing else is set', async () => {
    const tmpHome = await fs.mkdtemp(path.join(os.tmpdir(), 'lb-node-config-default-'));
    const mod = await loadConfigModule(tmpHome);

    const resolved = mod.resolveConfig();
    expect(resolved.baseURL).toBe('https://api.layerbrain.com');
  });

  it('resolves from toml files when env is not set', async () => {
    const tmpHome = await fs.mkdtemp(path.join(os.tmpdir(), 'lb-node-config-files-'));
    const layerbrainDir = path.join(tmpHome, '.layerbrain');

    await fs.mkdir(layerbrainDir, { recursive: true });
    await fs.writeFile(path.join(layerbrainDir, 'config.toml'), 'base_url = "https://staging.layerbrain.test/v1"\n');
    await fs.writeFile(path.join(layerbrainDir, 'credentials.toml'), 'api_key = "sk-file-key"\n');

    const mod = await loadConfigModule(tmpHome);
    const resolved = mod.resolveConfig();

    expect(resolved.apiKey).toBe('sk-file-key');
    expect(resolved.baseURL).toBe('https://staging.layerbrain.test');
  });

  it('prioritizes constructor overrides over env and files', async () => {
    const tmpHome = await fs.mkdtemp(path.join(os.tmpdir(), 'lb-node-config-overrides-'));
    const layerbrainDir = path.join(tmpHome, '.layerbrain');

    await fs.mkdir(layerbrainDir, { recursive: true });
    await fs.writeFile(path.join(layerbrainDir, 'config.toml'), 'base_url = "https://from-file.test"\n');
    await fs.writeFile(path.join(layerbrainDir, 'credentials.toml'), 'api_key = "sk-from-file"\n');

    vi.stubEnv('LAYERBRAIN_API_KEY', 'sk-from-env');
    vi.stubEnv('LAYERBRAIN_BASE_URL', 'https://from-env.test/v1');

    const mod = await loadConfigModule(tmpHome);
    const resolved = mod.resolveConfig({
      apiKey: 'sk-from-constructor',
      baseURL: 'https://from-constructor.test/v1',
    });

    expect(resolved.apiKey).toBe('sk-from-constructor');
    expect(resolved.baseURL).toBe('https://from-constructor.test');
  });
});
