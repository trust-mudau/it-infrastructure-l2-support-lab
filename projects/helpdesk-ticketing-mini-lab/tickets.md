# Ticket Scenarios

## TKT-001 — Password reset
**Issue:** User cannot sign in after forgetting their password.  
**Priority:** P3 — single user, standard productivity impact.  
**Diagnostic Questions:** Is the username correct? Is the account locked? Is MFA still available? Was the password recently changed?  
**Troubleshooting:** Confirm identity using the approved verification process; check account state; rule out lockout; initiate password reset; require password change at next sign-in where policy permits.  
**Resolution/Escalation:** Password reset completed and sign-in verified. No escalation.  
**User Communication:** Explain that the password was reset, provide the temporary-password process without exposing credentials in the ticket, and remind the user not to reuse passwords.  
**Closure Notes:** Identity verified; password reset; account active; successful sign-in confirmed; ticket resolved.

## TKT-002 — Locked user account
**Issue:** User receives an account-locked message after repeated sign-in attempts.  
**Priority:** P2 — user unable to work.  
**Diagnostic Questions:** When did lockout begin? Any recent password change? Which devices/apps are signed in? Is the user on VPN?  
**Troubleshooting:** Verify identity; confirm account lockout state; check for stale credentials on phone, Outlook, mapped drives or VPN; unlock only after identifying likely repeated-authentication source.  
**Resolution/Escalation:** Stale saved credentials removed and account unlocked; sign-in retested successfully. Escalate to identity/L2 if lockouts recur without an identified source.  
**User Communication:** Explain that an old saved password can repeatedly lock the account and ask the user to update credentials on all devices.  
**Closure Notes:** Account unlocked after stale-credential cause identified; successful sign-in confirmed; monitoring advice provided.

## TKT-003 — Shared-folder access denied
**Issue:** User can sign in but receives Access Denied on an approved shared folder.  
**Priority:** P2 — business work blocked.  
**Diagnostic Questions:** Which folder? Does access work for colleagues? Was access recently approved? Has the user changed teams?  
**Troubleshooting:** Verify the request/approval; confirm user and group membership; compare expected versus effective permissions; check for explicit deny or missing group membership; avoid broad permission changes.  
**Resolution/Escalation:** Correct approved group membership or conflicting permission and retest. Escalate if access is centrally managed or approval is missing.  
**User Communication:** Confirm access has been restored and ask the user to reopen the resource to verify.  
**Closure Notes:** Approved access verified; least-privilege correction applied; user successfully opened the folder.

## TKT-004 — Outlook will not launch
**Issue:** Outlook closes immediately after launch.  
**Priority:** P3 — email affected for one user with possible web-mail workaround.  
**Diagnostic Questions:** When did it last work? Any recent update/add-in change? Does Outlook Web work? Any error message?  
**Troubleshooting:** Confirm network and Microsoft 365 sign-in; test Outlook in safe mode; isolate add-ins; check profile/cache health; use web access as temporary workaround if available.  
**Resolution/Escalation:** Disable the failing add-in or rebuild the affected profile after preserving user data. Escalate if service-wide or server-side symptoms appear.  
**User Communication:** Explain the temporary workaround and the corrective action in plain language.  
**Closure Notes:** Outlook launches normally after isolating the local client fault; user confirmed mail access.

## TKT-005 — USB headset not detected
**Issue:** Headset is connected but unavailable in Teams/audio settings.  
**Priority:** P3 — user can work but calls are affected.  
**Diagnostic Questions:** Does the headset work on another USB port/device? Is it visible in Device Manager? Did it work before?  
**Troubleshooting:** Reseat device; test another port; check Windows audio/device settings; confirm default input/output device; inspect driver/device state; test alternate headset if available.  
**Resolution/Escalation:** Device recovered after port/device refresh or known-good replacement. Escalate to hardware support if the device consistently fails across systems.  
**User Communication:** Tell the user what was tested and which audio device is now selected.  
**Closure Notes:** Headset detected and tested in call settings; audio input/output confirmed.

