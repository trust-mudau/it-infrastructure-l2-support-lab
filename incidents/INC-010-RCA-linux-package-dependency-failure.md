# RCA — INC-010 Linux Package Dependency Failure

## Root cause
The custom DEB contained an unsatisfied dependency on `l2missing-runtime >= 9.9`, leaving `l2demo-app` in an unconfigured state.

## Evidence
- package control metadata showed the invalid dependency
- `dpkg -i` returned non-zero
- `dpkg --audit`/`apt-get check` exposed dependency health
- `apt-cache policy` showed the required package was unavailable

## Corrective action
Removed the broken package and deployed a corrected package version using an available dependency.

## Verification
Package status became `install ok installed`, package-manager consistency checks passed, and the installed application command executed successfully.

## Prevention
Validate package dependencies in CI against supported repositories before release and avoid ad-hoc production package modifications that diverge from vendor/source-of-truth artifacts.
