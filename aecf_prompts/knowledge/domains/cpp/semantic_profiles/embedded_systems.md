---
profile_id: cpp_embedded_systems
title: C++ Embedded and Real-Time Systems
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - cpp
requires: []
precedence: 85
fallback_mode: warn_continue
compatibility:
  - cpp
  - c
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=embedded c++
  - keyword=rtos
  - keyword=real-time
  - keyword=bare metal c++
  - keyword=constrained c++
max_lines_per_section: 6
tags:
  - cpp
  - embedded
  - rtos
  - real-time
  - constrained
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

C++ embedded and real-time development targets constrained hardware where deterministic timing, controlled memory usage, and predictable resource behavior are primary requirements. A subset of C++ features is used with restrictions on dynamic allocation and exceptions.

## ARCHITECTURE RULES

- Use RAII with static or pool-based allocation; avoid heap allocation in real-time paths.
- Separate hardware abstraction from application logic using templates or virtual interfaces depending on code-size constraints.
- Keep interrupt service routines in C-linkage or minimal C++ wrappers; avoid complex C++ in ISR context.
- Design for deterministic worst-case execution time in critical paths.
- Use namespaces and strong typing to prevent hardware register misuse.

## DESIGN PATTERNS

- RAII with placement new and static storage for deterministic lifetime management.
- CRTP for zero-cost polymorphism where virtual dispatch overhead is unacceptable.
- Type-safe register access using `constexpr` and strong types instead of raw bitmasks.
- Static memory pools for bounded dynamic-like allocation.
- State machines with `std::variant` or enum-based dispatch for device control.

## CODING RULES

- Restrict or disable exceptions and RTTI when the platform does not support them (`-fno-exceptions`, `-fno-rtti`).
- Use `constexpr` for compile-time computations and configuration tables.
- Prefer `std::array` over C arrays and `std::span` (C++20) for non-owning views.
- Mark ISR entry points with `extern "C"` linkage.
- Avoid `std::string`, `std::vector`, and other allocating containers in real-time code paths; use fixed-capacity alternatives.

## SECURITY RULES

- Validate all sensor and communication input at system boundaries.
- Protect firmware update and debug paths with integrity verification.
- Disable unused peripherals and debug interfaces in production builds.
- Use stack canaries and MPU (memory protection unit) when hardware supports it.

## TESTING RULES

- Test application logic on host with mock HAL; test hardware integration on target.
- Verify resource cleanup and RAII correctness in both normal and error paths.
- Measure worst-case stack usage and validate it fits within thread/task limits.
- Use sanitizers on host builds; use static analysis tools for embedded builds.
- Include one regression test for timing or interrupt-related behavior.

## COMMON MISTAKES

- Using heap-allocating STL containers in real-time code paths.
- Enabling exceptions or RTTI on platforms that do not support them, causing silent failures.
- Complex C++ object construction in ISR context.
- Ignoring worst-case execution time in priority-sensitive code.
- Tight coupling between application logic and hardware register access.

## AECF AUDIT CHECKS

- Verify no heap allocation occurs in real-time or ISR code paths.
- Verify RAII is used for all resource management with deterministic lifetime.
- Verify hardware abstraction separates register access from application logic.
- Verify platform constraints (no-exceptions, no-RTTI) are respected.
- Verify tests validate resource cleanup and timing-critical behavior.
