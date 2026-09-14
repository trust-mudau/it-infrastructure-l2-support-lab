# KB-011 — Windows Scheduled Task Runs but Backup Is Missing

## Checks
```powershell
Get-ScheduledTask -TaskName <name>
(Get-ScheduledTask -TaskName <name>).Actions
Get-ScheduledTaskInfo -TaskName <name>
```
Then inspect the script's own log, execution identity, arguments, destination access, and resulting archive.

## Verification standard
A backup ticket is not complete when the task merely returns success. Verify archive existence/integrity and perform a restore test to a separate location where practical.

## Common causes
Missing parameters, different working directory, wrong execution account, inaccessible network path, environment variables absent in non-interactive execution, and quota/storage failures.
