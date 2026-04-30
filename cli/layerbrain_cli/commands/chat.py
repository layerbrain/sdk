"""Chat completion commands for the Layerbrain CLI."""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain_cli._output import console, print_error
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="Run chat completions", no_args_is_help=True)
completions_app = typer.Typer(help="Run chat completions", no_args_is_help=True)
app.add_typer(completions_app, name="completions")


@completions_app.command("create")
def create(
    model: str = typer.Option(..., "--model", help="Model ID"),
    message: str = typer.Option(..., "--message", help="User message"),
    system: str | None = typer.Option(None, "--system", help="System prompt"),
    stream: bool = typer.Option(True, "--stream/--no-stream", help="Stream the response"),
) -> None:
    """Create a chat completion."""
    client = Layerbrain()

    messages = []
    if system is not None:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": message})

    try:
        if stream:
            for chunk in client.chat.completions.create(
                model=model, messages=messages, stream=True
            ):
                if chunk.choices and chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)
            print()
        else:
            response = client.chat.completions.create(
                model=model, messages=messages, stream=False
            )
            if response.choices and response.choices[0].message:
                console.print(response.choices[0].message.content or "")
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
