# C Domain

## What is this domain?

The **C** domain covers systems-level and embedded development using ISO C (C11/C17+). It provides rules and guardrails for writing portable, memory-safe, and well-structured C code — from embedded firmware to POSIX system utilities and CMake-based build pipelines.

## Capabilities

- **Code generation** with self-contained headers, include guards, clear `.h`/`.c` separation, and explicit memory ownership.
- **Safety rules** prohibiting unsafe string functions (`gets`, `sprintf`) and enforcing bounded alternatives.
- **Build system integration** respecting CMake, Makefile, or Meson project conventions.
- **Testing guidance** using lightweight C frameworks (Unity, CMocka, Check) with memory-safety regression checks.
- **Common pitfall detection** for memory leaks, ignored return values, struct portability, and platform assumptions.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `embedded_systems` | Bare-metal and RTOS firmware — MISRA awareness, ISR design, HAL patterns, static allocation. |
| `systems_programming` | POSIX systems code — OS interfaces, memory management, socket/IPC, process lifecycle. |
| `cmake_build` | CMake-based build infrastructure — targets, presets, dependency management, cross-compilation. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=c
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=c/embedded_systems
```
