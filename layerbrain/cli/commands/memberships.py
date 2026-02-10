"""Memberships commands for the Layerbrain CLI.

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

app = typer.Typer(help="Memberships", no_args_is_help=True)


@app.command("list")
def list_memberships(
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """List memberships based on query parameters:"""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.memberships.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Memberships", [("ID", "cyan"), ("Name", "blue")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""))
    console.print(table)


@app.command()
def create() -> None:
    """Create memberships or membership invites."""
    client = Layerbrain()
    try:
        result = client.memberships.create()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Memberships created.")
    print_json(result)


@app.command("accept")
def accept(
    id: str = typer.Argument(..., help="Memberships ID"),
) -> None:
    """Accept a membership invitation and connect the account to the membership."""
    client = Layerbrain()
    try:
        result = client.memberships.accept(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("cancel")
def cancel(
    id: str = typer.Argument(..., help="Memberships ID"),
) -> None:
    """Cancel a membership invitation. Both organization members and the invited user can cancel."""
    client = Layerbrain()
    try:
        result = client.memberships.cancel(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("get")
def get_memberships(
    id: str = typer.Argument(..., help="Memberships ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Retrieve a single membership."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.memberships.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())
