# KB-004 — Linux Service Fails Because Filesystem Is Full

## Symptoms

Common symptoms include:

- application fails to start or crashes unexpectedly
- `systemctl status` shows the service as failed
- `journalctl` reports `No space left on device`
- expected TCP port is not listening
- application cannot create logs, cache, PID/state or temporary files

## First response

Do not delete files immediately. Capture evidence first and determine whether the failure is caused by block capacity, inode exhaustion, permissions, filesystem errors, or another condition.

## Diagnostic workflow

### 1. Confirm service failure

```bash
systemctl status <service> --no-pager -l
journalctl -u <service> --no-pager -n 100
```

Look for write failures, exit codes and the exact path associated with the error.

### 2. Check filesystem block capacity

```bash
df -h
```

For the affected mount specifically:

```bash
df -h /path/to/application/storage
```

A filesystem at or near 100% utilization may prevent applications from creating required runtime data.

### 3. Check inode capacity separately

```bash
df -i /path/to/application/storage
```

A filesystem can have free bytes but still reject new files if all inodes are exhausted. Conversely, healthy inode availability helps rule that condition out.

### 4. Identify the largest directories

```bash
sudo du -xh --max-depth=2 /path/to/application/storage | sort -h
```

This narrows the search before making any changes.

### 5. Identify the largest files

```bash
sudo find /path/to/application/storage -type f -printf '%s %p\n' | sort -nr | head -20
```

Confirm ownership, purpose and retention requirements before deleting or truncating anything.

### 6. Check application/process state

```bash
ps -ef | grep <process-name>
sudo ss -ltnp
```

This helps confirm whether the application is running and whether the expected network listener exists.

## Remediation principles

Use the minimum safe action that addresses the confirmed cause.

Possible actions include:

- rotate or archive logs according to policy
- remove approved temporary/cache files
- clean package caches where appropriate
- increase filesystem capacity through the correct infrastructure process
- correct a runaway logging condition

Do not remove unknown files merely to make space.

## Verification

After remediation:

```bash
df -h /path/to/application/storage
df -i /path/to/application/storage
sudo systemctl restart <service>
systemctl is-active <service>
sudo ss -ltnp
```

Then perform an application-level health check rather than relying only on `systemctl`.

For an HTTP service:

```bash
curl -fsS http://127.0.0.1:<port>/
```

A complete resolution should prove both **capacity recovery** and **application recovery**.

## Escalate when

- cleanup conflicts with retention/compliance requirements
- storage growth is unexplained or immediately recurs
- expansion requires another team's authorization
- `dmesg`/system logs indicate I/O or filesystem corruption
- inode exhaustion is caused by an unknown process
- the application remains unavailable after sufficient capacity is restored

## Lab example

In INC-004, a 20 MiB isolated filesystem reached 100% utilization because an 18 MiB stale log consumed most of the capacity. Inodes remained at 1% utilization. Reducing the approved stale log to 1 MiB restored sufficient capacity; filesystem utilization fell to 25%, the service started, its 4 MiB runtime cache was created and the HTTP health check passed.
