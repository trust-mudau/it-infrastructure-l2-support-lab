# Incident Analysis — INC-012 Suspicious Linux Process

## Finding
A benign lab process `/tmp/.cache-update.py` was the source of both an unexpected decoy-file modification and a listener on `127.0.0.1:4444`.

## Evidence preserved
- PID/PPID, user, start time and command line
- process tree
- listening socket
- open files
- executable/interpreter path
- script metadata and SHA-256
- affected decoy file metadata/content

## Containment
The process was terminated only after evidence collection. Verification confirmed the PID was no longer active and the TCP 4444 listener disappeared.

## Production judgement
This would not be closed as routine support. Security/IR should receive the evidence for host-wide scope, persistence, credential exposure, lateral movement and integrity analysis.
