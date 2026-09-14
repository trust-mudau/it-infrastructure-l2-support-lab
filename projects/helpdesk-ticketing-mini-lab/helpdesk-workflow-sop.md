# Helpdesk Workflow SOP

This SOP models a Zendesk/Freshdesk-style first-line workflow without claiming production use of those products.

1. **Log the ticket** — capture user, issue, affected service/device, impact, contact method and timestamps.
2. **Classify** — choose category and priority based on impact and urgency, not user seniority.
3. **Acknowledge** — confirm receipt, restate the problem in plain language and set expectations.
4. **Diagnose** — ask targeted questions, reproduce where safe, gather evidence and record troubleshooting steps as they occur.
5. **Resolve at L1 where appropriate** — make the smallest authorised change and verify with the user.
6. **Escalate when required** — include impact, reproduction steps, evidence, actions already attempted and the exact reason L1 scope is exhausted.
7. **Communicate throughout** — update the user when status changes, when more information is needed and when escalation occurs.
8. **Close correctly** — record resolution, verification, user confirmation, residual risk and any reusable KB note.

## Priority model
- **P1:** security incident or critical service impact; immediate triage/escalation.
- **P2:** user or important business function blocked; expedited response.
- **P3:** standard single-user issue or planned request; normal queue handling.
- **P4:** low-impact information/request with no current productivity block.

## Status model
New -> Open -> Pending user / Pending third party -> Resolved -> Closed.  
Escalated tickets remain tracked by L1 until ownership is formally accepted.

## Escalation triggers
- administrator rights or system ownership outside L1 scope
- repeated failure after documented standard troubleshooting
- infrastructure-wide or multi-user impact
- security indicators such as phishing, malware or suspicious authentication
- missing approval for sensitive access
- risk of data loss, compliance impact or unsupported change

## Closure quality check
A ticket is not complete because a command succeeded. Closure should show: issue, cause or best-supported diagnosis, action taken, verification, user communication, escalation if applicable, and final status.