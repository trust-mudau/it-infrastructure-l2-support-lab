# INC-003 — Linux Service Fails to Start

**Priority:** P2  
**Category:** Linux / systemd / service availability  
**Platform:** GitHub-hosted Ubuntu runner  
**Status:** Scenario configured — execution evidence pending

## User / business impact

A small internal application is unavailable after a deployment. Users receive connection errors and the expected TCP port is not listening. The service is managed by `systemd`, so the support engineer must determine whether the failure is caused by the application, service definition, permissions, process state, port binding or another OS-level condition.

## Initial symptoms

- application endpoint is unavailable
- `systemd` service does not remain active
- expected TCP port `8090` is not listening

## Known environment

- Ubuntu GitHub-hosted runner
- service name: `l2support.service`
- application path: `/opt/l2lab/service.sh`
- application content path: `/opt/l2lab/www`
- expected endpoint: `http://127.0.0.1:8090/`

## L2 objective

Reproduce the service-start failure, gather evidence before remediation, use `systemctl` and `journalctl` to identify the root cause, apply the minimum safe change, restart the service and independently verify application availability.

## Investigation requirements

Capture at minimum:

- OS and kernel
- service status
- service unit contents
- recent journal entries
- process state
- listening ports
- file ownership and permissions
- corrective action
- post-fix service state
- HTTP verification

## Escalation rule

Escalate if the service definition and local permissions are correct but the process still crashes, if logs indicate an application defect, if required dependencies are unavailable, if the port is owned by an unrelated critical service, or if remediation requires a change outside the technician's authorization.

## Evidence location

The workflow will upload a `scenario-03-evidence` artifact after execution.
