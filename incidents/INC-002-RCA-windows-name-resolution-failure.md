# INC-002 Root Cause Analysis — Windows Name Resolution Failure

## Incident summary

A Windows-hosted support application was healthy and reachable by IP address, but failed when accessed through its expected hostname. The incident was reproduced and resolved on a GitHub-hosted Windows Server 2025 runner.

## Impact

Users relying on the hostname could not access the service even though the application process and listener remained healthy.

## Detection

Direct IP access returned HTTP `200`, while hostname access failed with a connection-refused error.

## Technical findings

### Healthy service path

The application responded successfully at:

```text
127.0.0.1:8080
```

`Test-NetConnection` confirmed TCP connectivity to `127.0.0.1:8080`.

### Faulted name-resolution path

The Windows hosts file contained:

```text
127.0.0.2 support-app.lab
```

The standard resolver returned `127.0.0.2`, and `Test-NetConnection support-app.lab -Port 8080` showed:

```text
RemoteAddress: 127.0.0.2
TcpTestSucceeded: False
```

The service listener itself remained on `127.0.0.1:8080`.

## Root cause

The local hostname mapping pointed the client to the wrong loopback address. As a result, hostname-based traffic was sent to `127.0.0.2`, where no application listener existed.

## Resolution

The mapping was corrected to:

```text
127.0.0.1 support-app.lab
```

The Windows DNS resolver cache was then flushed.

## Verification

Post-fix validation confirmed:

- resolver returned `127.0.0.1`
- TCP test by hostname succeeded
- HTTP request by hostname returned `200`
- expected application content was returned

Final result:

```text
Scenario result: RESOLVED
```

## Escalation decision

No escalation was required because the problem was isolated to endpoint-local configuration and was resolved within scope.

Escalation would have been appropriate if:

- the listener was absent
- direct IP access also failed
- hostname resolution was correct but connectivity still failed
- the wrong record came from managed enterprise DNS
- upstream firewall or routing evidence indicated infrastructure outside endpoint control

## Preventive actions

- document expected hostname-to-address mappings
- avoid unnecessary local hosts-file overrides in managed environments
- clear stale resolver state after approved name-resolution changes
- compare direct-IP and hostname tests when isolating application-access incidents
- verify service restoration at both transport and application layers

## Evidence

- GitHub Actions run: `34872487525`
- artifact: `scenario-02-evidence`
- artifact ID: `10359174408`
- platform: Windows Server 2025 Datacenter
- PowerShell version: `7.6.5`

## L2 support takeaway

The important troubleshooting step was separating application health from name-resolution health. Because direct IP access succeeded and the listener was present, the investigation could focus on how the hostname resolved rather than restarting the application or changing unrelated firewall settings.
