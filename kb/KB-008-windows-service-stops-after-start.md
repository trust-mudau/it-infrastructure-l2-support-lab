# KB-008 — Windows Service Starts Then Stops: Event Log First

## Symptom
A Windows service is registered correctly but stops immediately after startup.

## L2 workflow
1. `Get-Service <name>` — confirm current state.
2. `sc.exe qc <name>` — verify binary path, account, start type, dependencies.
3. Check the expected process and listening port.
4. Query service/application events: `Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='<provider>'}`.
5. Validate referenced files, paths, ports, credentials, and dependent services before changing security or reinstalling software.

## Lab example
INC-008 showed Event ID 8001 reporting a missing `port.txt`. Restoring only that dependency allowed the service to run and listen on TCP 8092.

## Avoid
Do not jump straight to reinstalling the service, disabling security controls, or changing the service account when logs identify a narrower dependency failure.
