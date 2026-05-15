# Changelog

All notable changes to this project are documented in this file.

## 0.0.2 - 2026-05-15

- Send WebSocket request payloads in `body` for machine session commands.
- Refresh machine WebSocket contract examples from the public OpenAPI spec.

## 0.0.1 - 2026-04-30

- Move the Node SDK under the Layerbrain multi-package repository.
- Keep the published npm package name as `layerbrain`.
- Generate the public resource surface and API docs from the repository OpenAPI contract.

## 0.1.2 - 2026-02-18

- Update documentation examples to consistently pass `apiKey` in client construction.
- Release republish after npm token update.

## 0.1.1 - 2026-02-18

- Add tag-driven npm publish workflow for GitHub Actions (`v*` tags).
- Align README format with python repo style.
- Document API key usage in the machine WebSocket example.

## 0.1.0 - 2026-02-18

- Initialize the `layerbrain` Node.js SDK package with TypeScript and Vitest tooling.
- Add core config resolution, HTTP transport, retries/timeouts, SSE streaming, and typed errors.
- Implement pagination primitives and async auto-paging support.
- Add machine WebSocket transport and `MachineConnection.exec()` for the `machine.command` session path.
- Add generated API resources and normalized client surface (`apiKeys`, `images`, `videos`, `threeD`, `chat.completions`).
- Add openai-node style documentation (`README.md`, `api.md`).
- Add parity-focused test coverage for config/auth/error/retry/pagination/streaming/models/machines behavior.
