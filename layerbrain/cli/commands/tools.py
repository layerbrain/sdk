"""Tools commands for the Layerbrain CLI.

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

app = typer.Typer(help="Tools", no_args_is_help=True)


@app.command("fetch")
def fetch(
    id: str = typer.Argument(..., help="Tools ID"),
) -> None:
    """Fetch web page content using Playwright."""
    client = Layerbrain()
    try:
        result = client.tools.fetch()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("search")
def search(
    id: str = typer.Argument(..., help="Tools ID"),
) -> None:
    """Search the web using Brave Search API."""
    client = Layerbrain()
    try:
        result = client.tools.search()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)
