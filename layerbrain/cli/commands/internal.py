"""Internal developer commands -- hidden from public help."""

from __future__ import annotations

import typer

from layerbrain.cli._output import console, print_error, print_success

app = typer.Typer(help="Internal developer tools", no_args_is_help=True, hidden=True)


@app.command("pull-spec")
def pull_spec(
    url: str | None = typer.Option(
        None, "--url", help="Override the spec URL"
    ),
) -> None:
    """Pull the OpenAPI spec and refresh the local tracked copy."""
    from layerbrain.sdk.openapi.pull import pull

    console.print("Pulling OpenAPI spec...")
    try:
        path = pull(url=url)
    except Exception as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_success(f"OpenAPI spec written to {path}")


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
