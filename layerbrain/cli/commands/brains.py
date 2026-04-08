"""Brain resource commands."""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain.cli._input import load_json_input
from layerbrain.cli._output import print_error, print_json, print_success
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="Brains", no_args_is_help=True)


@app.command()
def create(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create a new brain resource."""
    client = Layerbrain()
    try:
        result = client.brains.create(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success("Brain created.")
    print_json(result)


@app.command("get")
def get_brain(
    id: str = typer.Argument(..., help="Brain ID."),
) -> None:
    """Retrieve a brain by ID."""
    client = Layerbrain()
    try:
        result = client.brains.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command()
def archive(
    id: str = typer.Argument(..., help="Brain ID."),
) -> None:
    """Archive a brain."""
    client = Layerbrain()
    try:
        result = client.brains.archive(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Brain {id} archived.")
    print_json(result)


@app.command()
def delete(
    id: str = typer.Argument(..., help="Brain ID."),
) -> None:
    """Delete a brain."""
    typer.confirm(f"Delete brain {id}?", abort=True)
    client = Layerbrain()
    try:
        result = client.brains.delete(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Brain {id} deleted.")
    print_json(result)
