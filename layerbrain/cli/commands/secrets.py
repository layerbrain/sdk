"""Secrets commands for the Layerbrain CLI.

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

app = typer.Typer(help="Secrets", no_args_is_help=True)


@app.command("list")
def list_secrets(
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """List secrets for the authenticated user's organization."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.secrets.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Secrets", [("ID", "cyan"), ("Name", "blue")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""))
    console.print(table)


@app.command()
def create(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Handle secret creation."""
    client = Layerbrain()
    try:
        result = client.secrets.create(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success("Secrets created.")
    print_json(result)


@app.command()
def delete(
    id: str = typer.Argument(..., help="Secrets ID"),
) -> None:
    """Handle secret deletion."""
    typer.confirm(f"Delete secrets {id}?", abort=True)
    client = Layerbrain()
    try:
        client.secrets.delete(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Secrets {id} deleted.")


@app.command("get")
def get_secrets(
    id: str = typer.Argument(..., help="Secrets ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Handle secret retrieval."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.secrets.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())


@app.command("update")
def update(
    id: str = typer.Argument(..., help="Secrets ID"),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Handle secret updates via PATCH."""
    client = Layerbrain()
    try:
        result = client.secrets.update(id, **load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("reveal")
def reveal_secret(
    id: str = typer.Argument(..., help="Secret ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Reveal the unmasked secret value."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.secrets.reveal(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())
