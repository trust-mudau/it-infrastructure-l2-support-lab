# RCA — INC-011 Windows Scheduled Backup Failure

## Root cause
The Scheduled Task action launched `backup.ps1` without the required `BackupRoot` parameter. The script exited with code 23 and no archive was generated.

## Corrective action
Re-registered the task action under the same SYSTEM principal with the explicit approved backup destination.

## Verification
The corrected scheduled execution returned `LastTaskResult 0`, generated the ZIP archive, produced a SHA-256 hash, and passed a separate restore/file-list test.

## L2 lesson
A script that is valid in isolation can fail under Task Scheduler because arguments, environment, working directory, identity, or permissions differ. Always inspect the actual scheduled action and runtime result instead of assuming script logic is broken.
