"""Tests for configuration management."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from layerbrain.sdk._config import Config


class TestConfig(unittest.TestCase):
    """Test Config reads and writes TOML files correctly."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.config_file = Path(self.tmpdir) / "config.toml"
        self.creds_file = Path(self.tmpdir) / "credentials.toml"

    def _make_config(self):
        """Create a Config with patched file paths."""
        with patch("layerbrain.sdk._config.CONFIG_FILE", self.config_file), \
             patch("layerbrain.sdk._config.CREDENTIALS_FILE", self.creds_file), \
             patch("layerbrain.sdk._config.CONFIG_DIR", Path(self.tmpdir)):
            return Config()

    def test_default_base_url(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("LAYERBRAIN_BASE_URL", None)
            config = self._make_config()
            self.assertEqual(config.base_url, "https://api.layerbrain.com")

    def test_base_url_from_env(self):
        with patch.dict(os.environ, {"LAYERBRAIN_BASE_URL": "https://staging.api.com"}):
            config = self._make_config()
            self.assertEqual(config.base_url, "https://staging.api.com")

    def test_api_key_from_env(self):
        with patch.dict(os.environ, {"LAYERBRAIN_API_KEY": "sk-env-test"}):
            config = self._make_config()
            self.assertEqual(config.api_key, "sk-env-test")

    def test_set_and_get_api_key(self):
        with patch("layerbrain.sdk._config.CONFIG_FILE", self.config_file), \
             patch("layerbrain.sdk._config.CREDENTIALS_FILE", self.creds_file), \
             patch("layerbrain.sdk._config.CONFIG_DIR", Path(self.tmpdir)):
            os.environ.pop("LAYERBRAIN_API_KEY", None)
            config = Config()
            config.api_key = "sk-saved-key"

            # Reload
            config2 = Config()
            self.assertEqual(config2.api_key, "sk-saved-key")

    def test_set_and_get_config_value(self):
        with patch("layerbrain.sdk._config.CONFIG_FILE", self.config_file), \
             patch("layerbrain.sdk._config.CREDENTIALS_FILE", self.creds_file), \
             patch("layerbrain.sdk._config.CONFIG_DIR", Path(self.tmpdir)):
            config = Config()
            config.set("default_output", "json")

            config2 = Config()
            self.assertEqual(config2.get("default_output"), "json")

    def test_clear_credentials(self):
        with patch("layerbrain.sdk._config.CONFIG_FILE", self.config_file), \
             patch("layerbrain.sdk._config.CREDENTIALS_FILE", self.creds_file), \
             patch("layerbrain.sdk._config.CONFIG_DIR", Path(self.tmpdir)):
            os.environ.pop("LAYERBRAIN_API_KEY", None)
            config = Config()
            config.api_key = "sk-to-clear"
            self.assertTrue(self.creds_file.exists())

            config.clear_credentials()
            self.assertFalse(self.creds_file.exists())

    def test_default_output_format(self):
        config = self._make_config()
        self.assertEqual(config.default_output, "table")


if __name__ == "__main__":
    unittest.main()
