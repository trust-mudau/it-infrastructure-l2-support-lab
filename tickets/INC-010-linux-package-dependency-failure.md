# INC-010 — Linux Package Install Leaves Application Unconfigured

**Priority:** P2  
**Category:** Linux / Packages / Dependencies  
**Platform:** Ubuntu 24.04  
**Status:** Lab validated  
**Execution:** https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34875864469

## Impact
Deployment of `l2demo-app` failed and `dpkg` left the package unconfigured.

## Investigation
The package metadata was inspected with `dpkg-deb -I`. `dpkg -i` reproduced the failure. `dpkg-query`, `dpkg --audit`, `apt-get check`, and `apt-cache policy l2missing-runtime` were used to distinguish a dependency problem from application execution failure.

## Root cause
Version 1.0 declared an unavailable dependency: `l2missing-runtime (>= 9.9)`.

## Resolution
Removed the broken package and installed corrected version 1.1 with the valid runtime dependency `bash`.

## Verification
`dpkg-query` returned `install ok installed`, `apt-get check` completed cleanly, and `l2demo-app` returned `l2demo-app=healthy`.

## Escalation
In production, a bad vendor/repository dependency declaration should be escalated to packaging/release engineering rather than silently edited on managed endpoints.
