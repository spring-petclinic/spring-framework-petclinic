# C# Domain

## What is this domain?

The **C#** domain covers C# language-specific development patterns, conventions, and guardrails. It complements the broader `.NET` domain with language-level guidance for classes, records, interfaces, async patterns, nullable reference types, and XML documentation. It is designed to work alongside platform domains like Business Central, Dynamics 365 CE, and .NET.

## Capabilities

- **Code generation** with modern C# idioms: records, pattern matching, nullable annotations, and async/await.
- **Documentation guidance** for XML doc comments, public API documentation, and object explanation patterns.
- **Testing rules** for xUnit/NUnit with data-driven test patterns and mock frameworks.
- **Packaging and release** rules around `.csproj`, `Directory.Build.props`, and assembly metadata.
- **Common pitfall detection** for async deadlocks, nullable suppression, mutable collection exposure, and broad exception catching.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `aspnetcore_webapi` | ASP.NET Core Web API — controllers, middleware, DI, minimal APIs. |
| `efcore_data` | Entity Framework Core — DbContext, migrations, query patterns, change tracking. |
| `csharp_class_library` | C# class library / NuGet package design — API surface, packaging, versioning. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=csharp
```

Or use a semantic profile for more targeted guidance:

```
@aecf run skill=refactor stack=csharp/aspnetcore_webapi
```
