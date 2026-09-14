# INC-002 — Windows Application Reachable by IP but Not by Hostname

**Priority:** P2  
**Category:** Windows / Networking / Name resolution  
**Platform:** GitHub-hosted Windows Server 2025 runner  
**Status:** Lab validated — resolved  
**Execution:** GitHub Actions run `34872487525`

## User / business impact

A support application remained healthy and reachable directly by IP, but users could not access it by the expected hostname. This isolated the incident away from a total application outage and toward the name-resolution/connectivity path.

## Initial symptoms

- direct IP HTTP request succeeded with status `200`
- application content was returned correctly
- hostname HTTP request failed with connection refused
- service was listening on `127.0.0.1:8080`

## Environment

- Windows Server 2025 Datacenter hosted runner
- OS build: `26100`
- PowerShell: `7.6.5`
- service endpoint: `127.0.0.1:8080`
- expected hostname: `support-app.lab`

## Investigation performed

### 1. Verified the application itself

Direct IP access succeeded:

```text
Direct IP status: 200
Direct IP content: Support application healthy - scenario 02
```

This demonstrated that the local service process and TCP listener were healthy.

### 2. Reproduced the hostname failure

The request to the expected hostname failed:

```text
Hostname request failed as reported.
Exception type: System.Net.Http.HttpRequestException
Message: No connection could be made because the target machine actively refused it. (support-app.lab:8080)
```

### 3. Checked the listening socket

Windows reported a listener on:

```text
127.0.0.1:8080
```

### 4. Inspected name resolution

The local hosts entry contained:

```text
127.0.0.2 support-app.lab
```

The standard .NET resolver also returned:

```text
127.0.0.2
```

### 5. Compared IP and hostname TCP tests

Direct IP test:

```text
RemoteAddress: 127.0.0.1
TcpTestSucceeded: True
```

Hostname test:

```text
RemoteAddress: 127.0.0.2
TcpTestSucceeded: False
```

This confirmed that name resolution was sending the client to the wrong endpoint while the actual application remained available.

## Root cause

**Confirmed root cause:** the local Windows hosts configuration mapped `support-app.lab` to `127.0.0.2`, while the healthy application listener was bound to `127.0.0.1:8080`.

The failure was therefore a local name-resolution configuration issue, not an application-process or listening-port failure.

## Corrective action

The incorrect local mapping was replaced with:

```text
127.0.0.1 support-app.lab
```

The Windows DNS resolver cache was then flushed successfully.

## Verification

Post-fix validation returned:

```text
Resolved address: 127.0.0.1
TCP test succeeded: True
HTTP status: 200
Application content verified: PASS
Scenario result: RESOLVED
```

## Escalation decision

**No escalation required.**

The issue was endpoint-local, the incorrect name mapping was within the lab technician's control, and the service was independently verified after correction.

Escalation would have been required if:

- the service was not listening
- direct IP connectivity also failed
- hostname resolution was correct but TCP still failed
- enterprise DNS outside endpoint control was returning the wrong record
- firewall or upstream network infrastructure appeared responsible

## Evidence

GitHub Actions run: `34872487525`  
Evidence artifact: `scenario-02-evidence`  
Artifact ID: `10359174408`  
Artifact SHA-256: `c7ec6efc81cd595ca9c1db35630d2fffecb099c3c1f6c458946695a9daf9615b`

## L2 skills demonstrated

- Windows PowerShell troubleshooting
- service/listener validation
- IP-versus-hostname fault isolation
- Windows TCP diagnostics with `Test-NetConnection`
- resolver/hosts-file inspection
- DNS cache flushing
- minimum-change remediation
- application-layer verification after network repair
- escalation judgement
- structured incident documentation
