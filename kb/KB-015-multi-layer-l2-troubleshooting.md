# KB-015 — Multi-layer L2 Troubleshooting: Restore One Layer, Then Re-test

Complex incidents often contain more than one fault. Avoid changing service, network, permissions and backup controls simultaneously.

## Recommended sequence
1. **Service/process:** `systemctl status`, `journalctl -u`, service account, unit definition.
2. **Files/permissions:** `namei -l`, `stat`, identity/group membership.
3. **Local application:** verify direct IP/loopback and listening socket with `ss` + `curl`.
4. **Name resolution:** `getent hosts`, resolver/hosts configuration.
5. **Backup path:** run as the real backup identity, inspect destination permissions/capacity.
6. **Recovery verification:** hash the archive, restore separately, compare restored data.

## Key principle
After each minimum corrective change, re-test at that layer before moving upward. Direct-IP health can prove the application works even while DNS/hostname access is still broken.

## Escalation
Escalate when configuration drift is not attributable to an approved change, centrally managed settings conflict with local fixes, recovery can destroy newer data, or multiple hosts/users indicate broader scope.
