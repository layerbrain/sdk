"""Tests for the Auth resource."""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, MagicMock

from layerbrain.sdk._types import AuthIntent, AuthToken, DeviceAuthorization
from layerbrain.sdk.resources.auth import Auth


class TestAuth(unittest.IsolatedAsyncioTestCase):
    """Test async Auth resource."""

    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_client._post = AsyncMock()
        self.auth = Auth(self.mock_client)

    async def test_login_email_returns_auth_token(self):
        self.mock_client._post.return_value = {
            "object": "token",
            "access": "eyJ...",
            "refresh": "eyJ...",
            "email": "user@example.com",
            "id": "acc_123",
            "name": "Test User",
            "membership": "mem_123",
            "organization": "org_123",
        }
        result = await self.auth.login(email="user@example.com", password="secret", type="email")
        self.assertIsInstance(result, AuthToken)
        self.assertEqual(result.access, "eyJ...")
        self.assertEqual(result.email, "user@example.com")

    async def test_login_magic_returns_intent(self):
        self.mock_client._post.return_value = {
            "object": "intent",
            "type": "login",
            "status": "pending",
            "expires": "2025-01-01T00:00:00Z",
            "id": "int_123",
            "host": "app.layerbrain.com",
            "redirect_url": "https://app.layerbrain.com/auth/callback",
        }
        result = await self.auth.login(
            email="user@example.com",
            type="magic",
            host="app.layerbrain.com",
        )
        self.assertIsInstance(result, AuthIntent)
        self.assertEqual(result.type, "login")

    async def test_signup_returns_intent(self):
        self.mock_client._post.return_value = {
            "object": "intent",
            "type": "signup",
            "status": "pending",
            "id": "int_456",
        }
        result = await self.auth.signup(
            email="new@example.com",
            password="secret",
            host="app.layerbrain.com",
        )
        self.assertIsInstance(result, AuthIntent)
        self.mock_client._post.assert_called_once_with(
            "/auth/signup",
            json={
                "email": "new@example.com",
                "password": "secret",
                "host": "app.layerbrain.com",
            },
        )

    async def test_confirm_returns_token(self):
        self.mock_client._post.return_value = {
            "object": "token",
            "access": "eyJ...",
            "refresh": "eyJ...",
            "email": "user@example.com",
            "id": "acc_123",
        }
        result = await self.auth.confirm("int_123", key="abc123")
        self.assertIsInstance(result, AuthToken)

    async def test_device_returns_device_authorization(self):
        self.mock_client._post.return_value = {
            "device_code": "abc123",
            "code": "abc123",
            "verification_uri": "https://app.layerbrain.com/device",
            "verification_uri_complete": "https://app.layerbrain.com/device?code=abc123",
            "expires_in": 1800,
            "interval": 5,
        }
        result = await self.auth.device(client_id="test-cli")
        self.assertIsInstance(result, DeviceAuthorization)
        self.assertEqual(result.device_code, "abc123")
        self.assertEqual(result.interval, 5)

    async def test_token_exchange_with_token_response(self):
        self.mock_client._post.return_value = {
            "object": "token",
            "access": "new-access",
            "refresh": "new-refresh",
            "email": "user@example.com",
            "id": "acc_123",
        }
        result = await self.auth.token_exchange(
            grant_type="device_code",
            device_code="abc123",
            client_id="test-cli",
        )
        self.assertIsInstance(result, AuthToken)
        self.assertEqual(result.access, "new-access")

    async def test_token_exchange_with_error_response(self):
        self.mock_client._post.return_value = {
            "error": "authorization_pending",
            "error_description": "Device authorization is pending",
        }
        result = await self.auth.token_exchange(
            grant_type="device_code",
            device_code="abc123",
            client_id="test-cli",
        )
        # Returns raw dict when object != "token"
        self.assertIsInstance(result, dict)
        self.assertEqual(result["error"], "authorization_pending")

    async def test_logout(self):
        self.mock_client._post.return_value = {
            "object": "logout",
            "message": "Logged out successfully",
        }
        result = await self.auth.logout()
        self.assertEqual(result["message"], "Logged out successfully")


if __name__ == "__main__":
    unittest.main()
