"""Tool commands."""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain.cli._input import load_json_input
from layerbrain.cli._output import print_error, print_json
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="Tools", no_args_is_help=True)


@app.command("web-search")
def web_search(
    query: str = typer.Option(..., "--query", help="Search query."),
    count: int | None = typer.Option(None, "--count", help="Optional result count."),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Search the web."""
    payload = load_json_input(data, data_file)
    payload.setdefault("query", query)
    if count is not None:
        payload.setdefault("count", count)

    client = Layerbrain()
    try:
        result = client.tools.web_search(**payload)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)
