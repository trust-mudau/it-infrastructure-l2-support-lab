# INC-015 — Multi-layer L2 Capstone: Service, Hostname and Backup Failures

**Priority:** P1/P2 capstone  
**Category:** Linux / Service / Name resolution / Permissions / Backup-Recovery  
**Platform:** Ubuntu 24.04.5 hosted runner  
**Status:** Lab validated  
**Execution:** https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34876267799

## Impact
After a simulated maintenance change, the `l2portal` application was unavailable, `portal.lab` did not point to the real listener, and the service account could not create its backup archive.

## Initial reproduced failures
- `systemctl is-active l2portal.service` failed (`service_rc=3`)
- HTTP through `portal.lab:8095` failed (`http_rc=7`)
- backup script failed (`backup_rc=2`)

## L2 investigation
`systemctl status` and `journalctl` showed `/srv/l2portal/config/app.env: Permission denied`. `namei`/`stat` showed the file was `0600 root:l2app`, preventing group read. `getent hosts` showed `portal.lab -> 127.0.0.2`; the intended application listener was `127.0.0.1:8095`. The backup destination was `0550 root:l2app`, so the `l2app` account could not create an archive.

## Corrective sequence
1. Changed `app.env` to `0640 root:l2app`, preserving least privilege.
2. Verified direct-IP HTTP health before changing name resolution.
3. Corrected `portal.lab` to `127.0.0.1` and verified hostname HTTP health.
4. Changed the backup directory to controlled group-write mode `0770 root:l2app`.
5. Created a backup, calculated SHA-256, restored it separately, and compared restored web data with the source.

## Final verification
- service state: `active`
- listener: `127.0.0.1:8095`
- `portal.lab`: `127.0.0.1`
- HTTP: `portal-status=healthy`
- config: `640 root:l2app`
- backup directory: `770 root:l2app`
- backup archive created by `l2app`
- SHA-256: `158095deba1b580fa86acc7be09e44670f06a08f705f7bd4bad351b7f69f4a12`
- restore check: PASS

## Escalation
No escalation was required in the controlled lab. In production, unexplained multi-control drift after maintenance should be correlated with change records and escalated when ownership, approved baselines, or data-recovery impact is unclear.
