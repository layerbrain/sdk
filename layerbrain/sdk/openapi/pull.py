"""Pull and load the local OpenAPI spec."""

from __future__ import annotations

import json
from pathlib import Path

import httpx

SPEC_DIR = Path(__file__).parent
SPEC_FILE = SPEC_DIR / "openapi.json"
REPO_ROOT = Path(__file__).resolve().parents[3]
REPO_SPEC_FILE = REPO_ROOT / "openapi" / "openapi.json"

SPEC_URL = (
    "https://raw.githubusercontent.com/layerbrain/openapi/main/openapi.json"
)


def _write_spec(spec: dict) -> Path:
    serialized = json.dumps(spec, indent=2) + "\n"
    SPEC_FILE.parent.mkdir(parents=True, exist_ok=True)
    SPEC_FILE.write_text(serialized)
    if (REPO_ROOT / "pyproject.toml").exists():
        REPO_SPEC_FILE.parent.mkdir(parents=True, exist_ok=True)
        REPO_SPEC_FILE.write_text(serialized)
    return SPEC_FILE


def pull(url: str | None = None) -> Path:
    """Fetch the OpenAPI spec and save the local copies.

    Args:
        url: Override the spec URL. Defaults to the layerbrain/openapi repo.

    Returns:
        Path to the written spec file.
    """
    response = httpx.get(url or SPEC_URL, timeout=30.0, follow_redirects=True)
    response.raise_for_status()
    return _write_spec(response.json())


def load() -> dict:
    """Load the local OpenAPI spec from disk.

    Returns:
        Parsed OpenAPI spec dict.

    Raises:
        FileNotFoundError: If the spec hasn't been pulled yet.
    """
    source = REPO_SPEC_FILE if REPO_SPEC_FILE.exists() else SPEC_FILE
    if not source.exists():
        raise FileNotFoundError(
            f"No OpenAPI spec found at {source}. "
            "Run 'layerbrain internal pull-spec' to fetch it."
        )
    return json.loads(source.read_text())
