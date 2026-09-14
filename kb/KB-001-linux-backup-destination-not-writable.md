# KB-001 — Linux Backup Fails Because Destination Is Not Writable

## Purpose

Use this article when a Linux backup job fails because the destination directory exists but the backup process cannot write to it.

## Symptoms

Typical indicators include:

- backup exits non-zero
- no new archive is created
- logs report `permission denied` or `destination is not writable`
- source data remains readable

Example lab message:

```text
ERROR: backup destination is not writable
```

## Initial checks

### Confirm the executing identity

```bash
id
```

Determine which user and groups the backup process is actually running as.

### Check destination permissions and ownership

```bash
ls -ld /path/to/backup
stat /path/to/backup
```

Review:

- owner
- group
- user/group/other permission bits
- whether the executing identity has write access

### Check available capacity

```bash
df -h /path/to/backup
```

A write failure can be caused by permissions or by exhausted storage, so do not assume the cause from the first error message alone.

### Confirm source availability

```bash
find /path/to/source -maxdepth 1 -type f -ls
```

Confirm the expected data exists and is readable.

## Diagnosis

If the destination is owned by the service account but has a mode similar to:

```text
0555 / dr-xr-xr-x
```

then the directory does not grant write permission even to its owner.

That is sufficient to prevent new backup files from being created.

## Resolution approach

Determine the permissions required by policy and the backup process. Apply the minimum required change rather than making the directory broadly writable.

Lab example:

```bash
chmod 0750 /path/to/backup
```

Do **not** automatically use `chmod 777`. Broad write permissions can introduce unnecessary security risk.

Where ownership is wrong, investigate why before changing it. A possible correction may involve `chown`, but only after confirming the intended account and group.

## Verification

A successful command alone is not enough to prove backup health.

After remediation:

1. rerun the backup
2. confirm the expected archive exists
3. validate a checksum if available
4. extract the backup to a separate restore location
5. compare restored content against the source

Example commands:

```bash
sha256sum -c backup.tar.gz.sha256
mkdir -p /tmp/restore-test
tar -xzf backup.tar.gz -C /tmp/restore-test
diff -ru /path/to/source /tmp/restore-test
```

A clean comparison plus a valid checksum provides stronger closure evidence than simply seeing a successful backup exit code.

## Escalate when

Escalate to storage, platform or product engineering when:

- the destination is writable but the backup still fails
- filesystem or I/O errors appear
- checksum verification fails
- restored files are corrupted or incomplete
- permissions repeatedly revert without an identified cause
- the issue involves protected storage or permissions you are not authorized to modify
- evidence suggests a defect in the backup product

## Prevention

- monitor backup exit codes
- alert on failed scheduled jobs
- document the expected backup service account
- validate target ownership and permissions after system changes
- monitor free storage capacity
- perform periodic restore tests

## Lab validation

This article was derived from executed lab scenario `INC-001`, in which an Ubuntu-hosted runner reproduced a backup failure with destination mode `0555`, corrected it to `0750`, successfully reran the backup, passed SHA-256 verification and restored the source data without differences.
