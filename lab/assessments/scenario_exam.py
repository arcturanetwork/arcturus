"""Unified, original scenario-practice engine. It never marks platform evidence complete."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
import hashlib
import json
from pathlib import Path
import random


BANKS = {
    "ncp-aai": Path("studies/ncp-aai/scenario-labs.json"),
    "aws-sap": Path("studies/aws-sap/task-labs.json"),
    "cka": Path("studies/cka/performance-labs.json"),
    "ncp-genl": Path("studies/ncp-genl/scenario-labs.json"),
    "ccsp": Path("studies/ccsp/scenario-labs.json"),
    "google-pmle": Path("studies/google-pmle/scenario-labs.json"),
}
DIMENSIONS = ("knowledge", "selection", "safety", "verification", "explanation")
ERROR_CLASSES = {"knowledge", "scope", "sequencing", "governance", "reading", "command-speed"}


@dataclass(frozen=True)
class Attempt:
    track: str
    attempted_on: str
    scenario_ids: tuple[str, ...]
    earned: int
    possible: int
    elapsed_minutes: int
    allowed_minutes: int
    evidence_links: tuple[str, ...]
    error_classes: tuple[str, ...]
    bank_digest: str

    @property
    def rate(self) -> float:
        return self.earned / self.possible if self.possible else 0.0

    @property
    def within_time(self) -> bool:
        return self.elapsed_minutes <= self.allowed_minutes


def _id(item: dict[str, object]) -> str:
    return str(item.get("id") or f"AWS-{item['task']}")


def load_bank(track: str) -> list[dict[str, object]]:
    if track not in BANKS:
        raise ValueError(f"unknown track: {track}")
    return json.loads(BANKS[track].read_text())


def bank_digest(track: str) -> str:
    return hashlib.sha256(BANKS[track].read_bytes()).hexdigest()[:16]


def draw(track: str, count: int, seed: int) -> list[dict[str, object]]:
    bank = load_bank(track)
    if count <= 0 or count > len(bank):
        raise ValueError("count must be between 1 and bank size")
    # Round-robin across domains/sections so a short attempt cannot collapse to one area.
    key = "domain" if "domain" in bank[0] else "section" if "section" in bank[0] else "task"
    groups: dict[str, list[dict[str, object]]] = {}
    for item in bank:
        group = str(item[key]).split(".")[0]
        groups.setdefault(group, []).append(item)
    rng = random.Random(seed)
    for items in groups.values(): rng.shuffle(items)
    order = list(groups); rng.shuffle(order)
    selected = []
    while len(selected) < count:
        made_progress = False
        for group in order:
            if groups[group] and len(selected) < count:
                selected.append(groups[group].pop()); made_progress = True
        if not made_progress: break
    return selected


def score_attempt(track: str, scenarios: list[dict[str, object]], ratings: dict[str, dict[str, int]],
                  attempted_on: str, elapsed_minutes: int, evidence_links: list[str],
                  error_classes: list[str]) -> Attempt:
    date.fromisoformat(attempted_on)
    unknown_errors = set(error_classes) - ERROR_CLASSES
    if unknown_errors: raise ValueError(f"unknown error classes: {sorted(unknown_errors)}")
    expected_ids = {_id(item) for item in scenarios}
    if set(ratings) != expected_ids: raise ValueError("ratings must cover exactly the drawn scenarios")
    earned = 0
    for scenario_id, dimensions in ratings.items():
        if set(dimensions) != set(DIMENSIONS):
            raise ValueError(f"{scenario_id} must score all rubric dimensions")
        if any(not isinstance(value, int) or not 0 <= value <= 2 for value in dimensions.values()):
            raise ValueError("rubric scores must be integer values from 0 to 2")
        earned += sum(dimensions.values())
    allowed = sum(int(item.get("minutes", 10)) for item in scenarios)
    return Attempt(track, attempted_on, tuple(_id(item) for item in scenarios), earned,
                   len(scenarios) * len(DIMENSIONS) * 2, elapsed_minutes, allowed,
                   tuple(evidence_links), tuple(error_classes), bank_digest(track))


def readiness_gate(attempts: list[Attempt]) -> dict[str, object]:
    passing = sorted((a for a in attempts if a.rate >= .85 and a.within_time and a.evidence_links),
                     key=lambda a: a.attempted_on)
    separated_pair = None
    for i, first in enumerate(passing):
        for second in passing[i + 1:]:
            if (date.fromisoformat(second.attempted_on) - date.fromisoformat(first.attempted_on)).days >= 7:
                separated_pair = (first, second); break
        if separated_pair: break
    recurring = set()
    if separated_pair:
        recurring = set(separated_pair[0].error_classes) & set(separated_pair[1].error_classes)
    ready = bool(separated_pair) and not recurring
    return {"ready": ready, "passing_attempts": len(passing),
            "separated_pair": [a.attempted_on for a in separated_pair] if separated_pair else None,
            "recurring_error_classes": sorted(recurring),
            "limitations": "Scenario gate only; platform/lab and official-version gates remain separate."}


def append_attempt(path: Path, attempt: Attempt) -> None:
    history = json.loads(path.read_text()) if path.exists() else []
    history.append({**asdict(attempt), "rate": attempt.rate, "within_time": attempt.within_time})
    path.write_text(json.dumps(history, indent=2) + "\n")
