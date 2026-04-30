# Layerbrain CLI

The Layerbrain CLI installs the `layerbrain` command for account, model, machine, webhook, and API operations from a terminal.

## Install

```sh
curl -fsSL https://layerbrain.com/install.sh | sh
```

Install a specific CLI release:

```sh
curl -fsSL https://layerbrain.com/install.sh | LAYERBRAIN_VERSION=cli-v0.0.1 sh
```

The website installer should mirror [`install.sh`](./install.sh) from this repository.

By default the installer writes the binary to `~/.layerbrain/bin/layerbrain`. Add that directory to your `PATH` if the installer reports that it is not already available.

## Usage

```sh
layerbrain login
layerbrain whoami
layerbrain models list
layerbrain machines list
layerbrain listen --events machine.created
layerbrain webhooks list
```

## Development

Install the Python SDK and CLI in editable mode:

```sh
python -m pip install -e ../layerbrain-python
python -m pip install -e .
python -m unittest discover -s tests -v
```

Build the installable CLI artifact for the current platform from the repository root:

```sh
cli/scripts/build-artifact.sh
```

The artifact is written as `cli/dist/layerbrain-<platform>-<architecture>.tar.gz`, matching the name expected by `install.sh`.

The CLI is released as a command artifact, not as the `layerbrain` PyPI package. The `layerbrain` PyPI package belongs to the Python SDK.
