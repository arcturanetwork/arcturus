# AWS Solutions Architect Professional objective map

Authoritative baseline: AWS SAP-C02 Exam Guide retrieved 2026-09-03. Target exam: SAP-C03, whose full guide is scheduled for 2026-10-27. Status vocabulary: `studied`, `designed`, `tested`, `cloud-lab-required`.

Each of the 20 C02 tasks now has an original timed [architecture lab](task-labs.json) and a [14-point rubric](task-lab-rubric.md). Completion requires written responses and review; the presence of the lab bank is not a passing score.

## Domain 1 — Organizational complexity (26% in C02)

| Task | Required competence | Evidence | Status |
|---|---|---|---|
| 1.1 Network connectivity | Multi-VPC/hybrid options, DNS, segmentation, Regions/AZs, traffic diagnosis, endpoints | TrustGraph hub-and-spoke network decision and failure cases | designed |
| 1.2 Security controls | Cross-account identity, federation, encryption, centralized audit/security events | Identity, key, log-archive and delegated-security design | designed |
| 1.3 Reliability/resilience | RTO/RPO, DR choice, backup/restore, automatic recovery, scale | Tiered workload DR table and restore-test protocol | designed |
| 1.4 Multi-account environment | Organizations/Control Tower, resource sharing, notification, governance | OU/account model, SCP boundaries and centralized services | designed |
| 1.5 Cost visibility | Cost tools, purchasing, rightsizing, tagging | Mandatory cost-allocation tags, budgets and anomaly response | designed |

## Domain 2 — New solutions (29% in C02)

| Task | Required competence | Evidence | Status |
|---|---|---|---|
| 2.1 Deployment | IaC, CI/CD, change/configuration, rollback, managed services | Immutable deployment and rollback ADR | designed |
| 2.2 Business continuity | Global infrastructure, routing, RTO/RPO, DR, replication/testing | Failure matrix and quarterly recovery test | designed |
| 2.3 Security | Least privilege, flows, attack mitigation, encryption, endpoints, patching | Layered controls and private service access | designed |
| 2.4 Reliability | Multi-AZ/Region, scaling, decoupling, quotas, DNS routing | SQS buffering, idempotency, quota and failover plan | designed |
| 2.5 Performance | Metrics, compute/storage/database selection, cache/buffer/replica, rightsizing | Workload-specific selection table and SLOs | designed |
| 2.6 Cost | Monitoring, purchase models, storage tiering, transfer, expenditure controls | Cost-driver model and guardrails | designed |

## Domain 3 — Continuous improvement (25% in C02)

| Task | Required competence | Evidence | Status |
|---|---|---|---|
| 3.1 Operations | Monitoring/logging, deployment, configuration, automation, failure exercises | Central telemetry, alarms, runbooks and game days | designed |
| 3.2 Security | Retention/sensitivity, secrets, Config, least privilege, patch/backup/remediation | Data classes, secrets rotation, conformance and response | designed |
| 3.3 Performance | Metrics/KPIs, bottlenecks, global delivery, scale/rightsize | SLO-derived dashboard and load-test plan | designed |
| 3.4 Reliability | Replication, scaling, HA/DR, quotas, single-point remediation | Dependency/failure matrix | designed |
| 3.5 Cost | Utilization, unused resources, CUR, alarms and allocation tags | FinOps review loop | designed |

## Domain 4 — Migration and modernization (20% in C02)

| Task | Required competence | Evidence | Status |
|---|---|---|---|
| 4.1 Select workloads | Portfolio discovery, wave planning, 7 Rs, TCO | Example portfolio and wave criteria | designed |
| 4.2 Migration approach | Data/app/database transfer, network/DNS, identity, governance, security | Transfer decision table and cutover controls | designed |
| 4.3 New architecture | Compute/container/storage/database selection | Target-state mapping for three workload shapes | designed |
| 4.4 Modernization | Decoupling, serverless, containers, purpose-built data, integration | Event-driven TrustGraph target design | designed |

## Emerging AI controls present in the current C02 guide

The retrieved guide explicitly mentions Bedrock Guardrails for content/compliance, AgentCore Identity for agent access, and Step Functions for human approval. These are emerging/pretest topics in C02, not a substitute for the unpublished C03 tasks.

## C03 delta register

AWS announced five domains but no weights yet: cloud-native architecture; security/compliance/governance; cost optimization; resilience/migration/business continuity; operational excellence/automation. Announced additions include serverless data pipelines, durable Step Functions workflows, VPC Lattice/ECS Service Connect, image security, multi-tenancy, real-time data, pipeline scanning, multi-account pipelines, container and AI/ML monitoring, synthetic/RUM, Lake Formation/Iceberg, Clean Rooms, and KMS use of ML-DSA/ML-KEM.

Do not mark this track exam-ready until the published C03 tasks are diffed line by line.
