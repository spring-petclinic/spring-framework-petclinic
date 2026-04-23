---
profile_id: go_service_base_architecture
title: Go Service Base Architecture
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: architecture
stack_nodes:
  - go
requires:
  - go
precedence: 80
fallback_mode: warn_continue
compatibility:
  - go
  - microservices
  - event-driven
  - observability
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - manifest=go.mod
  - extension=.go
  - path=cmd/
  - keyword=golang
max_lines_per_section: 6
tags:
  - go
  - service
  - architecture
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

Go backends should be organized around a small composition root, explicit package ownership, and predictable module boundaries anchored by `go.mod`.

## ARCHITECTURE RULES

- Keep `cmd/` entrypoints focused on bootstrapping and dependency wiring.
- Put reusable business behavior in `internal/` packages or clearly scoped modules.
- Keep external clients, repositories, and transport adapters separate from domain services.

## DESIGN PATTERNS

- Thin `main` packages delegating to application services.
- Consumer-owned interfaces for repositories and external dependencies.
- Feature or bounded-context packages rather than broad utility buckets.

## CODING RULES

- Accept `context.Context` on request-scoped or I/O-heavy boundaries.
- Return structured errors and translate them at transport boundaries.
- Keep goroutine lifecycles, cancellation, and timeouts explicit.

## SECURITY RULES

- Validate HTTP, gRPC, and message inputs before they reach domain services.
- Keep secrets and credentials out of package globals.
- Review timeout, retry, and log behavior for sensitive outbound calls.

## TESTING RULES

- Use table-driven tests for core behavior and `httptest` for transport contracts.
- Cover success, invalid input, and one timeout, cancellation, or race-adjacent edge case.
- Add at least one non-regression assertion around package boundary behavior.

## COMMON MISTAKES

- Stuffing business logic into handlers or the `main` package.
- Hiding dependency ownership inside package-level singletons.
- Creating circular or ambiguous package responsibilities.

## AECF AUDIT CHECKS

- Verify package layout reflects ownership and import direction.
- Verify request/context boundaries and error translation are explicit.
- Verify tests cover both domain rules and transport failure behavior.