# RCA — INC-004 Linux Disk Exhaustion

## Incident summary

A `systemd`-managed Linux application failed during startup because the application filesystem had no remaining block capacity. The condition was reproduced and resolved on a GitHub-hosted Ubuntu 24.04.5 LTS environment.

## Impact

The application process exited before it could begin listening on TCP `8091`. Users would have experienced a connection failure until storage capacity was recovered and the service restarted.

## Detection

The incident was confirmed by three independent symptoms:

1. `systemctl is-active l2storage.service` returned a non-active result.
2. HTTP connectivity to `127.0.0.1:8091` failed.
3. `journalctl` recorded `No space left on device` while the service attempted to create its startup cache.

## Technical timeline

### Failure state

The isolated application filesystem was a 20 MiB `tmpfs`.

An 18 MiB stale application log already occupied most of the filesystem. The application attempted to create a 4 MiB startup cache.

The write stopped after approximately 2 MiB because the filesystem reached 100% utilization.

### Evidence gathered before remediation

The investigation used:

- `systemctl status`
- `journalctl -u`
- `mount`
- `df -h`
- `df -B1`
- `df -i`
- `du -xh`
- `find ... -printf`
- `ps`
- `ss -ltnp`

`df` confirmed 20 MiB used with zero space available. `df -i` showed only 1% inode utilization. This separated block-capacity exhaustion from inode exhaustion.

`du` and `find` identified `/mnt/l2lab-disk/logs/application.log` as the dominant storage consumer at 18,874,368 bytes.

## Root cause

The direct root cause was **filesystem block-capacity exhaustion caused by an oversized stale application log**.

The service itself and its `systemd` definition were not the source of the fault. The service failed because its normal runtime write could not complete.

## Contributing condition

The scenario represents an environment where log growth is not sufficiently bounded by rotation, retention or capacity monitoring.

In a real environment, this would prompt a follow-up review of log rotation, alert thresholds and storage-growth trends rather than treating manual cleanup as the permanent solution.

## Corrective action

After confirming that the stale log was the approved cleanup target, the log was reduced from 18 MiB to 1 MiB. The service was restarted.

No application-code or service-unit change was made.

## Verification

Post-remediation evidence showed:

- filesystem utilization: `25%`
- inode utilization: `1%`
- startup cache size: `4,194,304` bytes
- service state: `active`
- TCP `8091`: listening
- expected HTTP content: returned successfully

## Escalation judgement

No escalation was required in the controlled lab because the technician had authority to clean the synthetic stale log and the service recovered after the local correction.

Escalation would be appropriate when:

- logs are subject to retention or legal-hold requirements
- the storage volume requires expansion by another infrastructure team
- capacity immediately rises again after cleanup
- filesystem or kernel logs suggest I/O errors or corruption
- the largest consumer cannot be attributed safely
- the application still fails after adequate free space is restored

## Preventive recommendations

- configure and test log rotation
- establish disk-capacity warning and critical thresholds
- monitor growth rate, not only current percentage
- define retention ownership before incidents occur
- alert on failed runtime writes and repeated service restarts
- document approved cleanup locations and escalation boundaries

## Skills demonstrated

Linux storage troubleshooting, `df`, inode analysis, `du`, file-size analysis, `systemd`, `journalctl`, service recovery, root-cause analysis, risk-aware cleanup, independent verification and escalation judgement.
