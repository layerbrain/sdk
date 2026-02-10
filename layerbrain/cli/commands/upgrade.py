"""Upgrade command for the Layerbrain CLI."""

from __future__ import annotations

import subprocess
import sys

import typer

from layerbrain import __version__
from layerbrain.cli._output import console, print_error, print_success


def upgrade() -> None:
    """Upgrade the Layerbrain CLI to the latest version."""
    console.print(f"Installed version: {__version__}")

    # Check latest version on PyPI
    result = subprocess.run(
        [sys.executable, "pip", "index", "versions", "layerbrain"],
        capture_output=True,
        text=True,
    )

    latest = None
    if result.returncode == 0 and result.stdout:
        # pip index versions output: "layerbrain (0.2.0)"
        line = result.stdout.strip().split("\n")[0]
        if "(" in line:
            latest = line.split("(")[1].split(")")[0]

    if latest:
        console.print(f"Latest version:    {latest}")
        if latest == __version__:
            print_success("Already up to date.")
            return
        console.print(f"\nA newer version is available: {latest}\n")
    else:
        console.print("Could not determine latest version. Attempting upgrade.\n")

    # Detect install method
    uv_result = subprocess.run(
        ["uv", "tool", "list"],
        capture_output=True,
        text=True,
    )
    if uv_result.returncode == 0 and "layerbrain" in uv_result.stdout:
        console.print("Detected install method: uv_tool")
        console.print("Running: uv tool upgrade layerbrain")
        upgrade_result = subprocess.run(
            ["uv", "tool", "upgrade", "layerbrain"],
            capture_output=True,
            text=True,
        )
    else:
        console.print("Detected install method: pip")
        console.print(f"Running: {sys.executable} -m pip install --upgrade layerbrain")
        upgrade_result = subprocess.run(
            [sys.executable, "pip", "install", "--upgrade", "layerbrain"],
            capture_output=True,
            text=True,
        )

    if upgrade_result.returncode == 0:
        print_success("Successfully upgraded!")
    else:
        print_error(f"Upgrade failed:\n{upgrade_result.stderr}")
        raise typer.Exit(1)
