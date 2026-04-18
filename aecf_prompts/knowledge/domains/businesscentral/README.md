# Business Central Domain

## What is this domain?

The **Business Central** domain covers Microsoft Dynamics 365 Business Central development using AL language. It provides rules, patterns, and guardrails for building extensions that run on the Business Central platform — including tables, pages, codeunits, reports, and integration surfaces.

## Capabilities

- **Code generation** aligned with `app.json` manifest conventions, proper object naming, and extension boundaries.
- **Architecture guidance** that keeps domain logic in codeunits rather than UI triggers.
- **Testing rules** for Business Central test codeunits covering posting, validation, and permission scenarios.
- **Packaging and release** rules around `app.json` dependencies, schema upgrades, and deployment readiness.
- **Common pitfall detection** for object ID conflicts, tenant data assumptions, and misplaced business logic.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `al_extension_app` | AL extension development for Business Central apps — object design, event subscribers, test codeunits. |
| `al_object_documentation` | AL object taxonomy and documentation — tables, pages, codeunits, reports, enums, XMLports, permissions. |

## Activation Example

To activate this domain with a skill, pass the `stack` parameter:

```
@aecf run skill=create_tests stack=businesscentral
```

Or use a semantic profile for more targeted guidance:

```
@aecf run skill=refactor stack=businesscentral/al_extension_app
```
