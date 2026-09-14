# INC-007 — Linux SSH Remote Access Fails Despite Correct Public Key

**Priority:** P2  
**Category:** Linux / SSH / Remote access / Security  
**Platform:** GitHub-hosted Ubuntu runner  
**Status:** Scenario configured — execution evidence pending

## User / business impact

A support engineer cannot remotely administer a Linux server using the approved SSH key. The SSH daemon is expected to be running on TCP 2222 and the correct public key has been placed in the target account's `authorized_keys` file, but the client receives `Permission denied (publickey)`.

## Initial symptoms

- server is reachable locally
- SSH daemon should be listening on TCP 2222
- public-key authentication is required
- the expected key exists in `authorized_keys`
- login still fails

## Known environment

- Ubuntu GitHub-hosted runner
- temporary user: `l2support`
- dedicated SSH daemon: `l2sshd.service`
- SSH port: `2222`
- authentication method: public key only
- server log: `/var/log/l2sshd.log`
- intentional fault: insecure permissions on `~/.ssh/authorized_keys`

## L2 objective

Reproduce the SSH failure, prove the service and network path are healthy before changing authentication settings, inspect the client debug output and server-side SSH logs, identify why the correct key is being rejected, apply the minimum security-preserving correction, and independently verify remote command execution.

## Investigation requirements

Capture at minimum:

- OS/kernel
- SSH service status
- process and listening socket
- local TCP connectivity to port 2222
- firewall state where available
- target-user identity/home information
- `.ssh` and `authorized_keys` ownership/modes
- SSH client verbose output
- server-side SSH log entries
- SSH daemon effective configuration
- corrective action
- successful key-based remote command
- final permission state
- escalation decision

## Escalation rule

Escalate if TCP 2222 is blocked outside the host, the SSH daemon cannot start because of package/configuration corruption, authentication policy is centrally managed, the approved public key cannot be verified, account lockout is policy-driven, host keys are compromised, server logs indicate a broader security incident, or access remains unavailable after local permissions and daemon configuration are verified.

## Evidence location

The workflow will upload a `scenario-07-evidence` artifact after execution.
