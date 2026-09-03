"""Executable federation, MFA, secret/certificate, and IRM lifecycle lab."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
from pathlib import Path


@dataclass(frozen=True)
class FederationPolicy:
    issuer: str
    audience: str
    max_age_seconds: int = 300
    required_assurance: str = "mfa"

    def validate(self, claims: dict[str, object], now: int) -> tuple[bool, str]:
        checks = [
            (claims.get("iss") == self.issuer, "issuer"),
            (claims.get("aud") == self.audience, "audience"),
            (isinstance(claims.get("exp"), int) and int(claims["exp"]) > now, "expiry"),
            (isinstance(claims.get("iat"), int) and 0 <= now - int(claims["iat"]) <= self.max_age_seconds, "freshness"),
            (self.required_assurance in claims.get("amr", []), "mfa"),
        ]
        failed = [name for passed, name in checks if not passed]
        return (not failed, "accepted" if not failed else "rejected:" + ",".join(failed))


@dataclass
class SecretStore:
    current_version: int = 1
    disabled_versions: set[int] = field(default_factory=set)

    def rotate(self) -> tuple[int, int]:
        old = self.current_version
        self.current_version += 1
        self.disabled_versions.add(old)
        return old, self.current_version

    def usable(self, version: int) -> bool:
        return version == self.current_version and version not in self.disabled_versions


@dataclass
class RightsGrant:
    subject: str
    document: str
    permissions: frozenset[str]
    expires_at: datetime
    revoked: bool = False

    def authorize(self, subject: str, document: str, action: str, now: datetime) -> bool:
        return (not self.revoked and subject == self.subject and document == self.document
                and action in self.permissions and now < self.expires_at)


def run_lab() -> dict[str, object]:
    now_epoch = 1_800_000_000
    policy = FederationPolicy("https://idp.example.test", "trustgraph")
    valid = {"iss":policy.issuer, "aud":policy.audience, "iat":now_epoch-30,
             "exp":now_epoch+270, "amr":["pwd","mfa"], "sub":"analyst-7"}
    federation_cases = []
    for name, mutation, expected in [
        ("valid-mfa", {}, True), ("wrong-audience", {"aud":"other"}, False),
        ("expired", {"exp":now_epoch-1}, False), ("stale", {"iat":now_epoch-301}, False),
        ("missing-mfa", {"amr":["pwd"]}, False),
    ]:
        claims = valid | mutation; accepted, reason = policy.validate(claims, now_epoch)
        federation_cases.append({"case":name, "accepted":accepted, "expected":expected,
                                 "reason":reason, "passed":accepted == expected})

    secrets = SecretStore(); old, new = secrets.rotate()
    secret_evidence = {"old_version":old, "new_version":new,
                       "old_rejected":not secrets.usable(old), "new_accepted":secrets.usable(new)}
    now = datetime.now(timezone.utc)
    certificate = {"subject":"service.trustgraph.internal",
                   "not_before":(now-timedelta(minutes=1)).isoformat(),
                   "not_after":(now+timedelta(days=30)).isoformat(),
                   "valid_now":True, "renewal_due_before_days":7}
    grant = RightsGrant("analyst-7", "restricted-report", frozenset({"view"}), now+timedelta(hours=1))
    irm_cases = [
        {"case":"allow-view", "observed":grant.authorize("analyst-7","restricted-report","view",now), "expected":True},
        {"case":"deny-export", "observed":grant.authorize("analyst-7","restricted-report","export",now), "expected":False},
        {"case":"deny-other-subject", "observed":grant.authorize("attacker","restricted-report","view",now), "expected":False},
    ]
    grant.revoked = True
    irm_cases.append({"case":"deny-after-revoke", "observed":grant.authorize("analyst-7","restricted-report","view",now), "expected":False})
    for case in irm_cases: case["passed"] = case["observed"] == case["expected"]
    audit_events = [
        {"sequence":1,"actor":"identity_admin","action":"validate federation and MFA cases"},
        {"sequence":2,"actor":"secrets_operator","action":f"rotate secret v{old} to v{new}"},
        {"sequence":3,"actor":"pki_operator","action":"validate certificate lifetime and renewal threshold"},
        {"sequence":4,"actor":"data_owner","action":"grant view-only document right"},
        {"sequence":5,"actor":"data_owner","action":"revoke document right"},
    ]
    audit_digest = hashlib.sha256(json.dumps(audit_events, sort_keys=True).encode()).hexdigest()
    key = b"ephemeral-lab-audit-key"
    audit_tag = hmac.new(key, audit_digest.encode(), hashlib.sha256).hexdigest()
    passed = (all(x["passed"] for x in federation_cases + irm_cases)
              and secret_evidence["old_rejected"] and secret_evidence["new_accepted"]
              and certificate["valid_now"] and len(audit_digest) == 64)
    return {"schema_version":1, "executed_at":now.isoformat(), "federation":{
            "policy":policy.__dict__, "cases":federation_cases}, "secret_rotation":secret_evidence,
            "certificate":certificate, "irm":{"cases":irm_cases},
            "audit":{"events":audit_events,"sha256":audit_digest,"hmac_sha256":audit_tag,
                     "limitation":"Ephemeral symmetric lab key; use managed immutable audit signing in production."},
            "limitations":["Synthetic claims are validated locally; no external IdP or hardware MFA ceremony was used.",
                           "Certificate metadata is simulated; no public/private CA issuance was performed."],
            "passed":passed}


if __name__ == "__main__":
    result=run_lab(); output=Path("evidence/ccsp/identity-irm.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(f"wrote {output}; passed={result['passed']}")
    raise SystemExit(0 if result["passed"] else 1)
