# C++ Domain

## What is this domain?

The **C++** domain covers modern C++ development (C++17/C++20+) across application, embedded, GUI, and game engine contexts. It provides rules for RAII-based resource management, smart pointer usage, build system alignment, and safety-first coding patterns.

## Capabilities

- **Code generation** with RAII, smart pointers, `const`/`constexpr`/`noexcept` contracts, and clean header separation.
- **Build system integration** respecting CMake, Meson, Bazel, or Makefile conventions with reproducible dependency management (vcpkg, Conan, FetchContent).
- **Testing guidance** using Google Test, Catch2, or doctest with sanitizer integration (ASan, UBSan, TSan).
- **Exception safety** validation for basic, strong, and nothrow guarantees.
- **Common pitfall detection** for raw `new`/`delete`, C-style casts, unnecessary copies, and thread-safety gaps.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `modern_application` | Modern C++ server/CLI apps — STL containers, smart pointers, move semantics, modules. |
| `embedded_systems` | Embedded C++ — constrained environments, static allocation, MISRA C++ awareness, HAL patterns. |
| `qt_application` | Qt-based GUI applications — signals/slots, QObject lifecycle, model/view, resource management. |
| `game_engine` | Game engine and real-time C++ — ECS patterns, memory pools, frame budgets, deterministic updates. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=cpp
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=cpp/qt_application
```
