# .NET Domain

## What is this domain?

The **.NET** domain covers Microsoft .NET development (ASP.NET Core, Entity Framework, class libraries). It provides rules for clean architecture composition, dependency injection, service isolation, and test coverage across controllers, application services, and infrastructure layers.

## Capabilities

- **Architecture guidance** with ASP.NET Core composition root patterns and explicit DI registration.
- **Service isolation** keeping application/domain logic separate from transport and Entity Framework details.
- **Clean architecture boundaries** for new service and module generation.
- **Configuration management** treating secrets, config bindings, and environment-specific values as external concerns.
- **Testing rules** covering controllers/endpoints and application services, not only infrastructure.

### Semantic Profiles

This domain provides general .NET guardrails. For C# language-specific guidance including ASP.NET Core, Entity Framework Core, and class library patterns, see the `csharp` domain.

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=dotnet
```

When semantic profiles become available:

```
@aecf run skill=refactor stack=dotnet/aspnetcore_webapi
```
