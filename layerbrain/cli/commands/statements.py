"""Statements commands for the Layerbrain CLI.

Auto-generated from OpenAPI spec. Manual edits will be overwritten
on next regeneration.
"""

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

app = typer.Typer(help="Statements", no_args_is_help=True)


@app.command("list")
def list_statements(
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """List usage statements with filtering and pagination."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.statements.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Statements", [("ID", "cyan"), ("Name", "blue")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""))
    console.print(table)


@app.command("get")
def get_statements(
    statement_id: str = typer.Argument(..., help="Statements ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Retrieve a specific statement by ID, creating it if it doesn't exist."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.statements.retrieve(statement_id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())
