# Dynamics 365 Marketing Domain Pack

## Code Generation Rules
- Treat Power Platform customization as the primary extension mechanism: custom connectors, Power Automate flows, and solution-aware components.
- Use JavaScript for form customizations, custom controls (PCF), and event-handling within the marketing app forms.
- Keep customization logic aligned with the Dataverse solution model; all components must belong to a managed solution.
- Use Power Automate for orchestration and automation instead of implementing custom workflow activities when possible.
- Keep PCF controls modular, typed with TypeScript, and framework-independent where feasible.

## Testing Rules
- Test Power Automate flows with dedicated test runs and validate trigger conditions and error paths.
- Test PCF controls with standard web testing frameworks (Jest, Vitest) in isolation from the platform runtime.
- Cover form script happy paths, validation logic, and one regression around user role visibility.
- Validate custom connector authentication and error handling with contract tests.

## Packaging And Release Rules
- Keep solution publisher prefix, component dependencies, and environment variables aligned with the solution manifest.
- Use solution-aware ALM pipelines with Power Platform CLI, Azure DevOps, or GitHub Actions.
- Treat environment variables and connection references as deployment-time configuration, not hardcoded values.
- Avoid unmanaged customizations in non-development environments.

## Common Pitfalls
- Do not embed automation logic only in form scripts when it should be server-side in Power Automate.
- Do not ignore solution layering; unmanaged customizations in production block upgrades.
- Do not bypass environment variables by hardcoding tenant or environment URLs.
- Do not create PCF controls with tight coupling to a specific entity schema.
