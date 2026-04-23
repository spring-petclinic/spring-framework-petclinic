---
profile_id: ngrx_state_management
title: Angular NgRx State Management
version: 1.0.0
status: active
owner: AECF
last_review: 2026-04-07
profile_type: architecture
stack_nodes:
  - ngrx_state_management
requires:
  - angular
precedence: 80
fallback_mode: warn_continue
compatibility:
  - angular
  - standalone_components
  - observability
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=@ngrx/store
  - keyword=createreducer
  - keyword=createeffect
  - keyword=providestate
max_lines_per_section: 6
tags:
  - angular
  - ngrx
  - state-management
  - frontend
---

LAST_REVIEW: 2026-04-07
OWNER SEACHAD

## STACK

Angular applications using NgRx should treat the store as an explicit application-state boundary, not as a default container for every piece of transient UI behavior.

## ARCHITECTURE RULES

- Keep store slices aligned with durable business capabilities, not arbitrary component trees.
- Separate reducers, selectors, effects, and facade or orchestration layers clearly.
- Keep ephemeral form state, modal state, and view-only toggles out of the store unless there is a real cross-feature need.

## DESIGN PATTERNS

- Selectors as the read contract and effects as the async side-effect boundary.
- Facades only when they simplify component contracts instead of hiding store semantics.
- Normalized entities and explicit loading or error state for network-backed feature slices.

## CODING RULES

- Keep actions event-oriented and avoid command-style overloading that hides side effects.
- Do not mutate state in reducers or derive business decisions in components from raw store internals.
- Prefer memoized selectors over repeated projection logic in components.

## SECURITY RULES

- Do not store secrets, tokens, or trust-sensitive authorization facts in replayable client state without justification.
- Review effects that call external APIs or persist browser data as security boundaries.
- Keep error payloads and diagnostics sanitized before committing them to store state.

## TESTING RULES

- Cover reducer happy path, invalid or unexpected action handling, and one selector or effect edge case.
- Add non-regression tests around loading, error, or concurrency-sensitive flows when effects change.
- Verify components rely on selectors or facades, not handwritten store-shape assumptions.

## COMMON MISTAKES

- Putting every UI flag into NgRx and inflating the state model beyond business value.
- Hiding orchestration in effects without clear action boundaries or cancellation behavior.
- Letting components dispatch and select ad hoc without a stable feature contract.

## AECF AUDIT CHECKS

- Verify store ownership is justified and bounded to durable application state.
- Verify reducers, selectors, and effects keep responsibilities separate.
- Verify tests cover state transitions and side-effect behavior intentionally.