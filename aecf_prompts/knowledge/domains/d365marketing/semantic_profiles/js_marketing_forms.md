---
profile_id: d365marketing_js_forms
title: Dynamics 365 Marketing JavaScript Form Scripting
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - d365marketing
requires: []
precedence: 80
fallback_mode: warn_continue
compatibility:
  - d365marketing
  - d365ce
  - node
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=marketing form script
  - keyword=d365marketing javascript
  - keyword=real-time marketing
max_lines_per_section: 6
tags:
  - javascript
  - d365marketing
  - dynamics365
  - formscripting
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

Dynamics 365 Marketing JavaScript form scripting extends model-driven app forms within the marketing module, using the supported Xrm SDK for form events, field manipulation, and data access.

## ARCHITECTURE RULES

- Namespace-isolate all functions to prevent global scope collisions with other web resources.
- Separate Xrm SDK interaction from pure business logic for testability.
- Keep form scripts focused on UI behavior; server-side rules belong in plugins or Power Automate.
- Register event handlers declaratively through the form editor.
- Organize scripts by functional area, not by entity.

## DESIGN PATTERNS

- Module pattern or IIFE for encapsulation and namespace safety.
- Thin form event handlers that delegate to business logic functions.
- Xrm.WebApi async calls with proper await and error handling.
- Conditional field visibility and validation driven by configuration or metadata.
- Shared utility namespace for cross-form reusable logic.

## CODING RULES

- Use `formContext` from `executionContext.getFormContext()`; never use deprecated `Xrm.Page`.
- Use only supported Xrm SDK methods; avoid DOM manipulation or internal APIs.
- Handle all async promise rejections explicitly.
- Avoid hardcoded field names or GUIDs; use constants defined in a shared module.
- Pass `executionContext` as the first parameter in all registered handlers.

## SECURITY RULES

- Do not include secrets, tokens, or sensitive credentials in client-side scripts.
- Validate user security roles before enabling privileged actions in the UI.
- Do not call external APIs without approved CORS and authentication configuration.
- Sanitize any user-derived input before constructing queries.

## TESTING RULES

- Unit test business logic functions independently of the Xrm runtime.
- Mock `formContext` and `executionContext` for handler-level tests.
- Cover visibility rules, validation logic, and error handling paths.
- Test async data retrieval with simulated success and failure responses.
- Keep tests executable outside the Dynamics environment.

## COMMON MISTAKES

- Using deprecated `Xrm.Page` API instead of `formContext`.
- Polluting the global scope with unnamespaced function declarations.
- Calling unsupported internal Dynamics APIs that break on updates.
- Ignoring promise rejection handling on async Web API calls.
- Mixing UI behavior logic with server-side enforcement concerns.

## AECF AUDIT CHECKS

- Verify namespace isolation on all exported functions.
- Verify only supported Xrm SDK methods are used.
- Verify `formContext` pattern is used instead of `Xrm.Page`.
- Verify async calls include proper error handling.
- Verify business logic is testable independently of the form runtime.
