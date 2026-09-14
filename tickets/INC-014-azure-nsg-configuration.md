# INC-014 — Azure-Style Web Workload Missing HTTPS NSG Rule

**Priority:** P2 configuration scenario  
**Category:** Cloud / Azure fundamentals / Network security  
**Platform:** Azure CLI + Bicep on Ubuntu hosted runner  
**Status:** Configuration lab validated  
**Execution:** https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34876110072

## Scope
No live Azure subscription or production resource was modified. This demonstrates Azure/Bicep configuration analysis only.

## Incident
An NSG Bicep definition allowed administrative SSH from `10.10.0.0/24` at priority 100, then explicitly denied all inbound traffic at priority 4096. No inbound rule allowed TCP 443.

## Investigation
The Bicep template was compiled with Azure CLI. The compiled JSON was queried to confirm the inbound HTTPS allow-rule count was `0`.

## Resolution
Added `Allow-HTTPS-Web`, inbound TCP 443, priority 200, before the deny-all rule, then rebuilt the template.

## Verification
The compiled configuration contained exactly one expected HTTPS allow rule and its priority was lower than the deny-all priority.

## Escalation
A real cloud change requires network/security change approval and validation of source restrictions, application design, exposure requirements and organizational policy.
