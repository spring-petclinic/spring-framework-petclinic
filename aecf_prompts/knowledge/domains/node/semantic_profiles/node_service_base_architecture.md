---
profile_id: node_service_base_architecture
title: Node.js Service Base Architecture
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: architecture
stack_nodes:
  - node
requires:
  - node
precedence: 79
fallback_mode: warn_continue
compatibility:
  - node
  - event-driven
  - observability
  - ci-cd
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - manifest=package.json
  - extension=.js
  - path=server.js
  - keyword=express
max_lines_per_section: 6
tags:
  - node
  - backend
  - architecture
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

Node.js services should be treated as explicit asynchronous backends with a clear composition root, validated configuration, and thin transport layers.

## ARCHITECTURE RULES

- Separate routes or controllers from orchestration, domain services, and infrastructure clients.
- Keep startup, dependency wiring, and process lifecycle management centralized.
- Isolate background consumers, schedulers, or queue handlers from HTTP transport code.

## DESIGN PATTERNS

- App factory or bootstrap module that assembles middleware, routes, and adapters.
- Service or use-case modules behind route/controller boundaries.
- Dedicated infrastructure adapters for persistence, queues, and external APIs.

## CODING RULES

- Await or return every promise path intentionally.
- Validate env-derived configuration once at startup.
- Keep framework-specific request objects out of core business modules.

## SECURITY RULES

- Validate request payloads and headers at the boundary.
- Review dependency provenance and keep secrets out of source and logs.
- Treat `process.env`, external payloads, and deserialized objects as untrusted input.

## TESTING RULES

- Cover pure service logic separately from app or route integration tests.
- Include success, invalid input, and one async failure or authorization case.
- Add a non-regression assertion around startup config or route contract behavior.

## COMMON MISTAKES

- Fat route handlers mixing validation, business rules, and persistence.
- Unhandled promise rejections or hidden background failures.
- Shared singleton state that leaks across requests or tests.

## AECF AUDIT CHECKS

- Verify startup wiring, route boundaries, and adapter ownership are explicit.
- Verify async error handling and configuration validation are production-aware.
- Verify tests cover transport contracts plus failure behavior.