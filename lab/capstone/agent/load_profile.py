"""Reproducible local HTTP load/failure profile for the TrustGraph gateway."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
from threading import Thread
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from capstone.agent.server import build_server


def percentile(values: list[float], quantile: float) -> float:
    if not values or not 0 <= quantile <= 1:
        raise ValueError("non-empty values and quantile in [0, 1] required")
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int((len(ordered) - 1) * quantile + .5)))
    return ordered[index]


def summarize(results: list[dict[str, object]], elapsed_seconds: float) -> dict[str, object]:
    if not results or elapsed_seconds <= 0:
        raise ValueError("results and positive elapsed time required")
    latencies = [float(row["latency_ms"]) for row in results]
    unexpected = [row for row in results if not row["expected"]]
    request_ids = [str(row["request_id"]) for row in results]
    return {"requests": len(results), "elapsed_seconds": elapsed_seconds,
            "throughput_rps": len(results) / elapsed_seconds,
            "latency_ms": {"p50": percentile(latencies, .50), "p95": percentile(latencies, .95),
                           "p99": percentile(latencies, .99), "max": max(latencies)},
            "status_counts": {str(code): sum(row["status"] == code for row in results)
                              for code in sorted({int(row["status"]) for row in results})},
            "unexpected_outcomes": len(unexpected),
            "correlation_integrity": len(request_ids) == len(set(request_ids)),
            "limitations": ["loopback dependency-free handler, not a model call",
                            "no container, Kubernetes, GPU, external dependency, or sustained soak claim"]}


def run_profile(total_requests: int = 200, workers: int = 20,
                unauthorized_every: int = 10) -> dict[str, object]:
    if total_requests < 1 or workers < 1 or unauthorized_every < 1:
        raise ValueError("positive load parameters required")
    server = build_server(); thread = Thread(target=server.serve_forever, daemon=True); thread.start()
    base = f"http://127.0.0.1:{server.server_port}"

    def invoke(index: int) -> dict[str, object]:
        request_id = f"load-{index}"
        unauthorized = index % unauthorized_every == 0
        payload = ({"request_id":request_id, "tool":"publish_report", "arguments":{"title":"blocked"},
                    "approval_token":"invented", "idempotency_key":f"blocked-{index}"}
                   if unauthorized else
                   {"request_id":request_id, "tool":"search_documents", "arguments":{"query":str(index)}})
        request = Request(base + "/v1/invoke", json.dumps(payload).encode(),
                          {"Content-Type":"application/json"}, method="POST")
        started = time.perf_counter()
        try:
            with urlopen(request, timeout=5) as response:
                status = response.status; echoed = response.headers.get("X-Request-ID")
        except HTTPError as error:
            status = error.code; echoed = None; error.close()
        latency_ms = (time.perf_counter() - started) * 1000
        expected = status == (403 if unauthorized else 200) and (unauthorized or echoed == request_id)
        return {"request_id":request_id, "status":status, "latency_ms":latency_ms,
                "expected":expected, "case":"unauthorized_write" if unauthorized else "read"}

    started = time.perf_counter()
    try:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(invoke, range(total_requests)))
    finally:
        server.shutdown(); server.server_close(); thread.join()
    report = summarize(results, time.perf_counter() - started)
    report.update({"recorded_at":datetime.now(timezone.utc).isoformat(),
                   "configuration":{"workers":workers, "unauthorized_every":unauthorized_every,
                                    "listen_backlog":server.request_queue_size},
                   "expected_policy_rejections":sum(x["case"] == "unauthorized_write" for x in results)})
    return report


if __name__ == "__main__":
    report = run_profile()
    output = Path("evidence/ncp-aai/http-load-profile.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {output}; requests={report['requests']}; unexpected={report['unexpected_outcomes']}")
