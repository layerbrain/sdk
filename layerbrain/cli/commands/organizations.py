"""Organizations commands for the Layerbrain CLI.

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

app = typer.Typer(help="Organizations", no_args_is_help=True)


@app.command("list")
def list_organizations(
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """List organizations for the authenticated user."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.organizations.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Organizations", [("ID", "cyan"), ("Name", "blue")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""))
    console.print(table)


@app.command()
def create() -> None:
    """Handle organization creation."""
    client = Layerbrain()
    try:
        result = client.organizations.create()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Organizations created.")
    print_json(result)


@app.command()
def delete(
    id: str = typer.Argument(..., help="Organizations ID"),
) -> None:
    """Delete an organization."""
    typer.confirm(f"Delete organizations {id}?", abort=True)
    client = Layerbrain()
    try:
        client.organizations.delete(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Organizations {id} deleted.")


@app.command("get")
def get_organizations(
    id: str = typer.Argument(..., help="Organizations ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Retrieve a single organization."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.organizations.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())


@app.command("update")
def update(
    id: str = typer.Argument(..., help="Organizations ID"),
) -> None:
    """Update an organization."""
    client = Layerbrain()
    try:
        result = client.organizations.update(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)
