"""Validate and score checklist evidence for original architecture task labs."""
import json
from pathlib import Path

BANK = Path("studies/aws-sap/task-labs.json")

def load_labs(): return json.loads(BANK.read_text())

def coverage(response: str, lab: dict[str, object]) -> dict[str, object]:
    """Self-audit aid only; semantic grading still requires review."""
    text = response.lower()
    terms = []
    for requirement in lab["must_address"]:
        anchors = [word.strip("/(),") for word in str(requirement).lower().split() if len(word.strip("/(),")) > 4]
        matched = any(anchor in text for anchor in anchors)
        terms.append({"requirement": requirement, "mentioned": matched})
    return {"task": lab["task"], "mentioned": sum(item["mentioned"] for item in terms),
            "total": len(terms), "details": terms,
            "warning":"Keyword coverage does not prove a correct architecture."}

