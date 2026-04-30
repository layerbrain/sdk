"""Upgrade command for the Layerbrain CLI."""

from __future__ import annotations

import os
import subprocess

import typer

from layerbrain_cli._version import __version__
from layerbrain_cli._output import console, print_error, print_success

DEFAULT_INSTALL_URL = "https://layerbrain.com/install.sh"


def upgrade() -> None:
    """Upgrade the Layerbrain CLI to the latest version."""
    console.print(f"Installed version: {__version__}")
    install_url = os.environ.get("LAYERBRAIN_INSTALL_URL", DEFAULT_INSTALL_URL)
    console.print(f"Running installer: {install_url}")
    download_result = subprocess.run(
        ["curl", "-fsSL", install_url],
        capture_output=True,
        text=True,
    )

    if download_result.returncode != 0:
        print_error(f"Upgrade failed:\n{download_result.stderr or download_result.stdout}")
        raise typer.Exit(1)

    upgrade_result = subprocess.run(
        ["sh"],
        input=download_result.stdout,
        capture_output=True,
        text=True,
    )

    if upgrade_result.returncode == 0:
        print_success("Successfully upgraded!")
        return

    output = upgrade_result.stderr or upgrade_result.stdout
    print_error(f"Upgrade failed:\n{output}")
    raise typer.Exit(1)
