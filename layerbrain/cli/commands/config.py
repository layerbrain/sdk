"""CLI configuration commands for the Layerbrain CLI."""

from __future__ import annotations

import typer

from layerbrain.sdk._config import Config
from layerbrain.cli._output import console, print_success

app = typer.Typer(help="Configure the CLI", no_args_is_help=True)


@app.command("set")
def set_config(
    key: str = typer.Argument(..., help="Configuration key"),
    value: str = typer.Argument(..., help="Configuration value"),
) -> None:
    """Set a configuration value."""
    Config().set(key, value)
    print_success(f"Set {key} = {value}")


@app.command("get")
def get_config(
    key: str = typer.Argument(..., help="Configuration key"),
) -> None:
    """Get a configuration value."""
    result = Config().get(key)
    if result is None:
        console.print(f"[dim]{key} is not set[/dim]")
    else:
        console.print(f"[cyan]{key}[/cyan] = {result}")
