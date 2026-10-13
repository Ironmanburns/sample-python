from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


SERVICE = os.environ.get("SERVICE_NAME", "sample-python")
VERSION = os.environ.get("APP_VERSION", "0.1.0")
PORT = int(os.environ.get("PORT", "8080"))


class Handler(BaseHTTPRequestHandler):
    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self._json(200, {"status": "ok"})
        elif self.path == "/version":
            self._json(200, {"version": VERSION, "service": SERVICE})
        else:
            self._json(404, {"error": "not_found"})

    def log_message(self, fmt: str, *args) -> None:
        return


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
