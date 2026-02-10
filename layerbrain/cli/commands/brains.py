"""Brains commands for the Layerbrain CLI.

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

app = typer.Typer(help="Brains", no_args_is_help=True)


@app.command()
def create() -> None:
    """Create a new brain resource."""
    client = Layerbrain()
    try:
        result = client.brains.create()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Brains created.")
    print_json(result)
