"""Tests for the machines CLI commands."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from layerbrain_cli.main import app

runner = CliRunner()


class TestMachinesListCommand(unittest.TestCase):
    """Test layerbrain machines list command."""

    @patch("layerbrain_cli.commands.machines.Layerbrain")
    def test_list_table_output(self, mock_cls):
        mock_client = MagicMock()
        mock_page = MagicMock()
        mock_page.data = [
            {
                "id": "mach_1",
                "name": "dev",
                "environment": "personal",
                "state": "active",
                "zone": "us-east-1",
                "host": "1.2.3.4",
            },
            {
                "id": "mach_2",
                "name": "prod",
                "environment": "work",
                "state": "stopped",
                "zone": "eu-west-1",
                "host": "5.6.7.8",
            },
        ]
        mock_client.machines.list.return_value = mock_page
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["machines", "list"])
        print(f"CLI output:\n{result.output}")
        if result.exception:
            print(f"Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("mach_1", result.output)
        self.assertIn("mach_2", result.output)

    @patch("layerbrain_cli.commands.machines.Layerbrain")
    def test_list_json_output(self, mock_cls):
        mock_client = MagicMock()
        mock_page = MagicMock()
        mock_page.data = [
            {"id": "mach_1", "name": "dev"},
        ]
        mock_client.machines.list.return_value = mock_page
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["machines", "list", "--output", "json"])
        print(f"CLI output:\n{result.output}")
        if result.exception:
            print(f"Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("mach_1", result.output)


class TestMachinesGetCommand(unittest.TestCase):
    """Test layerbrain machines get command."""

    @patch("layerbrain_cli.commands.machines.Layerbrain")
    def test_get_machine(self, mock_cls):
        mock_client = MagicMock()
        mock_machine = MagicMock()
        mock_machine.id = "mach_123"
        mock_machine.name = "my-machine"
        mock_machine.state = "active"
        mock_machine.zone = "us-east-1"
        mock_machine.type = "A100"
        mock_machine.environment = "personal"
        mock_machine.host = "1.2.3.4"
        mock_machine.ipv4 = "1.2.3.4"
        mock_machine.ipv6 = None
        mock_client.machines.retrieve.return_value = mock_machine
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["machines", "get", "--id", "mach_123"])
        print(f"CLI output:\n{result.output}")
        if result.exception:
            print(f"Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("mach_123", result.output)


class TestMachinesDeleteCommand(unittest.TestCase):
    """Test layerbrain machines delete command."""

    @patch("layerbrain_cli.commands.machines.Layerbrain")
    def test_delete_confirmed(self, mock_cls):
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        result = runner.invoke(app, ["machines", "delete", "--id", "mach_123"], input="y\n")
        print(f"CLI output:\n{result.output}")
        if result.exception:
            print(f"Exception: {result.exception}")
        self.assertEqual(result.exit_code, 0)
        mock_client.machines.delete.assert_called_once_with("mach_123")


if __name__ == "__main__":
    unittest.main()
