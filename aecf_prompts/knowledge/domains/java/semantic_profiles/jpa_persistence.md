---
profile_id: jpa_persistence
title: JPA Persistence
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: library
stack_nodes:
  - jpa
requires:
  - java
precedence: 70
fallback_mode: warn_continue
compatibility:
  - java
  - spring
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=hibernate
  - keyword=@entity
  - keyword=entitymanager
max_lines_per_section: 6
tags:
  - java
  - persistence
  - jpa
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

JPA persistence should be treated as an explicit persistence layer with clear aggregate boundaries, transactional scope, and mapping ownership.

## ARCHITECTURE RULES

- Keep repositories at aggregate or application boundaries, not scattered across services.
- Make transaction ownership explicit and local to the use case.
- Keep ORM entities from leaking into public transport contracts.

## DESIGN PATTERNS

- Repository interfaces for domain-facing access.
- Dedicated mappers where entity and domain models diverge.
- Explicit read-model strategies when query complexity grows.

## CODING RULES

- Avoid ad-hoc query logic spread across controller and service classes.
- Be explicit about fetch strategies and lazy-loading assumptions.
- Keep entity lifecycle side effects understandable and testable.

## SECURITY RULES

- Avoid unsafe dynamic query construction.
- Review database credentials, migration credentials, and connection configuration.
- Ensure authorization rules do not depend only on repository filtering.

## TESTING RULES

- Cover transactional rollback behavior and constraint failures.
- Validate persistence mappings that are easy to break during refactors.
- Keep database integration tests targeted to persistence behavior, not entire app flows.

## COMMON MISTAKES

- Treating ORM entities as domain or API contracts.
- Hiding business rules in persistence callbacks.
- Ignoring fetch-plan and N+1 query behavior until production.

## AECF AUDIT CHECKS

- Verify transaction scope and repository ownership are explicit.
- Verify entities do not leak outside persistence boundaries without intent.
- Verify persistence tests cover failure and rollback paths.