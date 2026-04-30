# Layerbrain TypeScript and JavaScript API Library

This library provides convenient access to the Layerbrain REST API from TypeScript or JavaScript.

## Installation

```sh
npm install layerbrain
```

## Usage

```ts
import { Layerbrain } from 'layerbrain';

const client = new Layerbrain({
  apiKey: process.env.LAYERBRAIN_API_KEY, // default: LAYERBRAIN_API_KEY or ~/.layerbrain/credentials.toml
});

const completion = await client.chat.completions.create({
  model: 'meta-llama/llama-3.1-8b',
  messages: [{ role: 'user', content: 'Hello!' }],
});

console.log(completion);
```

The full API surface is documented in [api.md](./api.md).

## Streaming responses

```ts
import { Layerbrain } from 'layerbrain';

const client = new Layerbrain({
  apiKey: process.env.LAYERBRAIN_API_KEY,
});

const stream = await client.chat.completions.create({
  model: 'meta-llama/llama-3.1-8b',
  messages: [{ role: 'user', content: 'Count to 5' }],
  stream: true,
});

for await (const chunk of stream) {
  console.log(chunk);
}
```

## Machine WebSocket connections

```ts
import { Layerbrain } from 'layerbrain';

const client = new Layerbrain({
  apiKey: process.env.LAYERBRAIN_API_KEY,
});
const conn = await client.machines.connect('mach_abc123');

const result = await conn.shell.execute('ls -la ~/brain');
console.log(result.stdout);

const files = await conn.filesystem.list('~/brain');
console.log(files);

await conn.close();
```

## Handling errors

When the SDK cannot connect to the API, or the API returns a non-success response, it throws typed errors:

```ts
import { APIError, AuthenticationError, Layerbrain, RateLimitError } from 'layerbrain';

const client = new Layerbrain({
  apiKey: process.env.LAYERBRAIN_API_KEY,
});

try {
  await client.machines.create({ compute: 'na-us-ca-sfo_s.small' });
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.error('Invalid API key');
  } else if (error instanceof RateLimitError) {
    console.error('Rate limited');
  } else if (error instanceof APIError) {
    console.error(error.statusCode, error.message);
  } else {
    throw error;
  }
}
```

### Error map

| Status | Error Type |
| --- | --- |
| 400 | `ValidationError` |
| 401 | `AuthenticationError` |
| 402 | `InsufficientFundsError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 405 | `MethodNotAllowedError` |
| 409 | `ConflictError` |
| 429 | `RateLimitError` |
| 500 | `InternalServerError` |
| 502 | `ProviderError` |
| 503 | `CapacityError` |
| N/A | `ConnectionError` / `TimeoutError` |

## Retries

Requests are not retried by default.

```ts
const client = new Layerbrain({
  apiKey: process.env.LAYERBRAIN_API_KEY,
  maxRetries: 0, // default
});
```

You can override globally or per-request at the transport level.

## Timeouts

Requests use a `30_000ms` timeout by default.

```ts
const client = new Layerbrain({
  apiKey: process.env.LAYERBRAIN_API_KEY,
  timeout: 20_000,
});
```

## Auto-pagination

List methods return a `ListPage` with convenience helpers.

```ts
const client = new Layerbrain({
  apiKey: process.env.LAYERBRAIN_API_KEY,
});

const page = await client.machines.list();

for await (const machine of page) {
  console.log(machine.id);
}

const next = await page.nextPage();
console.log(next.data.length);
```

## Advanced usage

### Configuration resolution order

1. Explicit client options (`apiKey`, `baseURL`)
2. Environment variables (`LAYERBRAIN_API_KEY`, `LAYERBRAIN_BASE_URL`)
3. Files (`~/.layerbrain/credentials.toml`, `~/.layerbrain/config.toml`)

### Base URL normalization

If `baseURL` ends with `/v1`, the SDK strips it to avoid `/v1/v1` paths.

### Authentication

This SDK requires a non-empty API key for all HTTP calls.

## Requirements

- Node.js 18+
