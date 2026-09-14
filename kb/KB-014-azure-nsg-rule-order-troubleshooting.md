# KB-014 — Azure NSG Rule-Order Troubleshooting with Bicep

When reviewing an Azure NSG, evaluate both **whether a rule exists** and **its priority/order**.

## Questions
- Is direction Inbound or Outbound?
- Is access Allow or Deny?
- Does protocol/port match the application?
- Is the source appropriately restricted?
- Does a lower-numbered rule take precedence before a broader deny?

## IaC validation
Compile Bicep with Azure CLI and inspect the resulting JSON before deployment. Configuration validation can catch missing rules without requiring a live resource.

## Security principle
Do not solve reachability by adding broad `*`/Any-source access when a narrower application-specific rule is appropriate.
