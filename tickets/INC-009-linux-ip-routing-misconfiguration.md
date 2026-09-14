# INC-009 — Linux Client Cannot Reach Healthy Service After IP Misconfiguration

**Priority:** P2  
**Category:** Linux / TCP-IP / Routing  
**Platform:** Ubuntu 24.04 network namespace lab  
**Status:** Lab validated  
**Execution:** https://github.com/trust-mudau/it-infrastructure-l2-support-lab/actions/runs/34875835212

## Impact
An isolated client could not reach a healthy HTTP service at `10.77.0.1:8088`.

## Investigation
The host service was verified locally and its socket was listening. Client evidence was gathered with `ip -br addr`, `ip route`, `ip route get`, `ip neigh`, and `ping`. The client interface held `10.77.1.20/24`, while the directly connected service network was `10.77.0.0/24`.

## Root cause
A stale/fallback client address placed the client in the wrong subnet.

## Resolution
Flushed the incorrect address and assigned `10.77.0.20/24` to the isolated client interface.

## Verification
Client route, ICMP reachability, and HTTP retrieval of `scenario09-network-service=healthy` all succeeded.

## Escalation
No upstream escalation was required. Escalate if DHCP repeatedly issues the wrong network, VLAN assignment is incorrect, or the gateway/upstream route is outside local ownership.
