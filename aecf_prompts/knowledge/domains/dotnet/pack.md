# .NET

- Prefer ASP.NET Core composition root patterns with explicit DI registration.
- Keep application/domain services isolated from transport and Entity Framework details.
- Use clean architecture boundaries when generating new services or modules.
- Treat configuration, secrets, and environment-specific bindings as external concerns.
- Add tests around controllers/endpoints plus application services, not only infrastructure.