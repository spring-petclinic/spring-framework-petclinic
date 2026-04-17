---
profile_id: standalone_components
title: Angular Standalone Components
version: 1.0.0
status: active
owner: AECF
last_review: 2026-04-07
profile_type: architecture
stack_nodes:
  - standalone_components
requires:
  - angular
precedence: 82
fallback_mode: warn_continue
compatibility:
  - angular
  - ngrx_state_management
  - observability
  - ci-cd
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=bootstrapapplication
  - keyword=standalone:true
  - keyword=providerouter
  - path=src/main.ts
max_lines_per_section: 6
tags:
  - angular
  - standalone
  - frontend
  - architecture
---

LAST_REVIEW: 2026-04-07
OWNER SEACHAD

## STACK

Standalone Angular applications should keep bootstrap, routing, provider scope, and feature composition explicit so the app remains modular without hidden NgModule-era coupling.

## ARCHITECTURE RULES

- Keep application bootstrap in `main.ts` and app-shell wiring explicit with `bootstrapApplication` and provider registration.
- Prefer feature-local route definitions and lazy loading where it improves boundary clarity.
- Keep provider scope intentional so feature-specific services do not silently become app-wide singletons.

## DESIGN PATTERNS

- Standalone feature entry components paired with route configuration and focused providers.
- Shared UI primitives separated from domain-aware smart containers or facades.
- Composition through `provideRouter`, `provideHttpClient`, and environment providers instead of broad module indirection.

## CODING RULES

- Avoid recreating monolithic pseudo-modules through giant shared barrel files.
- Keep imports explicit at the component level when they define rendering dependencies.
- Use route-level or feature-level providers when behavior should stay bounded.

## SECURITY RULES

- Review route guards, resolvers, and client-stored auth state as trust boundaries.
- Do not assume lazy loading or provider boundaries enforce authorization by themselves.
- Keep HTML rendering and dynamic template inputs sanitized and justified.

## TESTING RULES

- Cover standalone bootstrap or route composition behavior when changing provider wiring.
- Include success, invalid navigation or guard behavior, and one lazy-loading or teardown edge case.
- Add a non-regression assertion when replacing module-based wiring with standalone providers.

## COMMON MISTAKES

- Treating standalone components as a cosmetic syntax change while keeping the same hidden shared-state issues.
- Registering feature-local providers globally and broadening lifetime accidentally.
- Moving too much orchestration into app bootstrap instead of feature composition.

## AECF AUDIT CHECKS

- Verify bootstrap, routing, and provider scope are explicit and reviewable.
- Verify standalone composition does not hide shared-state or auth assumptions.
- Verify tests cover route and provider behavior, not just template rendering.