"""Api-Keys commands for the Layerbrain CLI.

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

app = typer.Typer(help="Api-Keys", no_args_is_help=True)


@app.command("list")
def list_api_keys(
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Get list"""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.api_keys.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Api-Keys", [("ID", "cyan"), ("Name", "blue")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""))
    console.print(table)


@app.command("api-keys")
def api_keys(
    id: str = typer.Argument(..., help="Api-Keys ID"),
) -> None:
    """Post create"""
    client = Layerbrain()
    try:
        result = client.api_keys.api_keys()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command()
def delete(
    id: str = typer.Argument(..., help="Api-Keys ID"),
) -> None:
    """Delete destroy"""
    typer.confirm(f"Delete api-keys {id}?", abort=True)
    client = Layerbrain()
    try:
        client.api_keys.delete(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Api-Keys {id} deleted.")


@app.command("get")
def get_api_keys(
    id: str = typer.Argument(..., help="Api-Keys ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Get retrieve"""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.api_keys.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())


@app.command("update")
def update(
    id: str = typer.Argument(..., help="Api-Keys ID"),
) -> None:
    """Patch patch"""
    client = Layerbrain()
    try:
        result = client.api_keys.update(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("rotate")
def rotate(
    id: str = typer.Argument(..., help="Api-Keys ID"),
) -> None:
    """Post rotate"""
    client = Layerbrain()
    try:
        result = client.api_keys.rotate(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)
