"""Engrams commands for the Layerbrain CLI.

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

app = typer.Typer(help="Engrams", no_args_is_help=True)


@app.command("list")
def list_engrams(
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Get list"""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.engrams.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Engrams", [("ID", "cyan"), ("Name", "blue")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("name", ""))
    console.print(table)


@app.command()
def create() -> None:
    """Post create"""
    client = Layerbrain()
    try:
        result = client.engrams.create()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Engrams created.")
    print_json(result)


@app.command("delete-all")
def delete_all() -> None:
    """Delete all engrams for the user's organization."""
    typer.confirm("Delete ALL engrams? This cannot be undone.", abort=True)
    client = Layerbrain()
    try:
        result = client.engrams.delete_all()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success("All engrams deleted.")
    print_json(result)


@app.command()
def delete(
    id: str = typer.Argument(..., help="Engrams ID"),
) -> None:
    """Delete delete"""
    typer.confirm(f"Delete engrams {id}?", abort=True)
    client = Layerbrain()
    try:
        client.engrams.delete(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"Engrams {id} deleted.")


@app.command("get")
def get_engrams(
    id: str = typer.Argument(..., help="Engrams ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Get retrieve"""
    validate_output_format(output)
    client = Layerbrain()
    try:
        result = client.engrams.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())


@app.command("update")
def update(
    id: str = typer.Argument(..., help="Engrams ID"),
) -> None:
    """Patch patch"""
    client = Layerbrain()
    try:
        result = client.engrams.update(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("archive")
def archive(
    id: str = typer.Argument(..., help="Engrams ID"),
) -> None:
    """Post archive"""
    client = Layerbrain()
    try:
        result = client.engrams.archive(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("restore")
def restore(
    id: str = typer.Argument(..., help="Engrams ID"),
) -> None:
    """Post restore"""
    client = Layerbrain()
    try:
        result = client.engrams.restore(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)
