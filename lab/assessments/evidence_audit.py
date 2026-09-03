"""Report unresolved evidence honestly from mastery-map language."""
from pathlib import Path
import json, re

MAPS = {
    "ncp-aai": Path("studies/ncp-aai/objective-map.md"),
    "aws-sap": Path("studies/aws-sap/objective-map.md"),
    "cka": Path("studies/cka/objective-map.md"),
    "ncp-genl": Path("studies/ncp-genl/objective-map.md"),
    "ccsp": Path("studies/ccsp/objective-map.md"),
    "google-pmle": Path("studies/google-pmle/objective-map.md"),
}
PENDING = re.compile(r"\b(pending|required|remain|partial|studied|design-only|cloud lab|platform lab|gpu/model|live cluster|live exercises)\b", re.I)

def audit() -> dict[str, object]:
    tracks = {}
    for track, path in MAPS.items():
        text = path.read_text(); lines = []
        for number, line in enumerate(text.splitlines(), 1):
            if PENDING.search(line): lines.append({"line": number, "text": line.strip()})
        tracks[track] = {"map": str(path), "unresolved_lines": lines, "ready": not lines}
    return {"tracks": tracks, "all_ready": all(item["ready"] for item in tracks.values())}

if __name__ == "__main__":
    report = audit(); output = Path("assessments/evidence-audit.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {output}; all_ready={report['all_ready']}")

