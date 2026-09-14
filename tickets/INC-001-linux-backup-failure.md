# INC-001 — Linux Backup Job Failure

**Priority:** P2  
**Category:** Backup / Linux permissions  
**Platform:** GitHub-hosted Ubuntu 24.04.5 runner  
**Status:** Lab validated — resolved  
**Execution:** GitHub Actions run `34871967005`

## User / business impact

The scheduled backup job for a small Linux-hosted service failed. Source data remained available, but no new recovery point could be created while the destination was unwritable. If left unresolved, the recovery-point objective would be missed.

## Initial symptoms

The backup script exited non-zero and no new archive was written to the destination directory.

## Environment

- Runner OS: Ubuntu 24.04.5 LTS
- Source: generated lab data under `lab/source`
- Destination: `lab/backup`
- Backup utility: `scripts/bash/backup.sh`
- Expected output: compressed `.tar.gz` archive plus SHA-256 checksum

## Investigation performed

Evidence was gathered before changing configuration.

### 1. Reproduced the failure

The backup command returned:

```text
ERROR: backup destination is not writable
Observed exit code: 13
```

### 2. Checked executing identity

```text
uid=1001(runner) gid=1001(runner)
```

### 3. Checked directory permissions

The destination was confirmed as:

```text
dr-xr-xr-x  lab/backup
Access: (0555/dr-xr-xr-x)
Owner: runner
Group: runner
```

The executing identity owned the directory but had no write bit.

### 4. Ruled out filesystem capacity

The filesystem had approximately 87 GB available and was 41% used, so disk exhaustion was not the cause.

### 5. Confirmed source data was present

The two expected source files were present and readable:

- `app.conf`
- `customers.csv`

## Root cause

**Confirmed root cause:** the backup destination existed but was configured with mode `0555`, which removed write permission from the account executing the backup job.

The failure was therefore a local filesystem-permission issue, not a capacity, source-data, archive-command or storage-corruption issue.

## Corrective action

Applied the minimum lab correction required to permit the service account to write while avoiding world-writable permissions:

```bash
chmod 0750 lab/backup
```

The backup was then rerun.

## Verification

The rerun created:

```text
support-backup-20260914T165958Z.tar.gz
support-backup-20260914T165958Z.tar.gz.sha256
```

Independent verification completed successfully:

- backup rerun: **PASS**
- SHA-256 checksum: **PASS**
- archive extraction: **PASS**
- restored-data comparison against source: **PASS**
- final scenario result: **RESOLVED**

## Escalation decision

**No escalation required.**

The fault was isolated to a local permission configuration, the minimum corrective action restored the backup operation, and both integrity and recovery were independently verified. Escalation would have been required if the backup still failed after permissions were corrected, if checksum/restore validation failed, or if evidence suggested storage corruption or a product defect.

## Evidence

GitHub Actions run: `34871967005`  
Evidence artifact: `scenario-01-evidence`  
Artifact ID: `10359781568`  
Artifact retention: 30 days from execution

The artifact contains the failed command output, exit code, investigation output, successful backup output, checksum verification, restore comparison and final verification summary.

## L2 skills demonstrated

- failure reproduction before remediation
- Linux identity and permission analysis
- filesystem-capacity checks
- evidence-first troubleshooting
- hypothesis elimination
- minimum-change remediation
- backup integrity validation
- restore testing
- escalation judgement
- incident documentation
