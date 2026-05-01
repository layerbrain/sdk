"""CLI surface tests for the merged package."""

from __future__ import annotations

import unittest

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
        self.assertNotIn("tools", result.output)


if __name__ == "__main__":
    unittest.main()
