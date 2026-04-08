"""Storage commands."""

from __future__ import annotations

import typer

from layerbrain import Layerbrain
from layerbrain.cli._input import load_json_input
from layerbrain.cli._output import (
    build_table,
    console,
    print_error,
    print_json,
    print_success,
    validate_output_format,
)
from layerbrain.exceptions import LayerbrainError

app = typer.Typer(help="Storage", no_args_is_help=True)


def _render_page(title: str, page, output: str, columns: list[tuple[str, str]]) -> None:
    if output == "json":
        print_json(page.data)
        return

    table = build_table(title, columns)
    for item in page.data:
        row = [
            str(item.get(column.lower().replace(" ", "_"), ""))
            for column, _ in columns
        ]
        table.add_row(*row)
    console.print(table)


@app.command("list-backends")
def list_backends(
    output: str = typer.Option("table", "--output", help="Output format: table or json."),
) -> None:
    """List storage backends."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.storage.list_backends()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    _render_page("Storage Backends", page, output, [("ID", "cyan"), ("Name", "blue")])


@app.command("create-backend")
def create_backend(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create a storage backend."""
    client = Layerbrain()
    try:
        result = client.storage.create_backend(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success("Storage backend created.")
    print_json(result)


@app.command("get-backend")
def get_backend(
    id: str = typer.Argument(..., help="Backend ID."),
) -> None:
    """Retrieve a storage backend."""
    client = Layerbrain()
    try:
        result = client.storage.retrieve_backend(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command("update-backend")
def update_backend(
    id: str = typer.Argument(..., help="Backend ID."),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Update a storage backend."""
    client = Layerbrain()
    try:
        result = client.storage.update_backend(id, **load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command("delete-backend")
def delete_backend(
    id: str = typer.Argument(..., help="Backend ID."),
) -> None:
    """Delete a storage backend."""
    typer.confirm(f"Delete storage backend {id}?", abort=True)
    client = Layerbrain()
    try:
        result = client.storage.delete_backend(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success(f"Storage backend {id} deleted.")
    print_json(result)


@app.command("validate-backend")
def validate_backend(
    id: str = typer.Argument(..., help="Backend ID."),
) -> None:
    """Validate a storage backend."""
    client = Layerbrain()
    try:
        result = client.storage.validate_backend(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command("list-buckets")
def list_buckets(
    output: str = typer.Option("table", "--output", help="Output format: table or json."),
) -> None:
    """List storage buckets."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.storage.list_buckets()
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    _render_page("Storage Buckets", page, output, [("ID", "cyan"), ("Name", "blue")])


@app.command("create-bucket")
def create_bucket(
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create a storage bucket."""
    client = Layerbrain()
    try:
        result = client.storage.create_bucket(**load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success("Storage bucket created.")
    print_json(result)


@app.command("get-bucket")
def get_bucket(
    id: str = typer.Argument(..., help="Bucket ID."),
) -> None:
    """Retrieve a storage bucket."""
    client = Layerbrain()
    try:
        result = client.storage.retrieve_bucket(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command("update-bucket")
def update_bucket(
    id: str = typer.Argument(..., help="Bucket ID."),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Update a storage bucket."""
    client = Layerbrain()
    try:
        result = client.storage.update_bucket(id, **load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command("delete-bucket")
def delete_bucket(
    id: str = typer.Argument(..., help="Bucket ID."),
) -> None:
    """Delete a storage bucket."""
    typer.confirm(f"Delete storage bucket {id}?", abort=True)
    client = Layerbrain()
    try:
        result = client.storage.delete_bucket(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success(f"Storage bucket {id} deleted.")
    print_json(result)


@app.command("list-bucket-keys")
def list_bucket_keys(
    id: str = typer.Argument(..., help="Bucket ID."),
    output: str = typer.Option("table", "--output", help="Output format: table or json."),
) -> None:
    """List bucket keys."""
    validate_output_format(output)
    client = Layerbrain()
    try:
        page = client.storage.list_bucket_keys(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    _render_page("Bucket Keys", page, output, [("ID", "cyan"), ("Name", "blue")])


@app.command("create-bucket-key")
def create_bucket_key(
    id: str = typer.Argument(..., help="Bucket ID."),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create a bucket key."""
    client = Layerbrain()
    try:
        result = client.storage.create_bucket_key(id, **load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success(f"Bucket key created for {id}.")
    print_json(result)


@app.command("presign-bucket")
def presign_bucket(
    id: str = typer.Argument(..., help="Bucket ID."),
    data: str | None = typer.Option(None, "--data", help="Inline JSON request body."),
    data_file: str | None = typer.Option(None, "--data-file", help="Path to a JSON request body."),
) -> None:
    """Create a presigned bucket request."""
    client = Layerbrain()
    try:
        result = client.storage.presign_bucket(id, **load_json_input(data, data_file))
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_json(result)


@app.command("delete-bucket-key")
def delete_bucket_key(
    id: str = typer.Argument(..., help="Bucket key ID."),
) -> None:
    """Delete a bucket key."""
    typer.confirm(f"Delete bucket key {id}?", abort=True)
    client = Layerbrain()
    try:
        result = client.storage.delete_bucket_key(id)
    except LayerbrainError as e:
        print_error(str(e))
        raise typer.Exit(1) from e
    print_success(f"Bucket key {id} deleted.")
    print_json(result)
