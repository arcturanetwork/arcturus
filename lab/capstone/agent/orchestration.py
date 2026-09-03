"""Typed, bounded multi-agent orchestration and feedback primitives."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable
import uuid

class MessageKind(str, Enum):
    TASK = "task"
    RESULT = "result"
    ERROR = "error"
    APPROVAL_REQUEST = "approval_request"

@dataclass(frozen=True)
class AgentMessage:
    message_id: str
    correlation_id: str
    sender: str
    recipient: str
    kind: MessageKind
    payload: dict[str, object]
    remaining_hops: int

    @classmethod
    def create(cls, sender: str, recipient: str, kind: MessageKind,
               payload: dict[str, object], remaining_hops: int = 4,
               correlation_id: str | None = None):
        if remaining_hops < 0: raise ValueError("hop budget cannot be negative")
        return cls(str(uuid.uuid4()), correlation_id or str(uuid.uuid4()), sender,
                   recipient, kind, payload, remaining_hops)

@dataclass(frozen=True)
class AgentRole:
    name: str
    accepts: frozenset[MessageKind]
    handler: Callable[[AgentMessage], AgentMessage | None]

class OrchestrationError(RuntimeError): pass

class Orchestrator:
    def __init__(self, roles: list[AgentRole]): self.roles = {role.name: role for role in roles}
    def route(self, initial: AgentMessage) -> list[AgentMessage]:
        transcript, current = [], initial
        seen = set()
        while current is not None:
            if current.message_id in seen: raise OrchestrationError("message replay detected")
            seen.add(current.message_id); transcript.append(current)
            if current.remaining_hops == 0: raise OrchestrationError("hop budget exhausted")
            role = self.roles.get(current.recipient)
            if role is None or current.kind not in role.accepts:
                raise OrchestrationError("recipient or message kind not allowed")
            response = role.handler(current)
            if response is not None:
                if response.correlation_id != current.correlation_id:
                    raise OrchestrationError("correlation id changed")
                if response.remaining_hops >= current.remaining_hops:
                    raise OrchestrationError("hop budget did not decrease")
            current = response
        return transcript

@dataclass(frozen=True)
class Feedback:
    case_id: str
    evaluator: str
    rating: int
    category: str
    comment: str

class FeedbackStore:
    def __init__(self): self.items: list[Feedback] = []
    def add(self, feedback: Feedback) -> None:
        if feedback.rating not in range(1, 6): raise ValueError("rating must be 1 through 5")
        if feedback.category not in {"correctness","safety","groundedness","usability"}:
            raise ValueError("unknown feedback category")
        if not feedback.evaluator or not feedback.case_id: raise ValueError("traceable evaluator and case required")
        self.items.append(feedback)
    def summary(self) -> dict[str, float]:
        categories = {item.category for item in self.items}
        return {category: sum(x.rating for x in self.items if x.category == category) /
                sum(1 for x in self.items if x.category == category) for category in categories}

