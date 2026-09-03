# Track 2 — AWS Certified Solutions Architect – Professional

**Target:** SAP-C03, announced for 2026-11-17. Its detailed guide was not yet published when this course was checked on 2026-09-03. The stable core below maps SAP-C02; the final module is a controlled C03 delta.

Track evidence: [task-level objective map](../studies/aws-sap/objective-map.md), [TrustGraph architecture dossier](../capstone/aws/trustgraph-architecture.md), and [machine-checked design manifest](../capstone/aws/architecture-manifest.json). Design evidence is not represented as hands-on AWS deployment.

## Stable SAP-C02 map

| Domain | C02 weight | Course outcome |
|---|---:|---|
| Organizational complexity | 26% | Multi-account, identity, network, governance, and hybrid designs |
| New solutions | 29% | Reliable, secure, performant, cost-aware architectures |
| Continuous improvement | 25% | Operational excellence, resilience, security, and cost remediation |
| Migration and modernization | 20% | Portfolio discovery, migration patterns, data transfer, modernization |

## Ten-week sprint

1. Requirements, tradeoffs, AWS Well-Architected reasoning, RTO/RPO and ADRs.
2. Organizations, Control Tower concepts, SCPs, IAM federation, resource sharing.
3. Multi-account networking, Transit Gateway, private connectivity, DNS and hybrid routing.
4. Data architecture: relational, NoSQL, object, cache, analytics, replication and consistency.
5. Compute and integration: EC2, containers, serverless, queues, events and workflow patterns.
6. Resilience: multi-AZ/Region, backup, pilot light/warm standby/active-active, chaos cases.
7. Security and observability: KMS, secrets, detective controls, centralized logs, incident paths.
8. Cost/performance: pricing models, rightsizing, caching, data transfer and sustainability.
9. Migration/modernization: 7 Rs, Application Migration Service, databases and data movement.
10. C03 delta: agentic architectures, AI/ML integration, post-quantum concepts, DevSecOps, modern resilience, security and compliance—replace with exact tasks when AWS publishes the guide.

## Scenario labs

- Design a regulated, multi-account landing zone; include break-glass access and log immutability.
- Produce three DR designs for TrustGraph and calculate qualitative cost/RTO/RPO tradeoffs.
- Diagnose a transitive-routing failure and an unexpected cross-AZ/data-transfer bill.
- Design asynchronous ingestion with deduplication, backpressure, DLQs, replay and observability.
- Create a migration wave plan that separates rehost, replatform and refactor decisions.

## Exit gate

For three unseen architecture briefs, produce a diagram and ADR in 45 minutes each. Every answer must cover security, reliability, performance, cost, operations, migration constraints, and rejected alternatives—not simply name services.

Primary links: [AWS certification page](https://aws.amazon.com/certification/certified-solutions-architect-professional/), [official exam guides](https://docs.aws.amazon.com/aws-certification/latest/examguides/aws-certification-exam-guides.html), [SAP-C03 announcement](https://aws.amazon.com/blogs/training-and-certification/september-2026-new-offerings/), [AWS Architecture Center](https://aws.amazon.com/architecture/), [AWS Events videos](https://www.youtube.com/@AWSEventsChannel).
