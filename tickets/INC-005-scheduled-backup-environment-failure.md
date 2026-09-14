# INC-005 — Scheduled Backup Job Fails While Manual Run Succeeds

**Priority:** P2  
**Category:** Linux / Scheduled jobs / Backup / Environment configuration  
**Platform:** GitHub-hosted Ubuntu 24.04.5 LTS runner  
**Status:** **Lab validated — resolved**

## User / business impact

A scheduled backup job failed even though the same backup script succeeded when run manually with the required environment. The backup window was missed and no new scheduled recovery point was produced.

## Initial symptoms

- manual backup command succeeded
- scheduled backup service failed
- no new archive appeared in the expected backup destination
- source data remained available
- failure occurred only in the non-interactive scheduled execution context

## Investigation summary

The manual execution was first proven healthy by running the same script with `BACKUP_DEST=/var/backups/l2support`; it created the expected archive successfully.

A real `systemd` timer then triggered `l2backup.service`. The scheduled service failed with exit code `1`, and no archive was created. `systemctl status` and `journalctl -u l2backup.service` reported:

```text
BACKUP_DEST: BACKUP_DEST must be defined
```

`systemctl show l2backup.service -p Environment -p EnvironmentFiles` confirmed the service had no configured environment. Source and destination permissions were also inspected and did not explain the failure.

## Root cause

The backup script required the `BACKUP_DEST` environment variable. The successful manual run explicitly supplied it, but the `systemd` service did not inherit that interactive value. The scheduled job therefore exited before archive creation.

## Corrective action

Created `/etc/l2backup/backup.env` containing:

```text
BACKUP_DEST=/var/backups/l2support
```

Then referenced it from the service with:

```ini
EnvironmentFile=/etc/l2backup/backup.env
```

The service was reloaded and rerun without changing the backup script itself.

## Verification

After remediation:

- `l2backup.service` completed with `Result=success`
- backup archive was created
- SHA-256 verification returned `OK`
- archive was restored to a separate directory
- restored contents matched the source with `diff -ru`
- scenario result: `RESOLVED`

## Escalation decision

No escalation was required because the root cause was local service-environment configuration, the correction was within lab authorization, and backup integrity plus recoverability were independently verified.

## Commands / tools demonstrated

- `systemctl status`
- `systemctl list-timers`
- `systemctl show`
- `systemctl cat`
- `journalctl -u`
- `env`
- `tar`
- `sha256sum`
- `diff`
- Linux file/directory permission inspection
- `systemd` service and timer troubleshooting

## Evidence

GitHub Actions run:

https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34874198298

Workflow artifact: `scenario-05-evidence`  
Artifact SHA-256: `8554da3890fc13ac3d1f98bdc8d98df5ddcad721e3acd5bc16699e39a000b5a4`
