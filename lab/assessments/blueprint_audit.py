"""Validate blueprint provenance and recency without performing network checks."""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path


REGISTRY = Path("resources/certification-registry.json")
ALLOWED_STATES = {"published", "prelaunch", "provisional-successor"}


def audit(as_of: date, maximum_age_days: int = 3) -> dict[str, object]:
    registry = json.loads(REGISTRY.read_text())
    results = []
    for track in registry["tracks"]:
        checked = date.fromisoformat(track["guide_checked"])
        age = (as_of - checked).days
        paths = {name: Path(track[name]).exists() for name in ("map", "bank")}
        state_valid = track["blueprint_state"] in ALLOWED_STATES
        structure = track["objective_structure"]
        structure_valid = bool(structure) and all(isinstance(v, int) and v > 0 for v in structure.values())
        current = 0 <= age <= maximum_age_days
        blockers = []
        if not current: blockers.append("official blueprint recency")
        if track["blueprint_state"] != "published": blockers.append("target blueprint is provisional or prelaunch")
        if not all(paths.values()): blockers.append("local objective map or assessment bank missing")
        if not state_valid or not structure_valid: blockers.append("registry metadata invalid")
        results.append({"id": track["id"], "age_days": age, "source_current": current,
                        "blueprint_state": track["blueprint_state"], "paths": paths,
                        "objective_structure": structure, "blockers": blockers,
                        "booking_ready": not blockers})
    return {"as_of": as_of.isoformat(), "maximum_age_days": maximum_age_days,
            "tracks": results, "all_booking_ready": all(x["booking_ready"] for x in results)}


if __name__ == "__main__":
    today = date.today()
    report = audit(today)
    output = Path("assessments/blueprint-audit.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {output}; all_booking_ready={report['all_booking_ready']}")
