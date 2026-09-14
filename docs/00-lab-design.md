# Lab Design

## Delivery model

This project uses disposable GitHub-hosted Windows and Linux runners instead of requiring local VM installation. That keeps the lab reproducible and lets scenarios generate real command output, logs and recovery evidence.

## Scope

The lab is built around support incidents rather than tutorials. Every incident includes:

- business/user impact
- initial symptoms
- technical evidence
- investigation path
- corrective action
- independent verification
- escalation decision
- root-cause statement
- reusable documentation

## Platforms

### Linux
GitHub-hosted Ubuntu runners are used for Bash, permissions, filesystems, networking, processes, services, logs, backup and recovery scenarios.

### Windows
GitHub-hosted Windows runners will be used for PowerShell, Windows networking, services, event/log inspection and Windows-specific support scenarios.

## Limitations

A hosted runner is not the same as administering a persistent production server or an employer-managed environment. Where a scenario cannot reproduce a production feature faithfully, the repository will label that work as scenario-based or designed only.

## Planned incident domains

1. Backup failure and recovery
2. Linux service failure
3. DNS resolution failure
4. IP/network configuration issue
5. SSH access failure
6. File and group permission issue
7. Disk capacity incident
8. Package/dependency failure
9. Scheduled job failure
10. Windows service failure
11. Windows DNS/network incident
12. Security-related account/access incident
13. Virtualization/snapshot recovery decision
14. Cloud connectivity/configuration incident
15. Multi-symptom L2 escalation case
