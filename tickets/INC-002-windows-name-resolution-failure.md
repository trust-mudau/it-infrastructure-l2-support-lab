# INC-002 — Windows Application Reachable by IP but Not by Hostname

**Priority:** P2  
**Category:** Windows / Networking / Name resolution  
**Platform:** GitHub-hosted Windows runner  
**Status:** Scenario configured — execution evidence pending

## User / business impact

A support application is running locally and responds when accessed directly by IP address, but users cannot reach it by its expected hostname. The application itself appears healthy, so the incident requires the support engineer to isolate whether the failure is at the application, port, IP, DNS/name-resolution or host-configuration layer.

## Initial symptoms

- direct IP connection succeeds
- hostname connection fails
- application process remains running
- expected TCP port is listening

## Known environment

- Windows hosted runner
- local web service bound to `127.0.0.1:8080`
- expected hostname: `support-app.lab`
- Windows hosts file used to create a controlled name-resolution fault

## L2 objective

Determine whether the incident is caused by application failure, port failure, local firewall/network path, or incorrect hostname resolution. Gather evidence before changing configuration, apply the smallest safe correction, flush stale resolver state where appropriate, and independently verify access by hostname.

## Investigation requirements

Capture at minimum:

- Windows version / PowerShell version
- local IP configuration
- active listening port
- direct IP connectivity result
- hostname resolution result
- hostname connectivity result
- relevant hosts-file entry
- corrective action
- post-fix resolution and HTTP verification

## Escalation rule

Escalate if the service is not listening, direct IP access also fails after confirming the process is running, the hosts/DNS result is correct but hostname connectivity still fails, the issue is controlled by enterprise DNS outside the technician's authorization, or evidence suggests firewall/network infrastructure outside the endpoint.

## Evidence location

The GitHub Actions workflow will upload a `scenario-02-evidence` artifact after execution.
