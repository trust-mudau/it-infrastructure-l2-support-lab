# KB-006 — Windows NTFS Access Denied Even When Group Membership Is Correct

## Purpose

Use this article when a Windows user belongs to the expected local/domain group but still receives **Access Denied** on a file or folder.

## Key principle

Correct group membership does **not** prove that effective access is correct.

NTFS authorization can still fail because of:

- explicit deny ACEs
- inherited denies
- conflicting direct user permissions
- missing inheritance
- incorrect path ACLs
- stale/incorrect group assumptions
- ownership or centrally managed policy

An explicit deny can override an allow inherited through group membership.

## Recommended L2 workflow

### 1. Confirm the exact identity

```powershell
whoami
whoami /groups
```

Do not troubleshoot a permissions problem until you know which security principal is actually being used.

### 2. Confirm expected group membership

```powershell
Get-LocalGroupMember -Group 'L2-App-Support'
```

For domain environments, use the organization's approved AD/Entra/domain tooling instead.

### 3. Capture the ACL before changing it

```powershell
Get-Acl 'C:\Path\To\Folder' | Format-List *
icacls 'C:\Path\To\Folder'
```

Inspect:

- identity reference
- allow vs deny
- inherited vs explicit
- inheritance flags
- rights granted/denied

### 4. Check both directory and file

```powershell
Get-Acl 'C:\Path\To\Folder'
Get-Acl 'C:\Path\To\Folder\file.txt'
icacls 'C:\Path\To\Folder\file.txt'
```

A correct parent ACL does not guarantee the child object has the expected permissions.

### 5. Look for explicit denies

Example:

```text
user:(DENY)(RD)
support-group:(M)
```

This is a strong indication that the direct user deny is overriding the group allow.

### 6. Apply the smallest authorized fix

Prefer removing the incorrect conflicting ACE rather than adding broader permissions.

Avoid shortcuts such as:

```text
Everyone: Full Control
```

unless there is an explicit approved requirement for that configuration.

### 7. Verify behavior, not just ACL text

After remediation, perform the operation that originally failed.

For example:

```powershell
Get-Content 'C:\Path\To\Folder\file.txt'
Add-Content 'C:\Path\To\Folder\file.txt' -Value 'verification'
```

Also re-check the ACL and group membership.

## Escalate when

Escalate if:

- Group Policy or configuration management recreates the deny
- the deny is security/compliance policy
- permissions are controlled by another team
- access involves sensitive data outside technician authorization
- ownership changes would be required
- the root cause appears to be domain/identity infrastructure rather than the local ACL
- the user still cannot access the object after the confirmed ACL conflict is fixed

## Lab validation

Validated in `INC-006` on a GitHub-hosted Windows Server 2025 Datacenter environment.

The lab reproduced a real Access Denied condition, confirmed correct local-group membership, identified a direct `ReadData` deny using `Get-Acl` and `icacls`, removed only the conflicting deny, and verified successful read/write access while preserving the group-based `Modify` grant.
