# INC-003 — Linux Service Fails to Start

**Priority:** P2  
**Category:** Linux / systemd / service availability  
**Platform:** GitHub-hosted Ubuntu 24.04.5 LTS runner  
**Status:** **Lab validated — resolved**

## User / business impact

A small internal application was unavailable after a deployment. Users would have received connection errors because the `systemd`-managed process was not running and TCP port `8090` was not listening.

## Initial symptoms reproduced

- `systemctl start l2support.service` returned control, but the service immediately entered `failed`
- `systemctl is-active` returned non-active with exit code `3`
- HTTP request to `127.0.0.1:8090` failed with curl exit code `7`
- no process was serving the expected port

## Investigation

Evidence was gathered before remediation using:

```bash
systemctl status l2support.service --no-pager -l
systemctl cat l2support.service
journalctl -u l2support.service --no-pager -n 60 -o short-iso
ls -l /opt/l2lab/service.sh
stat /opt/l2lab/service.sh
namei -l /opt/l2lab/service.sh
ps -ef
ss -ltnp
```

### Key findings

`systemctl status` reported:

```text
Active: failed (Result: exit-code)
ExecStart=/opt/l2lab/service.sh (code=exited, status=203/EXEC)
```

`journalctl` confirmed the service's main process exited with `status=203/EXEC`.

The unit file referenced:

```text
ExecStart=/opt/l2lab/service.sh
```

The target file existed but had mode:

```text
-rw-r--r--
0644
```

Therefore the service target was present and readable, but not executable.

## Root cause

The `ExecStart` target `/opt/l2lab/service.sh` did not have execute permission. `systemd` could locate the file but could not execute it, causing the service to fail with `203/EXEC`.

## Corrective action

Applied the minimum required permission change:

```bash
sudo chmod 0755 /opt/l2lab/service.sh
sudo systemctl restart l2support.service
```

No application-code change or service-unit redesign was required.

## Verification

Post-remediation checks confirmed:

```text
Service state: active
Listening address: 127.0.0.1:8090
Application content verified: PASS
Scenario result: RESOLVED
```

An HTTP request returned:

```text
L2 support application healthy - scenario 03
```

## Escalation decision

**No escalation required.**

The fault was isolated to an OS-level execution-permission issue within the support scope. The service was restored using a low-risk local change and independently verified at the service, TCP-port and HTTP layers.

Escalation would have been appropriate if:

- the executable permission was correct but `203/EXEC` persisted
- logs indicated an application crash or dependency defect
- the required port was owned by an unrelated critical service
- remediation required an unauthorized production change

## Evidence

GitHub Actions run:

`https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34873490939`

Evidence artifact:

- `scenario-03-evidence`
- artifact ID: `10359952520`
- SHA-256 digest: `622d347a626c7b430e73828a29fa2fe05c93cae98d12eec46039fd25a0364b1f`

The lab environment was cleaned up after evidence capture.
