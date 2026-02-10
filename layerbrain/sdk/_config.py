"""Configuration management for the Layerbrain SDK and CLI.

Reads from:
  1. Environment variables (LAYERBRAIN_API_KEY, LAYERBRAIN_BASE_URL)
  2. Config file (~/.layerbrain/config.toml)
  3. Credentials file (~/.layerbrain/credentials.toml)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import tomli_w


DEFAULT_BASE_URL = "https://api.layerbrain.com"
CONFIG_DIR = Path.home() / ".layerbrain"
CONFIG_FILE = CONFIG_DIR / "config.toml"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.toml"


class Config:
    """Layerbrain SDK/CLI configuration."""

    def __init__(self) -> None:
        self._config = self._load_toml(CONFIG_FILE)
        self._credentials = self._load_toml(CREDENTIALS_FILE)

    @staticmethod
    def _load_toml(path: Path) -> dict:
        if not path.exists():
            return {}
        with open(path, "rb") as f:
            return tomllib.load(f)

    @staticmethod
    def _save_toml(path: Path, data: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            tomli_w.dump(data, f)

    @property
    def api_key(self) -> Optional[str]:
        return os.environ.get("LAYERBRAIN_API_KEY") or self._credentials.get("api_key")

    @api_key.setter
    def api_key(self, value: str) -> None:
        self._credentials["api_key"] = value
        self._save_toml(CREDENTIALS_FILE, self._credentials)

    @property
    def base_url(self) -> str:
        return (
            os.environ.get("LAYERBRAIN_BASE_URL")
            or self._config.get("base_url")
            or DEFAULT_BASE_URL
        )

    @base_url.setter
    def base_url(self, value: str) -> None:
        self._config["base_url"] = value
        self._save_toml(CONFIG_FILE, self._config)

    @property
    def default_output(self) -> str:
        return self._config.get("default_output", "table")

    @default_output.setter
    def default_output(self, value: str) -> None:
        self._config["default_output"] = value
        self._save_toml(CONFIG_FILE, self._config)

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self._config.get(key, default)

    def set(self, key: str, value: str) -> None:
        self._config[key] = value
        self._save_toml(CONFIG_FILE, self._config)

    def clear_credentials(self) -> None:
        """Remove stored credentials."""
        self._credentials = {}
        if CREDENTIALS_FILE.exists():
            CREDENTIALS_FILE.unlink()
