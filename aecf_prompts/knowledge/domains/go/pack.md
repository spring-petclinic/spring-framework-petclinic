# Go Domain Pack

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## Architecture Rules
- Treat `go.mod` as the authoritative module contract and keep package ownership explicit.
- Keep `cmd/` entrypoints thin and push business behavior into reusable internal packages.
- Prefer clear import direction and avoid circular package dependencies.

## Coding Rules
- Pass `context.Context` deliberately across request and integration boundaries.
- Return errors instead of panicking for expected failures.
- Keep interfaces small and define them near the consuming package.

## Testing Rules
- Prefer table-driven tests for business rules and `httptest` for HTTP boundaries.
- Cover happy path, invalid input, and one concurrency or timeout edge case.
- Run deterministic tests that remain safe under `-race` where relevant.

## Dependency Rules
- Keep third-party packages justified and lightweight.
- Avoid unnecessary frameworks when the standard library is sufficient.
- Isolate infrastructure SDKs behind focused adapters or clients.

## Common Pitfalls
- Putting orchestration and configuration directly in `main()`.
- Sharing mutable globals across handlers or goroutines.
- Using broad utility packages that blur bounded contexts.