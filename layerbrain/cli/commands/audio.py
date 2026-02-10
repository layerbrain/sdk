"""Audio commands for the Layerbrain CLI.

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

app = typer.Typer(help="Audio", no_args_is_help=True)


@app.command("speech")
def speech(
    id: str = typer.Argument(..., help="Audio ID"),
) -> None:
    """Create text-to-speech generation."""
    client = Layerbrain()
    try:
        result = client.audio.speech()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("transcriptions")
def transcriptions(
    id: str = typer.Argument(..., help="Audio ID"),
) -> None:
    """Create speech-to-text transcription."""
    client = Layerbrain()
    try:
        result = client.audio.transcriptions()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)
