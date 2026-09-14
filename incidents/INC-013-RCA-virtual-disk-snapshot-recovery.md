# RCA — INC-013 Virtual Disk Snapshot Recovery

## Summary
A virtual disk's active state no longer matched a pre-change baseline after a simulated change.

## Evidence
- qcow2 image created with `qemu-img`
- baseline pattern written and verified with `qemu-io`
- internal snapshot `clean-state` captured
- post-change pattern `0x42` verified
- baseline `0x41` check failed before rollback

## Recovery action
Activated the known-good `clean-state` snapshot.

## Verification
The original block pattern was restored and `qemu-img check` reported image consistency.

## Operational lesson
A snapshot can accelerate rollback but is not a substitute for backup. Before rollback, determine whether newer data must be preserved and whether the application/database requires an application-consistent recovery method.
