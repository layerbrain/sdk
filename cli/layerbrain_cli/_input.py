"""Command input helpers for JSON request bodies."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer


def load_json_input(data: str | None, data_file: str | None) -> dict[str, Any]:
    """Load a JSON object from inline data or a file path."""
    if data and data_file:
        raise typer.BadParameter("Use either --data or --data-file, not both.")

    if data_file:
        raw = Path(data_file).read_text()
    elif data:
        raw = data
    else:
        return {}

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"Invalid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise typer.BadParameter("JSON input must be an object.")

    return payload
