# CKA objective mastery map

Source: Linux Foundation CKA domains checked 2026-09-03; exam page states Kubernetes v1.35 and a two-hour performance exam. Local environment check found no usable kubectl, kind, minikube, helm or kubeadm, and Docker Desktop integration is disabled. Therefore manifest checks below are static evidence only—not cluster mastery.

The [24 original performance labs](performance-labs.json) cover each published competency, with a [safety/diagnosis/verification rubric](performance-rubric.md). They remain unscored until executed on varied disposable clusters.

| Domain | Weight | Evidence | Status |
|---|---:|---|---|
| Troubleshooting | 30% | Symptom-to-evidence runbook and fault drills | studied; live cluster required |
| Architecture/install/configuration | 25% | Namespaced least-privilege RBAC plus bootstrap, upgrade, etcd, HA, CNI/CSI/CRI, Helm/Kustomize and operator runbook | statically tested/studied; live kubeadm/Helm/operator work required |
| Services/networking | 20% | ClusterIP, default deny, scoped ingress/DNS egress, HTTPRoute | statically tested; live CNI/Gateway/DNS required |
| Workloads/scheduling | 15% | Rolling Deployment, probes, resources, HPA, spread, ConfigMap/Secret refs, PDB | statically tested; live scheduling/rollout required |
| Storage | 10% | StorageClass with delayed binding/retention/expansion plus PVC | statically tested; CSI/PV lifecycle required |

## Exam-relevant distinctions studied

- A Service selects ready endpoints by labels; a matching selector does not prove the application listens on `targetPort`.
- NetworkPolicy behavior requires a supporting CNI. Policies are additive; selecting a pod for ingress or egress isolates that direction.
- A PDB constrains voluntary disruption, not crashes, and cannot manufacture capacity.
- HPA CPU utilization needs resource requests; otherwise the utilization denominator is missing.
- `WaitForFirstConsumer` delays binding so topology-aware provisioning can follow scheduling.
- Gateway API resources require the CRDs and a controller; an HTTPRoute alone creates no data plane.
- Draining respects controllers and PDBs; control-plane and etcd upgrades require ordered, version-skew-aware procedures.
