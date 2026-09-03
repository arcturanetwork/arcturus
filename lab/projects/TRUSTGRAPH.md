# Shared capstone — Arcturus

Build a small evidence-aware research system that ingests approved documents, retrieves passages with provenance, lets agents propose bounded actions, and records human approvals and operational evidence.

## Architecture increments

1. **Agentic AI:** orchestrator, researcher and verifier roles; typed tool contracts; termination/budget rules; human approval for writes.
2. **AWS:** multi-account production architecture, private networking, durable ingestion, immutable audit trail, DR and cost model.
3. **CKA:** deploy services to a disposable cluster with storage, policy, probes, resources, ingress/Gateway API and troubleshooting runbooks.
4. **LLM engineering:** baseline vs RAG vs adaptation experiment, GPU/inference plan, evaluation suite and model/data cards.
5. **CCSP:** data lifecycle, threat model, control matrix, provider assessment, incident tabletop and legal/compliance assumptions.
6. **Google PMLE:** alternate Vertex AI pipeline, governed artifacts, deployment strategy, monitoring and retraining policy.

## Minimum repository artifacts

```text
capstone/
  README.md
  architecture/
    context.md
    decisions/
    threat-model.md
  evals/
    dataset-card.md
    rubric.md
    results.md
  operations/
    slos.md
    runbooks/
    incident-review.md
  governance/
    data-lifecycle.md
    control-matrix.md
    model-card.md
```

## Acceptance criteria

- Every answer exposes document identity and passage provenance.
- Retrieved content is untrusted data, never executable instruction.
- Authorization is enforced at retrieval and action time.
- Side effects require explicit scope, idempotency, audit logging and appropriate human approval.
- Evaluation includes representative, edge, adversarial and regression cases.
- Architecture documents RTO/RPO, SLOs, failure modes, cost drivers and rollback.
- Logs and screenshots contain no secrets or sensitive source content.

