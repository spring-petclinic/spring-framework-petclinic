# Rust Domain

## What is this domain?

The **Rust** domain covers Rust application and systems development. It provides rules for explicit ownership and error handling, trait-based composition, crate boundary management, and safety-first coding patterns — leveraging `cargo` tooling and the Rust type system.

## Capabilities

- **Architecture guidance** with explicit `Cargo.toml` crate boundaries, domain/transport separation, and composition roots.
- **Coding rules** for `Result` types at boundaries, strong typing for identifiers/payloads, and minimal shared mutability.
- **Testing guidance** using `cargo test` across unit, integration, and boundary-error scenarios with ownership edge cases.
- **Dependency management** with minimal, stable, well-maintained crates and explicit feature flags.
- **Common pitfall detection** for premature `Arc<Mutex<...>>`, generic catch-all error conversions, and framework leakage into domain modules.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `rust_base_architecture` | Rust project architecture — crate layout, error handling, trait design, async patterns. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=rust
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=rust/rust_base_architecture
```
