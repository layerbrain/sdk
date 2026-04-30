"""CLI surface tests for the merged package."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from layerbrain_cli.main import app

runner = CliRunner()


class TestMainHelp(unittest.TestCase):
    def test_public_help_includes_current_public_groups(self):
        result = runner.invoke(app, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("networks", result.output)
        self.assertIn("network-rules", result.output)
        self.assertIn("network-flows", result.output)
        self.assertIn("snapshots", result.output)
        self.assertIn("storage", result.output)
        self.assertIn("webhooks", result.output)
        self.assertNotIn("environments", result.output)


class TestToolsCommands(unittest.TestCase):
    @patch("layerbrain_cli.commands.tools.Layerbrain")
    def test_web_search_calls_public_sdk_method(self, mock_cls):
        mock_client = MagicMock()
        mock_client.tools.web_search.return_value = {"object": "tool.web_search", "results": []}
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["tools", "web-search", "--query", "layerbrain"])

        self.assertEqual(result.exit_code, 0)
        mock_client.tools.web_search.assert_called_once_with(query="layerbrain")


if __name__ == "__main__":
    unittest.main()
