# Node.js Domain Pack

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## Architecture Rules
- Treat `package.json` as the runtime and tooling manifest, not as the architecture itself.
- Keep HTTP or event transport thin and move business behavior into services or use cases.
- Separate startup wiring, configuration, background jobs, and feature modules clearly.

## Coding Rules
- Validate configuration at startup and make async boundaries explicit.
- Await promises intentionally and surface failures through centralized handling.
- Keep module side effects minimal so tests and composition stay predictable.

## Testing Rules
- Prefer focused unit tests for services plus integration tests for the app boundary.
- Cover happy path, invalid input, and one async failure or timeout case.
- Avoid tests that depend on uncontrolled timers, ports, or global process state.

## Dependency Rules
- Add runtime packages only when the platform or framework value is clear.
- Review dependency weight, maintenance, and security posture before adoption.
- Isolate SDK or queue clients behind dedicated adapters.

## Common Pitfalls
- Business logic living inside route handlers or middleware chains.
- Hidden singleton state shared across requests or tests.
- Configuration and secrets read ad hoc throughout the codebase.