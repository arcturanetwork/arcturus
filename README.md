# Arcturus — Elite Agentic AI Operator

> Arctura Network's elite agentic AI operator. Trained on the full NVIDIA NCP-AAI stack. Ten competency domains, from ReAct reasoning to production deployment. Backed by a six-track certification lab with working agent code.

[![Status](https://img.shields.io/badge/Status-Active-3ea89b)](https://arcturus-arctura-network.netlify.app/)
[![NCP-AAI](https://img.shields.io/badge/NCP--AAI-100%25%20Domains-3ea89b)](https://www.nvidia.com/en-us/training/certification/)
[![Standard](https://img.shields.io/badge/Standard-Work%20Standard-c9a35c)](https://arctura.network/work-standard/)
[![Tests](https://img.shields.io/badge/Lab-6%20Tracks%20%7C%20128%20Files-c9a35c)](lab/)

---

## What Arcturus Is

Not a chatbot. An operator.

Arcturus is the agent that carries out the network's work — reasoning, retrieval, tool use, deployment, governance. It operates inside published limits: reasoning frameworks, memory architectures, guardrails, and evaluation gates that are visible, checkable, and reproducible.

## Competency Domains

All 10 NCP-AAI certification domains:

| # | Domain | Weight | Coverage |
|---|--------|--------|----------|
| 1 | Reasoning Frameworks — ReAct, Reflexion, ReWOO | 15% | ✅ |
| 2 | Agent Development & Tool Integration | 15% | ✅ |
| 3 | Evaluation and Tuning | 13% | ✅ |
| 4 | Deployment and Scaling | 13% | ✅ |
| 5 | Cognition, Planning, and Memory | 10% | ✅ |
| 6 | Knowledge Integration — Graphs & RAG | 10% | ✅ |
| 7 | NVIDIA Platform Implementation | 7% | ✅ |
| 8 | Run, Monitor, and Maintain | 5% | ✅ |
| 9 | Safety, Ethics, and Governance | 5% | ✅ |
| 10 | Human-AI Interaction and Oversight | 5% | ✅ |

## Operator Training Infrastructure

The `lab/` directory contains the full certification stack — six tracks, a working agent implementation, assessment tools, and evidence capture:

| Track | Certification | Effort |
|------|---------------|--------|
| 1 | NVIDIA NCP-AAI (primary) | 6 weeks / 60h |
| 2 | AWS SAP-C03 | 10 weeks / 100h |
| 3 | CKA | 7 weeks / 70h |
| 4 | NVIDIA NCP-GENL | 8 weeks / 80h |
| 5 | CCSP | 8 weeks / 80h |
| 6 | Google PMLE | 8 weeks / 80h |

The capstone is a working agent — typed tool contracts, bounded multi-agent orchestration, memory policies, knowledge retrieval with authorization, and a 50-case policy evaluation suite. All dependency-free Python.

See [lab/README.md](lab/README.md) for the full structure.

## Operating Stack

| Layer | Component | Function |
|-------|-----------|----------|
| Reasoning | ReAct / Reflexion / ReWOO | Plan, act, observe, reflect |
| Orchestration | NeMo Agent Toolkit | Workflow definition, profiling, eval |
| Inference | NIM microservices | TensorRT-LLM optimized generation |
| Safety | NeMo Guardrails (Colang 2.0) | Input/output screening, topic control |
| Memory | Vector store + Graph DB | Episodic, semantic, procedural memory |
| Knowledge | GraphRAG + Vector RAG | Global + local retrieval |
| Observability | OpenTelemetry | Distributed tracing, metrics, logs |
| Governance | The Five Checks | Need, Clarity, Usefulness, Durability, Reversal |

## The Five Checks

Inherited from Arctura Network's Work Standard:

1. **Need** — Is there a real reason for this action?
2. **Clarity** — Can someone outside the room understand what happened and who owns it?
3. **Usefulness** — Does this serve the network, not just whoever proposed it?
4. **Durability** — Will this still make sense later?
5. **Reversal** — Can it be undone if the assumption is wrong?

## Related

- [Agentic AI Mastery — Full Technical Reference](https://dominicvael.github.io/agentic-ai-mastery/)
- [Training Lab](lab/) — six-track certification infrastructure
- [Arctura Network — Work Standard](https://arctura.network/work-standard/)
- [Arctura Network — Authority Record](https://arctura.network/authority/)

## Live Page

**[arcturus-arctura-network.netlify.app](https://arcturus-arctura-network.netlify.app/)**

---

*© 2026 Arctura Network — Work. Proof. Stewardship.*