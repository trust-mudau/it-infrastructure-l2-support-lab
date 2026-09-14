# INC-013 — Virtual Disk State Corrupted After Change; Snapshot Recovery Required

**Priority:** P2  
**Category:** Virtualization / Snapshot / Recovery  
**Platform:** QEMU qcow2 tooling on Ubuntu 24.04  
**Status:** Lab validated  
**Execution:** https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34875963864

## Scope
This scenario demonstrates virtual-disk snapshot and rollback mechanics with QEMU qcow2. It is **not** a claim of production VMware or Hyper-V administration.

## Incident
An 8 MiB qcow2 virtual disk had a known-good block pattern (`0x41`). A `clean-state` internal snapshot was created. A simulated post-change corruption overwrote the active block with `0x42`, and validation of the original baseline failed.

## Recovery
Used `qemu-img snapshot -a clean-state` to revert the disk.

## Verification
`qemu-io` confirmed the original `0x41` pattern returned, `qemu-img check` passed, and the named snapshot remained identifiable.

## Escalation
In production, snapshot rollback requires change approval and data-loss assessment when newer writes may need preservation.
