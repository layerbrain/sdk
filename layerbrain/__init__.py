"""Layerbrain Python SDK + CLI.

Usage::

    from layerbrain import Layerbrain
    from layerbrain.exceptions import NotFoundError

    client = Layerbrain(api_key="sk-...")
    machines = client.machines.list()
"""

from layerbrain.sdk import Layerbrain
from ._version import __version__

__all__ = [
    "Layerbrain",
    "__version__",
]
