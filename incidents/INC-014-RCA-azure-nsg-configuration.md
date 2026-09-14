# RCA — INC-014 Azure NSG Configuration Gap

## Summary
Configuration review showed a web workload would be unreachable over HTTPS because its NSG definition contained no inbound TCP 443 allow rule before an explicit deny-all rule.

## Evidence
- Azure CLI and Bicep tooling executed successfully
- initial Bicep compiled successfully
- compiled rule inspection found zero inbound allow rules for TCP 443
- deny-all rule existed at priority 4096

## Corrective action
Added `Allow-HTTPS-Web` at priority 200 and recompiled the Bicep definition.

## Verification
The corrected JSON contained the HTTPS rule and confirmed priority 200 evaluates before priority 4096.

## Scope limitation
This is hands-on infrastructure-as-code/cloud configuration exposure. It does not represent live Azure tenant administration or deployment.
