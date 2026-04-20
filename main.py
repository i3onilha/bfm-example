"""
Demo client that connects to the BFF server and calls its tools.

Python rewrite of main.go.
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


logging.basicConfig(level=logging.INFO)


class BackendHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload: dict) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self) -> None:  # noqa: N802 (stdlib method name)
        parsed = urlparse(self.path)
        if parsed.path != "/api/process_order":
            self._send_json(404, {"error": "not found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)
        try:
            body = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid json"})
            return

        status = "confirmed"
        if body.get("priority") == "high":
            status = "expedited"

        self._send_json(
            200,
            {
                "orderId": body.get("orderId"),
                "status": status,
                "estimatedAt": "2026-04-18T10:00:00Z",
            },
        )

    def do_GET(self) -> None:  # noqa: N802 (stdlib method name)
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/users/"):
            self._send_json(404, {"error": "not found"})
            return

        user_id = parsed.path.removeprefix("/api/users/")
        users = {
            "u1": {"id": "u1", "name": "Alice", "email": "alice@example.com"},
            "u2": {"id": "u2", "name": "Bob", "email": "bob@example.com"},
        }
        user = users.get(user_id)
        if user is None:
            self._send_json(404, {"error": "user not found"})
            return

        self._send_json(200, user)

    def log_message(self, fmt: str, *args) -> None:  # suppress default server logs
        return


def run_backend_http_server() -> None:
    """Start a mock backend REST API for testing."""
    server = ThreadingHTTPServer(("0.0.0.0", 8082), BackendHandler)
    logging.info("Starting Backend HTTP Server on :8082")
    server.serve_forever()


async def main() -> None:
    # Infrastructure layer: Backend HTTP API.
    threading.Thread(target=run_backend_http_server, daemon=True).start()
    time.sleep(0.1)

    backend_addr = "localhost:8081"
    headers = {
        "X-Tenant-Id": "tenant-123",
        "X-Correlation-Id": "corr-abc",
    }

    # Connect to the BFF server and call process_order.
    async with streamablehttp_client(
        f"http://{backend_addr}/mcp",
        headers=headers,
    ) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            order_result = await session.call_tool(
                "process_order",
                {"orderId": "ORD-42", "userId": "u1", "priority": "high"},
            )
            print(json.dumps(order_result.model_dump(), default=str))


if __name__ == "__main__":
    asyncio.run(main())
