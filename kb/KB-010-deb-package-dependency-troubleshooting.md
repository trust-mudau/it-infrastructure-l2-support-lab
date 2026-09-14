# KB-010 — Debian/Ubuntu Package Dependency Troubleshooting

## Useful checks
```bash
dpkg-deb -I package.deb
dpkg-query -W -f='${Package} ${Version} ${Status}\n' <package>
dpkg --audit
sudo apt-get check
apt-cache policy <dependency>
```

## Interpretation
A failed `dpkg -i` may leave a package unpacked but unconfigured. Determine whether the dependency exists in configured repositories before attempting repairs.

## Escalate when
The dependency metadata comes from a vendor/release pipeline, repository signing is suspect, required repositories are centrally controlled, or the fix would require unsupported package versions.
