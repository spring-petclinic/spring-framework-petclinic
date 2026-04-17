# C Domain Pack

## Code Generation Rules
- Prefer standard C (C11/C17) unless the project explicitly targets an earlier standard.
- Keep header files self-contained with include guards or `#pragma once`.
- Separate interface declarations (`.h`) from implementation (`.c`) consistently.
- Minimize global mutable state; prefer passing context through function parameters.
- Use explicit memory management with clear ownership conventions documented per module.

## Testing Rules
- Prefer a lightweight C test framework (Unity, CMocka, Check) aligned with the project's existing choice.
- Cover happy path, invalid/null input, boundary conditions, and one memory-safety regression for each new behavior.
- Avoid test dependencies on platform-specific behavior unless the test explicitly targets that platform.
- Validate resource cleanup (malloc/free pairing, file descriptor closure) in test teardown.

## Build And Dependency Rules
- Respect the existing build system: CMake projects stay CMake, Makefile projects stay Makefile, Meson stays Meson.
- Keep third-party dependencies minimal, vendored or version-pinned, and documented.
- Separate platform-specific code behind conditional compilation or abstraction layers.
- Keep compiler warning levels high (`-Wall -Wextra -Werror` or equivalent) and treat warnings as errors in CI.

## Common Pitfalls
- Do not use `gets()`, `sprintf()`, or other unsafe string functions; prefer bounded alternatives (`fgets`, `snprintf`).
- Do not assume struct layout or size across compilers/platforms without explicit packing or static assertions.
- Do not leak allocated memory; document ownership transfer for every allocation.
- Do not ignore return values from system calls and library functions.
