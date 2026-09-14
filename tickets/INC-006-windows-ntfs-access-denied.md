# INC-006 — Windows NTFS Access Denied Despite Correct Group Membership

**Priority:** P2  
**Category:** Windows / Local groups / NTFS permissions / Access control  
**Platform:** GitHub-hosted Windows Server 2025 Datacenter runner  
**Status:** **Lab validated — resolved**

## User / business impact

A support technician was a member of the approved local support group but received **Access Denied** when attempting to read protected application-support data.

## Executed symptoms

- local group `L2-App-Support` existed
- current account was confirmed as a member of the group
- the group had an NTFS `Modify` allow ACE
- `Get-Content` against `C:\l2lab\secure-data\support-notes.txt` failed with `Access to the path ... is denied`
- no disk, service, or path-availability issue was involved

## Investigation performed

The lab captured:

- Windows Server 2025 Datacenter / build 26100
- current Windows identity
- `whoami /groups`
- local-group configuration and membership
- folder and file ACLs with `Get-Acl`
- access rules including inheritance and allow/deny types
- `icacls` output for both directory and file

The investigation confirmed a direct explicit deny ACE:

```text
runneradmin:(OI)(CI)(DENY)(RD)
```

while the approved group retained:

```text
L2-App-Support:(OI)(CI)(M)
```

The direct deny took precedence over access granted through group membership.

## Root cause

A direct explicit `ReadData` deny ACE was assigned to the current user. That deny overrode the user's group-based allow permission and caused the observed access failure.

## Corrective action

Removed **only** the conflicting direct deny ACE.

No `Everyone` permission, broad Full Control grant, administrator bypass, ownership takeover, or unrelated ACL redesign was used.

The approved `L2-App-Support` group retained its `Modify` permission.

## Independent verification

Post-remediation checks confirmed:

- approved group membership: **PASS**
- direct deny removed: **PASS**
- group-based Modify grant preserved: **PASS**
- protected file read: **PASS**
- protected file write: **PASS**
- final scenario result: **RESOLVED**

## Escalation decision

**No escalation required.**

The cause was a local ACL conflict, the minimum correction was within lab authorization, and access was restored without broadening permissions.

Escalation would have been required if the deny was policy-mandated, centrally managed, involved regulated data outside technician scope, or if access remained broken after the local ACL conflict was corrected.

## Evidence

GitHub Actions run:

`https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34874603327`

Uploaded artifact:

`scenario-06-evidence` — artifact ID `10360990929`

Evidence includes the failed access output, environment details, identity/group/ACL investigation, corrective action, final verification, and incident summary.
