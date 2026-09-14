# RCA — INC-005 Scheduled Backup Environment Failure

## Executive summary

A scheduled Linux backup failed while the same backup script worked during manual execution. The issue was isolated to a difference between interactive and `systemd` service environments: the script required `BACKUP_DEST`, but the scheduled service did not define it.

## Impact

The scheduled backup did not produce a current archive, creating a stale recovery point and a backup-window failure.

## Timeline

1. Confirmed the backup script succeeds manually when `BACKUP_DEST=/var/backups/l2support` is supplied.
2. Started a real `systemd` timer configured to trigger the backup service.
3. Confirmed the timer fired and the service entered a failed state.
4. Verified no scheduled archive was created.
5. Collected service state, timer state, journal output, unit definitions, environment configuration and permissions.
6. Identified missing `BACKUP_DEST` in the service environment.
7. Added a root-managed `EnvironmentFile` and referenced it from the service.
8. Reran the service successfully.
9. Verified the archive checksum and performed a test restore with a source-to-restore comparison.

## Technical findings

The scheduled service failed with:

```text
/opt/l2backup/run-backup.sh: line 3: BACKUP_DEST: BACKUP_DEST must be defined
```

The manual execution had explicitly supplied:

```text
BACKUP_DEST=/var/backups/l2support
```

Before remediation, `systemctl show` reported no service environment configured. The source and destination filesystem permissions were valid, so a permission fault was ruled out.

## Root cause

The backup script depended on an environment variable that was present only during manual execution. `systemd` did not inherit the administrator's interactive shell environment, so the scheduled job lacked `BACKUP_DEST` and terminated before creating the archive.

## Corrective action

Created a root-managed environment file:

```text
/etc/l2backup/backup.env
```

with:

```text
BACKUP_DEST=/var/backups/l2support
```

and added the following to `l2backup.service`:

```ini
EnvironmentFile=/etc/l2backup/backup.env
```

No backup-script code change was required.

## Verification

The corrected service returned `Result=success`. The backup archive was created, its SHA-256 checksum validated successfully, the archive was restored to an isolated directory, and `diff -ru` found no differences from the source data.

## Why this is an L2 issue

The failure could easily be misclassified as a broken backup script because the scheduled job failed. L2 troubleshooting required comparing execution contexts, validating the scheduler itself, reading service logs, checking environment state, ruling out permissions and confirming recoverability rather than stopping at archive creation.

## Preventive actions

- document required environment variables for scheduled jobs
- keep scheduler-specific configuration in managed environment files
- alert on missed backup windows and stale recovery points
- validate backups with periodic restore testing, not only job exit status
- avoid relying on interactive shell profiles for production automation

## Escalation criteria

Escalate when missing values are secrets requiring another team's ownership, remote backup targets are unavailable, central configuration management overrides local changes, the backup still fails with a complete environment, or integrity/restore verification fails.

## Evidence

Executed GitHub Actions run:

https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34874198298

Evidence artifact: `scenario-05-evidence`
