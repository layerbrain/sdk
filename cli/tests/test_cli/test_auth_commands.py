"""Tests for the auth CLI commands."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from layerbrain_cli.main import app

runner = CliRunner()


class TestWhoamiCommand(unittest.TestCase):
    """Test layerbrain auth whoami command."""

    @patch("layerbrain_cli.commands.auth.Layerbrain")
    def test_whoami_shows_account(self, mock_cls):
        mock_client = MagicMock()
        mock_page = MagicMock()
        mock_page.data = [
            {"id": "acc_123", "email": "user@example.com", "name": "Test User"},
        ]
        mock_client.accounts.list.return_value = mock_page
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["whoami"])
        print(f"CLI output:\n{result.output}")
        if result.exception:
            print(f"Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("acc_123", result.output)
        self.assertIn("user@example.com", result.output)
        self.assertIn("Test User", result.output)


class TestLogoutCommand(unittest.TestCase):
    """Test layerbrain auth logout command."""

    @patch("layerbrain_cli.commands.auth.Config")
    @patch("layerbrain_cli.commands.auth.CLIAuthClient")
    def test_logout_clears_credentials(self, mock_cls, mock_config_cls):
        mock_client = MagicMock()
        mock_client.logout.return_value = {"message": "ok"}
        mock_cls.return_value = mock_client
        mock_config = MagicMock()
        mock_config_cls.return_value = mock_config

        result = runner.invoke(app, ["logout"])
        print(f"CLI output:\n{result.output}")
        if result.exception:
            print(f"Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)
        mock_config.clear_credentials.assert_called_once()


if __name__ == "__main__":
    unittest.main()
