# Source register and media policy

Verified **2026-09-03**. Primary vendor pages govern when any secondary source conflicts.

Machine-readable version, objective-range/count, discrepancy, and mandatory-refresh metadata lives in the [certification registry](certification-registry.json). Run `python3 -m assessments.blueprint_audit` before a readiness decision; this validates recorded provenance and recency but does not access the network or claim that a page is unchanged. Run `python3 -m assessments.objective_coverage` to expand the numbered ranges and catch registry/map count drift.

| Track | Blueprint/status source | Practice and learning source | Version note |
|---|---|---|---|
| NVIDIA Agentic AI | [NCP-AAI page](https://www.nvidia.com/en-us/learn/certification/agentic-ai-professional/) | [Building Agentic AI Applications With LLMs](https://learn.nvidia.com/courses/course-detail?course_id=course-v1:DLI+C-FX-26+V1), [DLI](https://www.nvidia.com/en-us/training/), [developer videos](https://www.youtube.com/@NVIDIADeveloper) | Coming soon; DLI anchor listed as 8 h/$90; recheck guide, course terms and registration |
| AWS SAP | [exam guides](https://docs.aws.amazon.com/aws-certification/latest/examguides/aws-certification-exam-guides.html), [C03 announcement](https://aws.amazon.com/blogs/training-and-certification/september-2026-new-offerings/) | [Skill Builder](https://skillbuilder.aws/), [Architecture Center](https://aws.amazon.com/architecture/), [AWS Events](https://www.youtube.com/@AWSEventsChannel) | C03 guide due 2026-10-27; exam 2026-11-17 |
| CKA | [certification/domains](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/) | [Kubernetes docs](https://kubernetes.io/docs/), [CNCF videos](https://www.youtube.com/@cncf) | v1.35 shown; tracks recent minor versions |
| NVIDIA GENL | [NCP-GENL page](https://www.nvidia.com/en-us/learn/certification/generative-ai-llm-professional/) | [DLI](https://www.nvidia.com/en-us/training/), [NeMo docs](https://docs.nvidia.com/nemo-framework/) | Coming soon; live table has apparent copy errors |
| CCSP | [outline effective 2026-08-01](https://www.isc2.org/certifications/ccsp/ccsp-certification-exam-outline) | [official self-study](https://www.isc2.org/certifications/ccsp/ccsp-self-study-resources), [ISC2 videos](https://www.youtube.com/@ISC2Official) | Use 2026 outline, not older summaries |
| Google PMLE | [exam guide](https://cloud.google.com/learn/certification/guides/machine-learning-engineer) | [learning path](https://cloud.google.com/learn/training/machinelearning-ai), [Cloud Tech videos](https://www.youtube.com/@googlecloudtech) | Recheck guide before booking |

## How to curate videos

Prefer official vendor/CNCF sessions with a matching current objective. For each video, record title, URL, publisher, publication date, objective, useful timestamps, product/version, and a one-sentence reason to watch. Reject content that mainly sells dumps, promises guaranteed passes, reproduces recalled exam questions, lacks a version/date, or conflicts with current documentation.

Video search is intentionally a supplement. A clear older lecture can teach a durable concept, but commands, UI flows, service limits, exam logistics and blueprint coverage must be checked against current official documentation.

## Audited third-party NCP-AAI material

- [emrekuruu/nvidia-NCP-AAI-study-notes](https://github.com/emrekuruu/nvidia-NCP-AAI-study-notes) is a useful 53-topic index whose notes link to underlying sources. The supplied archive is recorded in `resources/audits/emrekuruu-ncp-aai.json`. It has no license file, so link and consult it but do not copy its generated prose. Its README mirrors the PDF weights, which total 92%, not a valid normalized exam distribution.
- [akshan-main/NCP-AAI](https://github.com/akshan-main/NCP-AAI) is MIT-licensed and publicly describes 13 modules, 12 labs, two capstones, setup guides, and 55 original practice questions. The pinned audit is recorded in `resources/audits/akshan-ncp-aai.json`. Its exercises are reference material rather than completion evidence: many are Markdown procedures, dependency assumptions vary by toolkit release, and its key-display instruction is prohibited here. Use the original [safe platform runbook](../studies/ncp-aai/free-nvidia-platform-runbook.md).
- NVIDIA's current certification page remains authoritative: $200, 120 minutes, 60–70 questions, and currently marked “Coming soon.” The current live domain table totals 98%, so neither third-party nor live weights should be silently normalized without a corrected NVIDIA publication.

## Legal and integrity boundary

This curriculum contains original summaries and labs based on public objectives. Do not collect or redistribute copyrighted paid-course assets, unauthorized recordings, braindumps, recalled live questions, or confidential exam content. Link to lawful sources and write new explanations and scenarios.
