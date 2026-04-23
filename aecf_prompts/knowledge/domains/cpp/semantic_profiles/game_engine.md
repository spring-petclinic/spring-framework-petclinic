---
profile_id: cpp_game_engine
title: C++ Game and Graphics Engine Development
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - cpp
requires: []
precedence: 80
fallback_mode: warn_continue
compatibility:
  - cpp
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=game engine
  - keyword=unreal
  - keyword=vulkan
  - keyword=opengl
  - keyword=directx
  - keyword=ecs
max_lines_per_section: 6
tags:
  - cpp
  - game
  - graphics
  - engine
  - ecs
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

C++ game and graphics engine development emphasizes frame-budget-aware code, cache-friendly data layout, deterministic memory management, and separation between engine systems and game logic.

## ARCHITECTURE RULES

- Separate engine systems (rendering, physics, audio, input) from game-specific logic.
- Use Entity-Component-System (ECS) or component-based architecture for composable game objects.
- Keep hot-path code cache-friendly with data-oriented design (SOA over AOS where measurable).
- Design for frame-budget awareness; profile and measure before optimizing.
- Use layered initialization and shutdown sequences for deterministic resource management.

## DESIGN PATTERNS

- ECS for decoupled, composable game object behavior.
- Custom memory allocators (arena, pool, linear) for predictable allocation patterns.
- Command pattern for input handling and undo/redo systems.
- Observer/event system for decoupled inter-system communication.
- Job/task system for multi-threaded workload distribution.

## CODING RULES

- Avoid heap allocation in per-frame hot paths; use pre-allocated pools and arenas.
- Prefer value types and contiguous containers (`std::vector`, custom arrays) for cache locality.
- Keep virtual function calls out of per-entity inner loops where performance matters.
- Use `constexpr` for compile-time constants and configuration tables.
- Profile before micro-optimizing; prefer correct and readable code first.

## SECURITY RULES

- Validate all asset loading and deserialization from external files.
- Protect network protocol parsing against malformed packets and buffer overflows.
- Sandbox scripting environments (Lua, Wren, etc.) exposed to modders.
- Review plugin and mod loading paths for code injection risks.

## TESTING RULES

- Unit test game logic and engine systems independently of rendering.
- Cover ECS component interactions, state machine transitions, and serialization round-trips.
- Use deterministic simulation for replay-based regression testing.
- Validate memory usage with custom allocator tracking and leak detection.
- Include one performance regression test for frame-budget-critical paths.

## COMMON MISTAKES

- Dynamic allocation in per-frame code paths causing unpredictable frame timing.
- Monolithic game objects instead of composable component architecture.
- Ignoring cache layout and iterating over scattered pointers in inner loops.
- Premature optimization without profiling evidence.
- Tight coupling between rendering API and game logic.

## AECF AUDIT CHECKS

- Verify engine systems are decoupled from game-specific logic.
- Verify hot-path code avoids heap allocation and virtual dispatch where measured.
- Verify asset loading validates input against malformed or untrusted data.
- Verify memory management uses deterministic patterns (pools, arenas).
- Verify tests cover game logic independently of rendering subsystem.
