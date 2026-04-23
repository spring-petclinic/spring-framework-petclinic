# C++ Domain Pack

## Code Generation Rules
- Prefer modern C++ (C++17/C++20) unless the project explicitly constrains to an earlier standard.
- Use RAII for all resource management; avoid raw `new`/`delete` in application code.
- Prefer smart pointers (`std::unique_ptr`, `std::shared_ptr`) over raw pointers for ownership.
- Keep header-implementation separation clear; use forward declarations to minimize include chains.
- Use `const`, `constexpr`, and `noexcept` where semantically correct to strengthen contracts.

## Testing Rules
- Prefer Google Test, Catch2, or doctest aligned with the project's existing test framework.
- Cover happy path, invalid input, RAII resource cleanup, and one edge case for every new behavior.
- Use sanitizers (ASan, UBSan, TSan) in CI test runs when the toolchain supports them.
- Test exception safety guarantees (basic, strong, nothrow) for operations that manage resources.

## Build And Dependency Rules
- Respect the existing build system: CMake, Meson, Bazel, or Makefile.
- Keep third-party dependencies managed through a reproducible mechanism (vcpkg, Conan, FetchContent, vendored).
- Maintain consistent compiler warning levels and treat warnings as errors in CI.
- Keep platform-specific code behind abstractions or conditional compilation.

## Common Pitfalls
- Do not use raw `new`/`delete` when smart pointers or containers can manage lifetime.
- Do not ignore move semantics; avoid unnecessary copies for large objects.
- Do not mix C-style casts with C++ code; use `static_cast`, `dynamic_cast`, `reinterpret_cast`.
- Do not expose implementation details through public headers; use the PIMPL idiom or forward declarations when appropriate.
- Do not ignore thread safety when using shared mutable state.
