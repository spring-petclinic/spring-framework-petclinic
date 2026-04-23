---
profile_id: cpp_modern_application
title: Modern C++ Application Development
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - cpp
requires: []
precedence: 90
fallback_mode: warn_continue
compatibility:
  - cpp
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - extension=.cpp
  - extension=.hpp
  - keyword=modern c++
  - keyword=c++17
  - keyword=c++20
max_lines_per_section: 6
tags:
  - cpp
  - modern
  - c++17
  - c++20
  - application
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

Modern C++ application development should leverage C++17/C++20 features including RAII, smart pointers, structured bindings, `std::optional`, `std::variant`, concepts, and coroutines where supported.

## ARCHITECTURE RULES

- Use RAII exclusively for resource management; no manual new/delete in application code.
- Keep class hierarchies shallow; prefer composition and templates over deep inheritance.
- Use namespaces to organize modules and avoid name collisions.
- Separate interface headers from implementation to control compilation dependencies.
- Use dependency injection through constructor parameters or templates, not global singletons.

## DESIGN PATTERNS

- RAII wrappers for all external resources (files, handles, connections, locks).
- Type-safe variants (`std::variant`, `std::optional`) for values that may be absent or polymorphic.
- Value semantics with move support for efficient data transfer.
- CRTP or policy-based design for compile-time polymorphism where runtime overhead matters.
- `std::function` and lambdas for configurable callbacks and strategies.

## CODING RULES

- Use `auto` for complex type deductions but keep public API return types explicit.
- Prefer `std::unique_ptr` for exclusive ownership and `std::shared_ptr` only when shared ownership is genuinely needed.
- Use `constexpr` and `consteval` for compile-time computation where possible.
- Mark functions `noexcept` when they genuinely cannot throw; do not use it speculatively.
- Prefer range-based for loops and standard algorithms over raw index loops.
- Use `[[nodiscard]]` on functions where ignoring the return value is likely a bug.

## SECURITY RULES

- Use bounded containers (`std::array`, `std::span`) instead of raw C arrays.
- Validate all external input before processing; prefer strong typing over stringly-typed data.
- Avoid `reinterpret_cast` and undefined behavior; use `std::bit_cast` (C++20) when needed.
- Keep dependencies updated and audited; pin versions in the build system.
- Review thread safety for shared mutable state; prefer immutable data and message passing.

## TESTING RULES

- Use Google Test, Catch2, or doctest aligned with the project's existing framework.
- Test RAII correctness: verify resources are released on both normal and exception paths.
- Cover move semantics, edge cases for `std::optional`/`std::variant`, and template instantiations.
- Run ASan, UBSan, and TSan in CI to catch undefined behavior and data races.
- Include one regression test for exception safety guarantees.

## COMMON MISTAKES

- Using raw `new`/`delete` instead of smart pointers or containers.
- Overusing `std::shared_ptr` when `std::unique_ptr` suffices, creating false shared ownership.
- Ignoring move semantics, causing unnecessary copies of large objects.
- Using C-style casts instead of named casts.
- Catching exceptions by value instead of by const reference.
- Writing header-only code that inflates compile times without justification.

## AECF AUDIT CHECKS

- Verify RAII is used for all resource management with no raw new/delete.
- Verify smart pointer usage is appropriate (unique vs shared).
- Verify modern C++ idioms are used consistently (range-for, algorithms, structured bindings).
- Verify sanitizers are enabled in CI build configurations.
- Verify exception safety is documented and tested for resource-managing code.
