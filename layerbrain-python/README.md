# Layerbrain Python SDK

The official Python SDK for the [Layerbrain](https://layerbrain.com) API.

## Installation

```sh
pip install layerbrain
```

## Quick Start

```python
from layerbrain import Layerbrain

client = Layerbrain()
models = client.models.list()
```

The client reads `LAYERBRAIN_API_KEY` by default. You can also pass an API key directly:

```python
client = Layerbrain(api_key="sk-...")
```

## Chat Completions

```python
response = client.chat.completions.create(
    model="meta-llama/llama-3.1-8b",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

## Streaming

```python
stream = client.chat.completions.create(
    model="meta-llama/llama-3.1-8b",
    messages=[{"role": "user", "content": "Count to 10"}],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

## Machines

```python
machine = client.machines.create(
    cpu=2,
    ram=4,
    disk=40,
    region="na-us-ca-sfo",
    ttl_minutes=60,
)
print(machine.id, machine.host)

machine = client.machines.retrieve("mch_abc123")
client.machines.delete("mch_abc123")
```

## Async

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

## Errors

```python
from layerbrain import Layerbrain
from layerbrain.exceptions import AuthenticationError, LayerbrainError

client = Layerbrain()

try:
    client.models.list()
except AuthenticationError:
    print("Invalid API key")
except LayerbrainError as error:
    print(error)
```

## Configuration

Configuration is resolved in this order:

1. Explicit client arguments: `Layerbrain(api_key="sk-...")`
2. Environment variables: `LAYERBRAIN_API_KEY`, `LAYERBRAIN_BASE_URL`
3. Local config files: `~/.layerbrain/credentials.toml`, `~/.layerbrain/config.toml`

## CLI

The `layerbrain` terminal command is distributed separately from the Python SDK:

```sh
curl -fsSL https://layerbrain.com/install.sh | sh
```
