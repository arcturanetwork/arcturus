from datetime import datetime, timedelta, timezone
import unittest

from capstone.security.identity_irm import FederationPolicy, RightsGrant, run_lab


class IdentityIrmTests(unittest.TestCase):
    def test_federation_rejects_forged_context(self):
        policy=FederationPolicy("issuer","aud")
        ok, reason=policy.validate({"iss":"attacker","aud":"aud","iat":90,"exp":200,"amr":["mfa"]},100)
        self.assertFalse(ok); self.assertIn("issuer",reason)

    def test_rights_bind_subject_object_action_expiry_and_revocation(self):
        now=datetime.now(timezone.utc)
        grant=RightsGrant("alice","doc",frozenset({"view"}),now+timedelta(seconds=5))
        self.assertTrue(grant.authorize("alice","doc","view",now))
        self.assertFalse(grant.authorize("alice","doc","export",now))
        self.assertFalse(grant.authorize("alice","doc","view",now+timedelta(seconds=6)))
        grant.revoked=True; self.assertFalse(grant.authorize("alice","doc","view",now))

    def test_complete_lab_has_negative_cases_and_rotation(self):
        result=run_lab(); self.assertTrue(result["passed"])
        self.assertGreaterEqual(sum(not x["accepted"] for x in result["federation"]["cases"]),4)
        self.assertTrue(result["secret_rotation"]["old_rejected"])
        self.assertTrue(result["irm"]["cases"][-1]["passed"])
        self.assertTrue(result["limitations"])


if __name__ == "__main__": unittest.main()
