"""Videos commands for the Layerbrain CLI.

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

app = typer.Typer(help="Videos", no_args_is_help=True)


@app.command("generations")
def generations(
    id: str = typer.Argument(..., help="Videos ID"),
) -> None:
    """Create video generation."""
    client = Layerbrain()
    try:
        result = client.videos.generations()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("get")
def get_videos(
    generation_id: str = typer.Argument(..., help="Videos ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Get video generation status and result."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.videos.retrieve(generation_id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())
