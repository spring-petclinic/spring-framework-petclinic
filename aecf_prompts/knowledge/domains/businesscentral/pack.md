# Business Central Domain Pack

## Code Generation Rules
- Treat `app.json` as the authoritative extension manifest and keep object IDs, name, publisher, and version coherent.
- Generate AL objects with clear naming and avoid unnecessary coupling between pages, tables, and codeunits.
- Keep domain logic in codeunits when possible instead of pushing logic into page triggers.
- Respect extension boundaries and avoid assumptions about direct base-app modification.

## Testing Rules
- Prefer Business Central test codeunits for behavioral coverage.
- Cover posting/validation happy paths, invalid business rules, and one regression around permissions or setup data.
- Keep test data setup explicit and isolated from production configuration.

## Packaging And Release Rules
- Keep permissions, dependencies, and target runtime aligned with `app.json`.
- Treat schema and data upgrade concerns explicitly when table structure changes.
- Avoid internet-time dependencies during compilation or publish flows.

## Common Pitfalls
- Do not bury business rules in UI triggers when they belong in reusable logic.
- Do not change object IDs casually.
- Do not assume tenant data state; seed or validate prerequisites explicitly.