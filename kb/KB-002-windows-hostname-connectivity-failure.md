# KB-002 — Windows Service Works by IP but Fails by Hostname

## Purpose

Use this article when a Windows-hosted service is reachable directly by IP address but fails when users connect through the expected hostname.

## Why this matters

If IP access works, the application and basic transport path may already be healthy. The fault can instead sit in name resolution, local hosts configuration, DNS, cached resolver state, or the mapping between the hostname and service address.

## Initial checks

### Verify direct IP access

```powershell
Test-NetConnection 127.0.0.1 -Port 8080
```

For HTTP services:

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8080/' -TimeoutSec 5
```

If this succeeds, avoid immediately restarting the application or changing firewall rules without evidence.

### Confirm the service is listening

```powershell
Get-NetTCPConnection -State Listen -LocalPort 8080
```

Check the exact local address and port.

### Test hostname resolution

```powershell
[System.Net.Dns]::GetHostAddresses('support-app.lab')
```

Compare the returned address with the address where the application is actually listening.

### Inspect the local hosts file

```powershell
Get-Content "$env:SystemRoot\System32\drivers\etc\hosts"
```

Look for local overrides that may supersede expected DNS resolution.

### Compare hostname TCP connectivity

```powershell
Test-NetConnection support-app.lab -Port 8080 -InformationLevel Detailed
```

Pay attention to:

- `RemoteAddress`
- `ResolvedAddresses`
- `TcpTestSucceeded`
- `NameResolutionSucceeded`

## Common interpretation

If the service listens on:

```text
127.0.0.1:8080
```

but the hostname resolves to:

```text
127.0.0.2
```

then name resolution is directing the connection to the wrong endpoint.

## Corrective action

Correct the name-resolution source that is actually responsible and that you are authorized to change.

For a local hosts-file issue, remove the incorrect mapping and add the correct one if policy requires a local override.

After an approved change, flush the local resolver cache:

```powershell
ipconfig /flushdns
```

## Verification

Do not stop at successful name resolution. Verify multiple layers:

```powershell
[System.Net.Dns]::GetHostAddresses('support-app.lab')
Test-NetConnection support-app.lab -Port 8080
Invoke-WebRequest -Uri 'http://support-app.lab:8080/' -TimeoutSec 5
```

A good closure check confirms:

1. hostname resolves to the intended address
2. TCP connection succeeds
3. the application returns the expected response

## Escalate when

Escalate when:

- the service is not listening
- direct IP connectivity also fails
- hostname resolution is correct but TCP still fails
- the wrong record is returned by enterprise DNS you do not administer
- firewall/routing evidence points outside the endpoint
- the name-resolution problem repeatedly returns without an identified local cause

## Lab validation

This article was derived from executed lab scenario `INC-002` on Windows Server 2025. The service returned HTTP `200` over `127.0.0.1`, while `support-app.lab` resolved to `127.0.0.2` and failed TCP connectivity. The local mapping was corrected to `127.0.0.1`, the DNS resolver cache was flushed, and post-fix TCP and HTTP tests both passed.
