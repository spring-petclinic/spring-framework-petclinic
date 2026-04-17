# Java Domain Pack

## Code Generation Rules
- Respect the existing build tool: Maven projects should stay Maven, Gradle projects should stay Gradle.
- Keep package names aligned with the existing source tree and avoid moving public APIs without a clear reason.
- Prefer constructor injection and explicit interfaces when the codebase already uses DI patterns.
- Keep business logic out of controllers and transport-layer DTOs.

## Testing Rules
- Prefer JUnit 5 style tests and use integration tests only where wiring or persistence matters.
- Keep test doubles local and obvious; avoid reflection-heavy test setups unless already established.
- Validate both success paths and failure contracts, especially exceptions and validation errors.

## Build And Runtime Rules
- Reuse the existing Java version and plugin conventions found in `pom.xml` or Gradle build files.
- Do not introduce framework migrations as part of unrelated feature work.
- Keep generated resources and annotation processing explicit when required.

## Common Pitfalls
- Avoid static mutable state unless the codebase already depends on it.
- Do not mix incompatible dependency versions across modules.
- Do not treat package-private access as a substitute for clear API boundaries.