# Digital Workplace IT Support Mini-Pack (Africa GreenCo-aligned)

A compact, role-targeted support scenario pack covering Microsoft 365 support thinking, onboarding/offboarding, access control, asset management, ticket/SLA discipline, SharePoint/intranet governance, security awareness and simple workflow automation.

## Evidence status

- **Professional experience:** not claimed by this pack.
- **Microsoft 365 / Outlook / Teams / SharePoint:** scenario-based support playbooks and synthetic tickets only; no live Microsoft tenant administration is claimed.
- **Asset register / ticket SLA / access-review checks:** synthetic data processed by an executable Python validation workflow in GitHub Actions.
- **Documentation:** authored SOPs/playbooks designed around realistic Tier 1 IT support responsibilities.

## What this pack demonstrates

| GreenCo requirement | Evidence in this pack | Status |
|---|---|---|
| Microsoft 365 support | Outlook/Teams/SharePoint troubleshooting playbook | Scenario demonstrated |
| Onboarding/offboarding | Joiner/leaver access checklist | Scenario demonstrated |
| User accounts/permissions | Access-request and review workflow | Scenario demonstrated |
| IT asset register | Structured asset inventory dataset + validation | Executed on synthetic data |
| Ticket management / SLA | Prioritised ticket queue + SLA calculation | Executed on synthetic data |
| Documentation / SOPs | Support playbooks and user-facing procedures | Demonstrated |
| Workflow automation | Python checks generate a support-readiness report | Executed |
| Intranet management | SharePoint/intranet governance and navigation plan | Scenario demonstrated |
| Security awareness | Password hygiene and phishing-reporting procedure | Scenario demonstrated |
| Access reviews | Review dataset, decisions and closure validation | Executed on synthetic data |
| ITSM / ITIL awareness | Incident/request, priority, escalation and SLA model | Demonstrated |

## Files

- `data/assets.csv` - synthetic IT asset register
- `data/tickets.csv` - synthetic support queue with priorities and SLA targets
- `data/access_review.csv` - synthetic access certification dataset
- `docs/01-m365-support-playbook.md` - Outlook, Teams and SharePoint troubleshooting
- `docs/02-onboarding-offboarding-access.md` - lifecycle and permissions checklist
- `docs/03-intranet-sharepoint-governance.md` - intranet/content governance
- `docs/04-security-awareness-and-access-review.md` - phishing, password hygiene and access reviews
- `docs/05-itsm-itil-sla-sop.md` - ITSM/ITIL-aware ticket/SLA workflow
- `scripts/validate_pack.py` - automation that validates records and calculates SLA performance

## Truthful CV wording

> Built a compact digital-workplace IT support scenario pack covering Microsoft 365 support workflows, onboarding/offboarding, access control, IT asset tracking, ticket/SLA handling, SharePoint/intranet governance, phishing reporting and access reviews; automated validation of synthetic asset, ticket and access-review records with Python and GitHub Actions.

Do not describe the Microsoft 365 portions as live tenant administration unless separately executed in an owned or authorised Microsoft environment.