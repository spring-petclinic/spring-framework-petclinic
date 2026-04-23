# Dynamics 365 Marketing Domain

## What is this domain?

The **D365 Marketing** domain covers Microsoft Dynamics 365 Marketing development using Power Platform customizations, Power Automate flows, PCF controls, and JavaScript form scripting. It provides rules for solution-aware low-code/pro-code extensions aligned with the Dataverse model.

## Capabilities

- **Power Platform customization** with custom connectors, Power Automate flows, and solution-aware components.
- **PCF control development** with TypeScript, modular structure, and framework-independent design.
- **JavaScript form scripting** for event handling, validation, and role-based visibility.
- **ALM pipeline guidance** using Power Platform CLI, Azure DevOps, or GitHub Actions with environment variables and connection references.
- **Common pitfall detection** for unmanaged customizations, hardcoded URLs, solution layering conflicts, and tightly coupled PCF controls.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `power_platform_customization` | Power Platform extensions — Power Automate, custom connectors, PCF, solution packaging. |
| `js_marketing_forms` | JavaScript form customizations — Xrm SDK events, validation, role-based UI, ribbon commands. |
| `d365marketing_component_documentation` | Marketing component documentation — journeys, segments, forms, email templates, events, PCF, flows. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=d365marketing
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=d365marketing/power_platform_customization
```
