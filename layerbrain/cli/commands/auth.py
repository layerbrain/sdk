"""Auth commands for the Layerbrain CLI (hand-written).

Exports standalone functions: login, logout, whoami.
These are imported directly by cli/app.py and registered as top-level commands.
"""

from __future__ import annotations

import time

import typer

from layerbrain import Layerbrain
from layerbrain.cli._auth_client import CLIAuthClient
from layerbrain.cli._output import (
    build_detail_table,
    console,
    print_error,
    print_success,
)
from layerbrain.sdk._config import Config


def login() -> None:
    """Authenticate with Layerbrain using the device flow."""
    client = CLIAuthClient(api_key="anonymous")

    console.print("[dim]Starting device authorization...[/dim]")
    device = client.device(client_id="layerbrain")

    console.print("\nOpen this URL in your browser:\n")
    console.print(f"  [bold cyan]{device.verification_uri_complete}[/bold cyan]\n")
    console.print(f"Your code: [bold]{device.code}[/bold]\n")
    console.print("[dim]Waiting for authorization...[/dim]")

    interval = device.interval
    expires_at = time.time() + device.expires_in

    while time.time() < expires_at:
        time.sleep(interval)
        result = client.token_exchange(
            grant_type="device_code",
            device_code=device.device_code,
            client_id="layerbrain",
        )
        # token_exchange returns raw dict when pending, AuthToken on success
        if isinstance(result, dict):
            error = result.get("error", "")
            if error == "authorization_pending":
                continue
            if error == "slow_down":
                interval += 1
                continue
            print_error(result.get("error_description", error))
            raise typer.Exit(1)

        # Got an AuthToken — save credentials
        config = Config()
        config.api_key = result.access
        print_success(f"Logged in as {result.email or result.id}")
        return

    print_error("Device authorization timed out.")
    raise typer.Exit(1)


def logout() -> None:
    """Logout and clear stored credentials."""
    client = CLIAuthClient()
    try:
        client.logout()
    finally:
        client.close()
    Config().clear_credentials()
    print_success("Logged out.")


def whoami() -> None:
    """Show the currently authenticated account."""
    client = Layerbrain()
    page = client.accounts.list()

    if not page.data:
        print_error("No account found. Are you logged in?")
        raise typer.Exit(1)

    account = page.data[0]
    table = build_detail_table("Account")
    table.add_row("ID", account.get("id", ""))
    table.add_row("Email", account.get("email", ""))
    table.add_row("Name", account.get("name", ""))
    console.print(table)
