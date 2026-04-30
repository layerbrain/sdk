"""Internal developer commands -- hidden from public help."""

from __future__ import annotations

import typer

from layerbrain_cli._output import console, print_error, print_success

app = typer.Typer(help="Internal developer tools", no_args_is_help=True, hidden=True)


@app.command("sync-spec")
def sync_spec(
    path: str = typer.Option(
        ..., "--path", help="Path to an exported public OpenAPI JSON file"
    ),
) -> None:
    """Refresh the local SDK OpenAPI copy from an exported spec."""
    from layerbrain.sdk.openapi.pull import sync

    console.print("Syncing OpenAPI spec...")
    try:
        written_path = sync(path)
    except Exception as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"OpenAPI spec written to {written_path}")


@app.command("show-spec")
def show_spec() -> None:
    """Show info about the local OpenAPI spec."""
    from layerbrain.sdk.openapi.pull import load

    try:
        spec = load()
    except FileNotFoundError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    info = spec.get("info", {})
    paths = spec.get("paths", {})
    tags = spec.get("tags", [])

    console.print(f"[cyan]Title:[/cyan] {info.get('title', 'N/A')}")
    console.print(f"[cyan]Version:[/cyan] {info.get('version', 'N/A')}")
    console.print(f"[cyan]Paths:[/cyan] {len(paths)}")
    console.print(f"[cyan]Tags:[/cyan] {len(tags)}")
    for tag in tags:
        console.print(f"  - {tag.get('name', '')}")
