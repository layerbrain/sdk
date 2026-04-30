# Layerbrain

Layerbrain ships separate SDK and CLI packages from one repository. The API exports the shared public contract to `openapi/openapi.json`; each language SDK owns its own runtime and package metadata.

## Packages

| Folder | Package | Install |
|---|---|---|
| `layerbrain-python/` | Python SDK | `pip install layerbrain` |
| `layerbrain-node/` | Node SDK | `npm install layerbrain` |
| `cli/` | CLI command | `curl -fsSL https://layerbrain.com/install.sh \| sh` |

## Python SDK

```python
from layerbrain import Layerbrain

client = Layerbrain()
models = client.models.list()
```

The Python SDK is the only artifact published to PyPI as `layerbrain`.

## Node SDK

```ts
import { Layerbrain } from "layerbrain";

const client = new Layerbrain();
const models = await client.models.list();
```

The Node SDK is the only artifact published to npm as `layerbrain`.

## CLI

```sh
layerbrain login
layerbrain whoami
layerbrain models list
layerbrain machines list
layerbrain listen --events machine.created
```

The CLI is installed as a command artifact. The website installer should mirror [`cli/install.sh`](cli/install.sh).

## Development

Run checks from each package folder:

```sh
cd layerbrain-python
python -m unittest discover -s tests -v

cd ../layerbrain-node
npm run generate:resources
npm run generate:api-docs
npm run build
npm test

cd ../cli
python -m unittest discover -s tests -v
```

Export the public API contract from the API repo before regenerating SDK code:

```sh
cd ../api
source venv/bin/activate
python manage.py openapi --path ../layerbrain/openapi/openapi.json

cd ../layerbrain
.venv/bin/python scripts/generate.py

cd layerbrain-node
npm run generate:resources
npm run generate:api-docs
```

Use `python scripts/check_versions.py` from the repository root before release.

The SDKs are generated from the public OpenAPI export. Do not use `python manage.py openapi --all` for SDK generation; `--all` is only for internal inspection.

## Releases

Each package releases from its own tag namespace:

| Tag | Publishes |
|---|---|
| `python-v0.0.1` | `layerbrain-python/` to PyPI as `layerbrain` |
| `node-v0.0.1` | `layerbrain-node/` to npm as `layerbrain` |
| `cli-v0.0.1` | `cli/` binaries for Linux and macOS to the GitHub release used by `install.sh` |

Package versions do not need to match across Python, Node, and CLI. `python scripts/check_versions.py --release-tag <tag>` verifies that the tag matches only the package being released.

The publish workflow uses these repository secrets:

| Secret | Used for |
|---|---|
| `PYPI_API_TOKEN` | Publishing the Python SDK to PyPI |
| `NPM_TOKEN` | Publishing the Node SDK to npm |

GitHub release uploads for the CLI use the built-in `GITHUB_TOKEN`; no extra repository secret is needed for that.
