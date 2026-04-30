"""Network commands."""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain_cli._input import load_json_input
from layerbrain_cli._output import (
    build_table,
    console,
    print_error,
    print_json,
    validate_output_format,
)
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="Networks", no_args_is_help=True)


@app.command("list")
def list_networks(
    output: str = typer.Option("table", "--output", help="Output format: table or json."),
) -> None:
    """List networks."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.networks.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Networks", [("ID", "cyan"), ("Name", "blue"), ("State", "magenta")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""), item.get("state", ""))
    console.print(table)


@app.command("get")
def get_network(
    id: str = typer.Argument(..., help="Network ID."),
) -> None:
    """Retrieve a network."""
    client = Layerbrain()
    try:
        result = client.networks.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command()
def update(
    id: str = typer.Argument(..., help="Network ID."),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Update a network."""
    client = Layerbrain()
    try:
        result = client.networks.update(id, **load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)
