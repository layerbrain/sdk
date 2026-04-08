"""Tests for the listen CLI command."""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from typer.testing import CliRunner

from layerbrain.cli.commands.listen import _build_signature_header, _merge_forward_url
from layerbrain.cli.main import app

runner = CliRunner()


class TestListenHelpers(unittest.TestCase):
    def test_merge_forward_url_uses_webhook_path_when_local_target_has_none(self):
        merged = _merge_forward_url(
            "http://localhost:4242",
            "https://example.com/dev/webhooks/events?source=dashboard",
        )
        self.assertEqual(merged, "http://localhost:4242/dev/webhooks/events?source=dashboard")

    def test_build_signature_header_matches_expected_format(self):
        header = _build_signature_header(b'{"id":"evt_123"}', "whsec_test", timestamp=1_700_000_000)
        self.assertTrue(header.startswith("t=1700000000,v1="))
        self.assertEqual(header.count("v1="), 1)


class TestListenCommand(unittest.TestCase):
    @patch("layerbrain.cli.commands.listen.asyncio.run")
    @patch("layerbrain.cli.commands.listen._run_listen", new_callable=AsyncMock)
    @patch("layerbrain.cli.commands.listen.Layerbrain")
    def test_listen_uses_webhooks_socket_path_and_event_filters(
        self,
        mock_layerbrain,
        mock_run_listen,
        mock_asyncio_run,
    ):
        mock_client = MagicMock()
        mock_client.webhooks.listen_request.return_value = (
            "wss://api.layerbrain.test/v1/webhooks?events=queue.created",
            {"Authorization": "Bearer sk_test"},
        )
        mock_layerbrain.return_value.__enter__.return_value = mock_client
        mock_asyncio_run.side_effect = lambda coro: coro.close()

        result = runner.invoke(app, ["listen", "--events", "queue.created", "--print-json"])

        self.assertEqual(result.exit_code, 0)
        mock_client.webhooks.listen_request.assert_called_once_with(events="queue.created")
        config = mock_run_listen.call_args.args[0]
        self.assertEqual(config.websocket_url, "wss://api.layerbrain.test/v1/webhooks?events=queue.created")
        self.assertEqual(config.websocket_headers["Authorization"], "Bearer sk_test")
        self.assertIsNone(config.forward_to)
        self.assertTrue(config.print_json)

    @patch("layerbrain.cli.commands.listen._generate_forward_secret", return_value="whsec_fixed")
    @patch("layerbrain.cli.commands.listen.asyncio.run")
    @patch("layerbrain.cli.commands.listen._run_listen", new_callable=AsyncMock)
    @patch("layerbrain.cli.commands.listen.Layerbrain")
    def test_listen_loads_webhook_configuration_and_merges_forward_path(
        self,
        mock_layerbrain,
        mock_run_listen,
        mock_asyncio_run,
        _mock_secret,
    ):
        mock_client = MagicMock()
        mock_client.webhooks.retrieve.return_value = {
            "id": "whk_123",
            "url": "https://api.layerbrain.com/dev/webhooks/events",
            "enabled_events": ["queue.created", "queue.updated"],
        }
        mock_client.webhooks.listen_request.return_value = (
            "wss://api.layerbrain.test/v1/webhooks?events=queue.created%2Cqueue.updated",
            {"Authorization": "Bearer sk_test"},
        )
        mock_layerbrain.return_value.__enter__.return_value = mock_client
        mock_asyncio_run.side_effect = lambda coro: coro.close()

        result = runner.invoke(
            app,
            [
                "listen",
                "--forward-to",
                "localhost:4242",
                "--load-from-webhooks-api",
                "whk_123",
            ],
        )

        self.assertEqual(result.exit_code, 0)
        mock_client.webhooks.retrieve.assert_called_once_with("whk_123")
        mock_client.webhooks.listen_request.assert_called_once_with(
            events="queue.created,queue.updated"
        )
        config = mock_run_listen.call_args.args[0]
        self.assertEqual(config.forward_to, "http://localhost:4242/dev/webhooks/events")
        self.assertEqual(config.forward_secret, "whsec_fixed")


if __name__ == "__main__":
    unittest.main()
