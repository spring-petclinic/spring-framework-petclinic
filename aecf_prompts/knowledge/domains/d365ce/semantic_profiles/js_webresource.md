---
profile_id: d365ce_js_webresource
title: Dynamics 365 CE JavaScript Web Resource
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - d365ce
requires: []
precedence: 80
fallback_mode: warn_continue
compatibility:
  - d365ce
  - node
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=web resource
  - keyword=xrm sdk
  - keyword=form scripting
  - keyword=d365ce javascript
max_lines_per_section: 6
tags:
  - javascript
  - d365ce
  - dynamics365
  - webresource
  - xrm
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

Dynamics 365 Customer Engagement JavaScript web resources run inside the model-driven app form runtime, using the supported Xrm SDK for form manipulation, data access, and navigation.

## ARCHITECTURE RULES

- Namespace-isolate all functions to avoid global scope collisions.
- Keep form event handlers thin; delegate business logic to internal helper functions.
- Separate Xrm SDK calls from pure business logic to enable testability.
- Register form events declaratively through the form editor, not programmatically at runtime.
- One web resource file per functional area; avoid monolithic script files.

## DESIGN PATTERNS

- Module pattern or IIFE for namespace isolation.
- Facade functions that wrap Xrm SDK calls for testability and reuse.
- Event handler registration through form configuration rather than runtime scripting.
- Async/await patterns for Web API calls with proper error handling.
- Configuration-driven visibility and field rules over hardcoded logic.

## CODING RULES

- Use only supported Xrm SDK methods and objects; avoid undocumented DOM manipulation.
- Pass `executionContext` as the first parameter in all form event handlers.
- Handle promise rejections in all async Xrm.WebApi calls.
- Do not hardcode entity logical names, field names, or GUIDs as magic strings.
- Use `formContext` obtained from `executionContext.getFormContext()` instead of deprecated `Xrm.Page`.

## SECURITY RULES

- Do not expose sensitive data in web resource scripts; they are client-accessible.
- Validate user roles and security context before enabling privileged UI actions.
- Do not call external APIs directly from web resources without approved CORS configuration.
- Avoid constructing queries with unsanitized user input.

## TESTING RULES

- Separate business logic from Xrm SDK wrappers so logic can be unit tested without the form runtime.
- Mock `formContext` and `executionContext` objects for handler tests.
- Cover show/hide logic, validation rules, and async data retrieval paths.
- Test error handling for failed Web API calls.
- Keep tests runnable outside the Dynamics form environment.

## COMMON MISTAKES

- Using `Xrm.Page` instead of `formContext` from execution context.
- Polluting the global JavaScript namespace with function declarations.
- Calling unsupported or internal Dynamics APIs that break on platform updates.
- Ignoring async error handling in Web API calls.
- Hardcoding GUIDs and field names without constants or configuration.

## AECF AUDIT CHECKS

- Verify namespace isolation is applied to all exported functions.
- Verify only supported Xrm SDK methods are used.
- Verify `formContext` is obtained from `executionContext`, not `Xrm.Page`.
- Verify async calls include error handling.
- Verify tests cover business logic independently of the Xrm runtime.
