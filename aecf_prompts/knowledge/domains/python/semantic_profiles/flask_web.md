---
profile_id: flask_web
title: Flask Web Applications
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: framework
stack_nodes:
  - flask
requires:
  - python
precedence: 90
fallback_mode: warn_continue
compatibility:
  - python
  - sqlalchemy
  - postgresql
  - redis
  - celery
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - framework=flask
  - keyword=blueprint
  - path=wsgi.py
max_lines_per_section: 6
tags:
  - web
  - backend
  - http
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

Flask acts as the HTTP delivery layer on top of Python. Keep transport concerns, business logic, and persistence boundaries explicit.

## ARCHITECTURE RULES

- Prefer an app factory and explicit extension wiring.
- Keep request handlers thin and move orchestration into services or use cases.
- Treat configuration as environment-specific and keep secrets outside code.

## DESIGN PATTERNS

- Service layer for non-trivial business flows.
- Repository or adapter boundaries around persistence.
- Blueprint separation by bounded context or feature area.

## CODING RULES

- Do not place business rules directly inside routes.
- Avoid implicit global state beyond framework-managed app context.
- Keep extension initialization separate from request handling code.

## SECURITY RULES

- Validate input at the HTTP boundary.
- Make authentication and authorization explicit before mutating actions.
- Keep secrets and credentials out of config modules and source files.

## TESTING RULES

- Test route contracts separately from service logic.
- Use app factory fixtures rather than shared mutable global apps.
- Cover invalid input and authorization failures as first-class cases.

## COMMON MISTAKES

- Fat blueprints that hide orchestration and side effects.
- Direct ORM usage spread across routes.
- Implicit configuration or extension state coupled to import order.

## AECF AUDIT CHECKS

- Verify app factory or equivalent explicit app construction.
- Verify handlers remain thin and delegate to service boundaries.
- Verify request validation, auth, and config hygiene are explicit.
