"""Tests for the core HTTP client."""

from __future__ import annotations

import json
import os
import unittest
from unittest.mock import MagicMock, patch

import httpx

from layerbrain.sdk._client import AsyncHTTPClient, SyncHTTPClient
from layerbrain.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    raise_for_status,
)


class TestRaiseForStatus(unittest.TestCase):
    """Test raise_for_status error mapping."""

    def test_200_does_not_raise(self):
        raise_for_status(200, {"object": "machine"})

    def test_201_does_not_raise(self):
        raise_for_status(201, {"id": "mach_123"})

    def test_400_raises_validation_error(self):
        with self.assertRaises(ValidationError) as ctx:
            raise_for_status(400, {"error": {"type": "validation_error", "message": "model is required"}})
        self.assertEqual(ctx.exception.message, "model is required")
        self.assertEqual(ctx.exception.status_code, 400)

    def test_401_raises_authentication_error(self):
        with self.assertRaises(AuthenticationError) as ctx:
            raise_for_status(401, {"error": {"type": "authentication_failed", "message": "Invalid token"}})
        self.assertEqual(ctx.exception.message, "Invalid token")

    def test_404_raises_not_found_error(self):
        with self.assertRaises(NotFoundError) as ctx:
            raise_for_status(404, {"error": {"type": "not_found", "message": "Machine not found"}})
        self.assertEqual(ctx.exception.message, "Machine not found")

    def test_500_raises_internal_server_error(self):
        with self.assertRaises(APIError) as ctx:
            raise_for_status(500, {"error": {"type": "internal_error", "message": "Something broke"}})
        self.assertEqual(ctx.exception.status_code, 500)

    def test_unknown_status_raises_api_error(self):
        with self.assertRaises(APIError) as ctx:
            raise_for_status(418, {"error": {"type": "teapot", "message": "I'm a teapot"}})
        self.assertEqual(ctx.exception.status_code, 418)
        self.assertEqual(ctx.exception.error_type, "teapot")


class TestSyncHTTPClient(unittest.TestCase):
    """Test the synchronous HTTP client."""

    def test_requires_auth(self):
        """Client raises AuthenticationError when no API key is set."""
        with patch.dict(os.environ, {}, clear=True):
            client = SyncHTTPClient(api_key=None, base_url="https://test.api.com")
            with self.assertRaises(AuthenticationError):
                client._get("/machines")

    def test_builds_correct_url(self):
        client = SyncHTTPClient(api_key="sk-test", base_url="https://test.api.com")
        self.assertEqual(client._full_url("/machines"), "https://test.api.com/v1/machines")
        self.assertEqual(client._full_url("machines"), "https://test.api.com/v1/machines")

    def test_base_url_strips_trailing_slash(self):
        client = SyncHTTPClient(api_key="sk-test", base_url="https://test.api.com/")
        self.assertEqual(client._base_url, "https://test.api.com")

    def test_auth_header_included(self):
        client = SyncHTTPClient(api_key="sk-test-key-123", base_url="https://test.api.com")
        headers = client._build_headers()
        self.assertEqual(headers["Authorization"], "Bearer sk-test-key-123")

    def test_user_agent_header(self):
        client = SyncHTTPClient(api_key="sk-test", base_url="https://test.api.com")
        headers = client._build_headers()
        self.assertIn("layerbrain-python/", headers["User-Agent"])

    @patch.object(httpx.Client, "request")
    def test_get_request(self, mock_request):
        """Test that _get makes a GET request and returns parsed JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"object": "list", "data": [], "has_more": False}
        mock_request.return_value = mock_response

        client = SyncHTTPClient(api_key="sk-test", base_url="https://test.api.com")
        result = client._get("/machines")

        self.assertEqual(result["object"], "list")
        mock_request.assert_called_once()

    @patch.object(httpx.Client, "request")
    def test_post_request(self, mock_request):
        """Test that _post makes a POST request with JSON body."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": "mach_123", "object": "machine"}
        mock_request.return_value = mock_response

        client = SyncHTTPClient(api_key="sk-test", base_url="https://test.api.com")
        result = client._post("/machines", json={"compute": "A100"})

        self.assertEqual(result["id"], "mach_123")

    @patch.object(httpx.Client, "request")
    def test_delete_request(self, mock_request):
        """Test that _delete makes a DELETE request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        client = SyncHTTPClient(api_key="sk-test", base_url="https://test.api.com")
        result = client._delete("/machines/mach_123")

        self.assertEqual(result, {})

    @patch.object(httpx.Client, "request")
    def test_error_response_raises(self, mock_request):
        """Test that error responses raise appropriate exceptions."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": {"type": "not_found", "message": "Not found"}}
        mock_request.return_value = mock_response

        client = SyncHTTPClient(api_key="sk-test", base_url="https://test.api.com")
        with self.assertRaises(NotFoundError):
            client._get("/machines/nonexistent")


class TestSyncHTTPClientEnvironment(unittest.TestCase):
    """Test environment-based configuration."""

    def test_api_key_from_env(self):
        with patch.dict(os.environ, {"LAYERBRAIN_API_KEY": "sk-env-key"}):
            client = SyncHTTPClient(base_url="https://test.api.com")
            headers = client._build_headers()
            self.assertEqual(headers["Authorization"], "Bearer sk-env-key")

    def test_explicit_key_overrides_env(self):
        with patch.dict(os.environ, {"LAYERBRAIN_API_KEY": "sk-env-key"}):
            client = SyncHTTPClient(api_key="sk-explicit", base_url="https://test.api.com")
            headers = client._build_headers()
            self.assertEqual(headers["Authorization"], "Bearer sk-explicit")


if __name__ == "__main__":
    unittest.main()
