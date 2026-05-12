"""Smoke tests for the zillow-full handler. No network — urlopen is mocked."""

import json
import os
import sys
import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import handler  # noqa: E402


def _mock_response(body):
    """Build a context-manager mock that returns `body` (bytes) from .read()."""
    cm = MagicMock()
    cm.__enter__.return_value.read.return_value = body
    return cm


class TestAuth(unittest.TestCase):
    def test_missing_key_returns_auth_error(self):
        with patch.dict(os.environ, {}, clear=True):
            result = handler.lookup_property_by_address("123 Main St, Austin TX")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "auth")
        self.assertIn("ZILLAPI_KEY", result["detail"])

    def test_empty_key_returns_auth_error(self):
        with patch.dict(os.environ, {"ZILLAPI_KEY": "   "}, clear=True):
            result = handler.lookup_property_by_address("123 Main St, Austin TX")
        self.assertEqual(result["error"], "auth")


class TestURLConstruction(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_lookup_by_address_hits_correct_endpoint(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": {"zpid": "123"}}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            handler.lookup_property_by_address("123 Main St, Austin TX")
        called_url = mock_urlopen.call_args[0][0].full_url
        self.assertIn("/v1/properties/by-address", called_url)
        self.assertIn("address=", called_url)
        self.assertIn("status=FOR_SALE", called_url)

    @patch("handler.urllib.request.urlopen")
    def test_lookup_by_zpid_uses_path_param(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": {"zpid": "42"}}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            handler.lookup_property_by_zpid("42")
        called_url = mock_urlopen.call_args[0][0].full_url
        self.assertIn("/v1/properties/42", called_url)
        self.assertNotIn("by-address", called_url)

    @patch("handler.urllib.request.urlopen")
    def test_search_listings_filters_none_params(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": []}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            handler.search_listings(location="Austin, TX", price_max=500000)
        called_url = mock_urlopen.call_args[0][0].full_url
        self.assertIn("location=Austin", called_url)
        self.assertIn("price_max=500000", called_url)
        # None-valued params must not appear in the querystring
        self.assertNotIn("bbox=", called_url)
        self.assertNotIn("price_min=", called_url)

    @patch("handler.urllib.request.urlopen")
    def test_authorization_header_is_set(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": {}}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_secret"}):
            handler.lookup_property_by_address("123 Main St")
        request_obj = mock_urlopen.call_args[0][0]
        self.assertEqual(request_obj.headers["Authorization"], "Bearer zk_secret")
        self.assertIn("zillow-skills", request_obj.headers["User-agent"])


class TestZestimateResolution(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_zestimate_with_zpid_skips_resolution(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": {"zestimate": 500000}}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            handler.get_zestimate(zpid="42")
        self.assertEqual(mock_urlopen.call_count, 1)
        self.assertIn("/properties/42/zestimate", mock_urlopen.call_args[0][0].full_url)

    @patch("handler.urllib.request.urlopen")
    def test_zestimate_with_address_resolves_zpid_first(self, mock_urlopen):
        # First call returns the zpid; second call returns the zestimate.
        mock_urlopen.side_effect = [
            _mock_response(b'{"data": {"zpid": "777"}}'),
            _mock_response(b'{"data": {"zestimate": 600000}}'),
        ]
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            result = handler.get_zestimate(address="123 Main St, Austin TX")
        self.assertEqual(mock_urlopen.call_count, 2)
        self.assertIn("/properties/777/zestimate", mock_urlopen.call_args_list[1][0][0].full_url)
        self.assertEqual(result["data"]["zestimate"], 600000)

    def test_zestimate_without_args_returns_error(self):
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            result = handler.get_zestimate()
        self.assertEqual(result["error"], "invalid_argument")


class TestErrorHandling(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_http_404_returns_structured_error(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://api.zillapi.com/v1/properties/by-address",
            404,
            "Not Found",
            {},
            BytesIO(b'{"error": {"code": "not_found"}}'),
        )
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            result = handler.lookup_property_by_address("999 Nonexistent")
        self.assertEqual(result["error"], "HTTP 404")
        self.assertIn("not_found", result["detail"])

    @patch("handler.urllib.request.urlopen")
    def test_network_error_returns_structured_error(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.URLError("connection refused")
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            result = handler.lookup_property_by_address("123 Main St")
        self.assertEqual(result["error"], "network")


if __name__ == "__main__":
    unittest.main()
