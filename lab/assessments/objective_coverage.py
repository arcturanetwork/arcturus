"""Expand numbered blueprint ranges and verify that mastery maps name every item."""
from __future__ import annotations

import json
import re
from pathlib import Path


REGISTRY = Path("resources/certification-registry.json")
RANGE = re.compile(r"^(\d+)\.(\d+)-(\d+)\.(\d+)$")


def expand_range(value: str) -> list[str]:
    match = RANGE.fullmatch(value)
    if not match:
        raise ValueError(f"invalid objective range: {value}")
    start_domain, start_item, end_domain, end_item = map(int, match.groups())
    if start_domain != end_domain or end_item < start_item:
        raise ValueError(f"range must stay in one domain and ascend: {value}")
    return [f"{start_domain}.{item}" for item in range(start_item, end_item + 1)]


def expanded_objectives(track: dict[str, object]) -> list[str]:
    return [objective for value in track["objective_ranges"] for objective in expand_range(value)]


def audit() -> dict[str, object]:
    registry = json.loads(REGISTRY.read_text())
    results = []
    for track in registry["tracks"]:
        objectives = expanded_objectives(track)
        declared_keys = [key for key in ("numbered_objectives", "numbered_tasks", "numbered_subdomains")
                         if key in track["objective_structure"]]
        declared = track["objective_structure"][declared_keys[0]] if declared_keys else None
        map_text = Path(track["map"]).read_text().replace("–", "-").replace("—", "-")
        missing_ranges = []
        for value in track["objective_ranges"]:
            objectives_in_range = expand_range(value)
            range_is_named = value in map_text
            every_item_is_named = all(re.search(rf"(?<![\d.]){re.escape(item)}(?![\d.])", map_text)
                                      for item in objectives_in_range)
            if not range_is_named and not every_item_is_named:
                missing_ranges.append(value)
        count_matches = declared is None or declared == len(objectives)
        results.append({"id": track["id"], "declared": declared, "expanded": len(objectives),
                        "count_matches": count_matches, "missing_ranges_in_map": missing_ranges,
                        "covered": count_matches and not missing_ranges})
    return {"tracks": results, "all_numbered_coverage_consistent":
            all(x["covered"] for x in results)}


if __name__ == "__main__":
    report = audit()
    output = Path("assessments/objective-coverage.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {output}; all_numbered_coverage_consistent={report['all_numbered_coverage_consistent']}")
