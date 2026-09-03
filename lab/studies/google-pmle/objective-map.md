# Google Professional Machine Learning Engineer objective map

Source: current five-page Google exam guide retrieved 2026-09-03. It uses **Gemini Enterprise Agent Platform** terminology and approximate weights 13/16/21/20/18/13 (rounded total 101%), materially different from the earlier outline.

| Section/tasks | Published coverage | Evidence/status |
|---|---|---|
| 1 (~13%): 1.1 BigQuery ML/Agent Platform AutoML; 1.2 APIs/foundation models | Model/feature/prediction/AutoML/Gemini tuning; Model Garden and industry APIs; cost/latency/availability | studied; Google Cloud lab required |
| 2 (~16%): 2.1 preprocess; 2.2 notebooks; 2.3 experiments | Tool choice by scale, Feature Store/privacy; secure Workbench/Colab and frameworks; Experiments/Pipelines/Kubeflow, evaluation, artifacts/lineage | shared preprocessing, privacy controls, immutable registry/fingerprints tested; cloud lab required |
| 3 (~21%): 3.1 build; 3.2 train; 3.3 hardware | ARIMA/DNN/LLM and product/deployment/interpretability choices; ingestion/custom/AutoML/tuning/foundation tuning; CPU/GPU/TPU and parallelism | validated deterministic training tested; accelerator/cloud training required |
| 4 (~20%): 4.1 serve; 4.2 scale online | Batch/online, containers, registry, A/B/canary, pre/postprocess; Feature Store, endpoint exposure, hardware, throughput/tuning | gated version deployment/rollback plus explicit batch/online, SLO, autoscaling and private-exposure decision tested; load/cloud lab required |
| 5 (~18%): 5.1 pipeline; 5.2 retraining | Data/model validation, managed/unmanaged orchestration, preprocessing parity; retraining policy and CI/CD/CT | executable validate→train→evaluate→register→deploy and drift trigger tested |
| 6 (~13%): 6.1 risks; 6.2 monitoring | Exfiltration/malicious prompts/sensitive data, regex/filters/Model Armor, bias/explainability; continuous metrics, skew/data/concept/attribution drift, gen-AI evaluation | NCP/CCSP controls, shared preprocessing fingerprint, normalized mean shift, four-way change classification and slice-aware release gate tested; Google monitoring required |

## Decision rules studied

- BigQuery ML suits SQL-centric data and low operational overhead; custom training is justified by unsupported algorithms or control needs, not prestige.
- Batch inference suits tolerant latency and scheduled volume; online endpoints suit interactive latency while incurring capacity/SLO cost.
- Data drift changes input distributions; concept drift changes input-target relationships; skew is training/serving mismatch; attribution drift changes feature contribution.
- Drift is diagnostic, not proof retraining helps. Retrain, validate against baselines and slices, approve, canary, then monitor.
- Feature Store aids reusable consistent features but does not replace lineage, governance, or point-in-time correctness.
- Private endpoints reduce exposure but do not replace IAM, data controls, monitoring, or application safety.

## Timed scenario practice

Use the [18 original guide-aligned scenarios](scenario-labs.json) and [evidence-first rubric](scenario-rubric.md). Three cases per current guide section test managed-versus-custom choices, collaboration, model scaling, serving, pipelines, monitoring, security, and responsible AI. Written passes do not replace Google Cloud service-operation evidence.
