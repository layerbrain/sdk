"""Network rule commands."""

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

app = typer.Typer(help="Network Rules", no_args_is_help=True)


@app.command("list")
def list_network_rules(
    output: str = typer.Option("table", "--output", help="Output format: table or json."),
) -> None:
    """List network rules."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.network_rules.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Network Rules", [("ID", "cyan"), ("Name", "blue"), ("Action", "magenta")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""), item.get("action", ""))
    console.print(table)


@app.command()
def create(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create a network rule."""
    client = Layerbrain()
    try:
        result = client.network_rules.create(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success("Network rule created.")
    print_json(result)


@app.command("get")
def get_network_rule(
    id: str = typer.Argument(..., help="Network rule ID."),
) -> None:
    """Retrieve a network rule."""
    client = Layerbrain()
    try:
        result = client.network_rules.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command()
def update(
    id: str = typer.Argument(..., help="Network rule ID."),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Update a network rule."""
    client = Layerbrain()
    try:
        result = client.network_rules.update(id, **load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command()
def delete(
    id: str = typer.Argument(..., help="Network rule ID."),
) -> None:
    """Delete a network rule."""
    typer.confirm(f"Delete network rule {id}?", abort=True)
    client = Layerbrain()
    try:
        result = client.network_rules.delete(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success(f"Network rule {id} deleted.")
    print_json(result)
