"""Main Typer CLI application for Layerbrain.

Entry point: `layerbrain` command.
"""

from __future__ import annotations

import typer

from ._version import __version__
from .commands.accounts import app as accounts_app
from .commands.api_keys import app as api_keys_app
from .commands.audio import app as audio_app
from .commands.auth import login, logout, whoami
from .commands.brains import app as brains_app
from .commands.chat import app as chat_app
from .commands.compute import app as compute_app
from .commands.config import app as config_app
from .commands.embeddings import app as embeddings_app
from .commands.images import app as images_app
from .commands.internal import app as internal_app
from .commands.listen import listen
from .commands.machines import app as machines_app
from .commands.memberships import app as memberships_app
from .commands.models import app as models_app
from .commands.network_flows import app as network_flows_app
from .commands.network_rules import app as network_rules_app
from .commands.networks import app as networks_app
from .commands.organizations import app as organizations_app
from .commands.secrets import app as secrets_app
from .commands.snapshots import app as snapshots_app
from .commands.statements import app as statements_app
from .commands.storage import app as storage_app
from .commands.subscriptions import app as subscriptions_app
from .commands.threed import app as threed_app
from .commands.upgrade import upgrade
from .commands.videos import app as videos_app
from .commands.webhooks import app as webhooks_app

app = typer.Typer(
    name="layerbrain",
    help=f"Layerbrain CLI (v{__version__})",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

# AI
app.add_typer(chat_app, name="chat", rich_help_panel="AI")
app.add_typer(models_app, name="models", rich_help_panel="AI")
app.add_typer(embeddings_app, name="embeddings", rich_help_panel="AI")
app.add_typer(images_app, name="images", rich_help_panel="AI")
app.add_typer(audio_app, name="audio", rich_help_panel="AI")
app.add_typer(videos_app, name="videos", rich_help_panel="AI")
app.add_typer(threed_app, name="3d", rich_help_panel="AI")

# Brain
app.add_typer(brains_app, name="brains", rich_help_panel="Brain")

# Compute
app.add_typer(compute_app, name="compute", rich_help_panel="Compute")
app.add_typer(networks_app, name="networks", rich_help_panel="Compute")
app.add_typer(network_rules_app, name="network-rules", rich_help_panel="Compute")
app.add_typer(network_flows_app, name="network-flows", rich_help_panel="Compute")
app.add_typer(snapshots_app, name="snapshots", rich_help_panel="Compute")
app.add_typer(storage_app, name="storage", rich_help_panel="Compute")

# Machines
app.add_typer(machines_app, name="machines", rich_help_panel="Machines")
app.add_typer(secrets_app, name="secrets", rich_help_panel="Machines")
app.command(rich_help_panel="Webhooks")(listen)
app.add_typer(webhooks_app, name="webhooks", rich_help_panel="Webhooks")

# Account
app.command(rich_help_panel="Account")(login)
app.command(rich_help_panel="Account")(logout)
app.command(rich_help_panel="Account")(whoami)
app.add_typer(accounts_app, name="accounts", rich_help_panel="Account")
app.add_typer(organizations_app, name="organizations", rich_help_panel="Account")
app.add_typer(memberships_app, name="memberships", rich_help_panel="Account")
app.add_typer(subscriptions_app, name="subscriptions", rich_help_panel="Account")
app.add_typer(statements_app, name="statements", rich_help_panel="Account")
app.add_typer(api_keys_app, name="api-keys", rich_help_panel="Account")
app.add_typer(config_app, name="config", rich_help_panel="Account")
app.command(rich_help_panel="Account")(upgrade)

# Internal (hidden from --help)
app.add_typer(internal_app, name="internal")


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit"),
) -> None:
    """Layerbrain CLI"""
    if version:
        typer.echo(f"layerbrain {__version__}")
        raise typer.Exit()


def main() -> None:
    """Entry point for the CLI."""
    app()
