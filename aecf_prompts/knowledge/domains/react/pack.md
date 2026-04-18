# React Domain Pack

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## Architecture Rules
- Treat React as a UI composition layer, not as the place where all business rules must live.
- Separate app shell, feature modules, reusable components, and data-access concerns clearly.
- Keep routing, state ownership, and side effects intentional and reviewable.

## Coding Rules
- Prefer explicit props, predictable hooks, and immutable state transitions.
- Keep asynchronous effects isolated from presentational components when possible.
- Make loading, error, and empty states explicit in user-facing flows.

## Testing Rules
- Prefer React Testing Library for behavior-driven UI checks.
- Cover happy path, invalid user interaction, and one state or routing edge case.
- Keep tests resilient to refactors by focusing on observable behavior.

## Dependency Rules
- Keep UI libraries and state tools justified by actual complexity.
- Avoid coupling feature logic tightly to router or styling implementation details.
- Review client-side packages for bundle impact and security posture.

## Common Pitfalls
- Fetching or mutating data directly inside leaf components.
- Duplicating derived state across multiple hooks or components.
- Mixing design-system primitives with domain behavior in the same layer.