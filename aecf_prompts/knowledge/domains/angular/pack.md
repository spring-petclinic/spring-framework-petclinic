# Angular Domain Pack

LAST_REVIEW: 2026-04-07
OWNER SEACHAD

## Architecture Rules
- Treat Angular as a structured application shell with explicit feature boundaries, routing ownership, and service boundaries.
- Keep components focused on presentation and interaction orchestration; move durable business logic into services, facades, or domain-oriented modules.
- Respect the existing composition style, including standalone components versus NgModule-based structure, unless the task explicitly changes architecture.

## Coding Rules
- Keep template logic shallow and move branching, transformation, and async coordination into TypeScript.
- Make signal, observable, and form-state ownership explicit; avoid duplicating the same state across components, services, and stores.
- Keep dependency injection scopes intentional and avoid singleton leakage for feature-local behavior.

## Testing Rules
- Prefer component behavior tests plus focused service tests over DOM-fragile implementation checks.
- Cover happy path, invalid interaction or validation, and one routing, async, or teardown edge case.
- Verify subscriptions, effects, and async UI flows clean up correctly.

## Dependency Rules
- Keep RxJS, state-management, UI-kit, and build-tooling choices aligned with the existing Angular workspace conventions.
- Review bundle and browser impact before adding client-side dependencies.
- Avoid introducing parallel state libraries or overlapping form abstractions without a clear migration plan.

## Common Pitfalls
- Fat smart components mixing template state, API orchestration, and domain rules.
- Manual subscriptions that leak across route changes or repeated component mounts.
- Business rules hidden in template expressions, pipes, or ad hoc form callbacks.