# Microsoft 365 Support Playbook

**Status:** scenario-based support knowledge. No live Microsoft 365 tenant administration is claimed.

## Outlook - mail send/receive issue

1. Confirm scope: one user, multiple users, desktop client only, or Outlook on the web too.
2. Confirm network connectivity and Microsoft 365 service availability.
3. Check whether the account can sign in through the browser.
4. Confirm mailbox is not obviously over quota and the user is not working offline.
5. Compare Outlook desktop behaviour with Outlook on the web to separate client from service/account issues.
6. Check cached credentials/profile symptoms and add-ins if the desktop client alone is affected.
7. Apply the smallest safe correction, such as restarting Outlook, re-authenticating or recreating the profile only after evidence points to a client profile fault.
8. Verify send/receive with a test message and document the outcome.
9. Escalate if service health, licensing, mailbox provisioning, transport rules or tenant-level controls are suspected.

## Microsoft Teams - audio/camera/login issue

1. Confirm whether Teams web and desktop are both affected.
2. Validate Windows privacy permissions for microphone/camera.
3. Confirm the intended input/output device is selected in Teams settings.
4. Check another application to separate hardware/OS from Teams.
5. Check sign-in/account state and time synchronisation if authentication is failing.
6. Clear/rebuild local cache only when a client-state issue is supported by evidence.
7. Verify with a test call.
8. Escalate tenant policy, licensing or service-health issues.

## SharePoint - access denied or missing content

1. Capture the exact site/library/page and requested business purpose.
2. Confirm the user is signed into the expected organisational identity.
3. Determine whether the problem is access, navigation, missing content or sync.
4. Validate the approved access path: site membership, Microsoft 365 group, security group or direct permission according to policy.
5. Avoid broad direct grants when group-based access is the approved model.
6. Verify access independently after the approved change.
7. Record request, approval, action and evidence in the ticket.
8. Escalate broken inheritance, sensitivity/compliance controls, external sharing or tenant-wide policy issues.

## Common Tier 1 principle

Start with scope and evidence, distinguish local client issues from account/service/tenant issues, make the minimum safe change, verify independently and document before closure.