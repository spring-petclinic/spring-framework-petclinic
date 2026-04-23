---
profile_id: rust_base_architecture
title: Rust Base Architecture
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: architecture
stack_nodes:
  - rust
requires:
  - rust
precedence: 82
fallback_mode: warn_continue
compatibility:
  - rust
  - clean-architecture
  - observability
  - ci-cd
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - manifest=cargo.toml
  - extension=.rs
  - path=src/main.rs
  - keyword=rust
max_lines_per_section: 6
tags:
  - rust
  - cargo
  - architecture
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

Rust systems should treat Cargo crates or workspaces as the structural boundary, with explicit separation between domain code, adapters, and runtime composition.

## ARCHITECTURE RULES

- Keep framework, async runtime, and infrastructure dependencies at the outer layers.
- Separate domain types and use cases from HTTP, messaging, or persistence modules.
- Use traits and constructors to make boundary contracts explicit.

## DESIGN PATTERNS

- Cargo workspace for multi-binary or multi-adapter systems.
- Trait-based ports with concrete adapters for storage or transport.
- Dedicated bootstrap/config modules for runtime assembly.

## CODING RULES

- Return explicit domain or boundary errors instead of panicking on recoverable failures.
- Keep ownership and borrowing choices local and understandable.
- Use typed request/response models at serialization and protocol boundaries.

## SECURITY RULES

- Never `unwrap` untrusted input or external payload parsing paths.
- Audit `unsafe` blocks and FFI boundaries explicitly.
- Keep secret loading and environment-derived configuration explicit and centralized.

## TESTING RULES

- Cover pure domain logic separately from adapter integration tests.
- Include success, invalid input, and one async or error-mapping edge case.
- Prefer deterministic `cargo test` coverage over timing-dependent runtime tests.

## COMMON MISTAKES

- Letting web/runtime concerns leak into domain crates.
- Using shared mutable state where message passing or ownership transfer is simpler.
- Flattening all errors into generic wrappers too early.

## AECF AUDIT CHECKS

- Verify Cargo structure and crate boundaries reflect architecture ownership.
- Verify trait boundaries isolate infrastructure from core logic.
- Verify tests cover both nominal behavior and boundary failures.