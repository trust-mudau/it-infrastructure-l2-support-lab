# KB-003 — Troubleshooting `systemd` Service Failures with `status=203/EXEC`

## Purpose

Use this article when a Linux service managed by `systemd` fails immediately and `systemctl status` reports `status=203/EXEC`.

## Typical symptoms

```text
Active: failed (Result: exit-code)
ExecStart=/path/to/service (code=exited, status=203/EXEC)
```

The application may be unavailable and its expected TCP port may not be listening.

## L2 troubleshooting sequence

### 1. Confirm service state

```bash
systemctl status SERVICE --no-pager -l
systemctl is-active SERVICE
```

Do not assume a successful `systemctl start` command means the service remained healthy. A service can start and then fail immediately.

### 2. Read the unit definition

```bash
systemctl cat SERVICE
```

Identify the exact `ExecStart` command and path.

### 3. Review service logs

```bash
journalctl -u SERVICE --no-pager -n 60 -o short-iso
```

Look for execution failures, interpreter errors, permission issues and repeated restarts.

### 4. Inspect the target path

```bash
ls -l /path/to/executable
stat /path/to/executable
namei -l /path/to/executable
```

Check:

- file exists
- execute bit is present where required
- ownership is appropriate
- every parent directory can be traversed
- the path in `ExecStart` is correct

### 5. Check interpreter / executable format

For scripts:

```bash
head -n 1 /path/to/script
which bash
which python3
```

A valid script normally requires a valid shebang such as:

```bash
#!/usr/bin/env bash
```

For binaries:

```bash
file /path/to/binary
ldd /path/to/binary
```

### 6. Check whether the application port is actually listening

```bash
ss -ltnp
```

If you know the port:

```bash
ss -ltnp | grep ':PORT'
```

### 7. Apply only the confirmed fix

If the root cause is missing execute permission, for example:

```bash
sudo chmod 0755 /path/to/service-script
sudo systemctl restart SERVICE
```

Do **not** use `chmod 777` as a generic fix.

### 8. Verify independently

Confirm at more than one layer:

```bash
systemctl is-active SERVICE
ss -ltnp | grep ':PORT'
curl -fsS http://127.0.0.1:PORT/
```

A complete validation should prove:

1. `systemd` sees the service as active.
2. the expected socket is listening.
3. the application responds correctly.

## Common causes of `203/EXEC`

- `ExecStart` file is not executable
- path in `ExecStart` is incorrect
- interpreter in the script shebang does not exist
- executable or script format is invalid
- parent-directory permissions prevent path traversal
- security controls such as SELinux/AppArmor prevent execution

## Escalate when

Escalate if:

- path and permissions are correct but `203/EXEC` persists
- logs indicate an application defect
- required runtime/interpreter is missing and installing it requires change approval
- mandatory access controls block execution outside your scope
- the executable may be corrupt or incompatible with the host architecture
- remediation requires modifying a production deployment outside your authorization

## Lab validation

This KB was produced from **INC-003** in the IT Infrastructure & L2 Technical Support Lab. The lab reproduced a real `systemd` `203/EXEC` failure, diagnosed it using `systemctl`, `journalctl`, `stat`, `namei`, process/socket checks, corrected the missing execute permission and verified recovery through service state, TCP listening state and HTTP response.
