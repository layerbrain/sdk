"""Snapshot commands."""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain_cli._input import load_json_input
from layerbrain_cli._output import (
    build_table,
    console,
    print_error,
    print_json,
    print_success,
    validate_output_format,
)
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="Snapshots", no_args_is_help=True)


@app.command("list")
def list_snapshots(
    output: str = typer.Option("table", "--output", help="Output format: table or json."),
) -> None:
    """List snapshots."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.snapshots.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Snapshots", [("ID", "cyan"), ("Name", "blue"), ("Machine", "magenta")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""), item.get("machine", ""))
    console.print(table)


@app.command()
def create(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create a snapshot."""
    client = Layerbrain()
    try:
        result = client.snapshots.create(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success("Snapshot created.")
    print_json(result)


@app.command("get")
def get_snapshot(
    id: str = typer.Argument(..., help="Snapshot ID."),
) -> None:
    """Retrieve a snapshot."""
    client = Layerbrain()
    try:
        result = client.snapshots.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command()
def download(
    id: str = typer.Argument(..., help="Snapshot ID."),
) -> None:
    """Fetch download metadata for a snapshot."""
    client = Layerbrain()
    try:
        result = client.snapshots.download(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command()
def restore(
    id: str = typer.Argument(..., help="Snapshot ID."),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Restore a snapshot."""
    client = Layerbrain()
    try:
        result = client.snapshots.restore(id, **load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success(f"Snapshot {id} restore requested.")
    print_json(result)
