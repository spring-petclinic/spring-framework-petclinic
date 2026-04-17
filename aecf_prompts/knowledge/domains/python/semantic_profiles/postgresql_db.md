---
profile_id: postgresql_db
title: PostgreSQL Database
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: database
stack_nodes:
  - postgresql
requires:
  - sqlalchemy
precedence: 70
fallback_mode: warn_continue
compatibility:
  - python
  - flask
  - sqlalchemy
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=postgresql
  - keyword=postgres
  - keyword=psql
max_lines_per_section: 6
tags:
  - database
  - relational
  - sql
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

PostgreSQL is the relational transactional data store. Schema ownership, migrations, access boundaries, and role discipline must remain explicit.

## ARCHITECTURE RULES

- Keep schema evolution versioned and reviewable.
- Centralize database access behind persistence adapters.
- Make connection handling, pooling, and transactional use explicit.

## DESIGN PATTERNS

- Migration-driven schema changes in CI and delivery workflows.
- Adapter-based persistence boundaries between application code and SQL concerns.
- Constraint-first design for integrity rules that belong in the database.

## CODING RULES

- Avoid ad-hoc SQL spread across handlers and services.
- Keep schema assumptions explicit in persistence code.
- Make timeout, transaction, and retry expectations visible.

## SECURITY RULES

- Use least-privilege roles and controlled credential distribution.
- Review TLS and network exposure where remote access exists.
- Treat migration and operational credentials as privileged secrets.

## TESTING RULES

- Validate migrations forward on representative schemas.
- Cover constraint failures and transaction rollback behavior.
- Check persistence behavior that depends on PostgreSQL-specific semantics.

## COMMON MISTAKES

- Unversioned schema drift.
- Over-privileged runtime database users.
- SQL or schema knowledge leaking into HTTP or orchestration layers.

## AECF AUDIT CHECKS

- Verify migration ownership and schema versioning discipline.
- Verify least-privilege access and secret handling.
- Verify database-specific behavior is isolated behind persistence boundaries.
