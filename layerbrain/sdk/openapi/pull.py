"""Pull the OpenAPI spec from the layerbrain/openapi GitHub repo."""

from __future__ import annotations

import json
from pathlib import Path

import httpx

SPEC_DIR = Path(__file__).parent
SPEC_FILE = SPEC_DIR / "openapi.json"

# Raw GitHub URL for the openapi repo
SPEC_URL = (
    "https://raw.githubusercontent.com/layerbrain/openapi/main/openapi.json"
)


def pull(url: str | None = None) -> Path:
    """Fetch the OpenAPI spec from GitHub and save it locally.

    Args:
        url: Override the spec URL. Defaults to the layerbrain/openapi repo.

    Returns:
        Path to the written spec file.
    """
    response = httpx.get(url or SPEC_URL, timeout=30.0, follow_redirects=True)
    response.raise_for_status()

    spec = response.json()
    SPEC_FILE.write_text(json.dumps(spec, indent=2) + "\n")
    return SPEC_FILE


def load() -> dict:
    """Load the local OpenAPI spec from disk.

    Returns:
        Parsed OpenAPI spec dict.

    Raises:
        FileNotFoundError: If the spec hasn't been pulled yet.
    """
    if not SPEC_FILE.exists():
        raise FileNotFoundError(
            f"No OpenAPI spec found at {SPEC_FILE}. "
            "Run 'layerbrain internal pull-spec' to fetch it."
        )
    return json.loads(SPEC_FILE.read_text())
