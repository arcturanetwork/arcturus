# CCSP incident tabletop — model data exposure

## Scenario

A retrieval index containing restricted customer documents was replicated to a disallowed Region. A service identity could query the index because of an overly broad role. Logs show access but omit document classification. A regulator notification clock may apply; a legal hold arrives while deletion is being planned.

## Expected response sequence

1. Activate the incident process; assign incident commander, evidence custodian, privacy/legal, service owner, provider liaison and communications owner.
2. Preserve volatile and provider-held evidence with timestamps, identities, configuration versions and documented custody. Do not destroy implicated data after legal hold.
3. Contain access using the smallest reversible control; preserve business-critical evidence and avoid unreviewed broad account shutdown.
4. Establish facts: affected subjects/data/classes, source and replica Regions, identities/actions, exposure duration, encryption/key access, downstream processors, contractual and regulatory duties.
5. Eradicate the policy/role/replication defect; rotate credentials where exposure warrants it; validate clean configuration.
6. Recover from known-good state and monitor for recurrence. Business, security and privacy owners validate recovery.
7. Legal/privacy determine notifications; communications use confirmed scope, approved audiences and required timelines.
8. Conduct after-action review: missing classification in logs, preventive residency policy, least privilege, detection latency, provider evidence access and restore/deletion proof.

## Examiner traps

- Technical containment does not replace legal/privacy assessment.
- Encryption does not eliminate breach analysis automatically.
- A legal hold overrides routine deletion schedules.
- A provider assurance report has a period, system boundary, control scope, exceptions and complementary customer controls; its logo is not blanket assurance.
- Evidence integrity and chain of custody matter before later forensic analysis.

