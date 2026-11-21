import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

import httpx
from google import genai
from google.genai import types

from ai_helper import create_client, generate_response, get_model_name
from list_models import main as list_models_main


class TrackingTransport(httpx.BaseTransport):
    def __init__(self):
        self.request = None
        self.closed = False

    def handle_request(self, request):
        self.request = request
        return httpx.Response(
            200,
            json={
                "candidates": [{
                    "content": {"parts": [{"text": "Analysis"}], "role": "model"},
                    "finishReason": "STOP",
                    "index": 0,
                }]
            },
        )

    def close(self):
        self.closed = True


class NoOpAsyncTransport(httpx.AsyncBaseTransport):
    async def handle_async_request(self, request):
        raise AssertionError("AI analysis should use the synchronous transport")

    async def aclose(self):
        pass


class AIHelperTests(unittest.TestCase):
    def test_client_requires_an_environment_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "GEMINI_API_KEY"):
                create_client()

    def test_generation_uses_configured_key_and_model(self):
        generate_content = Mock(return_value=SimpleNamespace(text="Analysis"))
        mock_client = MagicMock()
        mock_client.__enter__.return_value = mock_client
        mock_client.models.generate_content = generate_content

        with patch.dict(
            os.environ,
            {"GEMINI_API_KEY": "test-key", "GEMINI_MODEL": "test-model"},
            clear=True,
        ), patch("ai_helper.genai.Client", return_value=mock_client) as client_factory:
            self.assertEqual(generate_response("prompt"), "Analysis")

        client_factory.assert_called_once()
        self.assertEqual(client_factory.call_args.kwargs["api_key"], "test-key")
        self.assertEqual(
            client_factory.call_args.kwargs["http_options"].timeout, 20000
        )
        mock_client.__exit__.assert_called_once()
        generate_content.assert_called_once_with(
            model="test-model",
            contents="prompt",
        )

    def test_real_sdk_request_uses_and_closes_its_http_transport(self):
        transport = TrackingTransport()
        sdk_client_factory = genai.Client
        http_options = types.HttpOptions(
            base_url="https://gemini.test",
            client_args={"verify": False, "transport": transport},
            async_client_args={"verify": False, "transport": NoOpAsyncTransport()},
            retry_options=types.HttpRetryOptions(attempts=1),
        )

        with patch.dict(
            os.environ,
            {"GEMINI_API_KEY": "test-key", "GEMINI_MODEL": "test-model"},
            clear=True,
        ), patch(
            "ai_helper.genai.Client",
            side_effect=lambda **kwargs: sdk_client_factory(
                **{**kwargs, "http_options": http_options},
            ),
        ), patch(
            "google.genai._api_client.BaseApiClient._ensure_websocket_ssl_ctx",
            return_value={},
        ):
            self.assertEqual(generate_response("prompt"), "Analysis")

        self.assertIsNotNone(transport.request)
        self.assertIn("models/test-model:generateContent", transport.request.url.path)
        self.assertTrue(transport.closed)

    def test_model_listing_keeps_client_open_for_lazy_iteration(self):
        mock_client = MagicMock()
        mock_client.__enter__.return_value = mock_client

        def model_iterator():
            self.assertEqual(mock_client.__exit__.call_count, 0)
            yield SimpleNamespace(name="models/first")
            self.assertEqual(mock_client.__exit__.call_count, 0)
            yield SimpleNamespace(name="models/second")

        mock_client.models.list.return_value = model_iterator()
        with patch("list_models.create_client", return_value=mock_client), patch(
            "builtins.print"
        ) as print_model:
            list_models_main()

        self.assertEqual(
            [call.args[0] for call in print_model.call_args_list],
            ["models/first", "models/second"],
        )
        mock_client.__exit__.assert_called_once()

    def test_model_name_has_a_default(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(get_model_name(), "gemini-3.8-flash")


if __name__ == "__main__":
    unittest.main()