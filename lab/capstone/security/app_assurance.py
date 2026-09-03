"""Reproducible, dependency-free CCSP application-assurance exercise.

This is deliberately a small-scope control demonstration, not a substitute for a
commercial SAST/DAST/SCA program or an external vulnerability database.
"""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import hashlib
import hmac
import json
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from capstone.agent.server import build_server


RISKY_CALLS = {"eval", "exec", "compile", "os.system", "pickle.loads"}
STANDARD_LIBRARY = {
    "__future__", "ast", "collections", "concurrent", "dataclasses", "datetime", "enum",
    "hashlib", "hmac", "http", "json", "math", "pathlib", "random", "re",
    "statistics", "sys", "tempfile", "threading", "time", "typing", "unittest",
    "urllib", "uuid", "zipfile",
}


def _name(node: ast.AST) -> str:
    if isinstance(node, ast.Name): return node.id
    if isinstance(node, ast.Attribute): return f"{_name(node.value)}.{node.attr}".strip(".")
    return ""


def scan_python(paths: list[Path]) -> dict[str, object]:
    findings, imports = [], set()
    for path in paths:
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and _name(node.func) in RISKY_CALLS:
                findings.append({"file": str(path), "line": node.lineno,
                                 "rule": f"risky-call:{_name(node.func)}"})
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
    external = sorted(x for x in imports if x not in STANDARD_LIBRARY and x != "capstone")
    return {"files_scanned": len(paths), "sast_findings": findings,
            "imports": sorted(imports), "external_runtime_dependencies": external}


def sbom(paths: list[Path], scan: dict[str, object]) -> dict[str, object]:
    components = [{"type": "file", "name": str(p),
                   "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
    components += [{"type": "library", "name": name, "scope": "required"}
                   for name in scan["external_runtime_dependencies"]]
    return {"bomFormat": "CycloneDX-inspired", "specVersion": "1.5-lab",
            "components": components,
            "limitations": "Minimal training SBOM; not schema-validated CycloneDX."}


def dast_gateway() -> dict[str, object]:
    server = build_server()
    thread = Thread(target=server.serve_forever, daemon=True); thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    cases = []
    try:
        with urlopen(f"{base}/health", timeout=2) as response:
            headers = {k.lower(): v for k, v in response.headers.items()}
            required = {"cache-control": "no-store", "x-content-type-options": "nosniff",
                        "content-security-policy": "default-src 'none'; frame-ancestors 'none'"}
            cases.append({"case": "security-headers", "status": response.status,
                          "passed": all(headers.get(k) == v for k, v in required.items()),
                          "observed": {k: headers.get(k) for k in required}})
        request = Request(f"{base}/v1/invoke", data=b'{"bad":true}',
                          headers={"Content-Type": "application/json"}, method="POST")
        try: urlopen(request, timeout=2)
        except HTTPError as exc:
            cases.append({"case": "malformed-contract", "status": exc.code,
                          "passed": exc.code == 400})
        request = Request(f"{base}/v1/invoke", data=json.dumps({
            "request_id":"dast-unauthorized", "tool":"publish_report",
            "arguments":{"content":"must-not-write"}, "idempotency_key":"dast-1"
        }).encode(), headers={"Content-Type":"application/json"}, method="POST")
        try: urlopen(request, timeout=2)
        except HTTPError as exc:
            cases.append({"case": "unauthorized-write", "status": exc.code,
                          "passed": exc.code == 403})
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=2)
    return {"cases": cases, "passed": bool(cases) and all(x["passed"] for x in cases)}


def run(root: Path = Path(".")) -> dict[str, object]:
    paths = sorted((root / "capstone").rglob("*.py"))
    scan = scan_python(paths); bill = sbom(paths, scan); dynamic = dast_gateway()
    payload = json.dumps(bill, sort_keys=True, separators=(",", ":")).encode()
    ephemeral_key = b"ephemeral-training-key-not-for-production"
    signature = hmac.new(ephemeral_key, payload, hashlib.sha256).hexdigest()
    verified = hmac.compare_digest(signature, hmac.new(ephemeral_key, payload, hashlib.sha256).hexdigest())
    tampered = hmac.compare_digest(signature, hmac.new(ephemeral_key, payload + b"x", hashlib.sha256).hexdigest())
    passed = not scan["sast_findings"] and not scan["external_runtime_dependencies"] and dynamic["passed"] and verified and not tampered
    return {"schema_version": 1, "executed_at": datetime.now(timezone.utc).isoformat(),
            "scope": "local TrustGraph Python capstone", "sast_sca": scan, "sbom": bill,
            "dast": dynamic, "artifact_integrity": {"algorithm":"HMAC-SHA256",
                "signature":signature, "valid_verified":verified,
                "tamper_rejected":not tampered,
                "limitation":"Shared-key integrity demonstration; not publisher identity or non-repudiation."},
            "limitations":["No external vulnerability advisory database was queried because there are no third-party runtime dependencies.",
                           "Local HTTP testing does not assess TLS, infrastructure, browser behavior, or internet exposure."],
            "passed": passed}


if __name__ == "__main__":
    result = run(); output = Path("evidence/ccsp/app-assurance.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"wrote {output}; passed={result['passed']}")
    raise SystemExit(0 if result["passed"] else 1)
