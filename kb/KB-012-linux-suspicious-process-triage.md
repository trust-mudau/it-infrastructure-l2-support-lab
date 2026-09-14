# KB-012 — L2 Triage for a Suspicious Linux Process

## Preserve evidence before destructive action
```bash
ps -p <pid> -o pid,ppid,user,lstart,etime,args
pstree -aps <pid>
ss -ltnp
lsof -p <pid>
readlink -f /proc/<pid>/exe
tr '\0' ' ' < /proc/<pid>/cmdline
sha256sum <suspicious-file>
stat <suspicious-file>
```

## Escalate when
The process is unexplained, runs from a temporary/user-writable path, opens an unauthorized listener, changes business files, persists unexpectedly, or may involve credentials/data exposure.

## Do not
Delete binaries, clear logs, reboot reflexively, or make unsupported attribution claims before preserving evidence and following incident-response policy.
