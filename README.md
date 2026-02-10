# Layerbrain Python SDK

[![PyPI version](https://img.shields.io/pypi/v/layerbrain.svg)](https://pypi.org/project/layerbrain/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/layerbrain/layerbrain-python/blob/main/LICENSE)

The official Python SDK and CLI for the [Layerbrain](https://layerbrain.com) API.

## Installation

```sh
# SDK only
pip install layerbrain

# SDK + CLI
pip install layerbrain[cli]
```

## Quick Start

```python
from layerbrain import Layerbrain

client = Layerbrain()
```

The client reads your API key from the `LAYERBRAIN_API_KEY` environment variable by default. You can also pass it explicitly:

```python
client = Layerbrain(api_key="sk-...")
```

## SDK

### Chat Completions

```python
response = client.chat.completions.create(
    model="meta-llama/llama-3.1-8b",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

### Streaming

```python
stream = client.chat.completions.create(
    model="meta-llama/llama-3.1-8b",
    messages=[{"role": "user", "content": "Count to 10"}],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

### Machines

```python
# List available compute
compute = client.compute.list()

# Create a machine
machine = client.machines.create(compute="na-us-ca-sfo_s.small", duration_minutes=60)
print(machine.id, machine.host)

# Get machine details
machine = client.machines.retrieve("mach_abc123")

# Delete
client.machines.delete("mach_abc123")
```

### Machine Connect (WebSocket)

Connect to a running machine via WebSocket for shell and filesystem access:

```python
import asyncio
from layerbrain import Layerbrain

async def main():
    client = Layerbrain()

    # Connect to a running machine via WebSocket
    async with await client.machines.connect("mach_abc123") as conn:
        # Shell - execute commands
        result = await conn.shell.execute("ls -la ~/brain")
        print(result["stdout"])

        result = await conn.shell.execute("pip install requests", cwd="/root")
        print(result["code"])  # 0 = success

        # Filesystem - list files
        files = await conn.filesystem.list("~/brain")
        for f in files:
            print(f["name"], f["kind"])  # "docs" "folder", "main.py" "file"

        # Filesystem - read/write files
        await conn.filesystem.write("~/brain/hello.txt", "Hello World")
        content = await conn.filesystem.read("~/brain/hello.txt")

        # Filesystem - directory operations
        await conn.filesystem.mkdir("~/brain/newdir")
        await conn.filesystem.move("~/brain/hello.txt", "~/brain/newdir/hello.txt")
        await conn.filesystem.copy("~/brain/newdir/hello.txt", "~/brain/backup.txt")
        await conn.filesystem.delete("~/brain/backup.txt")

        # Filesystem - search
        results = await conn.filesystem.search("*.py", path="~/brain")
        recents = await conn.filesystem.recents(limit=10, days=3)

asyncio.run(main())
```

#### Shell Operations

| Method | Description |
|---|---|
| `conn.shell.execute(cmd, cwd=None, timeout=30)` | Execute command, returns `{stdout, stderr, code}` |

#### Filesystem Operations

| Method | Description |
|---|---|
| `conn.filesystem.list(path, show_all=False)` | List directory contents |
| `conn.filesystem.stat(path)` | Get file/folder metadata |
| `conn.filesystem.read(path)` | Read file (base64 encoded) |
| `conn.filesystem.write(path, data, encoding="utf-8")` | Write file |
| `conn.filesystem.mkdir(path)` | Create directory (recursive) |
| `conn.filesystem.delete(path)` | Delete file or directory |
| `conn.filesystem.move(src, dst)` | Move/rename |
| `conn.filesystem.copy(src, dst)` | Copy |
| `conn.filesystem.search(pattern, path, limit)` | Search by name |
| `conn.filesystem.recents(path, limit, days)` | Recently modified files |

### Models

```python
models = client.models.list()
for m in models.data:
    print(m["id"], m["type"])

model = client.models.retrieve("meta-llama/llama-3.1-8b")
```

### Tools

```python
# Web search
results = client.tools.search(query="python httpx tutorial", count=5)
for r in results["results"]:
    print(r["title"], r["url"])

# Fetch page content
page = client.tools.fetch(url="https://example.com")
print(page["content"])
```

### Secrets

```python
client.secrets.create(name="HF_TOKEN", value="hf_...")
secrets = client.secrets.list()
```

### Async

The same client works in async contexts -- just `await` the calls:

```python
import asyncio
from layerbrain import Layerbrain

async def main():
    async with Layerbrain() as client:
        response = await client.chat.completions.create(
            model="meta-llama/llama-3.1-8b",
            messages=[{"role": "user", "content": "Hello!"}],
        )
        print(response.choices[0].message.content)

asyncio.run(main())
```

### Error Handling

```python
from layerbrain import Layerbrain
from layerbrain.exceptions import (
    AuthenticationError,
    InsufficientFundsError,
    CapacityError,
    RateLimitError,
    APIError,
)

client = Layerbrain()

try:
    client.machines.create(compute="na-us-ca-sfo_s.small")
except AuthenticationError:
    print("Invalid API key")
except InsufficientFundsError:
    print("Not enough credits")
except CapacityError:
    print("No machines available")
except RateLimitError:
    print("Too many requests, back off")
except APIError as e:
    print(f"{e.status_code}: {e.message}")
```

| Status | Exception |
|---|---|
| 400 | `ValidationError` |
| 401 | `AuthenticationError` |
| 402 | `InsufficientFundsError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 409 | `ConflictError` |
| 429 | `RateLimitError` |
| 500 | `InternalServerError` |
| 502 | `ProviderError` |
| 503 | `CapacityError` |
| N/A | `ConnectionError` |
| N/A | `TimeoutError` |

## CLI

Requires `pip install layerbrain[cli]`.

```sh
# Account
layerbrain login
layerbrain whoami
layerbrain logout
layerbrain upgrade

# AI
layerbrain chat completions create --model meta-llama/llama-3.1-8b --message "Hello"
layerbrain models list
layerbrain models get meta-llama/llama-3.1-8b
layerbrain embeddings create --model BAAI/bge-large-en-v1.5 --input "Hello world"
layerbrain images generate --model black-forest-labs/flux-schnell --prompt "A cat"
layerbrain audio speech --model hexgrad/kokoro --input "Hello world"

# Tools
layerbrain tools search --query "python httpx"
layerbrain tools fetch --url "https://example.com"

# Brain
layerbrain brains create
layerbrain engrams list
layerbrain engrams create --name "my-session"

# Compute & Machines
layerbrain compute list
layerbrain machines list
layerbrain machines create --compute na-us-ca-sfo_s.small --duration 60
layerbrain machines get mach_abc123
layerbrain machines delete mach_abc123

# SSH into a machine (interactive session)
layerbrain machines ssh --id mach_abc123
layerbrain machines ssh --id mach_abc123 --user root

# Infrastructure
layerbrain environments list
layerbrain secrets list
layerbrain secrets create --name HF_TOKEN --value "hf_..."
layerbrain organizations list
layerbrain api-keys list
layerbrain api-keys create --name "production"

# Config
layerbrain config set default_output json
```

All list commands support `--output json` for JSON output.

## Configuration

The client reads configuration from (in priority order):

1. Explicit arguments: `Layerbrain(api_key="sk-...")`
2. Environment variables: `LAYERBRAIN_API_KEY`, `LAYERBRAIN_BASE_URL`
3. Config files: `~/.layerbrain/credentials.toml`, `~/.layerbrain/config.toml`

## Requirements

Python 3.10+
