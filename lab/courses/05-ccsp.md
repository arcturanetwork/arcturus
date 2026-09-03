# Track 5 — ISC2 Certified Cloud Security Professional

**Target:** CCSP outline effective 2026-08-01. The current computer-adaptive exam is 100–150 items in three hours; passing score is 700/1000.

Track evidence: [all 38 numbered subdomains](../studies/ccsp/objective-map.md), [18 timed scenarios](../studies/ccsp/scenario-labs.json), [executable data-governance rules](../capstone/security/governance.py), [control matrix](../capstone/security/control-matrix.json), [application-assurance runner](../capstone/security/app_assurance.py), [identity/IRM runner](../capstone/security/identity_irm.py), [incident-operations runner](../capstone/security/incident_operations.py), and [incident tabletop](../studies/ccsp/incident-tabletop.md). The application exercise produces runtime SAST/SCA inventory, SBOM hashes, live DAST denial tests, and tamper-verification evidence. Identity tests cover issuer/audience/freshness/MFA enforcement, secret rotation, certificate lifetime, rights binding, expiry, and revocation. The operations exercise correlates three SIEM signals and verifies role activation, custody, containment, vulnerability remediation, legal hold, audience-approved communications, RTO/RPO, and recurrence monitoring. Each records its simulation limits. This does not establish ISC2 professional-experience eligibility.

## Blueprint map

| Domain | Weight | Course outcome |
|---|---:|---|
| Cloud data security | 20% | Lifecycle, classification, encryption, DLP, retention and auditability |
| Concepts, architecture and design | 17% | Reference models, shared responsibility, design principles and provider evaluation |
| Platform and infrastructure security | 17% | Components, risk, controls, resilience and DR |
| Security operations | 17% | Harden, monitor, respond, maintain and manage change |
| Application security | 16% | Secure SDLC, testing, supply chain, APIs, containers and IAM |
| Legal, risk and compliance | 13% | Privacy, contracts, jurisdiction, audit, eDiscovery and risk frameworks |

## Eight-week sprint

1. Cloud models, roles, architecture, shared responsibility and provider assurance.
2. Data lifecycle, discovery/classification, key management, privacy and retention.
3. Infrastructure threat modeling, IAM, network isolation, virtualization and resilience.
4. Secure SDLC, APIs, supply chain, testing, threat modeling and CI/CD controls.
5. Operations: baselines, logging, vulnerability/change/incident management and forensics.
6. Legal, privacy, contracts, audit, jurisdiction, risk and compliance mappings.
7. AI/cloud overlay from the 2026 outline: dataset/model privacy and security, validation, threat detection, SOAR, ethics and regulation.
8. Scenario review: select the best governance/process answer before the most technically clever one.

## Required labs

- Create a cloud data flow and lifecycle map with owners, residency, retention and deletion proof.
- Threat-model TrustGraph using STRIDE; map preventive, detective and corrective controls.
- Draft CSP due-diligence questions, shared-responsibility matrix, SLA clauses and exit plan.
- Run an incident tabletop involving exposed model data, cross-border processing and incomplete logs.

## Experience caveat and exit gate

ISC2 requires five years of cumulative IT experience, including three in cybersecurity and one in a CCSP domain; permitted waivers/substitutions are limited. A passing candidate without the experience may become an Associate of ISC2 and has six years to earn it. Verify your own eligibility with ISC2.

Exit when two weighted scenario sets exceed 85% and every wrong answer is classified as knowledge, scope, sequencing, governance, or question-reading error.

Primary links: [current exam outline](https://www.isc2.org/certifications/ccsp/ccsp-certification-exam-outline), [CCSP overview and experience](https://www.isc2.org/certifications/CCSP), [official self-study resources](https://www.isc2.org/certifications/ccsp/ccsp-self-study-resources), [ISC2 videos](https://www.youtube.com/@ISC2Official).
