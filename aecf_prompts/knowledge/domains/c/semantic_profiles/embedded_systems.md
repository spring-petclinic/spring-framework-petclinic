---
profile_id: c_embedded_systems
title: C Embedded Systems Development
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - c
requires: []
precedence: 85
fallback_mode: warn_continue
compatibility:
  - c
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=embedded
  - keyword=firmware
  - keyword=microcontroller
  - keyword=rtos
  - keyword=bare metal
max_lines_per_section: 6
tags:
  - c
  - embedded
  - firmware
  - microcontroller
  - rtos
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

C embedded systems development targets resource-constrained hardware with deterministic timing, explicit memory management, and hardware-awareness as primary concerns.

## ARCHITECTURE RULES

- Separate hardware abstraction layer (HAL) from application logic; never access registers directly in business code.
- Use layered architecture: hardware drivers, platform abstraction, application services.
- Keep interrupt service routines (ISR) minimal; defer processing to main-loop or task context.
- Design for deterministic memory usage; prefer static allocation over dynamic allocation.
- Isolate platform-specific code behind well-defined interfaces for portability and testability.

## DESIGN PATTERNS

- HAL with register abstraction and driver interfaces behind function pointers.
- State machines for protocol and device control logic.
- Ring buffers for ISR-to-task data transfer.
- Callback registration for event-driven peripheral handling.
- Static memory pools instead of malloc/free for predictable footprint.

## CODING RULES

- Mark ISR functions appropriately and keep them as short as possible.
- Use `volatile` for hardware-mapped registers and shared ISR/main-loop variables.
- Avoid dynamic memory allocation (malloc/free) unless the RTOS or platform explicitly supports it.
- Use fixed-width integer types (`uint8_t`, `uint32_t`) for hardware register and protocol data.
- Document all timing constraints and critical sections.

## SECURITY RULES

- Validate all external input (serial, network, sensor) before processing.
- Protect firmware update paths with integrity verification and rollback capability.
- Review DMA, peripheral access, and debug port exposure for information leakage.
- Disable unused peripherals and debug interfaces in production builds.

## TESTING RULES

- Test application logic on host with mock HAL; test hardware integration on target.
- Cover state machine transitions, boundary values, and ISR edge cases.
- Validate memory usage stays within static budget using linker map analysis.
- Include one regression test for timing-critical or interrupt-sensitive behavior.
- Use sanitizers on host builds to catch memory errors early.

## COMMON MISTAKES

- Accessing hardware registers directly in application-level code without abstraction.
- Using dynamic allocation in memory-constrained or safety-critical contexts.
- Blocking in ISR context or performing long operations in interrupt handlers.
- Forgetting `volatile` on shared variables between ISR and main context.
- Ignoring stack overflow risks in deeply nested or recursive code.

## AECF AUDIT CHECKS

- Verify HAL layer separates hardware access from application logic.
- Verify ISRs are minimal and defer work to task context.
- Verify memory allocation strategy is deterministic and predictable.
- Verify external inputs are validated at system boundaries.
- Verify timing constraints and critical sections are documented and tested.
