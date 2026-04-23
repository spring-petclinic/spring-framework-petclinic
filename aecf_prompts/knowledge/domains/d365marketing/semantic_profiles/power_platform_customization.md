---
profile_id: d365marketing_power_platform
title: Dynamics 365 Marketing Power Platform Customization
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - d365marketing
requires: []
precedence: 85
fallback_mode: warn_continue
compatibility:
  - d365marketing
  - d365ce
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=dynamics marketing
  - keyword=power platform
  - keyword=power automate
  - keyword=pcf
  - keyword=d365marketing
max_lines_per_section: 6
tags:
  - powerplatform
  - d365marketing
  - dynamics365
  - pcf
  - powerautomate
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

Dynamics 365 Marketing Power Platform customization uses solution-aware components including Power Automate flows, PCF controls, custom connectors, and Dataverse entities within the marketing application context.

## ARCHITECTURE RULES

- Keep all customizations within managed solutions; never use unmanaged changes in non-dev environments.
- Use environment variables and connection references for environment-portable configuration.
- Separate automation orchestration (Power Automate) from UI customization (PCF, form scripts).
- Use custom connectors with explicit authentication and error contracts for external integrations.
- Keep PCF controls single-responsibility and decoupled from specific entity schemas.

## DESIGN PATTERNS

- Power Automate child flows for reusable automation fragments.
- PCF controls with ControlFramework lifecycle methods and explicit input/output properties.
- Custom connector with OpenAPI definition and delegated auth for external API integrations.
- Environment variable-driven configuration for URLs, feature flags, and tenant-specific values.
- Solution layering with publisher-prefixed components for clean upgrade paths.

## CODING RULES

- Use TypeScript for PCF controls; keep ControlFramework method implementations focused and deterministic.
- Define custom connector operations with explicit request/response schemas.
- Use environment variables instead of hardcoded URLs, keys, or tenant identifiers.
- Keep Power Automate expressions readable; avoid deeply nested expressions in single steps.
- Prefix custom components with the solution publisher prefix.

## SECURITY RULES

- Review custom connector authentication type and secret handling.
- Validate Power Automate flow run-as context and connection ownership.
- Do not expose sensitive configuration in PCF control manifest or client-accessible properties.
- Review Dataverse security roles for any new entities, actions, or custom APIs.

## TESTING RULES

- Test PCF controls with Jest or Vitest in isolation from the Power Apps runtime.
- Test Power Automate flows with explicit test runs covering trigger, action, and error paths.
- Validate custom connector operations with contract tests against expected schemas.
- Test form event scripts independently of the Dynamics form runtime.
- Keep test data creation deterministic and environment-independent.

## COMMON MISTAKES

- Deploying unmanaged customizations outside development environments.
- Hardcoding environment URLs or tenant-specific values instead of using environment variables.
- Creating monolithic Power Automate flows instead of composable child flows.
- Building PCF controls tightly coupled to a single entity schema.
- Ignoring connection reference ownership and delegation in shared environments.

## AECF AUDIT CHECKS

- Verify all components belong to a managed solution with consistent publisher prefix.
- Verify environment variables are used for environment-specific configuration.
- Verify Power Automate flows have error handling and do not use hardcoded values.
- Verify PCF controls are testable in isolation and use TypeScript.
- Verify custom connector auth and secrets are handled securely.
