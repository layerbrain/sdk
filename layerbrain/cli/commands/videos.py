"""Videos commands for the Layerbrain CLI.

Auto-generated from OpenAPI spec. Manual edits will be overwritten
on next regeneration.
"""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain.cli._input import load_json_input
from layerbrain.cli._output import (
    print_error,
    print_json,
    print_success,
)
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="Videos", no_args_is_help=True)


@app.command()
def create(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create video generation."""
    client = Layerbrain()
    try:
        result = client.videos.create(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success("Video generation created.")
    print_json(result)


@app.command("get")
def get_videos(
    generation_id: str = typer.Argument(..., help="Videos ID"),
) -> None:
    """Get video generation status and result."""
    client = Layerbrain()
    try:
        result = client.videos.retrieve(generation_id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())
