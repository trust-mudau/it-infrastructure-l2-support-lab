# INC-008 — Windows Service Stops During Startup

**Priority:** P2  
**Category:** Windows / Services / Event Log  
**Platform:** GitHub-hosted Windows Server 2025  
**Status:** Lab validated  
**Execution:** https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34875803731

## Impact
A local Windows support service would not remain running and TCP 8092 was unavailable.

## Investigation
1. Reproduced the stopped service state with `Get-Service`.
2. Confirmed the registered binary and LocalSystem service configuration with `sc.exe qc`.
3. Checked for a running process and listening TCP 8092 endpoint.
4. Queried the Application log with `Get-WinEvent`.
5. Event ID 8001 reported: `Startup failed: required configuration file port.txt is missing.`
6. `Test-Path` confirmed the file was absent.

## Resolution
Restored only `C:\l2lab\scenario08\port.txt` with the required lab port `8092`, then started the service again.

## Verification
- service state: `Running`
- `Test-NetConnection 127.0.0.1 -Port 8092`: `True`
- Event ID 8000: service started and listening on `127.0.0.1:8092`

## Escalation
No escalation was required because the failure was a local, recoverable configuration dependency. Escalate if the missing configuration is centrally managed, vendor-generated, or repeatedly disappears after remediation.
