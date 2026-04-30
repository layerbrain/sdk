"""Tests for the Chat Completions resource."""

from __future__ import annotations

import json
import unittest
from unittest.mock import MagicMock

from layerbrain.sdk._types import ChatCompletion, ChatCompletionChunk
from layerbrain.sdk.resources.chat.completions import Completions, Stream


class TestCompletions(unittest.TestCase):
    """Test Completions resource in sync context (no event loop)."""

    def setUp(self):
        self.mock_client = MagicMock()
        self.completions = Completions(self.mock_client)

    def test_create_non_streaming(self):
        self.mock_client._post.return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "model": "meta-llama/llama-3.1-8b",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "Hello!"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }

        result = self.completions.create(
            model="meta-llama/llama-3.1-8b",
            messages=[{"role": "user", "content": "Hello"}],
        )
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        self.assertIsInstance(result, ChatCompletion)
        self.assertEqual(result.id, "chatcmpl-123")
        self.assertEqual(result.choices[0].message.content, "Hello!")
        self.assertEqual(result.usage.total_tokens, 15)

    def test_create_streaming(self):
        chunks = [
            json.dumps({
                "id": "chatcmpl-123",
                "object": "chat.completion.chunk",
                "choices": [{"index": 0, "delta": {"role": "assistant", "content": "Hel"}}],
            }),
            json.dumps({
                "id": "chatcmpl-123",
                "object": "chat.completion.chunk",
                "choices": [{"index": 0, "delta": {"content": "lo!"}}],
            }),
            json.dumps({
                "id": "chatcmpl-123",
                "object": "chat.completion.chunk",
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            }),
        ]
        self.mock_client._stream_sse.return_value = iter(chunks)

        result = self.completions.create(
            model="meta-llama/llama-3.1-8b",
            messages=[{"role": "user", "content": "Hello"}],
            stream=True,
        )

        print(f"Stream type: {type(result)}")
        self.assertIsInstance(result, Stream)

        stream_chunks = list(result)
        self.assertEqual(len(stream_chunks), 3)
        self.assertIsInstance(stream_chunks[0], ChatCompletionChunk)
        self.assertEqual(stream_chunks[0].choices[0].delta.content, "Hel")
        self.assertEqual(stream_chunks[1].choices[0].delta.content, "lo!")
        self.assertEqual(stream_chunks[2].choices[0].finish_reason, "stop")

    def test_create_with_extra_kwargs(self):
        self.mock_client._post.return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "choices": [],
        }

        self.completions.create(
            model="test-model",
            messages=[{"role": "user", "content": "Hi"}],
            temperature=0.7,
            max_tokens=100,
        )
        call_args = self.mock_client._post.call_args
        self.assertEqual(call_args[1]["json"]["temperature"], 0.7)
        self.assertEqual(call_args[1]["json"]["max_tokens"], 100)


if __name__ == "__main__":
    unittest.main()
