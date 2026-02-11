"""Models commands for the Layerbrain CLI.

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

app = typer.Typer(help="Models", no_args_is_help=True)


@app.command("get")
def get_models(
    id: str = typer.Argument(..., help="Model ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Get a specific model by ID."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.models.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())
