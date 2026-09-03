# kubeadm cluster lifecycle and etcd recovery practice

This is a command-navigation runbook, not an executed transcript. Exact package/version commands must follow the exam's current Kubernetes version and Linux distribution documentation.

## Bootstrap mental model

1. Prepare compatible Linux hosts, kernel/network settings, time/DNS, container runtime and CRI integration.
2. Install version-matched kubeadm, kubelet and kubectl; respect supported version skew.
3. `kubeadm init` the first control-plane node using deliberate endpoint, Pod CIDR and configuration.
4. Install exactly one compatible CNI; nodes commonly remain NotReady before it is functional.
5. Generate time-limited join commands/tokens; add workers and additional control-plane nodes as designed.
6. Verify nodes, system Pods, DNS, scheduling, service networking and control-plane health.

## Upgrade sequence

Read the current kubeadm upgrade guide. Upgrade one supported minor step at a time: inspect plan, upgrade kubeadm, apply/execute control-plane upgrade, drain where appropriate, upgrade kubelet/kubectl packages, restart kubelet, uncordon, verify, then proceed node by node. Preserve capacity and PDB constraints. Never improvise a version jump from memory.

## etcd snapshot and restore drill

For stacked etcd, identify endpoints and certificate/key paths from the static Pod manifest rather than guessing. Record the etcdctl API/environment and run a snapshot status/integrity check. Store the snapshot and encryption material separately according to policy.

Restore into a new data directory using the documented etcdutl/etcd tooling for the installed version. Update the etcd static Pod configuration to use that directory, allow kubelet to reconcile it, then verify etcd/control-plane health and application objects. A snapshot command succeeding is not recovery evidence; application-state verification is required.

## HA and extension interfaces

A highly available control plane needs a stable API endpoint/load balancer and multiple control-plane/etcd members across failure domains. CNI implements Pod networking, CSI storage integration, and CRI runtime integration. CRDs extend the API schema; controllers/operators reconcile desired state. Installing a CRD alone does not run reconciliation.

Helm renders/manages chart releases; Kustomize overlays declarative resources. In exam practice, inspect rendered output and ownership before mutation, and know how to diagnose failed hooks, values, API versions, and controller readiness.

