# Security Awareness, Phishing Reporting and Access Review

## Password hygiene guidance

- Use unique passwords/passphrases and approved password-manager practices where available.
- Never share credentials or MFA approval codes.
- Treat unexpected MFA prompts as suspicious.
- Report suspected credential compromise immediately.
- Do not bypass access controls to restore convenience.

## Suspected phishing - Tier 1 response

1. Tell the user not to click links, open attachments, reply or enter credentials.
2. Capture sender, subject, time, recipients and user actions without forwarding unsafe content unnecessarily.
3. Determine whether the user clicked, downloaded, entered credentials or approved MFA.
4. Preserve the message/reporting evidence using the organisation's approved process.
5. Escalate according to security incident procedure when compromise is possible.
6. If credentials may have been entered, treat as urgent and follow the identity-security escalation path.
7. Document user impact, containment guidance, escalation owner and next action.

## Access review procedure

- Export or review current users, groups/resources and owners.
- Ask the business owner to Keep or Remove each access item; technicians should not invent business approval.
- Prioritise disabled/leaver accounts and privileged access.
- Execute approved removals or route them to the correct administrator.
- Verify the resulting state.
- Record unresolved exceptions and escalate policy/compliance issues.

The synthetic `access_review.csv` demonstrates the record-keeping model, including removal of a former user and unnecessary privileged access.