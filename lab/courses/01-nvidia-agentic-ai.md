# Track 1 — NVIDIA Certified Professional: Agentic AI

**Target:** NCP-AAI; official page checked 2026-09-03; exam marked coming soon. NVIDIA describes 60–70 questions in 120 minutes and recommends 1–2 years of relevant hands-on experience.

## Anchor course

Use NVIDIA DLI's [Building Agentic AI Applications With LLMs](https://learn.nvidia.com/courses/course-detail?course_id=course-v1:DLI+C-FX-26+V1) as the vendor-led core. NVIDIA's certification page currently lists it as an **8-hour, $90, self-paced** course with a course certificate and an instructor-led option. The course-detail page is JavaScript-rendered and did not expose its syllabus to the research crawler, so those details are taken from the certification learning path and should be confirmed at checkout.

The DLI course is one component, not complete exam coverage. Place it in week 2 after the agent-anatomy lab, then turn each example into an independently evaluated artifact. The certification blueprint also expects architecture, production deployment/scaling, NVIDIA platform knowledge, operations, safety/compliance, and human oversight.

The [objective mastery map](../studies/ncp-aai/objective-map.md) tracks all numbered study-guide objectives and separates conceptual study from tested implementation.

Use the [free NVIDIA platform lab runbook](../studies/ncp-aai/free-nvidia-platform-runbook.md) for hosted NIM, NeMo Agent Toolkit, and Guardrails setup. It pins current official commands, keeps credentials out of logs, distinguishes hosted from self-hosted NIM, and requires execution evidence before credit is awarded.

## Blueprint map

| Module | Weight | Build outcome |
|---|---:|---|
| Agent architecture and design | 15% | Choose agent boundaries, protocols, state, and failure semantics |
| Agent development | 15% | Implement tool contracts, structured outputs, retries, and idempotency |
| Evaluation and tuning | 13% | Create task sets, graders, traces, and regression gates |
| Deployment and scaling | 5% PDF / 13% webpage | Package and scale an agent service with bounded concurrency |
| Cognition, planning, and memory | 10% | Compare reactive, planner/executor, and state-machine approaches |
| Knowledge integration and data | 10% | Build citation-aware retrieval with access filtering |
| NVIDIA platform implementation | 7% | Explain and prototype NIM/NeMo-oriented deployment choices |
| Run, monitor, and maintain | 7% PDF / 5% webpage | Define SLOs, traces, cost and incident signals |
| Safety, ethics, and compliance | 5% | Threat-model tools, prompts, data, and autonomous actions |
| Human interaction and oversight | 5% | Add approval gates, escalation, audit records, and usable controls |

## Six-week sprint

1. Agent anatomy: environment, policy, model, tools, state; implement a deterministic tool router.
2. Planning and memory: build planner/executor and state-machine versions; compare failure rates.
3. Retrieval: ingest a small policy corpus; enforce document ACLs; require source attribution.
4. Multi-agent systems: define typed messages, budgets, termination, and conflict resolution.
5. Evaluation and safety: assemble 50 representative/adversarial tasks; track task success, unsafe-action rate, latency, and cost.
6. Production: containerize, add traces and human approval, run load/failure tests, and write an incident review.

### Official learning-path extensions

| NVIDIA resource | Published length/price | Use in this stack |
|---|---:|---|
| Building Agentic AI Applications With LLMs | 8 h / $90 | Week 2 anchor; implementation patterns |
| Building RAG Agents With LLMs | 8 h / $90 | Week 3; retrieval and tool-grounded behavior |
| Evaluating RAG and Semantic Search Systems | 3 h / $30 | Week 5; evaluation design |
| Introduction to Deploying RAG Pipelines for Production at Scale | 8 h / $90 | Week 6; deployment and scaling |
| Adding New Knowledge to LLMs | 8 h / $500, instructor-led | Optional depth; not required by this curriculum |

Prices and availability can change. Recheck NVIDIA before purchase; do not buy the whole list until the diagnostic labs show a gap.

## Required labs

- **Tool contract lab:** safe read tool plus side-effecting write tool; schemas, timeouts, retry rules, idempotency keys, and an approval boundary.
- **Memory lab:** compare no memory, rolling summary, retrieval memory, and explicit state on the same tasks.
- **Prompt-injection lab:** hostile retrieved content must not override tool policy; log detection and refusal evidence.
- **Evaluation lab:** baseline two agent architectures, report confidence intervals where meaningful, and prevent test-set leakage.
- **Operations lab:** simulate provider timeout, bad tool response, retrieval outage, and runaway loop.

## Exit gate

Build the TrustGraph agent gateway. Pass at least 45/50 owned evaluation cases, cause zero unauthorized writes in the adversarial set, expose traceable citations, and explain when a workflow/state machine is safer than an autonomous agent.

Primary links: [certification and blueprint](https://www.nvidia.com/en-us/learn/certification/agentic-ai-professional/), [Building Agentic AI Applications With LLMs](https://learn.nvidia.com/courses/course-detail?course_id=course-v1:DLI+C-FX-26+V1), [NVIDIA Deep Learning Institute](https://www.nvidia.com/en-us/training/), [NVIDIA Developer videos](https://www.youtube.com/@NVIDIADeveloper).
