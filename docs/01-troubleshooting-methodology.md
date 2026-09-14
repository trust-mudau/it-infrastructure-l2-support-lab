# L2 Troubleshooting Methodology

## 1. Confirm impact and scope

Establish who or what is affected, when the issue began, whether it is reproducible, and whether a workaround exists.

## 2. Preserve evidence

Capture relevant errors, timestamps, service state, permissions, resource usage, logs and configuration before making changes.

## 3. Build hypotheses

Rank likely causes by probability, impact and cost of testing. Avoid changing multiple variables at once.

## 4. Test safely

Start with read-only commands and low-risk checks. Prefer evidence that can falsify a hypothesis.

## 5. Correct minimally

Apply the smallest change that addresses the confirmed cause. Record the exact change.

## 6. Verify independently

Do not assume a command succeeding means the incident is resolved. Re-run the failed operation and verify the expected output or service behaviour.

## 7. Check recurrence and residual risk

Confirm whether scheduling, capacity, permissions, credentials, dependencies or monitoring could cause the issue again.

## 8. Decide whether to escalate

Escalate when the issue exceeds access, scope, risk tolerance or expertise; when data integrity is at risk; or when a deeper product defect is suspected.

## 9. Document

Close the ticket with symptom, evidence, cause, resolution, verification and follow-up. Create a KB article when the fix is reusable.
