---
profile_id: zkoss
title: ZKoss Server-Driven UI
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-25
profile_type: framework
stack_nodes:
  - zkoss
requires:
  - java
precedence: 85
fallback_mode: warn_continue
compatibility:
  - java
  - spring
  - jpa
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=zkoss
  - keyword=zul
  - keyword=selectorcomposer
  - keyword=executions.createcomponents
  - path=.zul
  - path=web-inf/zk.xml
max_lines_per_section: 6
tags:
  - java
  - zkoss
  - zul
  - ui
---

LAST_REVIEW: 2026-03-25
OWNER SEACHAD

## STACK

ZKoss should be treated as a server-driven Java UI framework where ZUL views, composers or view models, and application services remain clearly separated.

## ARCHITECTURE RULES

- Keep ZUL pages focused on presentation and bind them to thin composers or view models.
- Route business use cases through application services instead of directly from UI event handlers.
- Make desktop, session, and execution scope ownership explicit for stateful flows.

## DESIGN PATTERNS

- Prefer MVVM with binder-backed view models for form-heavy screens and reusable state.
- Use selector composers only when event wiring is clearer than binder expressions.
- Extract reusable ZUL fragments and backing models for repeated widgets or dialogs.

## CODING RULES

- Do not place business rules inside ZUL expressions, command bindings, or click handlers.
- Minimize direct access to `Executions`, `Sessions`, and desktop state outside dedicated UI adapters.
- Keep validation, navigation, and service orchestration explicit and easy to trace from the page entry point.

## SECURITY RULES

- Validate client-originated events, uploads, and bound parameters on the server side.
- Do not trust hidden fields, client state, or binder-managed values as authorization proof.
- Review desktop and session scoped state for cross-user leakage, stale data, and privilege drift.

## TESTING RULES

- Cover composer or view-model behavior with focused tests using service-level doubles.
- Add integration tests for critical binder, command, and event-driven flows on user-facing screens.
- Verify validation, authorization, and scope reset behavior across desktop or session lifecycle boundaries.

## COMMON MISTAKES

- Fat composers that mix UI orchestration, domain logic, and persistence concerns.
- Scattering the same rule across ZUL bindings, Java handlers, and service methods.
- Relying on implicit session state instead of explicit navigation and lifecycle cleanup.

## AECF AUDIT CHECKS

- Verify ZUL, composer or view-model, and service boundaries are explicit.
- Verify session and desktop scope usage is intentional, bounded, and authorization-aware.
- Verify tests cover critical UI event flows, validation failures, and privileged actions.