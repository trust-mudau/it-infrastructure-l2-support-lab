# INC-004 — Linux Disk Exhaustion Causes Application Startup Failure

**Priority:** P2  
**Category:** Linux / Storage / Service availability  
**Platform:** GitHub-hosted Ubuntu runner  
**Status:** Scenario configured — execution evidence pending

## User / business impact

An internal application fails to start after its local application filesystem becomes nearly full. The service is unavailable and the expected TCP port is not listening. The support engineer must determine whether the failure is caused by application code, service configuration, storage capacity, inode exhaustion, permissions, or another OS-level condition.

## Initial symptoms

- systemd-managed application does not remain active
- expected application port is not listening
- recent log growth is suspected
- application startup requires writing runtime data to the same filesystem

## Known environment

- Ubuntu GitHub-hosted runner
- isolated 20 MiB `tmpfs` mounted at `/mnt/l2lab-disk`
- application log path: `/mnt/l2lab-disk/logs/application.log`
- runtime data path: `/mnt/l2lab-disk/data`
- service: `l2storage.service`
- expected endpoint: `http://127.0.0.1:8091/`

## L2 objective

Reproduce the service failure, gather evidence before making changes, distinguish block-capacity exhaustion from inode exhaustion and other failure classes, identify the largest storage consumer, apply a safe minimum cleanup action, restart the service, and independently verify capacity and application recovery.

## Investigation requirements

Capture at minimum:

- OS and kernel
- service status and recent journal entries
- filesystem mount and capacity with `df`
- inode availability with `df -i`
- directory/file usage with `du` and `find`
- largest storage consumer
- process and listening-port state
- corrective action
- post-fix capacity
- service and HTTP verification

## Escalation rule

Escalate if capacity remains critically high after approved cleanup, the largest files cannot be removed because of retention/compliance requirements, inode exhaustion is caused by an unknown process, the filesystem reports I/O errors or corruption, storage expansion is required outside the technician's authorization, or the service still fails after adequate free space is restored.

## Evidence location

The workflow will upload a `scenario-04-evidence` artifact after execution.
