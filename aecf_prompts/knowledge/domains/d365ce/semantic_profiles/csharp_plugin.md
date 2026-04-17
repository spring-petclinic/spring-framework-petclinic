---
profile_id: d365ce_csharp_plugin
title: Dynamics 365 CE C# Plugin Development
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - d365ce
requires:
  - dotnet
precedence: 85
fallback_mode: warn_continue
compatibility:
  - d365ce
  - dotnet
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=dynamics crm
  - keyword=customer engagement
  - keyword=dataverse plugin
  - keyword=d365ce
max_lines_per_section: 6
tags:
  - csharp
  - d365ce
  - dynamics365
  - plugin
  - dataverse
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

Dynamics 365 Customer Engagement C# plugin development targets the Dataverse platform with server-side .NET assemblies registered against entity messages and pipeline stages.

## ARCHITECTURE RULES

- One plugin class per logical operation; avoid monolithic plugin assemblies.
- Keep business logic in dedicated service or handler classes; plugins should only orchestrate.
- Use early-bound entity classes for type safety and refactoring confidence.
- Respect plugin pipeline stages (pre-validation, pre-operation, post-operation) and choose the correct one.
- Separate integration logic from entity event logic.

## DESIGN PATTERNS

- Service locator via `IServiceProvider` for tracing, organization service, and context.
- Unit of Work with `IOrganizationService` wrapped in testable service classes.
- Configuration-driven behavior via secure and unsecure configuration strings.
- Custom API / Custom Action patterns for reusable server-side operations.
- Plugin step filtering attributes to limit unnecessary executions.

## CODING RULES

- Always check execution depth to prevent recursive plugin loops.
- Use early-bound types; avoid stringly-typed attribute access in production code.
- Keep plugin code stateless; do not store instance-level mutable data.
- Handle `InvalidPluginExecutionException` and throw it for user-facing validation failures.
- Never hardcode GUIDs, URLs, or environment-specific values.

## SECURITY RULES

- Respect calling user vs system user context; do not escalate privileges without explicit justification.
- Validate input entity attributes before trusting them for business decisions.
- Review registered plugin steps for least-privilege message and entity scope.
- Do not expose sensitive data in unsecure configuration; use secure config for secrets.

## TESTING RULES

- Use FakeXrmEasy, Moq, or similar frameworks to fake `IOrganizationService` and `IPluginExecutionContext`.
- Cover pre-validation and post-operation paths, invalid input, and recursion-depth guard.
- Test service classes in isolation from plugin orchestration.
- Validate security context escalation scenarios where applicable.
- Keep test data deterministic and independent of environment state.

## COMMON MISTAKES

- Registering plugins on broad messages without filtering attributes.
- Ignoring execution depth, causing infinite recursion.
- Using late-bound attribute access everywhere, losing type safety.
- Putting all business logic directly in the `Execute` method.
- Storing mutable state in plugin class fields across executions.

## AECF AUDIT CHECKS

- Verify plugin classes are focused and delegate to service/handler classes.
- Verify early-bound entity types are used for production entity access.
- Verify execution depth checks prevent recursive loops.
- Verify security context usage is explicit and justified.
- Verify tests cover happy path, validation failure, and recursion scenarios.
