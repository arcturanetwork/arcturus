# Readiness scorecard

Score each item 0–3: 0 unknown, 1 explain with help, 2 independently solve, 3 independently solve under time and explain tradeoffs.

| Capability | Score | Evidence link | Last tested |
|---|---:|---|---|
| Agent architecture, tools and state |  |  |  |
| Agent evaluation, safety and operations |  |  |  |
| AWS organization/network/data architecture |  |  |  |
| AWS resilience, migration and cost |  |  |  |
| Kubernetes cluster lifecycle and RBAC |  |  |  |
| Kubernetes workload/network/storage troubleshooting |  |  |  |
| LLM data, RAG and fine-tuning |  |  |  |
| LLM optimization, deployment and monitoring |  |  |  |
| Cloud data/application/infrastructure security |  |  |  |
| Cloud operations, legal, risk and compliance |  |  |  |
| Google Cloud ML data/training/serving |  |  |  |
| Google Cloud pipelines/monitoring/governance |  |  |  |

## Exam gate

A track is green only when:

- every row relevant to the track scores at least 2;
- weighted practice performance is at least 85% twice, seven days apart;
- the candidate completes its performance/scenario task within time;
- all lab claims link to evidence;
- the error log shows no recurring category across the last two attempts;
- the official blueprint/version was rechecked in the prior 72 hours.

## Error log template

| Date | Track/objective | Error class | Why the chosen answer/action failed | Correct rule | Remediation lab | Retest |
|---|---|---|---|---|---|---|
| | | Knowledge / scope / sequencing / governance / reading / command speed | | | | |

## Diagnostic scenario bank

The [24 original scenarios](bank/README.md) provide initial cross-track retrieval practice with objective tags and explanations. They are too small to prove readiness and must not be treated as live-exam replicas.

Run `python3 -m assessments.evidence_audit` to regenerate a conservative inventory of unresolved evidence from all six mastery maps. A green unit-test suite validates implemented artifacts; it does not override pending live-cloud, cluster, GPU, model, or timed-assessment requirements.

The shared [`scenario_exam` engine](scenario_exam.py) loads all six original lab banks, creates deterministic domain-spanning draws, enforces complete 0–2 rubric scoring, records evidence links and timing, and evaluates the two-passes/seven-days/error-recurrence gate. Its readiness result covers scenario performance only; official-version recency and hands-on platform evidence remain independent gates.

Run `python3 -m assessments.blueprint_audit` after rechecking the official sources. The generated report rejects stale source checks and keeps prelaunch/provisional targets from being labeled booking-ready. The command is a local registry audit, not a network freshness check.

Run `python3 -m assessments.objective_coverage` whenever a blueprint map changes. It expands every numbered range, reconciles declared totals, and verifies that the mastery map contains each declared range. CKA uses named competency groups rather than numbered objectives and is validated against its 24-task performance bank separately.

Run `python3 -m assessments.campaign_audit` for the authoritative combined gate. A track passes only if its blueprint is current and published, objective coverage is consistent, qualifying scenario attempts exist, and every required platform-evidence item is marked verified with existing proof files. Populate [platform-evidence.json](platform-evidence.json) only from actual runs; never promote design documents or synthetic scores to runtime proof.
