"""Executable CCSP incident/SIEM/vulnerability/forensics tabletop."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from capstone.security.evidence import EvidenceItem


REQUIRED_ROLES = {"incident_commander", "evidence_custodian", "privacy_legal",
                  "service_owner", "provider_liaison", "communications_owner"}


def correlate(events: list[dict[str, object]]) -> dict[str, object]:
    ordered = sorted(events, key=lambda x: int(x["minute"]))
    signals = {str(x["kind"]) for x in ordered}
    required = {"residency_violation", "privileged_query", "classification_gap"}
    detected = required <= signals
    return {"detected": detected, "signals": sorted(signals),
            "first_event_minute": int(ordered[0]["minute"]),
            "detection_minute": max(int(x["minute"]) for x in ordered if str(x["kind"]) in required) if detected else None,
            "rule": "three-signal restricted-index exposure"}


def run_exercise() -> dict[str, object]:
    events = [
        {"minute": 0, "kind": "residency_violation", "region": "disallowed-region"},
        {"minute": 2, "kind": "privileged_query", "principal": "overbroad-service-role"},
        {"minute": 4, "kind": "classification_gap", "field": "document_classification"},
    ]
    alert = correlate(events)
    roles = sorted(REQUIRED_ROLES)
    raw = json.dumps(events, sort_keys=True).encode()
    evidence = EvidenceItem("restricted-index-events", raw)
    evidence.record("evidence_custodian", "acquired from immutable audit export", evidence.digest)
    evidence.record("forensic_analyst", "received verified working copy", evidence.digest)

    timeline = [
        {"minute": 4, "phase": "detect", "action": "SIEM correlation alert"},
        {"minute": 5, "phase": "activate", "action": "assign incident roles"},
        {"minute": 7, "phase": "preserve", "action": "hash and hold provider audit export"},
        {"minute": 10, "phase": "contain", "action": "deny affected role and stop replication"},
        {"minute": 18, "phase": "assess", "action": "privacy/legal determines scope and clocks"},
        {"minute": 24, "phase": "eradicate", "action": "replace broad role and enforce residency policy"},
        {"minute": 31, "phase": "recover", "action": "restore approved index and validate controls"},
        {"minute": 36, "phase": "monitor", "action": "prove denial and no new replica events"},
    ]
    containment_minutes = 10 - int(alert["first_event_minute"])
    vulnerability = {"id": "IAM-WILDCARD-001", "severity": "high",
                     "finding": "service role permitted unrestricted index query",
                     "remediation": "resource-scoped role plus residency condition",
                     "owner": "service_owner", "verified": True,
                     "verification": "denied cross-region query and allowed approved-region read"}
    communications = [
        {"audience":"responders", "approved_by":"incident_commander", "content":"confirmed indicators, containment, assignments"},
        {"audience":"executives", "approved_by":"incident_commander", "content":"confirmed impact, risk, decisions required"},
        {"audience":"provider", "approved_by":"provider_liaison", "content":"scoped preservation and audit-log request"},
        {"audience":"regulator", "approved_by":"privacy_legal", "content":"confirmed scope and mitigation; no speculative attribution"},
    ]
    legal_hold = {"active": True, "deletion_requested": True, "deletion_performed": False,
                  "decision": "preserve: legal hold overrides routine deletion"}
    recovery = {"known_good_configuration": True, "business_owner_approved": True,
                "security_owner_approved": True, "privacy_owner_approved": True,
                "recurrence_query_count": 0, "rto_minutes": 60, "actual_minutes": 31,
                "rpo_minutes": 15, "observed_data_loss_minutes": 0}
    phases = [str(x["phase"]) for x in timeline]
    passed = (alert["detected"] and set(roles) == REQUIRED_ROLES and evidence.verify()
              and containment_minutes <= 15 and phases == ["detect","activate","preserve","contain","assess","eradicate","recover","monitor"]
              and vulnerability["verified"] and not legal_hold["deletion_performed"]
              and all(x["approved_by"] for x in communications)
              and recovery["actual_minutes"] <= recovery["rto_minutes"]
              and recovery["observed_data_loss_minutes"] <= recovery["rpo_minutes"])
    return {"schema_version":1, "executed_at":datetime.now(timezone.utc).isoformat(),
            "scenario":"restricted index replicated to a prohibited region", "siem":alert,
            "roles":roles, "timeline":timeline, "metrics":{"mttd_minutes":4,
            "containment_minutes":containment_minutes}, "vulnerability":vulnerability,
            "forensics":{"evidence_id":evidence.evidence_id, "sha256":evidence.digest,
                          "custody_events":[x.__dict__ for x in evidence.custody],
                          "integrity_verified":evidence.verify()},
            "legal_hold":legal_hold, "communications":communications, "recovery":recovery,
            "limitations":["Synthetic local tabletop; no CSP control-plane or external SIEM was used.",
                           "Notification applicability and deadlines require jurisdiction-specific counsel."],
            "passed":passed}


if __name__ == "__main__":
    result = run_exercise(); output = Path("evidence/ccsp/incident-operations.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"wrote {output}; passed={result['passed']}")
    raise SystemExit(0 if result["passed"] else 1)