## TKT-006 — Internal service unreachable
**Issue:** User has internet access but cannot reach an internal support portal.  
**Priority:** P2 — required business service unavailable.  
**Diagnostic Questions:** Is the issue user-specific? Does direct IP work? What hostname is used? Is VPN required?  
**Troubleshooting:** Check IP configuration, gateway, VPN state, DNS resolution and TCP reachability; compare hostname versus direct-IP results; flush/retest resolver where appropriate.  
**Resolution/Escalation:** Correct client-side DNS/VPN configuration if isolated locally. Escalate if multiple users fail or infrastructure-side DNS/service ownership is implicated.  
**User Communication:** Confirm the service is reachable again and explain whether the fault was local connectivity, name resolution or upstream.  
**Closure Notes:** Connectivity path validated; service reachable; user confirmed access.

## TKT-007 — Suspicious phishing email
**Issue:** User reports an email asking them to open an unexpected login link.  
**Priority:** P1 — potential security incident.  
**Diagnostic Questions:** Was the link clicked? Were credentials entered? Was an attachment opened? Who else received it?  
**Troubleshooting:** Tell user not to interact further; preserve message details; capture sender, subject, headers/link domain where policy permits; determine whether credentials or endpoint may be compromised.  
**Resolution/Escalation:** Escalate immediately to Security/Incident Response. If credentials were entered, follow approved password/session-revocation procedures.  
**User Communication:** Reassure the user for reporting it quickly, give clear next actions, and avoid asking them to investigate the malicious content themselves.  
**Closure Notes:** Evidence recorded; Security escalation created; user given containment instructions; helpdesk ticket linked to security case.

## TKT-008 — Business application repeatedly crashes
**Issue:** Line-of-business application crashes after login despite standard first-line steps.  
**Priority:** P2 — user cannot complete a core task.  
**Diagnostic Questions:** Exact error/time? Is it user-specific or widespread? Any recent update? Does another workstation reproduce it?  
**Troubleshooting:** Restart application/device; verify connectivity and account access; check local logs/event entries; clear safe cache where approved; reproduce fault and capture error evidence.  
**Resolution/Escalation:** Escalate to L2/application support with reproduction steps, timestamps, screenshots/log references and actions already attempted.  
**User Communication:** Explain that first-line checks are complete, the issue requires specialist investigation, and provide the escalation reference.  
**Closure Notes:** L1 scope exhausted; evidence attached; escalated to L2 with impact and troubleshooting history.

## TKT-009 — Network printer unavailable
**Issue:** User cannot print to a shared/network printer.  
**Priority:** P3 — limited user/device impact.  
**Diagnostic Questions:** Can others print? Is the printer powered/online? Is the queue paused? Has the device IP changed?  
**Troubleshooting:** Check reachability; inspect queue and spooler; remove stuck jobs; verify correct printer/IP; reconnect printer; restart spooler only if justified.  
**Resolution/Escalation:** Queue cleared and printer connection restored. Escalate if hardware is offline or multiple users indicate network/print-server fault.  
**User Communication:** Ask user to print a test page and explain the queue/printer status found.  
**Closure Notes:** Test page successful; printer reachable; user confirmed normal printing.

## TKT-010 — New starter access request
**Issue:** New employee needs account and approved baseline access before first working day.  
**Priority:** P3 — planned service request.  
**Diagnostic Questions:** Is the request approved? Start date? Manager? Required systems/groups? Any elevated access?  
**Troubleshooting:** Validate request and approvals; create/enable account according to SOP; assign approved baseline groups only; avoid copying another user's entire access; verify sign-in and group state.  
**Resolution/Escalation:** Complete approved provisioning; escalate non-standard/elevated access for application-owner or security approval.  
**User Communication:** Send first-day access instructions through the approved secure channel and identify where to get help.  
**Closure Notes:** Baseline access provisioned and verified; exceptional access excluded pending separate approval; request closed.