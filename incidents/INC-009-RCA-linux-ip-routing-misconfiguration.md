# RCA — INC-009 Linux IP/Subnet Misconfiguration

## Summary
A healthy service was unreachable from one client because the client had an IP address in the wrong /24 network.

## Root cause
The service side used `10.77.0.1/24`; the client used `10.77.1.20/24`. The host service itself remained healthy, so the fault was isolated to client addressing rather than the application.

## Diagnostic method
- prove server health locally
- inspect client interface address
- inspect client routing table and route lookup
- inspect neighbour state
- test ICMP and application-layer HTTP separately

## Corrective action
Replaced the stale client address with `10.77.0.20/24`.

## Verification
Ping and HTTP both succeeded after the correction, proving end-to-end recovery.

## Prevention
Validate DHCP/static-address source of truth and compare IP, prefix, gateway, VLAN and DNS values against the known-good network before modifying applications.
