"""Dependency-free agent primitives for NCP-AAI architecture practice."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
import hashlib
import json
import time


class Risk(str, Enum):
    READ = "read"
    WRITE = "write"


@dataclass(frozen=True)
class Tool:
    name: str
    risk: Risk
    handler: Callable[[dict[str, Any]], dict[str, Any]]


@dataclass
class TraceEvent:
    event: str
    detail: dict[str, Any]
    timestamp: float = field(default_factory=time.time)


@dataclass
class AgentState:
    request_id: str
    steps_remaining: int = 5
    approved_actions: set[str] = field(default_factory=set)
    trace: list[TraceEvent] = field(default_factory=list)
    seen_idempotency_keys: set[str] = field(default_factory=set)

    def record(self, event: str, **detail: Any) -> None:
        self.trace.append(TraceEvent(event, detail))


class PolicyError(RuntimeError):
    pass


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    retryable: tuple[type[Exception], ...] = (TimeoutError, ConnectionError)

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be positive")


@dataclass
class CircuitBreaker:
    failure_threshold: int = 3
    failures: int = 0
    is_open: bool = False

    def success(self) -> None:
        self.failures = 0

    def failure(self) -> None:
        self.failures += 1
        self.is_open = self.failures >= self.failure_threshold


class TrustAgent:
    def __init__(self, tools: list[Tool]) -> None:
        self.tools = {tool.name: tool for tool in tools}

    def invoke(self, state: AgentState, tool_name: str,
               arguments: dict[str, Any], *, approval_token: str | None = None,
               idempotency_key: str | None = None) -> dict[str, Any]:
        if state.steps_remaining <= 0:
            raise PolicyError("step budget exhausted")
        state.steps_remaining -= 1
        tool = self.tools.get(tool_name)
        if tool is None:
            state.record("tool_rejected", tool=tool_name, reason="unknown_tool")
            raise PolicyError("tool is not allowlisted")
        if tool.risk is Risk.WRITE:
            if approval_token not in state.approved_actions:
                state.record("tool_rejected", tool=tool_name, reason="approval_required")
                raise PolicyError("write requires explicit approval")
            if not idempotency_key:
                raise PolicyError("write requires an idempotency key")
            if idempotency_key in state.seen_idempotency_keys:
                state.record("duplicate_suppressed", tool=tool_name)
                return {"status": "duplicate_suppressed"}
            state.seen_idempotency_keys.add(idempotency_key)
        state.record("tool_started", tool=tool_name, args_hash=_digest(arguments))
        try:
            result = tool.handler(arguments)
        except Exception as exc:
            state.record("tool_failed", tool=tool_name, error=type(exc).__name__)
            raise
        state.record("tool_completed", tool=tool_name, result_hash=_digest(result))
        return result

    def invoke_resilient(self, state: AgentState, tool_name: str,
                         arguments: dict[str, Any], *,
                         retry: RetryPolicy = RetryPolicy(),
                         breaker: CircuitBreaker | None = None,
                         **authorization: Any) -> dict[str, Any]:
        """Retry transient failures only; never retry policy or validation errors."""
        breaker = breaker or CircuitBreaker()
        if breaker.is_open:
            state.record("circuit_rejected", tool=tool_name)
            raise ConnectionError("circuit is open")
        for attempt in range(1, retry.max_attempts + 1):
            try:
                result = self.invoke(state, tool_name, arguments, **authorization)
                breaker.success()
                return result
            except retry.retryable as exc:
                breaker.failure()
                state.record("retry_scheduled", tool=tool_name, attempt=attempt,
                             error=type(exc).__name__)
                if breaker.is_open or attempt == retry.max_attempts:
                    raise
        raise AssertionError("unreachable")


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, default=str).encode()
    return hashlib.sha256(encoded).hexdigest()[:12]


def search_documents(arguments: dict[str, Any]) -> dict[str, Any]:
    if not str(arguments.get("query", "")).strip():
        raise ValueError("query is required")
    return {"matches": [{"document_id": "policy-001",
                          "passage_id": "policy-001#p3",
                          "text": "Writes require human approval."}]}


def publish_report(arguments: dict[str, Any]) -> dict[str, Any]:
    title = str(arguments.get("title", "")).strip()
    if not title:
        raise ValueError("title is required")
    return {"status": "published", "title": title}


def build_agent() -> TrustAgent:
    return TrustAgent([Tool("search_documents", Risk.READ, search_documents),
                       Tool("publish_report", Risk.WRITE, publish_report)])
