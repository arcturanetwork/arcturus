import unittest

from capstone.security.incident_operations import REQUIRED_ROLES, correlate, run_exercise


class IncidentOperationsTests(unittest.TestCase):
    def test_correlation_requires_all_three_independent_signals(self):
        incomplete = [{"minute":0,"kind":"residency_violation"},
                      {"minute":2,"kind":"privileged_query"}]
        self.assertFalse(correlate(incomplete)["detected"])

    def test_exercise_covers_response_custody_and_recovery(self):
        result = run_exercise()
        self.assertTrue(result["passed"])
        self.assertEqual(set(result["roles"]), REQUIRED_ROLES)
        self.assertTrue(result["forensics"]["integrity_verified"])
        self.assertFalse(result["legal_hold"]["deletion_performed"])
        self.assertLessEqual(result["recovery"]["actual_minutes"], result["recovery"]["rto_minutes"])
        self.assertEqual(result["recovery"]["recurrence_query_count"], 0)
        self.assertTrue(result["limitations"])


if __name__ == "__main__": unittest.main()
