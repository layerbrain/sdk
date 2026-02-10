"""Accounts commands for the Layerbrain CLI.

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

app = typer.Typer(help="Accounts", no_args_is_help=True)


@app.command("list")
def list_accounts(
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Get current user's account."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.accounts.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Accounts", [("ID", "cyan"), ("Name", "blue")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""))
    console.print(table)


@app.command()
def create() -> None:
    """Create endpoint is not allowed for accounts."""
    client = Layerbrain()
    try:
        result = client.accounts.create()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Accounts created.")
    print_json(result)


@app.command()
def delete(
    id: str = typer.Argument(..., help="Accounts ID"),
) -> None:
    """Handles DELETE requests to delete account with cascading cleanup."""
    typer.confirm(f"Delete accounts {id}?", abort=True)
    client = Layerbrain()
    try:
        client.accounts.delete(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Accounts {id} deleted.")


@app.command("get")
def get_accounts(
    id: str = typer.Argument(..., help="Accounts ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Handles GET requests to retrieve account info."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.accounts.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())


@app.command("update")
def update(
    id: str = typer.Argument(..., help="Accounts ID"),
) -> None:
    """Handles PATCH requests to update account info."""
    client = Layerbrain()
    try:
        result = client.accounts.update(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("clear-data")
def clear_data(
    id: str = typer.Argument(..., help="Accounts ID"),
) -> None:
    """Clear all cloud storage data for the user's organization."""
    client = Layerbrain()
    try:
        result = client.accounts.clear_data(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("export")
def export(
    id: str = typer.Argument(..., help="Accounts ID"),
) -> None:
    """Generate presigned download URL for latest snapshot."""
    client = Layerbrain()
    try:
        result = client.accounts.export(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("onboard")
def onboard(
    id: str = typer.Argument(..., help="Accounts ID"),
) -> None:
    """Handle onboarding of a new account with activation code."""
    client = Layerbrain()
    try:
        result = client.accounts.onboard(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("switch")
def switch(
    id: str = typer.Argument(..., help="Accounts ID"),
) -> None:
    """Switch organization/membership endpoint - returns new token with specified or latest membership."""
    client = Layerbrain()
    try:
        result = client.accounts.switch(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)
