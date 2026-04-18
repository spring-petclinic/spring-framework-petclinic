---
profile_id: aspnetcore_webapi
title: ASP.NET Core Web API
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-16
profile_type: framework
stack_nodes:
  - csharp
  - dotnet
requires:
  - csharp
precedence: 90
fallback_mode: warn_continue
compatibility:
  - csharp
  - dotnet
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - manifest=.csproj
  - keyword=asp.net core
  - keyword=webapi
  - keyword=minimal api
  - keyword=controller
  - path=Program.cs
max_lines_per_section: 6
tags:
  - csharp
  - dotnet
  - webapi
  - aspnetcore
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## STACK

ASP.NET Core Web API development targets the .NET HTTP pipeline with controllers or minimal APIs, dependency injection, middleware, and model binding as core building blocks.

## ARCHITECTURE RULES

- Use the composition root in `Program.cs` or `Startup.cs` for explicit DI registration.
- Keep controllers thin; delegate business logic to application services or use-case classes.
- Separate transport concerns (model binding, validation, HTTP status codes) from domain logic.
- Use middleware for cross-cutting concerns (auth, logging, correlation IDs), not in-controller logic.
- Prefer minimal APIs for simple endpoints; use controllers for complex resource-oriented APIs.

## DESIGN PATTERNS

- Mediator pattern (MediatR) or direct service injection for command/query separation.
- Options pattern (`IOptions<T>`) for typed configuration binding.
- Result/envelope pattern for consistent API response contracts.
- Middleware pipeline for request/response transformation and filtering.
- Health check endpoints for operational readiness.

## CODING RULES

- Annotate controller actions with explicit HTTP method and route attributes.
- Use `[FromBody]`, `[FromQuery]`, `[FromRoute]` explicitly for model binding clarity.
- Return `IActionResult` or `ActionResult<T>` with explicit status codes.
- Use `CancellationToken` in async actions to enable request cancellation.
- Do not use `HttpContext` directly when `IHttpContextAccessor` or typed abstractions suffice.

## SECURITY RULES

- Apply `[Authorize]` at controller or action level; do not rely only on middleware.
- Validate and sanitize all request inputs at the boundary.
- Use `IDataProtector` or ASP.NET Core Data Protection for sensitive token handling.
- Configure CORS explicitly; do not use wildcard policies in production.
- Keep secrets in user-secrets, Key Vault, or environment variables — never in source.

## TESTING RULES

- Use `WebApplicationFactory<T>` for integration tests against the real HTTP pipeline.
- Unit test services and handlers independently from controllers.
- Cover request validation, authorization, error handling, and happy-path responses.
- Mock external dependencies at the DI boundary, not inside framework internals.
- Verify content negotiation and status codes in integration tests.

## COMMON MISTAKES

- Fat controllers that mix HTTP handling, validation, and business logic.
- Registering services with wrong lifetime (scoped vs singleton) causing captive dependency issues.
- Ignoring `CancellationToken` in async endpoints.
- Using `HttpContext.Items` for cross-layer state instead of explicit parameters.
- Not validating model state — relying on implicit `[ApiController]` validation without custom rules.

## AECF AUDIT CHECKS

- Verify controllers delegate to service/handler classes and remain thin.
- Verify DI registration lifetimes are correct and do not cause captive dependencies.
- Verify authorization attributes are applied explicitly.
- Verify request validation and error handling produce consistent responses.
- Verify integration tests use `WebApplicationFactory` and cover status codes and auth.
