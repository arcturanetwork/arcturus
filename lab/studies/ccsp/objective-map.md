# CCSP 2026 objective mastery map

Source: official ISC2 outline effective 2026-08-01, retrieved 2026-09-03. The outline contains 38 numbered subdomains across six domains. `Designed/tested` means capstone controls were exercised locally; it does not claim professional-experience eligibility.

## Domain 1 — Concepts, architecture and design (17%)

| Objectives | Coverage | Evidence/status |
|---|---|---|
| 1.1 concepts/roles/characteristics/building blocks | Service/deployment models, elasticity, pooling, tenancy, measured service, roles | studied |
| 1.2 reference architecture/shared considerations/emerging tech | Portability, reversibility, SLA, audit, privacy, AI/containers/edge/confidential computing | architecture dossier; designed |
| 1.3 cloud security concepts | Crypto/IAM/sanitization/network/virtualization/threats/hardening | Kubernetes and AWS controls; partial tested |
| 1.4 secure design | Data lifecycle, BIA/BCDR, requirements, patterns, DevSecOps | lifecycle engine and recovery architecture; tested concept |
| 1.5 provider evaluation | Criteria, Common Criteria, FIPS 140-2 | scoped assurance/product-validation checklist designed; real report review pending |
| 1.6 AI/ML | Threat detection, source verification, SOAR, ethics, regulation | provenance/evaluation and incident controls; partial tested |

## Domain 2 — Cloud data security (20%)

| Objectives | Coverage | Evidence/status |
|---|---|---|
| 2.1 lifecycle/dispersion/flows | Create, store, use, share, archive, destroy with locations/flows | data asset/policy model; tested concept |
| 2.2 storage architectures/threats | Ephemeral/object/volume/archive and remanence/access risks | studied |
| 2.3 protection technologies | Encryption, hashing, masking/anonymization, tokenization, DLP, secrets/certs | control matrix; designed |
| 2.4 discovery | Structured/semi/unstructured data and location | ingestion metadata controls; partial tested |
| 2.5 classification | Policy, mapping, labeling/tagging | four-level classification enum; tested concept |
| 2.6 IRM | Rights, provisioning/access, certificate issuance/revocation | studied; platform lab required |
| 2.7 retention/deletion/archive/legal hold | Expiry and hold precedence, cryptographic erase | lifecycle tests; tested concept |
| 2.8 auditability/traceability/accountability | Actor/network/location attributes, logging, custody/non-repudiation | agent trace and evidence controls; partial tested |
| 2.9 AI/ML data | Dataset/model privacy, integrity and validation | AI-01 control and dataset provenance tests; partial tested |

## Domain 3 — Platform and infrastructure security (17%)

| Objectives | Coverage | Evidence/status |
|---|---|---|
| 3.1 components | Physical, network, compute, virtualization, storage, management plane | studied |
| 3.2 secure data center | Tenant/access, location, environmental and connectivity resilience | provider-responsibility mapping; studied |
| 3.3 risk analysis | Identify/analyze threats/vulnerabilities; avoid/mitigate/transfer/share/accept | STRIDE plus owned qualitative risk register; tested structure |
| 3.4 controls | Physical, system/storage/comms, IAM and audit mechanisms | AWS/Kubernetes designs; partial tested |
| 3.5 BCDR | Requirements, RTO/RPO, create/implement/test | numeric objectives and restore protocol; designed |

## Domain 4 — Application security (16%)

| Objectives | Coverage | Evidence/status |
|---|---|---|
| 4.1 awareness | Development pitfalls; OWASP Top 10/API/LLM, ASVS, SANS 25 | prompt-injection and policy tests; partial |
| 4.2 SDLC | Business requirements and lifecycle/methodologies | studied |
| 4.3 apply secure SDLC | Cloud risks, STRIDE/DREAD/ATASM/PASTA, secure code/configuration | Trust-boundary STRIDE and code/config tests; partial tested |
| 4.4 assurance/validation | Functional/nonfunctional, SCA/IAST/SAST/DAST, QA, abuse cases | unit/adversarial tests; tool-specific scans pending |
| 4.5 verified software | APIs, supply chain, third party, licensing/integrity | dependency-free labs; formal SBOM/signing pending |
| 4.6 architecture | WAF/API gateway/load balancer/DAM, crypto, sandbox, containers/Kubernetes | AWS/Kubernetes designs; partial tested |
| 4.7 IAM | Federation/IdP/SSO/MFA/CASB/secrets/keys/certs | designed; identity-platform lab required |

## Domain 5 — Security operations (17%)

| Objectives | Coverage | Evidence/status |
|---|---|---|
| 5.1 build infrastructure | HSM/TPM, secure defaults, management plane, virtualization | studied; platform evidence required |
| 5.2 operate infrastructure | Access/network controls, hardening/patching, HA, capacity, backup, management plane | architecture/runbook; partial designed |
| 5.3 operational standards | Change, continuity, security, service improvement, incident/problem/release/config/SLA/capacity | control owners and evidence; designed |
| 5.4 forensics | Collection, acquisition, preservation and evidence management | custody procedure plus hash/transfer lab; tested concept |
| 5.5 communications | Vendors, customers, partners, regulators, stakeholders | audience/authority communications procedure; designed |
| 5.6 security operations | SOC, intelligent controls, SIEM/threat intel, IR, vulnerability and penetration testing | incident control; live exercises pending |

## Domain 6 — Legal, risk and compliance (13%)

| Objectives | Coverage | Evidence/status |
|---|---|---|
| 6.1 legal/cloud risks | Conflicting law, frameworks, eDiscovery and forensic standards | studied; counsel-dependent decisions identified |
| 6.2 privacy | Contractual/regulatory data, jurisdiction, ISO 27018/GAPP/GDPR, PIA | data map/control/residual-risk PIA plus residency test; designed |
| 6.3 audit | Internal/external controls, reports/scope, gaps/planning/ISMS, regulated sectors, distributed IT | control matrix and scoped assurance checklist; real report lab pending |
| 6.4 enterprise risk | Provider program, data roles, transparency, treatment/frameworks/metrics/environment | named risk owners/treatments/residual scores and responsibility model; tested structure |
| 6.5 contracts/outsourcing | SLA/MSA/SOW, viability/lock-in/escrow, audit/termination/ownership/insurance, supply chain | clause checklist and timed technical exit test; designed |

## Timed scenario practice

Use the [18 original scenarios](scenario-labs.json) and [CCSP rubric](scenario-rubric.md). Three cases per domain test governance priority, responsibility, sequence, audit evidence, and common distractors. These exercises do not establish ISC2 experience eligibility or substitute for real provider and operational evidence.
