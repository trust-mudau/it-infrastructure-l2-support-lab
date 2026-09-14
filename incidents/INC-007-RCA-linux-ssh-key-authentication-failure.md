# RCA — INC-007 Linux SSH Key Authentication Failure

## Incident summary

An approved L2 support account could reach a Linux SSH service but could not authenticate with the expected ED25519 key. The client returned `Permission denied (publickey)`.

## Impact

Remote administration was unavailable for the affected account. The host itself remained reachable and the SSH daemon remained healthy.

## Detection

The failure was reproduced in a GitHub-hosted Ubuntu 24.04.5 LTS environment through a dedicated `l2sshd.service` listening on `127.0.0.1:2222`.

## Evidence-led troubleshooting

The investigation deliberately separated layers:

1. **Service state:** `systemctl status` confirmed `l2sshd.service` was active.
2. **Process state:** the expected `sshd` process was running.
3. **Socket state:** `ss -ltnp` showed TCP 2222 listening.
4. **Connectivity:** `nc -vz 127.0.0.1 2222` succeeded.
5. **Firewall:** UFW reported inactive in the lab.
6. **Account:** `getent passwd` and `id` confirmed the target account existed.
7. **Daemon policy:** `sshd -T` confirmed public-key authentication enabled, password authentication disabled and `StrictModes yes`.
8. **Client evidence:** `ssh -vvv` confirmed the expected key was offered but rejected.
9. **Server evidence:** `/var/log/l2sshd.log` reported `Authentication refused: bad ownership or modes for file /home/l2support/.ssh/authorized_keys`.
10. **Filesystem evidence:** `namei -l` and `stat` showed `authorized_keys` mode `0666`.

## Root cause

`/home/l2support/.ssh/authorized_keys` had mode `0666`, making it writable by group and others. OpenSSH `StrictModes` correctly rejected the file as unsafe and therefore refused the public key.

## Contributing condition

The key itself was valid, which could have encouraged an incorrect response such as replacing keys, enabling password authentication or restarting the service repeatedly. The issue was specifically trust in the key-file permissions.

## Corrective action

The file was changed to mode `0600` with ownership retained as `l2support:l2support`.

Security configuration was intentionally preserved:

- `StrictModes yes`
- `PubkeyAuthentication yes`
- `PasswordAuthentication no`

## Verification

A fresh SSH connection using the same private key succeeded. The remote command returned `remote-user=l2support` and `ssh-recovery=PASS`.

Server logs changed from `Failed publickey` / `bad ownership or modes` to `Accepted publickey`.

## Escalation decision

No escalation was required because the issue was local, reproducible, understood and safely remediated within scope.

Escalation would be required for externally blocked ports, centrally managed SSH policy, suspected host-key compromise, unverifiable authorized keys, security-event indicators, or continued failure after local permissions/configuration were validated.

## Preventive actions

- enforce secure `.ssh` / `authorized_keys` permissions in provisioning scripts
- validate SSH path ownership/modes during onboarding
- include server authentication logs in remote-access troubleshooting
- avoid weakening security controls as a diagnostic shortcut

## Evidence reference

Successful workflow run: `34875106353`  
Evidence artifact: `scenario-07-evidence` / artifact ID `10360891980`
