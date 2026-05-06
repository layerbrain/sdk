# Layerbrain

Layerbrain ships SDK packages from one repository. The API exports the shared public contract to `openapi/openapi.json`; each language SDK owns its own runtime and package metadata.

## Packages

| Folder | Package | Install |
|---|---|---|
| `layerbrain-python/` | Python SDK | `pip install layerbrain` |
| `layerbrain-node/` | Node SDK | `npm install layerbrain` |

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

Package versions do not need to match across Python and Node. `python scripts/check_versions.py --release-tag <tag>` verifies that the tag matches only the package being released.

The publish workflow uses these repository secrets:

| Secret | Used for |
|---|---|
| `PYPI_API_TOKEN` | Publishing the Python SDK to PyPI |
| `NPM_TOKEN` | Publishing the Node SDK to npm |
