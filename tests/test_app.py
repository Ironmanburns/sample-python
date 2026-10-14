"""Contract tests for the sample-python health app.

Boots the real HTTP server on an ephemeral port and asserts the three
responses defined in STANDARD.md: /healthz, /version and the 404 fallback.
Run with `python -m unittest` or `pytest`.
"""
from __future__ import annotations

import json
import os
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer
from unittest import TestCase, main

# Import the handler under test; set env before import so module-level
# constants pick up deterministic values.
os.environ["SERVICE_NAME"] = "sample-python"
os.environ["APP_VERSION"] = "9.9.9-test"
import app  # noqa: E402


class ContractTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = HTTPServer(("127.0.0.1", 0), app.Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()

    def _get(self, path: str):
        url = f"http://127.0.0.1:{self.port}{path}"
        try:
            with urllib.request.urlopen(url) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read())

    def test_healthz_ok(self) -> None:
        status, body = self._get("/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"status": "ok"})

    def test_version_reports_service_and_version(self) -> None:
        status, body = self._get("/version")
        self.assertEqual(status, 200)
        self.assertEqual(body["service"], "sample-python")
        self.assertEqual(body["version"], "9.9.9-test")

    def test_unknown_route_is_404(self) -> None:
        status, body = self._get("/nope")
        self.assertEqual(status, 404)
        self.assertEqual(body, {"error": "not_found"})


if __name__ == "__main__":
    main()
