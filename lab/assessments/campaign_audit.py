"""Fail-closed campaign readiness across source, coverage, scenario and platform gates."""
from __future__ import annotations

from dataclasses import fields
from datetime import date
import json
from pathlib import Path

from assessments.blueprint_audit import audit as blueprint_audit
from assessments.objective_coverage import audit as objective_audit
from assessments.scenario_exam import Attempt, readiness_gate


LEDGER = Path("assessments/platform-evidence.json")
ATTEMPTS = Path("assessments/attempts")
ALLOWED_STATUS = {"pending", "verified"}


def platform_gate(requirements: list[dict[str, object]], root: Path = Path(".")) -> dict[str, object]:
    invalid = []
    pending = []
    for item in requirements:
        status, proof = item.get("status"), item.get("proof", [])
        existing = [value for value in proof if (root / str(value)).is_file()]
        if status not in ALLOWED_STATUS:
            invalid.append(str(item.get("id")))
        if status != "verified" or not proof or len(existing) != len(proof):
            pending.append(str(item.get("id")))
    return {"ready": not invalid and not pending, "pending": pending, "invalid": invalid}


def _load_attempts(track: str) -> list[Attempt]:
    path = ATTEMPTS / f"{track}.json"
    if not path.exists(): return []
    allowed = {field.name for field in fields(Attempt)}
    return [Attempt(**{key: tuple(value) if key in {"scenario_ids", "evidence_links", "error_classes"} else value
                       for key, value in row.items() if key in allowed})
            for row in json.loads(path.read_text())]


def audit(as_of: date) -> dict[str, object]:
    blueprints = {x["id"]: x for x in blueprint_audit(as_of)["tracks"]}
    objectives = {x["id"]: x for x in objective_audit()["tracks"]}
    ledger = json.loads(LEDGER.read_text())["tracks"]
    results = []
    for track in sorted(ledger):
        platform = platform_gate(ledger[track])
        scenario = readiness_gate(_load_attempts(track))
        gates = {"blueprint": blueprints[track]["booking_ready"],
                 "objective_coverage": objectives[track]["covered"],
                 "scenario": scenario["ready"], "platform": platform["ready"]}
        results.append({"id": track, "ready": all(gates.values()), "gates": gates,
                        "blueprint_blockers": blueprints[track]["blockers"],
                        "scenario": scenario, "platform": platform})
    return {"as_of": as_of.isoformat(), "tracks": results,
            "all_certifications_ready": all(x["ready"] for x in results)}


if __name__ == "__main__":
    report = audit(date.today())
    output = Path("assessments/campaign-audit.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {output}; all_certifications_ready={report['all_certifications_ready']}")
