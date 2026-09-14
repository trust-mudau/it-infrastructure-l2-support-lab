# KB-005 — systemd Scheduled Job Fails but Manual Script Run Succeeds

## Symptoms

A script succeeds from an administrator shell but fails when run by a `systemd` service or timer. The scheduled job may show a non-zero exit status and produce no expected output.

## Common cause

The interactive shell has environment variables, working-directory assumptions, PATH entries, credentials or profile settings that the `systemd` service does not inherit.

## Diagnostic workflow

### 1. Prove the script itself can work

Run the script manually with the required inputs and record the result.

Example:

```bash
sudo env BACKUP_DEST=/var/backups/l2support /opt/l2backup/run-backup.sh
```

If the manual run also fails, troubleshoot the script or dependencies first.

### 2. Confirm the scheduler actually fired

```bash
systemctl status l2backup.timer
systemctl list-timers l2backup.timer --all
```

Check the last-trigger time and the service the timer activates.

### 3. Inspect the service failure

```bash
systemctl status l2backup.service --no-pager -l
journalctl -u l2backup.service --no-pager -n 60
```

Look for missing variables, command-not-found errors, permissions, unavailable paths or authentication failures.

### 4. Compare service configuration with manual execution

```bash
systemctl cat l2backup.service
systemctl show l2backup.service -p Environment -p EnvironmentFiles
```

Do not assume your shell variables exist inside the service.

### 5. Check filesystem access

```bash
ls -ld /opt/l2backup/source /var/backups/l2support
ls -l /opt/l2backup/source
```

This prevents misdiagnosing a permission issue as an environment issue.

## Remediation pattern

For non-secret configuration, use a controlled environment file:

```ini
[Service]
EnvironmentFile=/etc/l2backup/backup.env
ExecStart=/opt/l2backup/run-backup.sh
```

Example file:

```text
BACKUP_DEST=/var/backups/l2support
```

Then reload and test:

```bash
sudo systemctl daemon-reload
sudo systemctl reset-failed l2backup.service
sudo systemctl start l2backup.service
```

For secrets, use the organization's approved secret-management mechanism rather than storing plaintext credentials in a public repository or world-readable configuration file.

## Verification

Do not close a backup incident after the service merely reports success. Verify the backup is usable.

```bash
sha256sum -c l2support-backup.tar.gz.sha256
mkdir /tmp/restore-test
tar -xzf l2support-backup.tar.gz -C /tmp/restore-test
diff -ru /source/path /tmp/restore-test
```

A good L2 closure confirms scheduler execution, artifact creation, integrity and recoverability.

## Escalate when

- required values are centrally managed or secret-owned
- a remote/cloud backup destination is unavailable
- the scheduler is controlled by another team
- credentials have expired
- the corrected execution context still fails
- checksum or restore validation fails
- policy prevents the proposed configuration change

## Related incident

`INC-005 — Scheduled Backup Job Fails While Manual Run Succeeds`
