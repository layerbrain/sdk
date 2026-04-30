import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import TOML from '@iarna/toml';

export const DEFAULT_BASE_URL = 'https://api.layerbrain.com';
export const CONFIG_DIR = path.join(os.homedir(), '.layerbrain');
export const CONFIG_FILE = path.join(CONFIG_DIR, 'config.toml');
export const CREDENTIALS_FILE = path.join(CONFIG_DIR, 'credentials.toml');

export interface ResolvedConfig {
  apiKey?: string;
  baseURL: string;
}

type TomlRecord = Record<string, unknown>;

function loadToml(filePath: string): TomlRecord {
  try {
    const contents = fs.readFileSync(filePath, 'utf8');
    const parsed = TOML.parse(contents);
    if (typeof parsed === 'object' && parsed !== null) {
      return parsed as TomlRecord;
    }
    return {};
  } catch {
    return {};
  }
}

function stringValue(obj: TomlRecord, key: string): string | undefined {
  const value = obj[key];
  return typeof value === 'string' && value.trim() ? value.trim() : undefined;
}

export function normalizeBaseURL(value: string): string {
  let result = value.trim().replace(/\/+$/, '');
  if (result.endsWith('/v1')) {
    result = result.slice(0, -3);
  }
  return result || DEFAULT_BASE_URL;
}

export function resolveConfig(overrides: { apiKey?: string; baseURL?: string } = {}): ResolvedConfig {
  const configToml = loadToml(CONFIG_FILE);
  const credentialsToml = loadToml(CREDENTIALS_FILE);

  const resolvedApiKey =
    overrides.apiKey ?? process.env.LAYERBRAIN_API_KEY?.trim() ?? stringValue(credentialsToml, 'api_key');

  const resolvedBaseURL =
    overrides.baseURL ??
    process.env.LAYERBRAIN_BASE_URL?.trim() ??
    stringValue(configToml, 'base_url') ??
    DEFAULT_BASE_URL;

  return {
    apiKey: resolvedApiKey && resolvedApiKey.length > 0 ? resolvedApiKey : undefined,
    baseURL: normalizeBaseURL(resolvedBaseURL),
  };
}
