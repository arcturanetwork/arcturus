"""Original scenario-bank loader and scorer. No exam dumps."""
import json
from pathlib import Path
from typing import Iterable

BANK = Path(__file__).parent / "bank" / "scenarios.json"

def load_bank() -> list[dict[str, object]]:
    return json.loads(BANK.read_text())

def score(responses: dict[str, int], questions: Iterable[dict[str, object]] | None = None) -> dict[str, object]:
    questions = list(questions or load_bank())
    by_track: dict[str, dict[str, int]] = {}
    missed = []
    for item in questions:
        track = str(item["track"]); bucket = by_track.setdefault(track, {"correct": 0, "total": 0})
        bucket["total"] += 1
        correct = responses.get(str(item["id"])) == item["answer"]
        bucket["correct"] += int(correct)
        if not correct: missed.append({"id": item["id"], "domain": item["domain"], "rationale": item["rationale"]})
    total = sum(bucket["total"] for bucket in by_track.values())
    correct = sum(bucket["correct"] for bucket in by_track.values())
    return {"correct": correct, "total": total, "rate": correct / total if total else 0,
            "by_track": by_track, "missed": missed}

