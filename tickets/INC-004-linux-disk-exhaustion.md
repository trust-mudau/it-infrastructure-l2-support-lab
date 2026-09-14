# INC-004 — Linux Disk Exhaustion Causes Application Startup Failure

**Priority:** P2  
**Category:** Linux / Storage / Service availability  
**Platform:** GitHub-hosted Ubuntu 24.04.5 LTS runner  
**Status:** **Lab validated — resolved**

## User / business impact

An internal application failed to start because its local application filesystem was exhausted. The service was unavailable and TCP port `8091` was not listening.

## Environment

- Ubuntu 24.04.5 LTS
- isolated 20 MiB `tmpfs` mounted at `/mnt/l2lab-disk`
- application log: `/mnt/l2lab-disk/logs/application.log`
- runtime data: `/mnt/l2lab-disk/data/startup.cache`
- service: `l2storage.service`
- endpoint: `http://127.0.0.1:8091/`

## Reproduction

The lab intentionally created an 18 MiB stale application log on the 20 MiB filesystem. On startup, the service attempted to create a 4 MiB runtime cache.

Observed results:

- `systemctl start` returned control, but the service did not remain active
- `systemctl is-active` returned exit code `3`
- HTTP check returned exit code `7`
- `journalctl` recorded: `No space left on device`
- service exited with status `1/FAILURE`

## Investigation

Storage evidence showed:

```text
Filesystem  Size  Used  Avail  Use%
tmpfs        20M   20M      0  100%
```

Inode evidence showed only `1%` inode use, ruling out inode exhaustion.

Directory analysis showed:

```text
18M  /mnt/l2lab-disk/logs
2.0M /mnt/l2lab-disk/data
20M  /mnt/l2lab-disk
```

Largest-file analysis identified:

```text
18874368 /mnt/l2lab-disk/logs/application.log
2097152  /mnt/l2lab-disk/data/startup.cache
```

The partial 2 MiB startup cache was created before the write failed. No process remained active and no service was listening on TCP `8091`.

## Root cause

An oversized stale application log consumed most of the available block capacity. The application required additional space to create a 4 MiB runtime cache during startup, but the filesystem had reached 100% utilization.

This was **block-capacity exhaustion**, not inode exhaustion.

## Corrective action

Under the lab's approved cleanup condition, the stale log was reduced from:

- `18,874,368` bytes

to:

- `1,048,576` bytes

The service was then restarted.

## Independent verification

Post-remediation checks confirmed:

- service state: `active`
- `python3` listening on `127.0.0.1:8091`
- HTTP response: `L2 storage application healthy - scenario 04`
- runtime cache successfully created at `4,194,304` bytes
- filesystem use reduced from `100%` to `25%`
- inode use remained `1%`
- scenario result: `RESOLVED`

## Escalation decision

**No escalation required.** The local storage consumer was identified, the cleanup action was within lab authorization, sufficient capacity was restored, and the service was independently verified.

In a production environment, escalation would be required if cleanup conflicted with retention/compliance requirements, storage expansion required infrastructure-owner approval, I/O or filesystem errors were present, or the service continued to fail after capacity recovery.

## Evidence

GitHub Actions run:

`34873849178`

Evidence artifact:

`scenario-04-evidence`

Artifact SHA-256:

`31e0ff61d8c2b68ecf3a63fab5007614b63e63e378fbbb54ad644b6037b1a1a1`
