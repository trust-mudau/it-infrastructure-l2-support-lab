# KB-009 — Linux Host Reachability Failure Caused by Wrong Subnet

When one client cannot reach a service that works locally on the server, separate application health from network-path health.

## Commands
```bash
ip -br addr
ip route
ip route get <target-ip>
ip neigh
ping -c 2 <target-ip>
ss -ltnp
curl -v http://<target-ip>:<port>/
```

## Reasoning
Compare the client IP/prefix with the destination network. A client on `10.77.1.0/24` does not have direct on-link reachability to a service on `10.77.0.0/24` unless an appropriate router/default route exists.

## Fix principle
Correct the authoritative IP configuration. Do not compensate for a wrong client address by changing a healthy server or opening firewall rules unnecessarily.
