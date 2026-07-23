#!/usr/bin/env python3
"""Serve a patched stock map.gzd locally and proxy all other map tiles to Azure.

Usage (from this folder):
  python map_proxy.py

Then set MapUrl in config.xml / SceneManager to:
  http://127.0.0.1:8765/maps/stock/map.gzd
"""

from __future__ import annotations

import http.client
import http.server
import socketserver
import urllib.parse
from pathlib import Path

PORT = 8765
UPSTREAM_HOST = "gizmosdk.blob.core.windows.net"
LOCAL_MAP = Path(__file__).resolve().parent / "map.gzd"


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        path = urllib.parse.urlparse(self.path).path
        if path in ("/maps/stock/map.gzd", "/map.gzd"):
            if not LOCAL_MAP.is_file():
                self.send_error(500, f"Missing local patched map: {LOCAL_MAP}")
                return
            data = LOCAL_MAP.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        # Proxy everything else to the public Azure map host
        conn = http.client.HTTPSConnection(UPSTREAM_HOST, timeout=60)
        try:
            conn.request("GET", path, headers={"User-Agent": "CSW-map-proxy"})
            resp = conn.getresponse()
            body = resp.read()
            self.send_response(resp.status)
            content_type = resp.getheader("Content-Type", "application/octet-stream")
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        finally:
            conn.close()

    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))


if __name__ == "__main__":
    if not LOCAL_MAP.is_file():
        raise SystemExit(f"Place patched map.gzd next to this script: {LOCAL_MAP}")
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Map proxy on http://127.0.0.1:{PORT}")
        print("MapUrl => http://127.0.0.1:8765/maps/stock/map.gzd")
        httpd.serve_forever()
