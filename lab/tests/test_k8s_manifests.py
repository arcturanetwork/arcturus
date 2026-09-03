import json
from pathlib import Path
import unittest


def load(name):
    return json.loads(Path(name).read_text())


class KubernetesManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deployment = load("capstone/k8s/base/workload.json")
        cls.service = load("capstone/k8s/base/service.json")
        cls.hpa = load("capstone/k8s/base/autoscaling.json")
        cls.storage = load("capstone/k8s/base/storage.json")
        cls.policies = load("capstone/k8s/networking/policies.json")["items"]
        cls.route = load("capstone/k8s/networking/gateway-route.json")
        cls.rbac = load("capstone/k8s/base/rbac.json")["items"]

    def test_service_selectors_match_pod_labels_and_named_port(self):
        labels = self.deployment["spec"]["template"]["metadata"]["labels"]
        self.assertEqual(self.service["spec"]["selector"], labels)
        ports = {p["name"] for p in self.deployment["spec"]["template"]["spec"]["containers"][0]["ports"]}
        self.assertIn(self.service["spec"]["ports"][0]["targetPort"], ports)

    def test_workload_has_probes_resources_and_hardening(self):
        pod = self.deployment["spec"]["template"]["spec"]
        container = pod["containers"][0]
        self.assertIn("readinessProbe", container)
        self.assertIn("livenessProbe", container)
        self.assertTrue(container["resources"]["requests"])
        self.assertTrue(pod["securityContext"]["runAsNonRoot"])
        self.assertFalse(container["securityContext"]["allowPrivilegeEscalation"])
        self.assertIn("ALL", container["securityContext"]["capabilities"]["drop"])

    def test_hpa_target_and_cpu_request_are_compatible(self):
        self.assertEqual(self.hpa["spec"]["scaleTargetRef"]["name"], self.deployment["metadata"]["name"])
        requests = self.deployment["spec"]["template"]["spec"]["containers"][0]["resources"]["requests"]
        self.assertIn("cpu", requests)
        self.assertLessEqual(self.hpa["spec"]["minReplicas"], self.deployment["spec"]["replicas"])

    def test_default_deny_and_explicit_dns_exist(self):
        default = next(p for p in self.policies if p["metadata"]["name"] == "default-deny")
        allow = next(p for p in self.policies if p["metadata"]["name"] == "allow-gateway-and-dns")
        self.assertEqual(default["spec"]["podSelector"], {})
        dns_ports = {p["port"] for rule in allow["spec"]["egress"] for p in rule["ports"]}
        self.assertIn(53, dns_ports)

    def test_storage_and_gateway_use_current_stable_apis(self):
        self.assertEqual(self.storage["apiVersion"], "storage.k8s.io/v1")
        self.assertEqual(self.storage["volumeBindingMode"], "WaitForFirstConsumer")
        self.assertEqual(self.route["apiVersion"], "gateway.networking.k8s.io/v1")

    def test_gateway_backend_matches_service(self):
        backend = self.route["spec"]["rules"][0]["backendRefs"][0]
        service_port = self.service["spec"]["ports"][0]["port"]
        self.assertEqual(backend["name"], self.service["metadata"]["name"])
        self.assertEqual(backend["port"], service_port)

    def test_rbac_is_namespaced_and_has_no_wildcards_or_secret_read(self):
        role = next(item for item in self.rbac if item["kind"] == "Role")
        binding = next(item for item in self.rbac if item["kind"] == "RoleBinding")
        self.assertEqual(role["metadata"]["namespace"], "trustgraph")
        flattened = {value for rule in role["rules"] for key in ("apiGroups","resources","verbs") for value in rule[key]}
        self.assertNotIn("*", flattened); self.assertNotIn("secrets", flattened)
        self.assertEqual(binding["roleRef"]["name"], role["metadata"]["name"])


if __name__ == "__main__":
    unittest.main()
