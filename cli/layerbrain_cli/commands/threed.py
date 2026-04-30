"""3D generation commands."""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain_cli._input import load_json_input
from layerbrain_cli._output import print_error, print_json, print_success
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="3D", no_args_is_help=True)


@app.command()
def create(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create a 3D generation."""
    client = Layerbrain()
    try:
        result = client.threed.create(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success("3D generation created.")
    print_json(result)


@app.command("get")
def get_generation(
    generation_id: str = typer.Argument(..., help="Generation ID."),
) -> None:
    """Retrieve a 3D generation by ID."""
    client = Layerbrain()
    try:
        result = client.threed.retrieve(generation_id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)
