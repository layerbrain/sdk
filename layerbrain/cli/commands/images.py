"""Images commands for the Layerbrain CLI.

Auto-generated from OpenAPI spec. Manual edits will be overwritten
on next regeneration.
"""

from __future__ import annotations

from typing import Optional

import typer

from layerbrain import Layerbrain
from layerbrain.exceptions import LayerbrainError
from layerbrain.cli._output import (
    build_table,
    console,
    print_error,
    print_json,
    print_success,
    validate_output_format,
)

app = typer.Typer(help="Images", no_args_is_help=True)


@app.command("edits")
def edits(
    id: str = typer.Argument(..., help="Images ID"),
) -> None:
    """Create image edit (image-to-image)."""
    client = Layerbrain()
    try:
        result = client.images.edits()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("generations")
def generations(
    id: str = typer.Argument(..., help="Images ID"),
) -> None:
    """Create image generation."""
    client = Layerbrain()
    try:
        result = client.images.generations()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)
