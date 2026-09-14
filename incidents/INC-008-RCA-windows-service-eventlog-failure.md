# RCA — INC-008 Windows Service Startup Failure

## Summary
A Windows service started and immediately stopped because a required local configuration file was missing.

## Root cause
`L2DemoService` required `C:\l2lab\scenario08\port.txt`. The file did not exist. The service wrote Application Event ID 8001 identifying the missing dependency and stopped.

## Evidence
- Windows Server 2025 hosted runner
- `Get-Service`: `Stopped`
- `sc.exe qc`: expected binary path and LocalSystem account
- no process/listener on TCP 8092 before remediation
- Application log Event ID 8001 identified the missing `port.txt`
- `Test-Path`: `False`

## Corrective action
Created the required file containing `8092`. No service-account, binary, firewall, or broad security setting was changed.

## Verification
The service remained `Running`, TCP 8092 accepted a connection, and Application Event ID 8000 confirmed successful startup.

## Prevention
Document service dependencies, validate required configuration during deployment, and alert on repeated service-start failures/Event Log errors.
