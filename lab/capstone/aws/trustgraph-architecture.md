# TrustGraph AWS architecture dossier

This is a design lab, not evidence of deployment in an AWS account. Every choice is conditional on stated requirements.

## Requirements

- Regulated documents; no public workload endpoints except the edge/API entry.
- Write operations require human approval and immutable audit evidence.
- Availability SLO 99.9%; ingestion RPO 15 minutes/RTO 4 hours; interactive query RTO 1 hour.
- Regional data residency; secondary Region only where legally permitted.
- Small baseline load with 20× bursts; avoid idle GPU expense.

## Organization and identity

Use Organizations with Security, Infrastructure, Workloads and Sandbox OUs. Separate Log Archive, Security Tooling, Network, Shared Services, Production, Staging and Development accounts. IAM Identity Center federates workforce identities; workloads assume narrow roles. SCPs deny disabling audit/configuration, leaving approved Regions, and unapproved public exposure. SCPs are guardrails, not grants. Emergency roles are isolated, monitored and regularly tested.

CloudTrail organization trails and configuration/security findings aggregate into protected central accounts. KMS keys are separated by data class and environment; policies permit service/workload use without giving administrators plaintext data access. Secrets Manager holds rotating service secrets; temporary role credentials replace static access keys.

## Network

Transit Gateway provides transitive hub routing across VPCs and approved hybrid links; route tables segment production, non-production, inspection and shared services. Direct Connect is the steady private hybrid path; VPN is a diverse backup, not assumed to share the same failure domain. Route 53 Resolver endpoints and rules integrate DNS deliberately.

Gateway endpoints serve S3/DynamoDB where applicable; interface endpoints/PrivateLink keep supported service traffic private. Security groups express stateful workload intent; network ACLs provide coarse stateless subnet controls. VPC Flow Logs, Transit Gateway Flow Logs, Reachability Analyzer and Network Access Analyzer support diagnosis and validation.

Rejected default: full-mesh VPC peering, because route management grows quadratically and peering is non-transitive.

## Application and data path

CloudFront and WAF protect the public API entry. Requests reach an API/load-balancing tier; durable work enters SQS with idempotency keys and a DLQ. Step Functions coordinates explicit workflows and approval callbacks. Stateless services run on ECS/Fargate initially; EKS is justified only if Kubernetes portability/control outweighs its operational cost. GPU inference scales from zero or a small warm floor according to latency needs.

S3 stores versioned source objects with retention controls where required. DynamoDB fits idempotency/workflow state; Aurora fits relational transactions; OpenSearch fits search, not authoritative system-of-record duties. ElastiCache is disposable acceleration. Selection follows access patterns, consistency, recovery and operational requirements—not brand preference.

## Resilience and recovery

| Component | AZ design | Regional recovery | Test |
|---|---|---|---|
| API/workers | Multi-AZ, autoscaled, stateless | IaC redeploy or warm standby | AZ evacuation and dependency failure |
| Queue/workflow | Managed multi-AZ | Replay from durable source/event strategy | poison message and backlog |
| S3 evidence | Versioning and retention | CRR only where residency permits | object/version restoration |
| Relational data | Aurora/RDS Multi-AZ | Cross-Region replica/snapshot per RPO | promotion plus application verification |
| Audit trail | Central protected destination | independent protected copy | denied deletion and evidence retrieval |

DNS failover is not instantaneous consistency. Recovery procedures include dependency order, data reconciliation, secret/key availability, quota readiness and business validation. Backups count only after restore tests.

## Delivery, operations and security

CloudFormation/CDK-style IaC passes lint, policy, image/dependency and security checks. A multi-account pipeline assumes deployment roles; production uses approval plus canary or blue/green rollout and automatic rollback on SLO signals. Systems Manager handles fleet inventory/patching where hosts remain.

Metrics cover availability, p50/p95/p99 latency, errors, saturation, queue age/depth, throttles, retrieval quality and agent unsafe-action rate. Logs are structured and correlated by request ID without leaking source text. Config, Security Hub, GuardDuty, Inspector and Access Analyzer feed owned response paths; service names alone are not a security strategy.

## Cost controls

Required tags include owner, product, environment, data class and cost center; tag policies and enforcement apply where supported. Budgets, anomaly detection, CUR analysis and Compute Optimizer findings feed a monthly review. Savings Plans cover stable compute only after measurement; Spot is limited to interruption-tolerant workers; S3 lifecycle follows access/retention needs. Model NAT, inter-AZ, cross-Region and internet transfer explicitly.

## Migration example

Portfolio scoring uses business criticality, dependencies, data gravity, compliance, technical fit and change tolerance. Retire unused services first; retain regulated legacy components when risk dominates; rehost only for schedule-driven moves; replatform databases where compatibility is proven; refactor high-change components into queue-backed services. Use Application Discovery/Migration Hub for inventory, MGN for suitable server moves, DMS/SCT for database paths, DataSync/Transfer/Snow choices by bandwidth, duration and online/offline constraints. Every wave has rollback criteria and reconciliation.

