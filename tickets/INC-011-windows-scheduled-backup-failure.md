# INC-011 — Windows Scheduled Backup Fails While Source Data Is Healthy

**Priority:** P2  
**Category:** Windows / Scheduled Tasks / Backup-Recovery  
**Platform:** Windows Server 2025  
**Status:** Lab validated  
**Execution:** https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34875898930

## Impact
A SYSTEM scheduled task executed but produced no backup archive and returned a non-zero task result.

## Investigation
`Get-ScheduledTask`, task Actions, `Get-ScheduledTaskInfo`, the backup script log, source files, and destination state were inspected. The script required `-BackupRoot`, but the task action invoked the script without it. The scripted failure code was `23`.

## Resolution
Updated only the Scheduled Task action to pass the managed backup destination explicitly.

## Verification
- `LastTaskResult = 0`
- backup ZIP existed
- SHA-256 was calculated
- archive was restored into a separate directory
- restored file list matched source data

## Escalation
Escalate if the task definition is centrally managed, credentials/service accounts fail, destination storage is unavailable, or the task succeeds but restore validation fails.
