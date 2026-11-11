import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from app import ApplicationHandler


class ApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), ApplicationHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

    def request(self, path):
        connection = HTTPConnection("127.0.0.1", self.port)
        connection.request("GET", path)
        response = connection.getresponse()
        body = response.read().decode("utf-8")
        connection.close()
        return response.status, body

    def test_root_returns_service_status(self):
        status, body = self.request("/")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["service"], "devops-demo")

    def test_health_endpoint(self):
        status, body = self.request("/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["status"], "healthy")

    def test_metrics_endpoint(self):
        status, body = self.request("/metrics")
        self.assertEqual(status, 200)
        self.assertIn("app_requests_total", body)


if __name__ == "__main__":
    unittest.main()