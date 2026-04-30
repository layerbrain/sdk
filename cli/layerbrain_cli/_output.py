"""Rich console output helpers for the Layerbrain CLI."""

from __future__ import annotations

import json
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()
error_console = Console(stderr=True)


# ---------------------------------------------------------------------------
# Output format helpers
# ---------------------------------------------------------------------------

def validate_output_format(output: str) -> None:
    if output not in ("table", "json"):
        error_console.print(f"[red]Invalid output format '{output}'. Use: table, json[/red]")
        raise SystemExit(1)


def print_json(data: Any) -> None:
    console.print(json.dumps(data, indent=2, default=str))


def print_error(message: str) -> None:
    error_console.print(f"[red]Error:[/red] {message}")


def print_success(message: str) -> None:
    console.print(f"[green]{message}[/green]")


# ---------------------------------------------------------------------------
# Table builder
# ---------------------------------------------------------------------------

def build_table(
    title: str,
    columns: list[tuple[str, str]],
    *,
    show_lines: bool = True,
) -> Table:
    """Build a Rich table with standard left-aligned styling.

    Args:
        title: Table title.
        columns: List of (header, style) tuples.
        show_lines: Show row separator lines.
    """
    table = Table(title=title, show_lines=show_lines)
    for header, style in columns:
        table.add_column(header, style=style, no_wrap=(header == "ID"))
    return table


def build_detail_table(title: str) -> Table:
    """Build a key-value detail table (like whoami output)."""
    table = Table(title=title, show_lines=False, show_header=False, padding=(0, 2))
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value")
    return table


# ---------------------------------------------------------------------------
# Status colors
# ---------------------------------------------------------------------------

MACHINE_STATUS_COLORS = {
    "active": "green",
    "provisioning": "yellow",
    "pending": "yellow",
    "stopped": "blue",
    "released": "dim",
    "error": "red",
}

API_KEY_STATUS_COLORS = {
    "active": "green",
    "expired": "dim",
    "revoked": "red",
}


def status_text(status: str, color_map: dict[str, str]) -> Text:
    """Create a colored Text object for a status string."""
    color = color_map.get(status, "white")
    return Text(status, style=color)
