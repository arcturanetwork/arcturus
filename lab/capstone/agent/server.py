"""Dependency-free HTTP boundary for the Arcturus agent lab."""
from __future__ import annotations

from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from threading import RLock
import time
from typing import Any

from capstone.agent.trust_agent import AgentState, PolicyError, TrustAgent, _digest, build_agent


@dataclass(frozen=True)
class Approval:
    request_id: str
    tool: str
    arguments_digest: str
    expires_at: float


class AgentGateway:
    def __init__(self, agent: TrustAgent | None = None) -> None:
        self.agent = agent or build_agent()
        self.states: dict[str, AgentState] = {}
        self.approvals: dict[str, Approval] = {}
        self.completed_writes: dict[str, tuple[str, dict[str, Any]]] = {}
        self.lock = RLock()

    def approve(self, token: str, request_id: str, tool: str,
                arguments: dict[str, Any], ttl_seconds: int = 300) -> None:
        if not token or ttl_seconds <= 0:
            raise ValueError("approval token and positive TTL required")
        with self.lock:
            self.approvals[token] = Approval(request_id, tool, _digest(arguments),
                                             time.time() + ttl_seconds)

    def invoke(self, payload: dict[str, Any]) -> dict[str, Any]:
        request_id = str(payload.get("request_id", "")).strip()
        tool = str(payload.get("tool", "")).strip()
        arguments = payload.get("arguments")
        if not request_id or not tool or not isinstance(arguments, dict):
            raise ValueError("request_id, tool, and object arguments are required")
        token = payload.get("approval_token")
        idempotency_key = payload.get("idempotency_key")
        with self.lock:
            state = self.states.setdefault(request_id, AgentState(request_id))
            if token is not None:
                approval = self.approvals.get(str(token))
                if approval is None or approval.expires_at < time.time():
                    raise PolicyError("approval is unknown or expired")
                if (approval.request_id, approval.tool, approval.arguments_digest) != (
                        request_id, tool, _digest(arguments)):
                    raise PolicyError("approval is not bound to this action")
                state.approved_actions.add(str(token))
            if tool == "publish_report" and idempotency_key:
                prior = self.completed_writes.get(str(idempotency_key))
                arguments_digest = _digest(arguments)
                if prior:
                    if prior[0] != arguments_digest:
                        raise PolicyError("idempotency key reused with different arguments")
                    return {"request_id": request_id, "result": {"status":"duplicate_suppressed"},
                            "trace_events": len(state.trace)}
            result = self.agent.invoke(state, tool, arguments, approval_token=str(token) if token else None,
                                       idempotency_key=str(idempotency_key) if idempotency_key else None)
            if tool == "publish_report" and idempotency_key:
                self.completed_writes[str(idempotency_key)] = (_digest(arguments), result)
            return {"request_id": request_id, "result": result, "trace_events": len(state.trace)}


class LabHTTPServer(ThreadingHTTPServer):
    # The parent default backlog is commonly 5, which creates artificial tail latency
    # during the deliberately bursty local profile.
    request_queue_size = 128
    daemon_threads = True


def handler_factory(gateway: AgentGateway):
    class Handler(BaseHTTPRequestHandler):
        server_version = "ArcturusLab/1"

        def _json(self, status: int, body: dict[str, Any]) -> None:
            encoded = json.dumps(body).encode()
            self.send_response(status); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
            self.send_header("X-Content-Type-Options", "nosniff")
            if "request_id" in body: self.send_header("X-Request-ID", str(body["request_id"]))
            self.end_headers(); self.wfile.write(encoded)

        def do_GET(self) -> None:
            if self.path == "/health": self._json(200, {"status":"ok"})
            else: self._json(404, {"error":"not_found"})

        def do_POST(self) -> None:
            if self.path != "/v1/invoke":
                self._json(404, {"error":"not_found"}); return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 65_536: raise ValueError("invalid request size")
                payload = json.loads(self.rfile.read(length))
                if not isinstance(payload, dict): raise ValueError("JSON object required")
                self._json(200, gateway.invoke(payload))
            except PolicyError as exc: self._json(403, {"error":"policy_rejected", "detail":str(exc)})
            except (ValueError, json.JSONDecodeError) as exc: self._json(400, {"error":"invalid_request", "detail":str(exc)})

        def log_message(self, _format: str, *args: object) -> None:
            return

    return Handler


def build_server(host: str = "127.0.0.1", port: int = 0,
                 gateway: AgentGateway | None = None) -> ThreadingHTTPServer:
    gateway = gateway or AgentGateway()
    return LabHTTPServer((host, port), handler_factory(gateway))
