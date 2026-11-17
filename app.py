"""
ChurnGuard — Dual-Portal Full-Stack Python Server (Client Admin Portal + Customer Login Portal)
Author: Mohammed Kaif Ahmed (https://kaifcode.com)
"""
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from database import ChurnGuardDatabase

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = ChurnGuardDatabase()
engine = db.engine


class ChurnGuardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def _send_json(self, data: dict, status: int = 200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self._send_json({"status": "ok"})

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/customers":
            return self._send_json({"customers": db.list_customers()})
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}
        if parsed.path == "/api/predict":
            return self._send_json({"status": "ok", "prediction": engine.predict_customer(body)})
        elif parsed.path == "/api/customers":
            return self._send_json({"status": "saved", "customer": db.upsert_customer(body)})
        elif parsed.path == "/api/events":
            return self._send_json({"status": "logged", "event": db.log_portal_event(body)})
        return self._send_json({"error": "Not found"}, status=404)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), ChurnGuardHandler)
    print("ChurnGuard Dual-Portal Server running at http://localhost:8000")
    server.serve_forever()
