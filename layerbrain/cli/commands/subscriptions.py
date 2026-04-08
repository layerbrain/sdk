"""Subscriptions commands for the Layerbrain CLI.

Auto-generated from OpenAPI spec. Manual edits will be overwritten
on next regeneration.
"""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain.cli._input import load_json_input
from layerbrain.cli._output import (
    build_table,
    console,
    print_error,
    print_json,
    print_success,
    validate_output_format,
)
from layerbrain.exceptions import LayerbrainError

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
def create(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Post create"""
    client = Layerbrain()
    try:
        result = client.subscriptions.create(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success("Subscriptions created.")
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
