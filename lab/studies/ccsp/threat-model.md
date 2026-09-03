# TrustGraph STRIDE threat model

Trust boundaries: browser→edge/API, API→agent orchestrator, agent→tools, ingestion→index, workload→cloud control plane, primary→recovery Region, and customer→CSP/support personnel.

| STRIDE class | Concrete threat | Control | Verification |
|---|---|---|---|
| Spoofing | Stolen user/service identity invokes a tool | Federation/MFA, short-lived workload identity, audience-bound tokens | Denied invalid/expired/wrong-audience requests |
| Tampering | Corpus passage or model artifact is changed | Hash/signature, immutable versions, protected pipeline and provenance | Alter artifact and verify admission/deploy failure |
| Repudiation | Operator denies approving a write | Authenticated approval, request/action IDs, protected timestamped audit | Reconstruct actor, intent, input hash and outcome |
| Information disclosure | Cross-tenant retrieval or sensitive logs | Authorization before retrieval, data classification, minimization/redaction | Negative ACL tests and log sample inspection |
| Denial of service | Runaway agent/tool calls exhaust compute | Step/token/time budgets, quotas, rate limits, queues, circuit breakers | Load and dependency-failure tests |
| Elevation of privilege | Retrieved instruction grants write access | Separate data/control channels; allowlist; policy enforcement outside model | Adversarial prompt-injection suite |

STRIDE finds threat categories; it does not quantify business risk. The risk register separately assigns owner, likelihood, impact, treatment and residual risk.

