# Security Domain Pack

## Cross-cutting Rules
- Treat security as a default engineering concern across generation, refactoring, and audit flows.
- Validate authentication, authorization, input handling, secret usage, and observability on every non-trivial change.
- Prefer explicit security controls over implicit framework defaults when the change touches trust boundaries.

## Required Review Angles
- Validate how the selected stack handles authn/authz, secrets, serialization, and unsafe input.
- Review whether logs, traces, or error paths can leak sensitive information.
- Check dependency and supply-chain impact when introducing new packages, images, or services.

## Override Guidance
- If the user passes an explicit `stack=...`, security guidance still applies as a common layer.
- If AECF uses a detected stack from persisted `STACK_JSON.json`, keep the same security checks but adapt them to the detected platform/framework.