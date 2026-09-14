# INC-007 — Linux SSH Remote Access Fails Despite Correct Public Key

**Priority:** P2  
**Category:** Linux / SSH / Remote access / Security  
**Platform:** GitHub-hosted Ubuntu 24.04.5 LTS runner  
**Status:** **Lab validated — resolved**  
**Successful workflow run:** `34875106353`

## User / business impact

A support engineer could not remotely administer a Linux server using the approved SSH key. The SSH daemon was running on TCP 2222 and the correct public key was present in the target account's `authorized_keys` file, but the client returned `Permission denied (publickey)`.

## Confirmed symptoms

- `l2sshd.service` was active and running
- `sshd` listened on `127.0.0.1:2222`
- `nc -vz 127.0.0.1 2222` succeeded
- host firewall was inactive in the lab
- the client offered the expected ED25519 key
- authentication failed with SSH exit code `255`
- server log reported: `Authentication refused: bad ownership or modes for file /home/l2support/.ssh/authorized_keys`

## Investigation

The L2 investigation intentionally separated the network/service layer from the authentication layer before making changes.

Commands/tools used included:

- `systemctl status l2sshd.service`
- `ps -ef`
- `ss -ltnp`
- `nc -vz`
- `getent passwd`
- `id`
- `namei -l`
- `stat`
- `sshd -T`
- `ssh -vvv`
- server-side OpenSSH verbose logging

The target path permissions were:

```text
/home/l2support                 0750 l2support:l2support
/home/l2support/.ssh            0700 l2support:l2support
/home/l2support/.ssh/authorized_keys 0666 l2support:l2support
```

The SSH daemon effective configuration confirmed:

- `Port 2222`
- `PubkeyAuthentication yes`
- `PasswordAuthentication no`
- `StrictModes yes`
- `AuthorizedKeysFile .ssh/authorized_keys`
- `AllowUsers l2support`

## Root cause

The correct `authorized_keys` file was writable by group and others (`0666`). With `StrictModes yes`, OpenSSH refused to trust the file and rejected the otherwise valid public key.

## Corrective action

Changed only the key file permissions:

```bash
chmod 0600 /home/l2support/.ssh/authorized_keys
chown l2support:l2support /home/l2support/.ssh/authorized_keys
```

No security control was weakened. `StrictModes` remained enabled and password authentication remained disabled.

## Verification

Using the same private key, a new SSH session successfully executed remote commands as `l2support`:

```text
remote-user=l2support
ssh-recovery=PASS
```

Post-fix checks confirmed:

- SSH service remained active
- TCP 2222 remained listening
- `authorized_keys` mode was `0600`
- key-based authentication succeeded
- password authentication remained disabled
- `StrictModes` remained enabled

## Escalation decision

No escalation was required because the network path, daemon, account and policy configuration were healthy; the fault was isolated to a local file-permission condition and was remediated without broadening access or weakening SSH policy.

Escalation would have been appropriate if the port were blocked externally, SSH policy were centrally managed, host keys appeared compromised, the approved public key could not be verified, or access remained unavailable after permissions and daemon configuration were validated.

## Evidence

Successful GitHub Actions run:

`https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34875106353`

Artifact: `scenario-07-evidence` (artifact ID `10360891980`, 30-day workflow retention).

The artifact contains the captured environment, failed SSH client output, server-side diagnostic evidence, corrective action, successful remote verification and incident summary.
