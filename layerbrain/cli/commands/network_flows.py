"""Network flow commands."""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain.cli._output import (
    build_table,
    console,
    print_error,
    print_json,
    validate_output_format,
)
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="Network Flows", no_args_is_help=True)


@app.command("list")
def list_network_flows(
    output: str = typer.Option("table", "--output", help="Output format: table or json."),
) -> None:
    """List network flows."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.network_flows.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Network Flows", [("ID", "cyan"), ("Name", "blue"), ("State", "magenta")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""), item.get("state", ""))
    console.print(table)


@app.command("get")
def get_network_flow(
    id: str = typer.Argument(..., help="Network flow ID."),
) -> None:
    """Retrieve a network flow."""
    client = Layerbrain()
    try:
        result = client.network_flows.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)
