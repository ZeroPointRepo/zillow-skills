"""Smoke tests for the zillow-zestimate handler. No network — urlopen is mocked."""

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
            result = handler.get_zestimate(zpid="42")
        self.assertEqual(result["error"], "auth")
        self.assertIn("ZILLAPI_KEY", result["detail"])
        self.assertIn("zillapi.com/signup", result["detail"])


class TestInputValidation(unittest.TestCase):
    def test_no_zpid_or_address_returns_error(self):
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            result = handler.get_zestimate()
        self.assertEqual(result["error"], "invalid_argument")


class TestEndpoint(unittest.TestCase):
    @patch("handler.urllib.request.urlopen")
    def test_zpid_hits_zestimate_endpoint_directly(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": {"zestimate": 500000}}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            result = handler.get_zestimate(zpid="42")
        self.assertEqual(mock_urlopen.call_count, 1)
        called_url = mock_urlopen.call_args[0][0].full_url
        self.assertIn("/v1/properties/42/zestimate", called_url)
        self.assertEqual(result["data"]["zestimate"], 500000)

    @patch("handler.urllib.request.urlopen")
    def test_address_resolves_zpid_then_calls_zestimate(self, mock_urlopen):
        mock_urlopen.side_effect = [
            _mock_response(b'{"data": {"zpid": "777"}}'),
            _mock_response(b'{"data": {"zestimate": 600000}}'),
        ]
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_test"}):
            result = handler.get_zestimate(address="123 Main St, Austin TX")
        self.assertEqual(mock_urlopen.call_count, 2)
        first_url = mock_urlopen.call_args_list[0][0][0].full_url
        second_url = mock_urlopen.call_args_list[1][0][0].full_url
        self.assertIn("/v1/properties/by-address", first_url)
        self.assertIn("/v1/properties/777/zestimate", second_url)
        self.assertEqual(result["data"]["zestimate"], 600000)

    @patch("handler.urllib.request.urlopen")
    def test_authorization_header_is_set(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(b'{"data": {}}')
        with patch.dict(os.environ, {"ZILLAPI_KEY": "zk_secret"}):
            handler.get_zestimate(zpid="42")
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.headers["Authorization"], "Bearer zk_secret")
        self.assertIn("zillow-skills", req.headers["User-agent"])


if __name__ == "__main__":
    unittest.main()
