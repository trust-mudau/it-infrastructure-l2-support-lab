# INC-006 — Windows NTFS Access Denied Despite Correct Group Membership

**Priority:** P2  
**Category:** Windows / Local groups / NTFS permissions / Access control  
**Platform:** GitHub-hosted Windows runner  
**Status:** Scenario configured — execution evidence pending

## User / business impact

A support technician is a member of the approved local support group but receives **Access Denied** when attempting to read a protected application-support file. Other system functions remain healthy. The incident requires distinguishing group membership problems from NTFS ACL inheritance, explicit deny entries, ownership, path issues, and application-layer errors.

## Initial symptoms

- approved support group exists
- technician is a member of that group
- group has an allow permission on the support folder
- direct file access fails with Access Denied
- no evidence of disk or service failure

## Known environment

- GitHub-hosted Windows Server runner
- protected path: `C:\l2lab\secure-data`
- protected file: `support-notes.txt`
- local group: `L2-App-Support`
- current runner account is added to the group
- group receives an NTFS allow ACE
- an intentional explicit deny ACE is applied directly to the current account

## L2 objective

Reproduce the access failure, capture identity and local-group evidence, inspect effective ACL structure with PowerShell and `icacls`, identify why the expected group-based allow is not sufficient, apply the minimum least-privilege correction, and independently verify that access is restored without granting administrative or broad Everyone permissions.

## Investigation requirements

Capture at minimum:

- Windows edition/version
- current identity
- local support-group membership
- folder and file ACLs
- `icacls` output
- inheritance state
- failed access result
- confirmed conflicting ACE
- corrective action
- post-fix ACL
- successful read/write verification
- escalation decision

## Escalation rule

Escalate if the deny ACE is required by policy, the ACL is centrally managed by Group Policy or another configuration-management system, ownership is controlled by another team, the path contains regulated/sensitive data outside technician authorization, access remains denied after the ACL is corrected, or a domain/identity issue is suspected beyond the local system.

## Evidence location

The workflow will upload a `scenario-06-evidence` artifact after execution.
