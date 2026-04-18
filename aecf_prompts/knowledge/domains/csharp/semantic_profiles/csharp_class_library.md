---
profile_id: csharp_class_library
title: C# Class Library and NuGet Package
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-16
profile_type: language
stack_nodes:
  - csharp
  - dotnet
requires:
  - csharp
precedence: 80
fallback_mode: warn_continue
compatibility:
  - csharp
  - dotnet
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - manifest=.csproj
  - keyword=class library
  - keyword=nuget
  - keyword=package
max_lines_per_section: 6
tags:
  - csharp
  - dotnet
  - library
  - nuget
  - api-design
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## STACK

C# class libraries expose reusable APIs consumed as project references or NuGet packages. API surface design, versioning, and documentation are critical for consumer experience.

## ARCHITECTURE RULES

- Define a clear public API surface; keep implementation details `internal`.
- Use `InternalsVisibleTo` for test projects that need access to internal APIs.
- Separate abstractions (interfaces, contracts) from implementations when the library is meant for extensibility.
- Target `netstandard2.0` or the lowest practical TFM for maximum compatibility.
- Keep dependency count minimal; avoid pulling transitive dependencies consumers do not expect.

## DESIGN PATTERNS

- Builder pattern for complex object construction with a fluent API.
- Factory pattern for creating instances whose concrete types should stay internal.
- Options/configuration pattern for library initialization with sensible defaults.
- Extension methods for non-invasive API enrichment.
- Decorator or middleware patterns for pipeline-composable behavior.

## CODING RULES

- Document all public types and members with XML doc comments (`///`).
- Use `<summary>`, `<param>`, `<returns>`, `<exception>`, and `<example>` tags consistently.
- Mark experimental APIs with `[Obsolete]` or `[Experimental]` before removal.
- Seal classes that are not designed for inheritance.
- Use `readonly struct` for small value types passed by value.

## SECURITY RULES

- Do not log sensitive data passed to library methods.
- Validate inputs at public API boundaries; trust internal callers.
- Avoid embedding credentials, tokens, or environment-specific values in library code.
- Use `SecureString` or ephemeral byte arrays for sensitive data that must be in memory temporarily.

## TESTING RULES

- Test public API contracts, not internal implementation details.
- Use `Theory`/`TestCase` for data-driven coverage of boundary values.
- Test API backward compatibility when evolving the public surface.
- Include at least one integration test showing the library used as a consumer would.
- Verify XML doc comments are present on all public symbols via build warnings or analyzers.

## COMMON MISTAKES

- Exposing internal types or implementation details on the public API surface.
- Breaking backward compatibility without a major version bump.
- Pulling unnecessary dependencies that bloat the dependency graph for consumers.
- Missing XML documentation on public members.
- Not sealing classes that have no intended extension points.

## AECF AUDIT CHECKS

- Verify public API surface is intentional and minimal.
- Verify XML doc comments cover all public types and members.
- Verify dependency count is justified and minimal.
- Verify TFM is appropriate for the intended audience.
- Verify tests cover backward compatibility and consumer-facing contracts.
