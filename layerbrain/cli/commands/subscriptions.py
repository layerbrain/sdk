"""Subscriptions commands for the Layerbrain CLI.

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

app = typer.Typer(help="Subscriptions", no_args_is_help=True)


@app.command("list")
def list_subscriptions(
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Get list"""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.subscriptions.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Subscriptions", [("ID", "cyan"), ("Name", "blue")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""))
    console.print(table)


@app.command()
def create() -> None:
    """Post create"""
    client = Layerbrain()
    try:
        result = client.subscriptions.create()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Subscriptions created.")
    print_json(result)


@app.command("balance")
def balance(
    id: str = typer.Argument(..., help="Subscriptions ID"),
) -> None:
    """Add to balance - creates Stripe checkout for one-time payment."""
    client = Layerbrain()
    try:
        result = client.subscriptions.balance()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("downgrade")
def downgrade(
    id: str = typer.Argument(..., help="Subscriptions ID"),
) -> None:
    """Downgrade subscription tier (scheduled at period end)."""
    client = Layerbrain()
    try:
        result = client.subscriptions.downgrade()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("pay-as-you-go")
def pay_as_you_go(
    id: str = typer.Argument(..., help="Subscriptions ID"),
) -> None:
    """Post pay_as_you_go"""
    client = Layerbrain()
    try:
        result = client.subscriptions.pay_as_you_go()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("portal")
def portal(
    id: str = typer.Argument(..., help="Subscriptions ID"),
) -> None:
    """Create Stripe billing portal session for managing subscription."""
    client = Layerbrain()
    try:
        result = client.subscriptions.portal()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("upgrade")
def upgrade(
    id: str = typer.Argument(..., help="Subscriptions ID"),
) -> None:
    """Upgrade subscription tier (immediate with proration)."""
    client = Layerbrain()
    try:
        result = client.subscriptions.upgrade()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("get")
def get_subscriptions(
    subscription_id: str = typer.Argument(..., help="Subscriptions ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Get retrieve"""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.subscriptions.retrieve(subscription_id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())
