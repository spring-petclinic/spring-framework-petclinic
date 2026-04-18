---
profile_id: c_cmake_build
title: C CMake Build System
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: tool
stack_nodes:
  - c
  - cpp
requires: []
precedence: 65
fallback_mode: warn_continue
compatibility:
  - c
  - cpp
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - manifest=CMakeLists.txt
  - keyword=cmake
max_lines_per_section: 6
tags:
  - c
  - cpp
  - cmake
  - build
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

CMake-based builds for C and C++ projects should use modern CMake (3.15+) with target-based dependency management and reproducible configurations.

## ARCHITECTURE RULES

- Use target-based `target_link_libraries`, `target_include_directories` instead of global `include_directories` or `link_libraries`.
- Separate library targets from executable targets for reusable modules.
- Keep platform-specific logic in dedicated CMake modules or toolchain files.
- Use `FetchContent` or package managers (vcpkg, Conan) for external dependencies.

## DESIGN PATTERNS

- Hierarchical `CMakeLists.txt` with `add_subdirectory` for multi-module projects.
- Toolchain files for cross-compilation targets.
- Presets (`CMakePresets.json`) for reproducible build configurations.
- CTest integration for test discovery and execution.

## CODING RULES

- Set `CMAKE_C_STANDARD` / `CMAKE_CXX_STANDARD` explicitly at the project level.
- Enable warnings with `target_compile_options` per target, not globally.
- Use generator expressions for configuration-specific settings.
- Keep `CMakeLists.txt` files readable; avoid deeply nested logic.

## SECURITY RULES

- Enable hardening flags (stack protector, ASLR, PIC/PIE) in release and CI builds.
- Pin dependency versions for reproducible builds.
- Review imported targets from external packages for supply-chain trust.

## TESTING RULES

- Integrate tests via `enable_testing()` and `add_test()` with CTest.
- Support sanitizer builds through CMake presets or options.
- Keep test targets separate from production targets.
- Ensure CI builds run CTest after successful compilation.

## COMMON MISTAKES

- Using global include paths and link libraries instead of target-scoped commands.
- Hardcoding compiler paths or platform assumptions that break portability.
- Forgetting to set C/C++ standard, leading to inconsistent behavior across compilers.
- Mixing `add_definitions` with target-scoped properties.

## AECF AUDIT CHECKS

- Verify target-based CMake patterns are used over global commands.
- Verify C/C++ standards are set explicitly.
- Verify warning flags are enabled at appropriate levels.
- Verify external dependencies are version-pinned and reproducible.
