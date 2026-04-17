# Dynamics 365 Customer Engagement Domain

## What is this domain?

The **D365 CE** domain covers Microsoft Dynamics 365 Customer Engagement (Sales, Service, Field Service) development. It provides rules for building C# server-side plugins, JavaScript web resources, custom APIs, and solution-based ALM — all aligned with the Dataverse platform model.

## Capabilities

- **Plugin development** with focused single-entity/message design, early-bound entity classes, and execution context management.
- **Web resource development** with namespace-isolated JavaScript, modular structure, and Xrm SDK best practices.
- **Solution-centric ALM** guidance for managed solution packaging, publisher prefix conventions, and environment-aware deployment.
- **Testing rules** using FakeXrmEasy for plugin tests, isolated JS unit tests, and integration round-trip validation.
- **Common pitfall detection** for infinite plugin loops, unsupported APIs, hardcoded environment values, and security role gaps.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `csharp_plugin` | C# server-side plugins — IPlugin, execution context, early-bound entities, pipeline stages. |
| `js_webresource` | JavaScript web resources — Xrm SDK, form events, namespace isolation, ribbon commands. |
| `d365ce_object_documentation` | CE object taxonomy and documentation — entities, attributes, forms, views, plugins, custom actions, security roles. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=d365ce
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=d365ce/csharp_plugin
```
