"""Load and sync the local OpenAPI spec."""

from __future__ import annotations

import json
from pathlib import Path

SPEC_DIR = Path(__file__).parent
SPEC_FILE = SPEC_DIR / "openapi.json"
REPO_ROOT = Path(__file__).resolve().parents[4]
REPO_SPEC_FILE = REPO_ROOT / "openapi" / "openapi.json"


def _write_spec(spec: dict) -> Path:
    serialized = json.dumps(spec, indent=2) + "\n"
    SPEC_FILE.parent.mkdir(parents=True, exist_ok=True)
    SPEC_FILE.write_text(serialized)
    if REPO_SPEC_FILE.parent.exists():
        REPO_SPEC_FILE.parent.mkdir(parents=True, exist_ok=True)
        REPO_SPEC_FILE.write_text(serialized)
    return SPEC_FILE


def sync(source: str | Path) -> Path:
    """Copy an OpenAPI spec into the SDK and repo contract locations.

    Args:
        source: Path to a public OpenAPI JSON file.

    Returns:
        Path to the written spec file.
    """
    return _write_spec(json.loads(Path(source).read_text()))


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
            "Export it with 'python manage.py openapi --path <repo>/openapi/openapi.json'."
        )
    return json.loads(source.read_text())
