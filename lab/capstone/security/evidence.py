"""Minimal chain-of-custody model for forensic procedure exercises."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib

@dataclass(frozen=True)
class CustodyEvent:
    actor: str
    action: str
    timestamp: str
    content_hash: str

@dataclass
class EvidenceItem:
    evidence_id: str
    content: bytes
    custody: list[CustodyEvent] = field(default_factory=list)
    @property
    def digest(self) -> str: return hashlib.sha256(self.content).hexdigest()
    def record(self, actor: str, action: str, expected_hash: str | None = None) -> None:
        if not actor.strip() or not action.strip(): raise ValueError("actor and action required")
        if expected_hash is not None and expected_hash != self.digest:
            raise ValueError("evidence integrity check failed")
        self.custody.append(CustodyEvent(actor, action, datetime.now(timezone.utc).isoformat(), self.digest))
    def verify(self) -> bool:
        return bool(self.custody) and all(event.content_hash == self.digest for event in self.custody)

