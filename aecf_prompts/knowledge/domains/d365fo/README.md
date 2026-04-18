# Dynamics 365 Finance and Operations Domain

## What is this domain?

The **D365 F&O** domain covers Microsoft Dynamics 365 Finance and Operations development using X++. It provides rules for building extensions aligned with the layered architecture — models, packages, extension classes, data entities, and OData integrations — without overlayering standard objects.

## Capabilities

- **X++ extension development** using `[ExtensionOf]` attributes, keeping business logic in classes/services instead of form handlers.
- **Data entity and OData** contract guidance for integration surfaces.
- **Testing rules** using the SysTest framework with explicit test data setup and data entity round-trip validation.
- **Packaging and release** aligned with model metadata, Azure DevOps pipelines, and LCS-compatible deployable packages.
- **Common pitfall detection** for overlayering, misplaced business logic, ignored configuration keys, and security role gaps.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `xpp_extension` | X++ extension development — extension classes, data entities, SysTest, model packaging. |
| `d365fo_object_documentation` | F&O object taxonomy and documentation — AxTable, AxClass, AxForm, AxDataEntity, AxReport, security artifacts, enums. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=d365fo
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=d365fo/xpp_extension
```
