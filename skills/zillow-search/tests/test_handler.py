"""Smoke tests for the zillow-search handler. No network — urlopen is mocked."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import handler  # noqa: E402


def _mock_response(body):
    cm = MagicMock()
    cm.__enter__.return_value.read.return_value = body
    return cm


class TestAuth(unittest.TestCase):
    def test_missing_key_returns_auth_error(self):
        with patch.dict(os.environ, {}, clear=True):
            result = handler.search_listings(location="Austin, TX")
        self.assertEqual(result["error"], "auth")
        self.assertIn("ZILLAPI_KEY", result["detail"])
        self.assertIn("zillapi.com/signup", result["detail"])


class TestInputValidation(unittest.TestCase):
    def test_no_location_or_bbox_returns_error(self):
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            result = handler.search_listings()
        self.assertEqual(result["error"], "invalid_argument")


class TestEndpoint(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_listings_endpoint_with_location(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": [], "meta": {"count": 0}}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            handler.search_listings(location="Austin, TX", price_max=500000)
        called_url = mock_urlopen.call_args[0][0].full_url
        self.assertIn("/v1/listings", called_url)
        self.assertIn("location=Austin", called_url)
        self.assertIn("price_max=500000", called_url)
        self.assertIn("status=for_sale", called_url)

    @patch("handler.urllib.request.urlopen")
    def test_listings_endpoint_with_bbox(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": []}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            handler.search_listings(bbox="-97.95,30.10,-97.55,30.50", status="for_rent")
        called_url = mock_urlopen.call_args[0][0].full_url
        self.assertIn("bbox=", called_url)
        self.assertIn("status=for_rent", called_url)

    @patch("handler.urllib.request.urlopen")
    def test_none_params_filtered_from_url(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": []}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            handler.search_listings(location="Austin, TX")
        called_url = mock_urlopen.call_args[0][0].full_url
        self.assertNotIn("bbox=", called_url)
        self.assertNotIn("price_min=", called_url)
        self.assertNotIn("beds_min=", called_url)

    @patch("handler.urllib.request.urlopen")
    def test_authorization_header_is_set(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": []}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_secret"}):
            handler.search_listings(location="Austin, TX")
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.headers["Authorization"], "Bearer zk_secret")
        self.assertIn("zillow-skills", req.headers["User-agent"])


if __name__ == "__main__":
    unittest.main()
