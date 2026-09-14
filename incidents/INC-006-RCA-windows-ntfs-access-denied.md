# RCA — INC-006 Windows NTFS Access Denied

## Incident summary

An approved support account could not read a protected support file even though it belonged to the expected `L2-App-Support` local group and that group had `Modify` access.

## Impact

The account was unable to access application-support data required for troubleshooting. The failure was limited to the protected path used in the lab.

## Detection

The issue was reproduced with:

```powershell
Get-Content C:\l2lab\secure-data\support-notes.txt
```

The command returned an access-denied error.

## Evidence gathered

The investigation used:

```powershell
whoami
whoami /groups
Get-LocalGroup -Name L2-App-Support
Get-LocalGroupMember -Group L2-App-Support
Get-Acl C:\l2lab\secure-data
Get-Acl C:\l2lab\secure-data\support-notes.txt
icacls C:\l2lab\secure-data
icacls C:\l2lab\secure-data\support-notes.txt
```

The current account was confirmed as a member of `L2-App-Support`. The ACL contained both:

- an explicit direct `ReadData` deny for the user
- an allow `Modify` ACE for `L2-App-Support`

## Root cause

The direct explicit deny ACE on the user overrode access granted through the local group.

This explains why simply confirming group membership was insufficient. The problem was not missing group membership; it was ACL precedence.

## Corrective action

The specific direct deny rule was identified and removed with PowerShell while preserving the group-based `Modify` rule.

The remediation followed least privilege:

- no `Everyone:FullControl`
- no broad administrator grant
- no ownership takeover
- no unrelated ACL reset

## Verification

After remediation:

- `Get-Content` successfully read the protected file
- `Add-Content` successfully modified it
- the current account remained in `L2-App-Support`
- the group-based `Modify` allow ACE remained present
- no direct deny for the current account remained

## Escalation decision

No escalation was required because the cause was local, understood, reversible, and within the lab's authorization boundary.

Escalation would be appropriate if:

- the deny ACE came from Group Policy or centralized configuration management
- the deny existed for a compliance/security reason
- ownership or ACL authority belonged to another team
- the user was accessing regulated data outside their approved role
- access still failed after the local ACL conflict was corrected

## Preventive actions

- prefer role/group-based permissions over direct user ACEs
- avoid mixing direct user denies with group-based allow models unless policy requires it
- document any intentional deny ACEs and their business justification
- when troubleshooting Access Denied, inspect the complete ACL rather than assuming group membership guarantees access
- verify the final effective behavior after every permission change

## Evidence reference

GitHub Actions run: `34874603327`  
Artifact: `scenario-06-evidence`  
Artifact ID: `10360990929`
