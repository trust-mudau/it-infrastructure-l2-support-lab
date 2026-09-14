# KB-013 — QEMU qcow2 Snapshot/Rollback Validation

## Core commands
```bash
qemu-img info disk.qcow2
qemu-img snapshot -c clean-state disk.qcow2
qemu-img snapshot -l disk.qcow2
qemu-img snapshot -a clean-state disk.qcow2
qemu-img check disk.qcow2
```
`qemu-io` can be used in a lab to verify known block patterns before and after recovery.

## L2 decision point
Before any rollback, identify the recovery point objective, newer writes at risk, application consistency requirements, and approval owner.

## Scope statement
This lab demonstrates virtualization concepts and qcow2 snapshot mechanics only; do not translate it into unsupported claims of production VMware/Hyper-V experience.
