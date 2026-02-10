"""Environments commands for the Layerbrain CLI.

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

app = typer.Typer(help="Environments", no_args_is_help=True)


@app.command("list")
def list_environments(
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """List environments for the authenticated user's organization."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.environments.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Environments", [("ID", "cyan"), ("Name", "blue")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""))
    console.print(table)


@app.command()
def create() -> None:
    """Create (or return) an environment by slug."""
    client = Layerbrain()
    try:
        result = client.environments.create()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Environments created.")
    print_json(result)


@app.command("get")
def get_environments(
    id: str = typer.Argument(..., help="Environments ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Retrieve a single environment by id."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.environments.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())
