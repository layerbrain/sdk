"""Audio commands for the Layerbrain CLI.

Auto-generated from OpenAPI spec. Manual edits will be overwritten
on next regeneration.
"""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain.cli._input import load_json_input
from layerbrain.cli._output import (
    print_error,
    print_json,
)
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="Audio", no_args_is_help=True)


@app.command("speech")
def speech(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create text-to-speech generation."""
    client = Layerbrain()
    try:
        result = client.audio.create_speech(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)


@app.command("transcriptions")
def transcriptions(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create speech-to-text transcription."""
    client = Layerbrain()
    try:
        result = client.audio.create_transcription(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e

    print_json(result)
