# Dynamics 365 Customer Engagement Domain Pack

## Code Generation Rules
- Treat C# server-side plugins and JavaScript web resources as the primary extension mechanisms.
- Keep plugins focused on a single entity and message; avoid monolithic plugin classes.
- Use early-bound entity classes for type safety in C# plugins; avoid stringly-typed attribute access.
- Keep JavaScript web resources modular and namespace-isolated; avoid polluting the global scope.
- Respect the solution-centric deployment model; keep all components in managed solutions.

## Testing Rules
- Prefer xUnit or NUnit with FakeXrmEasy or similar faking libraries for plugin unit tests.
- Cover plugin happy paths, invalid input handling, and one regression around user/team security.
- Test JavaScript web resources with isolated unit tests where business logic is separated from Xrm SDK calls.
- Validate custom API and action contracts with at least one integration round-trip test.

## Packaging And Release Rules
- Keep solution metadata, publisher prefix, and component dependencies aligned with the solution manifest.
- Use solution-aware ALM with Azure DevOps or GitHub Actions for CI/CD.
- Treat plugin assembly registration and secure/unsecure configuration as deployment artifacts.
- Avoid hardcoded environment URLs or tenant-specific values in plugin or web resource code.

## Common Pitfalls
- Do not register a plugin on too many messages or entities without justification.
- Do not embed business rules only in JavaScript form events when they need server-side enforcement.
- Do not ignore execution context depth to prevent infinite plugin loops.
- Do not use unsupported JavaScript APIs; stick to the supported Xrm SDK.
