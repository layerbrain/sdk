# Layerbrain

Official SDKs and CLI for the Layerbrain API.

## Python

Install the Python SDK:

```sh
pip install layerbrain
```

Use it from normal scripts:

```python
from layerbrain import Layerbrain

client = Layerbrain()
models = client.models.list()
```

Inside async code, create the client normally and await SDK calls:

```python
from layerbrain import Layerbrain

async def main():
    client = Layerbrain()
    models = await client.models.list()
```

## Node

Install the Node SDK:

```sh
npm install layerbrain
```

Use it from TypeScript or JavaScript:

```ts
import { Layerbrain } from "layerbrain";

const client = new Layerbrain();
const models = await client.models.list();
```

## CLI

Install the CLI:

```sh
curl -fsSL https://layerbrain.com/install.sh | sh
```

Use the `layerbrain` command:

```sh
layerbrain login
layerbrain models list
layerbrain machines list
layerbrain listen --events machine.created
```

## Packages

- Python SDK: [`layerbrain-python/`](layerbrain-python/)
- Node SDK: [`layerbrain-node/`](layerbrain-node/)
- CLI: [`cli/`](cli/)
