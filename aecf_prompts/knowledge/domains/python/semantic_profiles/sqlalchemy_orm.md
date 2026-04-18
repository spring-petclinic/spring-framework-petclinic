---
profile_id: sqlalchemy_orm
title: SQLAlchemy ORM
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: library
stack_nodes:
  - sqlalchemy
requires:
  - python
precedence: 70
fallback_mode: warn_continue
compatibility:
  - python
  - flask
  - postgresql
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=sqlalchemy
  - keyword=alembic
max_lines_per_section: 6
tags:
  - orm
  - persistence
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

SQLAlchemy provides ORM and query composition capabilities. Session lifecycle and transaction boundaries must remain explicit and controlled outside handlers.

## ARCHITECTURE RULES

- Scope sessions to requests or use cases, not to global process state.
- Keep persistence adapters separate from application services.
- Isolate model-to-domain translation where domain complexity exists.

## DESIGN PATTERNS

- Repository or adapter boundaries around ORM operations.
- Unit-of-work style transaction handling when workflows span multiple writes.
- Migration discipline through Alembic or equivalent tooling.

## CODING RULES

- Do not leak ORM models as external API contracts.
- Do not mix transaction orchestration with HTTP transport code.
- Avoid ad-hoc query logic scattered across modules.

## SECURITY RULES

- Use parameterized query construction and avoid unsafe dynamic SQL assembly.
- Keep connection strings and credentials out of source code.
- Protect migration credentials and privileged operational paths.

## TESTING RULES

- Test repositories or adapters against realistic persistence behavior.
- Cover rollback and error paths for failed writes.
- Validate persistence constraints and mapping edge cases.

## COMMON MISTAKES

- Long-lived sessions shared across unrelated flows.
- Business logic hidden in ORM models or query helpers.
- Transaction scope leaking across service boundaries.

## AECF AUDIT CHECKS

- Verify explicit session scope and transaction boundaries.
- Verify persistence access is centralized behind adapters or repositories.
- Verify migration discipline and persistence error handling are present.
