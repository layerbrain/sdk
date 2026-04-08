"""Webhook commands."""

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

app = typer.Typer(help="Webhooks", no_args_is_help=True)


@app.command("list")
def list_webhooks(
    output: str = typer.Option("table", "--output", help="Output format: table or json."),
) -> None:
    """List webhook endpoints."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.webhooks.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Webhooks", [("ID", "cyan"), ("URL", "blue")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("url", ""))
    console.print(table)


@app.command()
def create(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create a webhook endpoint."""
    client = Layerbrain()
    try:
        result = client.webhooks.create(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success("Webhook created.")
    print_json(result)


@app.command("get")
def get_webhook(
    id: str = typer.Argument(..., help="Webhook ID."),
) -> None:
    """Retrieve a webhook."""
    client = Layerbrain()
    try:
        result = client.webhooks.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command()
def update(
    id: str = typer.Argument(..., help="Webhook ID."),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Update a webhook."""
    client = Layerbrain()
    try:
        result = client.webhooks.update(id, **load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command()
def delete(
    id: str = typer.Argument(..., help="Webhook ID."),
) -> None:
    """Delete a webhook."""
    typer.confirm(f"Delete webhook {id}?", abort=True)
    client = Layerbrain()
    try:
        result = client.webhooks.delete(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success(f"Webhook {id} deleted.")
    print_json(result)


@app.command("rotate-secret")
def rotate_secret(
    id: str = typer.Argument(..., help="Webhook ID."),
) -> None:
    """Rotate a webhook signing secret."""
    client = Layerbrain()
    try:
        result = client.webhooks.rotate_secret(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success(f"Webhook {id} secret rotated.")
    print_json(result)
