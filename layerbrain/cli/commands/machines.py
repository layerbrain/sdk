"""Machines commands for the Layerbrain CLI (hand-written).

Includes SSH session support.
"""

from __future__ import annotations

import os
import subprocess
import tempfile

import typer

from layerbrain import Layerbrain
from layerbrain.cli._input import load_json_input
from layerbrain.cli._output import (
    MACHINE_STATUS_COLORS,
    build_detail_table,
    build_table,
    console,
    print_error,
    print_json,
    print_success,
    status_text,
    validate_output_format,
)

app = typer.Typer(help="Machines", no_args_is_help=True)


@app.command("list")
def list_machines(
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """List all active machines for user's organization."""
    validate_output_format(output)
    client = Layerbrain()
    page = client.machines.list()

    if output == "json":
        print_json(page.data)
        return

    table = build_table(
        "Machines",
        [("ID", "cyan"), ("Name", "blue"), ("State", "white"), ("Zone", "dim"), ("Host", "dim")],
    )
    for item in page.data:
        table.add_row(
            item.get("id", ""),
            item.get("name", ""),
            str(status_text(item.get("state", ""), MACHINE_STATUS_COLORS)),
            item.get("zone", ""),
            item.get("host", ""),
        )
    console.print(table)


@app.command("get")
def get_machine(
    id: str = typer.Option(..., "--id", help="Machine ID"),
    output: str = typer.Option("table", "--output", help="Output format: table or json"),
) -> None:
    """Get machine details."""
    validate_output_format(output)
    client = Layerbrain()
    machine = client.machines.retrieve(id)

    if output == "json":
        print_json(machine.model_dump())
        return

    table = build_detail_table(f"Machine {machine.id}")
    table.add_row("ID", machine.id)
    table.add_row("Name", machine.name or "")
    table.add_row("State", machine.state or "")
    table.add_row("Zone", machine.zone or "")
    table.add_row("Type", machine.type or "")
    table.add_row("Environment", machine.environment or "")
    table.add_row("Host", machine.host or "")
    table.add_row("IPv4", machine.ipv4 or "")
    table.add_row("IPv6", machine.ipv6 or "")
    console.print(table)


@app.command()
def create(
    compute: str = typer.Option(..., "--compute", help="Compute type (e.g. A100, H100)"),
    duration: int = typer.Option(15, "--duration", help="Duration in minutes"),
    name: str = typer.Option(None, "--name", help="Machine name"),
) -> None:
    """Create a new machine by purchasing a contract."""
    client = Layerbrain()
    kwargs = {"compute": compute, "duration_minutes": duration}
    if name is not None:
        kwargs["name"] = name
    machine = client.machines.create(**kwargs)
    print_success(f"Machine {machine.id} created ({machine.state}).")
    print_json(machine.model_dump())


@app.command()
def delete(
    id: str = typer.Option(..., "--id", help="Machine ID"),
) -> None:
    """Delete a machine by releasing it."""
    typer.confirm(f"Delete machine {id}?", abort=True)
    client = Layerbrain()
    client.machines.delete(id)
    print_success(f"Machine {id} deleted.")


@app.command()
def extend(
    id: str = typer.Option(..., "--id", help="Machine ID"),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Extend a machine contract."""
    client = Layerbrain()
    result = client.machines.extend(id, **load_json_input(data, data_file))
    print_success(f"Machine {id} extended.")
    print_json(result)


@app.command()
def restore(
    id: str = typer.Option(..., "--id", help="Machine ID"),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Restore a machine."""
    client = Layerbrain()
    result = client.machines.restore(id, **load_json_input(data, data_file))
    print_success(f"Machine {id} restored.")
    print_json(result)


@app.command()
def snapshot(
    id: str = typer.Option(..., "--id", help="Machine ID"),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create a machine snapshot."""
    client = Layerbrain()
    result = client.machines.snapshot(id, **load_json_input(data, data_file))
    print_success(f"Snapshot requested for machine {id}.")
    print_json(result)


@app.command()
def ssh(
    id: str = typer.Option(..., "--id", help="Machine ID"),
    user: str = typer.Option("root", "--user", "-u", help="SSH user"),
) -> None:
    """SSH into a machine.

    Retrieves the machine details and its SSH key from secrets,
    then opens an interactive SSH session.
    """
    client = Layerbrain()

    console.print(f"[dim]Retrieving machine {id}...[/dim]")
    machine = client.machines.retrieve(id)

    if machine.state != "active":
        print_error(f"Machine is not active (state: {machine.state})")
        raise typer.Exit(1)

    host = machine.ipv4 or machine.host
    if not host:
        print_error("Machine has no IP address or host.")
        raise typer.Exit(1)

    if not machine.ssh_secret_id:
        print_error("Machine has no SSH key configured (ssh_secret_id is empty).")
        raise typer.Exit(1)

    console.print("[dim]Retrieving SSH key...[/dim]")
    secret = client.secrets.reveal(machine.ssh_secret_id)
    ssh_key = secret.get("value") if isinstance(secret, dict) else secret.value

    if not ssh_key:
        print_error("SSH key secret has no value.")
        raise typer.Exit(1)

    # Write the key to a temp file so ssh can use it
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pem", delete=False) as f:
        f.write(ssh_key)
        key_path = f.name
    os.chmod(key_path, 0o600)

    console.print(f"[green]Connecting to {user}@{host}...[/green]")

    try:
        subprocess.run(
            [
                "ssh",
                "-i", key_path,
                "-o", "StrictHostKeyChecking=no",
                "-o", "UserKnownHostsFile=/dev/null",
                f"{user}@{host}",
            ],
            check=False,
        )
    finally:
        os.unlink(key_path)
