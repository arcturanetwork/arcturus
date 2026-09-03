# CKA troubleshooting runbook

Use the shortest evidence path: context → object status/events → logs → dependencies → node/control plane. Verify after every mutation.

| Symptom | First evidence | Likely branches | Verification |
|---|---|---|---|
| Pending Pod | describe Pod; events; requests/affinity/taints/PVC | insufficient resource, untolerated taint, impossible affinity, unbound claim | Pod scheduled on intended node; events clear |
| CrashLoopBackOff | current and previous logs; describe probes/exit code | application/config/secret, OOM, probe failure | restart count stable; readiness true |
| Service has no endpoints | EndpointSlices, selectors, Pod labels/readiness | selector mismatch, no ready pods, wrong namespace | expected addresses in EndpointSlice; request succeeds |
| Service timeout | endpoints, targetPort, listener, NetworkPolicy | wrong port, app bind, denied flow, kube-proxy/CNI | in-cluster DNS and connection succeed |
| DNS failure | resolv.conf, CoreDNS Pods/logs/Service, NetworkPolicy | CoreDNS unhealthy, blocked UDP/TCP 53, bad name | `nslookup` short and FQDN forms |
| Node NotReady | conditions/events, kubelet logs, disk/memory/PID pressure | kubelet/runtime/CNI/cert/resource failure | node Ready; system pods healthy |
| API unavailable | static pod manifests, kubelet, container runtime, control-plane logs | API/etcd/cert/config failure | health/readiness endpoints and kubectl succeed |
| PVC Pending | claim/events, StorageClass/provisioner, access/topology | absent/default class, CSI failure, topology mismatch | PVC Bound and mounted read/write test |

## Timed drill protocol

1. Confirm the requested context and namespace before mutation.
2. Save original state when rollback matters.
3. Spend at most two minutes on initial evidence before choosing a hypothesis.
4. Apply the smallest scoped correction.
5. Verify object state and user-visible behavior.
6. Record the fault class and command-navigation delay.

