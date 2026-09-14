# KB-007 — Linux SSH `Permission denied (publickey)` When the Correct Key Exists

## Purpose

Use this article when an SSH client reaches the server but public-key authentication fails even though the expected key appears to be present in `authorized_keys`.

## Key troubleshooting principle

Do not treat every SSH login failure as a network problem.

First determine which layer is failing:

1. host/network reachability
2. listening TCP socket
3. SSH daemon health
4. account eligibility
5. SSH policy/effective configuration
6. key-file path/ownership/permissions
7. client key selection
8. server authentication decision

## Useful checks

### Service state

```bash
systemctl status ssh
# or the relevant custom sshd unit
```

### Listening socket

```bash
ss -ltnp | grep ':22'
```

For a non-standard port, replace `22` with the configured port.

### TCP connectivity

```bash
nc -vz server.example.com 22
```

A successful TCP connection with a failed SSH login usually moves the investigation toward authentication/configuration rather than routing.

### Client-side verbose output

```bash
ssh -vvv -i ~/.ssh/id_ed25519 user@server
```

Look for whether the intended key is actually offered and what authentication methods the server permits.

### Effective sshd configuration

```bash
sudo sshd -T | grep -E '^(port|pubkeyauthentication|passwordauthentication|authorizedkeysfile|strictmodes|allowusers)'
```

### Account and path checks

```bash
getent passwd user
id user
namei -l /home/user/.ssh/authorized_keys
stat -c '%A %a %U:%G %n' \
  /home/user \
  /home/user/.ssh \
  /home/user/.ssh/authorized_keys
```

Typical secure values are commonly:

```text
~/.ssh               0700
~/.ssh/authorized_keys 0600
```

Ownership should normally belong to the target user unless the environment intentionally uses another managed design.

### Server logs

Depending on distribution/configuration:

```bash
journalctl -u ssh --since '10 minutes ago'
```

or inspect the configured SSH/auth log.

A highly useful message is:

```text
Authentication refused: bad ownership or modes for file .../authorized_keys
```

## Why insecure permissions cause failure

When `StrictModes yes` is enabled, OpenSSH checks ownership and permissions on user SSH files before accepting them. A key file writable by unauthorized users could allow someone else to insert their own key, so sshd rejects it rather than weakening trust.

## Safe remediation pattern

If policy confirms the user should control the key file:

```bash
sudo chown user:user /home/user/.ssh/authorized_keys
sudo chmod 0600 /home/user/.ssh/authorized_keys
sudo chmod 0700 /home/user/.ssh
```

Then test again using the same key.

## What not to do

Avoid these shortcuts unless explicitly required by policy:

- disabling `StrictModes`
- enabling password authentication just to bypass the problem
- setting broad `777` permissions
- replacing keys before confirming whether the existing key is actually wrong
- repeatedly restarting sshd without reviewing logs

## Verification

A proper resolution should verify all of the following:

- daemon remains active
- expected port remains listening
- key-file permissions are secure
- the same approved key authenticates successfully
- the remote session runs as the correct account
- security policy remains intact

Example:

```bash
ssh -i ~/.ssh/id_ed25519 user@server 'whoami'
```

## Escalate when

Escalate when the port is blocked outside the server, SSH configuration is centrally managed, keys cannot be validated, account restrictions are policy-driven, host keys may be compromised, logs suggest malicious activity, or the issue persists after service/network/file-permission checks.

## Lab evidence

This KB was created from lab-validated INC-007. The GitHub Actions scenario reproduced the failure with `authorized_keys` mode `0666`, captured a server-side `bad ownership or modes` error, corrected the file to `0600`, and verified successful key-based remote execution while leaving `StrictModes` enabled and password authentication disabled.
