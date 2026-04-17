---
profile_id: react_component_app_architecture
title: React Component App Architecture
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: architecture
stack_nodes:
  - react
requires:
  - react
precedence: 84
fallback_mode: warn_continue
compatibility:
  - react
  - observability
  - ci-cd
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - manifest=package.json
  - extension=.tsx
  - path=src/components
  - keyword=react
max_lines_per_section: 6
tags:
  - react
  - frontend
  - architecture
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

React applications should be structured as component-driven UIs with an explicit app shell, feature boundaries, and deliberate separation between rendering, state, and data access.

## ARCHITECTURE RULES

- Keep screens, features, shared UI primitives, and data hooks clearly separated.
- Move side effects and remote calls out of presentational components.
- Keep routing, layout, and state ownership explicit at the app-shell level.

## DESIGN PATTERNS

- Feature folders combining components, hooks, and tests around one user capability.
- Shared UI primitives distinct from business-aware containers.
- Dedicated hooks or service modules for remote data access and mutation flows.

## CODING RULES

- Use explicit prop contracts and avoid duplicating derived state.
- Keep hooks deterministic and respect the rules of hooks under refactor.
- Model loading, error, and empty states intentionally for async views.

## SECURITY RULES

- Treat browser-stored tokens, URLs, and HTML content as sensitive boundaries.
- Avoid unsafe HTML rendering unless it is sanitized and justified.
- Do not rely on client-side checks as the only authorization enforcement.

## TESTING RULES

- Cover UI behavior with React Testing Library instead of implementation details.
- Include success, invalid user interaction, and one routing or state edge case.
- Add at least one non-regression assertion around async rendering or component composition.

## COMMON MISTAKES

- Fetching directly inside leaf components without reusable state boundaries.
- Prop drilling or ad hoc global state without an ownership strategy.
- Coupling styling primitives tightly to domain logic.

## AECF AUDIT CHECKS

- Verify feature, component, and data-access boundaries are explicit.
- Verify async UI states and browser trust boundaries are handled deliberately.
- Verify tests cover observable user behavior and failure states.