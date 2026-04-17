# Rust Domain Pack

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## Architecture Rules
- Treat `Cargo.toml` and crate boundaries as the primary architectural contract.
- Keep domain logic separate from transport, persistence, and runtime wiring.
- Prefer explicit modules, traits, and composition roots over hidden framework magic.

## Coding Rules
- Return explicit `Result` types at boundaries and keep error translation intentional.
- Use strong types for inputs, identifiers, and protocol payloads when invariants matter.
- Avoid unnecessary shared mutability and keep ownership choices easy to reason about.

## Testing Rules
- Prefer `cargo test` coverage across unit, integration, and boundary-error scenarios.
- Cover happy path, invalid input, and one ownership or concurrency edge case.
- Keep tests deterministic and avoid timing-sensitive async assertions unless required.

## Dependency Rules
- Keep runtime dependencies minimal and justified per crate.
- Prefer stable, well-maintained crates and make feature flags explicit.
- Avoid leaking framework-specific crates into reusable domain modules.

## Common Pitfalls
- Mixing runtime/framework concerns directly into core logic.
- Hiding error semantics behind generic catch-all conversions everywhere.
- Overcomplicating ownership with premature `Arc<Mutex<...>>` patterns.