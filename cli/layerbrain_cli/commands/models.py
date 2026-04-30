"""Model commands."""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain_cli._output import (
    build_table,
    console,
    print_error,
    print_json,
    validate_output_format,
)
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="Models", no_args_is_help=True)


@app.command("list")
def list_models(
    output: str = typer.Option("table", "--output", help="Output format: table or json."),
) -> None:
    """List available models."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.models.list()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    if output == "json":
        print_json(page.data)
        return

    table = build_table("Models", [("ID", "cyan"), ("Type", "blue"), ("Provider", "magenta")])
    for item in page.data:
        table.add_row(item.get("id", ""), item.get("type", ""), item.get("provider", ""))
    console.print(table)


@app.command("get")
def get_model(
    id: str = typer.Argument(..., help="Model ID."),
) -> None:
    """Get a specific model by ID."""
    client = Layerbrain()
    try:
        result = client.models.retrieve(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result if isinstance(result, dict) else result.model_dump())
