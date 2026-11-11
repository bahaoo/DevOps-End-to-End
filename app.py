import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


START_TIME = time.time()
REQUESTS = 0


class ApplicationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global REQUESTS
        REQUESTS += 1

        if self.path == "/":
            self.send_json(200, '{"service":"devops-demo","status":"running"}')
        elif self.path == "/healthz":
            self.send_json(200, '{"status":"healthy"}')
        elif self.path == "/metrics":
            uptime = time.time() - START_TIME
            body = (
                "# HELP app_requests_total Total HTTP requests handled.\n"
                "# TYPE app_requests_total counter\n"
                f"app_requests_total {REQUESTS}\n"
                "# HELP app_uptime_seconds Application uptime in seconds.\n"
                "# TYPE app_uptime_seconds gauge\n"
                f"app_uptime_seconds {uptime:.2f}\n"
            )
            self.send_text(200, body, "text/plain; version=0.0.4")
        else:
            self.send_json(404, '{"error":"not found"}')

    def send_json(self, status, body):
        self.send_text(status, body, "application/json")

    def send_text(self, status, body, content_type):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), ApplicationHandler)
    print(f"devops-demo listening on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()