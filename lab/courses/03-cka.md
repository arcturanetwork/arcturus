# Track 3 — Certified Kubernetes Administrator

**Target:** CKA; official page checked 2026-09-03. The performance-based exam is two hours and currently uses Kubernetes v1.35. Linux Foundation says it follows the newest minor version approximately 4–8 weeks after release, so verify immediately before practice and exam day.

Track evidence: [objective map](../studies/cka/objective-map.md), [troubleshooting runbook](../studies/cka/troubleshooting-runbook.md), and [TrustGraph manifests](../capstone/k8s/base/workload.json). The current machine lacks a working cluster toolchain, so these artifacts are explicitly classified as static—not performance evidence.

## Blueprint map

| Domain | Weight | Course outcome |
|---|---:|---|
| Troubleshooting | 30% | Diagnose nodes, control plane, workloads, networking, logs and resource use |
| Cluster architecture, installation, configuration | 25% | kubeadm, lifecycle, HA concepts, RBAC, Helm/Kustomize, CRDs/operators, CNI/CSI/CRI |
| Services and networking | 20% | Pod connectivity, Services, NetworkPolicy, DNS, Ingress and Gateway API |
| Workloads and scheduling | 15% | Deployments, rollouts, ConfigMaps/Secrets, autoscaling, affinity and resources |
| Storage | 10% | StorageClasses, dynamic provisioning, PV/PVC, access modes and reclaim policies |

## Seven-week sprint

1. Fast `kubectl`, API discovery, YAML editing, contexts, namespaces and documentation navigation.
2. kubeadm cluster lifecycle, etcd backup/restore, upgrades, certificates and RBAC.
3. Workloads, scheduling, probes, resources, autoscaling, ConfigMaps and Secrets.
4. Services, DNS, NetworkPolicy, Ingress controllers and Gateway API.
5. Storage provisioning, access modes, expansion, reclaim and failure diagnosis.
6. Troubleshooting drills from symptom to hypothesis to evidence to fix.
7. Four two-hour simulations; maintain an error/command-speed log.

## Required labs

- Build a disposable multi-node cluster; join/cordon/drain/upgrade a worker safely.
- Back up and restore etcd in a throwaway environment; verify application state.
- Break DNS, selectors, readiness, scheduling, permissions, storage binding and network policy one at a time; diagnose without an answer key.
- Deploy TrustGraph with Helm or Kustomize, persistent state, Gateway API/Ingress, quotas and least-privilege service accounts.

## Exit gate

Complete two fresh simulations above 85% with at least 15 minutes remaining. Commands must target the correct context/namespace, verification must follow every mutation, and destructive operations must have explicit scope.

Primary links: [CKA certification and current domains](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/), [Kubernetes documentation](https://kubernetes.io/docs/), [Kubernetes official videos](https://www.youtube.com/@KubernetesCommunity).
