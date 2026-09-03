from pathlib import Path
import unittest

from capstone.security.app_assurance import run, scan_python


class AppAssuranceTests(unittest.TestCase):
    def test_risky_call_is_found(self):
        path = Path("/tmp/ccsp-risky-call.py")
        path.write_text("eval('1+1')\n")
        try: self.assertEqual(scan_python([path])["sast_findings"][0]["rule"], "risky-call:eval")
        finally: path.unlink(missing_ok=True)

    def test_assurance_run_includes_negative_tests_and_limitations(self):
        result = run()
        self.assertTrue(result["passed"])
        self.assertTrue(result["artifact_integrity"]["tamper_rejected"])
        self.assertEqual({x["case"] for x in result["dast"]["cases"]},
                         {"security-headers", "malformed-contract", "unauthorized-write"})
        self.assertTrue(result["limitations"])


if __name__ == "__main__": unittest.main()
