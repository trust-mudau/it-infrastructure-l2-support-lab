# RCA — INC-003 Linux systemd Service Failure

## Executive summary

A `systemd`-managed internal application failed to start on an Ubuntu 24.04.5 LTS lab host. The service unit loaded successfully, but the configured `ExecStart` target did not have execute permission. `systemd` therefore terminated the process with `status=203/EXEC`, leaving TCP port `8090` unavailable.

The issue was resolved by restoring execute permission to the service script and restarting the unit. Recovery was verified independently through service state, socket inspection and an HTTP request.

## Incident classification

- **Severity:** P2 lab incident
- **Platform:** Ubuntu 24.04.5 LTS
- **Service manager:** systemd
- **Service:** `l2support.service`
- **Affected endpoint:** `127.0.0.1:8090`
- **Resolution type:** Local OS permission correction

## Timeline

1. Lab service and unit were deployed.
2. `/opt/l2lab/service.sh` was intentionally left at mode `0644`.
3. `systemctl start l2support.service` was issued.
4. Service entered failed state.
5. HTTP validation failed and port `8090` was unavailable.
6. `systemctl status` and `journalctl` showed `203/EXEC`.
7. Unit configuration confirmed `ExecStart=/opt/l2lab/service.sh`.
8. `stat` and `ls -l` confirmed the file existed but was not executable.
9. Mode was corrected to `0755`.
10. Service was restarted.
11. Service state, listening port and HTTP response all passed validation.
12. Evidence was uploaded and temporary lab resources were removed.

## Evidence supporting root cause

### Service-manager evidence

`systemctl status` reported:

```text
Active: failed (Result: exit-code)
Process: ... ExecStart=/opt/l2lab/service.sh (code=exited, status=203/EXEC)
Main PID: ... (code=exited, status=203/EXEC)
```

`journalctl` recorded:

```text
l2support.service: Main process exited, code=exited, status=203/EXEC
l2support.service: Failed with result 'exit-code'.
```

### Unit-file evidence

```ini
[Service]
Type=simple
ExecStart=/opt/l2lab/service.sh
Restart=no
User=root
```

### File-permission evidence

```text
-rw-r--r-- root root /opt/l2lab/service.sh
Access: (0644/-rw-r--r--)
```

The parent path was traversable, the file existed, and the service unit pointed to the correct location. The missing execute bit was therefore the direct cause.

## Root cause

The deployment left `/opt/l2lab/service.sh` without execute permission. Since the file was the `ExecStart` target, `systemd` could not launch it and returned `203/EXEC`.

## Contributing factors

- deployment validation did not confirm executable permissions
- service health was not validated immediately after deployment
- the unit was syntactically valid, which could mislead a technician into focusing only on the service definition rather than the target file

## Corrective action

```bash
sudo chmod 0755 /opt/l2lab/service.sh
sudo systemctl restart l2support.service
```

The change was intentionally limited to the confirmed fault. No unrelated permissions, service configuration or application code were modified.

## Recovery verification

After remediation:

- `systemctl is-active l2support.service` returned `active`
- `ss -ltnp` showed `python3` listening on `127.0.0.1:8090`
- `curl http://127.0.0.1:8090/` returned the expected application content

This provided three independent validation layers: process manager, network socket and application response.

## Preventive recommendations

1. Validate executable ownership and mode as part of deployment checks.
2. Run a post-deployment `systemctl is-active` health check.
3. Capture `systemctl status` and `journalctl -u` output before making service changes.
4. Validate the configured `ExecStart` path with `systemctl cat`, `stat` and `namei` when `203/EXEC` occurs.
5. Avoid broad permission changes such as `chmod 777`; apply only the permissions required for the service to operate.

## Escalation analysis

Escalation was unnecessary because the fault was fully isolated to a local permission issue, the correction was within support scope and recovery was independently verified.

Escalation would be warranted if `203/EXEC` continued despite correct path and permissions, because further causes could include a bad interpreter, incompatible executable format, mandatory access controls or a product defect.
