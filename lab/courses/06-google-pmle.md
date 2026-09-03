# Track 6 — Google Cloud Professional Machine Learning Engineer

**Target:** current PMLE guide checked 2026-09-03. The current guide uses Gemini Enterprise Agent Platform terminology and supersedes the older weights originally recorded here. Coding is not directly assessed, but Python/SQL interpretation is expected.

Track evidence: [current objective map](../studies/google-pmle/objective-map.md), [18 timed scenarios](../studies/google-pmle/scenario-labs.json), and [provider-neutral pipeline lab](../capstone/ml/pipeline.py). These prove decision reasoning and pipeline mechanics, not Google Cloud product operation.

## Blueprint map

| Section | Weight | Course outcome |
|---|---:|---|
| Automating/orchestrating ML pipelines | 18% | Reproducible pipelines, retraining, CI/CD, metadata and lineage |
| Serving and scaling models | 20% | Batch/online inference, registry, endpoints, tests and tuning |
| Scaling prototypes into ML models | 21% | Architecture, training, tuning, hardware and distributed choices |
| Team data/model collaboration | 16% | Data processing, notebooks, experiments, privacy and governance |
| Monitoring ML solutions | 13% | Readiness, fairness, drift/skew, explainability and troubleshooting |
| Architecting low-code AI solutions | 13% | BigQuery ML, APIs, Model Garden, RAG/Agent Builder and AutoML |

The published rounded percentages total 101%; use them as approximate emphasis, exactly as Google labels them.

## Eight-week sprint

1. Translate business outcomes into ML framing, baselines, metrics, data and responsible-AI constraints.
2. BigQuery ML, AutoML, pretrained APIs, Model Garden and RAG/Agent Builder decisions.
3. Storage, BigQuery/Dataflow, features, Workbench, privacy and preprocessing consistency.
4. Custom training, tuning, framework/hardware selection and distributed failures.
5. Registry, batch/online endpoints, scaling, private access, A/B and shadow tests.
6. Vertex AI Pipelines/Kubeflow, triggers, metadata, lineage, CI/CD and retraining policy.
7. Monitoring skew/drift/performance/fairness, explainability, alerts and response playbooks.
8. End-to-end scenario reviews with cost, reliability, governance and team boundaries.

## Required labs

- Build one BigQuery ML baseline and one Vertex AI custom/AutoML candidate; compare operational burden as well as metrics.
- Create a parameterized pipeline with validation, training, evaluation, approval and conditional deployment.
- Simulate skew or drift; trigger an alert and execute rollback/retraining logic.
- Implement a grounded TrustGraph assistant and evaluate retrieval, answer quality, safety and latency.

## Exit gate

Deliver a reproducible pipeline plus model card, lineage evidence, cost estimate, monitoring dashboard design and rollback playbook. For unseen scenarios, justify managed versus custom services and batch versus online inference.

Primary links: [certification page](https://cloud.google.com/learn/certification/machine-learning-engineer), [official exam guide](https://cloud.google.com/learn/certification/guides/machine-learning-engineer), [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs), [Google Cloud Tech videos](https://www.youtube.com/@googlecloudtech).
