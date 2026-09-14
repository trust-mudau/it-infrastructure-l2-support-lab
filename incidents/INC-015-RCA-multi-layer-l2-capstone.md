# RCA — INC-015 Multi-layer L2 Capstone

## Executive summary
Three independent configuration faults combined to produce one user-visible outage plus a backup failure. The incident required layer-by-layer isolation instead of changing multiple controls at once.

## Root causes
1. **Service permission fault:** `/srv/l2portal/config/app.env` was `0600 root:l2app`; the `l2app` service account could not read it. The journal explicitly reported `Permission denied`.
2. **Name-resolution fault:** `/etc/hosts` mapped `portal.lab` to `127.0.0.2` while the healthy application listener used `127.0.0.1:8095`.
3. **Backup permission fault:** `/var/backups/l2portal` was `0550 root:l2app`, so `l2app` could not create `portal-data.tgz`.

## Troubleshooting method
First restore the service and prove health by direct IP. Only then correct hostname resolution. Treat the backup failure as a separate path and investigate its destination permissions rather than assuming it shares the application root cause.

## Corrective actions
- `app.env`: `0600` -> `0640 root:l2app`
- `portal.lab`: `127.0.0.2` -> `127.0.0.1`
- backup directory: `0550` -> `0770 root:l2app`

## Verification
`systemd` remained active, TCP 8095 listened on loopback, HTTP returned the expected health string by hostname, the backup archive was created, SHA-256 was captured, and a separate restore matched the source web directory.

## Prevention
Use post-change validation covering service account access, service state/ports, name resolution, and backup/restore health. When several symptoms appear together, maintain separate hypotheses until evidence proves a shared cause.
