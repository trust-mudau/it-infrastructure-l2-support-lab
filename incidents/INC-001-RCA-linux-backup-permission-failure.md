# INC-001 Root Cause Analysis — Linux Backup Permission Failure

## Incident summary

A scheduled Linux backup operation failed because the configured backup destination was not writable by the account executing the job. The incident was reproduced on a GitHub-hosted Ubuntu 24.04.5 runner and resolved after the destination permission was corrected.

## Impact

- no new backup recovery point could be created during the fault condition
- source data remained available
- continued failure would have increased recovery risk by causing the expected recovery-point objective to be missed

## Detection

The backup script returned a non-zero exit code and reported that the destination was not writable.

Observed result:

```text
ERROR: backup destination is not writable
Observed exit code: 13
```

## Timeline

| Stage | Result |
|---|---|
| Scenario prepared | Backup destination intentionally set to mode `0555` |
| Failure reproduced | Backup returned exit code `13` |
| Evidence gathered | Identity, permissions, storage capacity, source files and failure output inspected |
| Cause confirmed | Executing account owned destination but lacked write permission |
| Remediation applied | Destination changed to mode `0750` |
| Backup rerun | Successful |
| Integrity verification | SHA-256 check passed |
| Recovery verification | Archive restored and restored files matched source |
| Escalation | Not required |

## Technical findings

### Executing identity

```text
uid=1001(runner) gid=1001(runner)
```

### Faulted destination

```text
dr-xr-xr-x  lab/backup
Access: (0555/dr-xr-xr-x)
Owner: runner
Group: runner
```

### Storage capacity

The filesystem had approximately 87 GB available and was only 41% utilized. Capacity was ruled out.

### Source validation

Both expected source files existed and were readable:

- `app.conf`
- `customers.csv`

## Root cause

The backup destination had permissions `0555`. This allowed read and execute access but denied write access to all classes, including the owning account. The backup script correctly detected the unwritable destination and exited with code `13`.

## Contributing factors

The lab incident represents a class of operational problems that can occur after:

- an incorrect `chmod`
- ownership/permission changes during deployment
- mount replacement with different permissions
- hardening activity that removes required service-account access

No evidence in this execution indicated storage exhaustion, source corruption or a defect in the backup utility.

## Resolution

The destination was changed to:

```bash
chmod 0750 lab/backup
```

This restored owner write access without making the backup directory world writable.

## Independent validation

The incident was not considered resolved simply because the backup command returned success.

Validation included:

1. confirmation that a new compressed archive existed
2. SHA-256 checksum verification
3. archive extraction into a separate restore location
4. recursive comparison of restored content with source content

Results:

```text
Checksum: PASS
Restore comparison: PASS
Scenario result: RESOLVED
```

## Escalation decision

No escalation was required because:

- the cause was isolated to a local filesystem configuration
- remediation was low risk and reversible
- the backup completed after remediation
- integrity validation passed
- actual recovery testing passed

Escalation would have been appropriate if the fault persisted after permission correction, the restored data differed from source, checksum verification failed, underlying storage errors appeared, or the problem pointed to a product defect.

## Preventive actions

- validate destination writability before scheduled backup execution
- alert on non-zero backup exit codes
- preserve and review backup-job logs
- monitor permissions/ownership on backup targets
- periodically perform restore tests rather than relying only on successful backup creation
- document expected service-account permissions

## Evidence

- GitHub Actions run: `34871967005`
- evidence artifact: `scenario-01-evidence`
- artifact ID: `10359781568`
- executed platform: Ubuntu 24.04.5 LTS hosted runner

## L2 support takeaway

The key L2 behavior demonstrated here is not the `chmod` command itself. It is the sequence of reproducing the fault, gathering evidence before changing the environment, ruling out competing causes, applying the smallest safe correction and independently proving recoverability before closing the incident.
