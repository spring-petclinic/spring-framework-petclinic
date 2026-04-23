---
profile_id: azure_functions_python
title: Python Azure Functions Workloads
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: platform
stack_nodes:
  - azure
requires:
  - python
precedence: 70
fallback_mode: warn_continue
compatibility:
  - python
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=azure functions
  - path=function_app.py
  - manifest=requirements.txt
max_lines_per_section: 6
tags:
  - python
  - azure
  - serverless
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

Python on Azure Functions should be organized around the decorator-based app model, explicit bindings, environment-managed configuration, and observable serverless execution.

## ARCHITECTURE RULES

- Keep the function entry surface thin and move reusable logic into shared modules.
- Use the FunctionApp and blueprint model for larger applications.
- Separate trigger/binding code from business logic and integration adapters.

## DESIGN PATTERNS

- function_app.py as the composition root for function registration.
- Shared helper modules for pure logic and reusable integrations.
- Explicit binding decorators for input/output contracts.

## CODING RULES

- Do not hardcode app settings, secrets, or connection strings.
- Keep trigger handlers stateless and avoid assuming local file persistence.
- Use type annotations for request, response, and binding inputs where practical.

## SECURITY RULES

- Keep secrets in app settings or managed secret stores, never in source files.
- Review trigger exposure, auth level, and binding configuration for each function.
- Treat incoming payloads, events, and environment values as untrusted input.

## TESTING RULES

- Test user functions directly with mocked HttpRequest or binding objects.
- Cover success, invalid input, and one configuration-related failure path.
- Add at least one non-regression assertion around routing, bindings, or env settings.

## COMMON MISTAKES

- Putting too much orchestration inside the function entrypoint.
- Assuming local.settings.json is part of production deployment.
- Relying on temporary files or global state as if they were durable.

## AECF AUDIT CHECKS

- Verify function registration, bindings, and config ownership are explicit.
- Verify business logic is separated from trigger plumbing.
- Verify tests cover route/binding behavior and configuration edge cases.