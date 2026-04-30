"""Tests for pagination iterators."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from layerbrain.sdk._pagination import SyncPage


class TestSyncPage(unittest.TestCase):
    """Test synchronous pagination."""

    def test_iter_yields_data(self):
        page = SyncPage(
            data=[{"id": "a"}, {"id": "b"}],
            has_more=False,
            client=MagicMock(),
            path="/test",
        )
        items = list(page)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["id"], "a")

    def test_len_returns_data_count(self):
        page = SyncPage(
            data=[{"id": "a"}, {"id": "b"}, {"id": "c"}],
            has_more=False,
            client=MagicMock(),
            path="/test",
        )
        self.assertEqual(len(page), 3)

    def test_has_more_property(self):
        page = SyncPage(
            data=[{"id": "a"}],
            has_more=True,
            client=MagicMock(),
            path="/test",
        )
        self.assertTrue(page.has_more)

    def test_next_page_increments(self):
        mock_client = MagicMock()
        mock_client._get.return_value = {"data": [{"id": "c"}], "has_more": False}

        page = SyncPage(
            data=[{"id": "a"}, {"id": "b"}],
            has_more=True,
            client=mock_client,
            path="/test",
        )
        next_page = page.next_page()
        self.assertEqual(len(next_page), 1)
        self.assertEqual(next_page.data[0]["id"], "c")
        mock_client._get.assert_called_once_with("/test", params={"page": 2})

    def test_auto_paging_iter(self):
        mock_client = MagicMock()
        mock_client._get.return_value = {"data": [{"id": "c"}], "has_more": False}

        page = SyncPage(
            data=[{"id": "a"}, {"id": "b"}],
            has_more=True,
            client=mock_client,
            path="/test",
        )
        all_items = list(page.auto_paging_iter())
        self.assertEqual(len(all_items), 3)
        self.assertEqual([i["id"] for i in all_items], ["a", "b", "c"])

    def test_single_page_auto_paging(self):
        page = SyncPage(
            data=[{"id": "a"}],
            has_more=False,
            client=MagicMock(),
            path="/test",
        )
        all_items = list(page.auto_paging_iter())
        self.assertEqual(len(all_items), 1)

    def test_empty_page(self):
        page = SyncPage(
            data=[],
            has_more=False,
            client=MagicMock(),
            path="/test",
        )
        self.assertEqual(len(page), 0)
        self.assertEqual(list(page), [])


if __name__ == "__main__":
    unittest.main()
