# Dynamics 365 Finance and Operations Domain Pack

## Code Generation Rules
- Treat X++ as the primary extension language; use Visual Studio with the Finance and Operations extension tooling.
- Keep customizations aligned with the layered architecture: models, packages, and extension classes over overlayering.
- Generate extension classes with `[ExtensionOf]` attribute when modifying standard behavior; avoid direct modification of base objects.
- Respect the data entity and OData contract model for integration surfaces.
- Keep business logic in classes and services, not in form event handlers.

## Testing Rules
- Prefer SysTest framework for unit and integration tests.
- Cover posting and validation happy paths, invalid business rules, and one regression around security roles or configuration keys.
- Keep test data setup explicit using test data helper classes and isolated from production configuration.
- Validate data entity integrations with at least one round-trip test.

## Packaging And Release Rules
- Keep model metadata, dependencies, and build definitions aligned with the package manifest.
- Treat data upgrade scripts and schema changes as first-class release concerns.
- Build packages through Azure DevOps pipelines with LCS-compatible deployable artifacts.
- Avoid runtime dependencies on environment-specific configuration during build.

## Common Pitfalls
- Do not use overlayering when extension is available; extensions survive upgrades, overlays do not.
- Do not embed business rules only in form event handlers where they cannot be reused.
- Do not ignore configuration key dependencies and security role requirements.
- Do not bypass the data entity contract for integrations that require OData exposure.
