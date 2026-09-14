# INC-001 — Linux Backup Job Failure

**Priority:** P2  
**Category:** Backup / Linux permissions  
**Platform:** Ubuntu hosted runner  
**Status:** Scenario configured — execution evidence pending

## User / business impact

The scheduled backup job for a small Linux-hosted service reports failure. The source data remains available, but no new recovery point is being created. If the condition persists, the recovery-point objective will be missed.

## Initial symptoms

The backup command exits non-zero and no new archive appears in the destination directory.

## Known environment

- Linux host: ephemeral GitHub-hosted Ubuntu runner
- Source: generated lab data under `lab/source`
- Destination: `lab/backup`
- Backup utility: `scripts/bash/backup.sh`
- Expected output: compressed `.tar.gz` archive plus SHA-256 checksum

## L2 objective

Determine whether the failure is caused by capacity, missing paths, permissions, command syntax or another environmental condition. Apply the minimum safe corrective action and verify that the backup is usable by restoring and comparing the data.

## Investigation requirements

Capture at minimum:

- current identity
- destination permissions
- filesystem capacity
- failed command output and exit code
- successful rerun output
- archive checksum verification
- restore verification

## Escalation rule

Escalate if the backup still fails after the confirmed local filesystem/permission issue is corrected, if the archive cannot be verified/restored, or if evidence suggests underlying storage corruption or a product defect.

## Evidence location

The GitHub Actions workflow will upload a `scenario-01-evidence` artifact after execution.
