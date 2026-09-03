from concurrent.futures import ThreadPoolExecutor
import json
from threading import Thread
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from capstone.agent.server import AgentGateway, build_server


class AgentServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gateway = AgentGateway(); cls.server = build_server(gateway=cls.gateway)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True); cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def post(self, payload):
        request = Request(self.base + "/v1/invoke", json.dumps(payload).encode(),
                          {"Content-Type":"application/json"}, method="POST")
        with urlopen(request, timeout=2) as response:
            return response.status, response.headers, json.load(response)

    def test_health_and_correlated_read(self):
        self.assertGreaterEqual(self.server.request_queue_size, 20)
        with urlopen(self.base + "/health", timeout=2) as response:
            self.assertEqual(json.load(response), {"status":"ok"})
        status, headers, body = self.post({"request_id":"http-read", "tool":"search_documents",
                                           "arguments":{"query":"approval"}})
        self.assertEqual(status, 200); self.assertEqual(headers["X-Request-ID"], "http-read")
        self.assertIn("passage_id", body["result"]["matches"][0])

    def test_request_cannot_self_assert_approval(self):
        with self.assertRaises(HTTPError) as caught:
            self.post({"request_id":"self-approve", "tool":"publish_report",
                       "arguments":{"title":"x"}, "approval_token":"invented",
                       "idempotency_key":"http-write-1"})
        self.assertEqual(caught.exception.code, 403)

    def test_approval_is_bound_and_idempotency_is_global(self):
        arguments = {"title":"approved"}
        self.gateway.approve("token-1", "bound-request", "publish_report", arguments)
        payload = {"request_id":"bound-request", "tool":"publish_report", "arguments":arguments,
                   "approval_token":"token-1", "idempotency_key":"http-write-2"}
        self.assertEqual(self.post(payload)[2]["result"]["status"], "published")
        self.assertEqual(self.post(payload)[2]["result"]["status"], "duplicate_suppressed")
        self.gateway.approve("token-2", "another-request", "publish_report", arguments)
        payload["request_id"] = "another-request"
        payload["approval_token"] = "token-2"
        self.assertEqual(self.post(payload)[2]["result"]["status"], "duplicate_suppressed")
        payload["arguments"] = {"title":"changed"}
        with self.assertRaises(HTTPError) as caught: self.post(payload)
        self.assertEqual(caught.exception.code, 403)

    def test_concurrent_reads_complete_without_state_cross_talk(self):
        def call(index):
            return self.post({"request_id":f"concurrent-{index}", "tool":"search_documents",
                              "arguments":{"query":str(index)}})[2]["request_id"]
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(call, range(20)))
        self.assertEqual(set(results), {f"concurrent-{i}" for i in range(20)})


if __name__ == "__main__": unittest.main()
