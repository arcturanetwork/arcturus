# Program roadmap

## Learning loop

Every module uses the same loop:

1. **Learn:** read the relevant official objective and documentation.
2. **Build:** perform a small lab without following a click-by-click answer.
3. **Explain:** write a short architecture decision record (ADR) with tradeoffs.
4. **Break:** inject a failure, security issue, or bad assumption.
5. **Prove:** capture commands, diagrams, metrics, or test results.

Use a 60/25/15 time split: hands-on practice, primary-source reading, and recall/testing. Videos are orientation and reinforcement; they are not the source of truth.

## Three passes per certification

- **Pass A — coverage:** touch every blueprint objective and complete the small labs.
- **Pass B — integration:** extend TrustGraph and explain cross-domain tradeoffs.
- **Pass C — exam mode:** timed scenarios, closed-notes recall, error log, remediation.

Do not schedule an exam until the readiness scorecard is green twice at least seven days apart.

## Suggested calendar

The sequence is dependency-aware, not merely brand-aware. Agent design supplies the application; AWS supplies broad architecture; CKA supplies operations; NCP-GENL deepens model engineering; CCSP supplies governance; PMLE supplies an alternate production ML implementation.

AWS needs special handling in 2026:

- Until **2026-10-27**, study durable SAP-C02 architecture using its official guide while keeping a delta log.
- On or after **2026-10-27**, replace the provisional C03 section with task statements from the official SAP-C03 guide.
- SAP-C03 general availability is announced for **2026-11-17**. Do not infer detailed weights before AWS publishes them.

The two NVIDIA professional certification pages currently say **Coming soon**. Build the skills now, but verify registration status and study-guide revisions before purchasing or setting an exam date.

## Weekly rhythm

| Session | Work |
|---|---|
| 1 | Blueprint study + retrieval practice |
| 2 | Guided micro-lab |
| 3 | Independent scenario lab |
| 4 | Capstone increment + ADR |
| 5 | Timed quiz/task, error classification, remediation |

## Evidence standard

A completed lab contains: goal, constraints, diagram or command plan, execution evidence, failure test, security/cost considerations, teardown notes, and a 200-word explanation suitable for an interview. Never commit credentials, account IDs, private endpoints, proprietary exam questions, or customer data.

