# INC-005 — Scheduled Backup Job Fails While Manual Run Succeeds

**Priority:** P2  
**Category:** Linux / Scheduled jobs / Backup / Environment configuration  
**Platform:** GitHub-hosted Ubuntu runner  
**Status:** Scenario configured — execution evidence pending

## User / business impact

A scheduled backup job has begun failing even though the same backup script succeeds when an administrator runs it manually from an interactive shell. The backup window is being missed and the newest recovery point is stale.

## Initial symptoms

- manual backup command succeeds
- scheduled backup service fails
- no new archive appears in the expected backup destination
- source data remains available
- failure appears only in the non-interactive execution context

## Known environment

- Ubuntu GitHub-hosted runner
- backup script: `/opt/l2backup/run-backup.sh`
- source data: `/opt/l2backup/source`
- expected destination: `/var/backups/l2support`
- scheduled execution: `l2backup.service` triggered by `l2backup.timer`
- required environment setting: `BACKUP_DEST`

## L2 objective

Determine why the backup works interactively but fails when executed by the scheduler. Compare interactive and scheduled execution contexts, inspect `systemd` timer/service state and journal logs, identify the missing dependency or environment setting, apply the smallest safe correction, rerun the scheduled job, and verify archive integrity and recoverability.

## Investigation requirements

Capture at minimum:

- timer state and schedule
- service state and exit result
- recent `journalctl` entries
- service unit contents
- backup script contents
- interactive environment vs service environment
- source and destination permissions
- manual-run result
- scheduled-run result
- created archive metadata
- checksum verification
- test restore / source comparison
- corrective action and escalation decision

## Escalation rule

Escalate if the schedule is owned by another team, credentials/secrets are missing or expired, the destination is remote/unavailable, the service unit is centrally managed, the script fails even with the correct environment, backup data is corrupt, retention policy prevents safe remediation, or recovery verification fails.

## Evidence location

The workflow will upload a `scenario-05-evidence` artifact after execution.
