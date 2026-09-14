# INC-012 — Suspicious Linux Process Listening on Unapproved Port

**Priority:** P1/P2 security escalation scenario  
**Category:** Linux / Security / Process and socket triage  
**Platform:** Ubuntu 24.04  
**Status:** Lab validated — benign simulation  
**Execution:** https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34875933477

## Impact
A simulated unauthorized Python process launched from `/tmp`, modified a decoy finance file, and opened TCP 4444.

## Investigation
Before containment, evidence was captured with `ps`, `pstree`, `ss`, `lsof`, `/proc/<pid>/cmdline`, executable-path checks, `stat`, and SHA-256. The modified decoy file was also preserved.

## Containment
After preserving evidence, the process was terminated and TCP 4444 was verified closed.

## Escalation decision
**Escalate to Security/Incident Response in production.** Execution from a temporary path combined with an unexpected listener and business-file modification can indicate compromise. L2 support should preserve evidence and avoid simply deleting artifacts and closing the ticket.

## Safety note
The lab process was intentionally benign, local-only, and created solely for this scenario.
