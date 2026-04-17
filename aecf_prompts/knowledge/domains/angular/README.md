# Angular Domain

## What is this domain?

The **Angular** domain covers Angular applications and workspaces with guidance for component-driven UI composition, routing, dependency injection, RxJS-based async flows, and scalable feature boundaries. It is intended for Angular frontends that need explicit state ownership, testable presentation logic, and disciplined browser-side architecture.

## Capabilities

- **Application-shell guidance** for routing, feature boundaries, and dependency injection scopes.
- **Component and template discipline** keeping presentation logic separate from durable business behavior.
- **Async flow guidance** for observables, signals, subscriptions, and teardown safety.
- **Testing rules** for components, services, route flows, and validation-heavy UI behavior.
- **State-management guidance** for deciding when local component state is enough and when store-based patterns are justified.
- **Common pitfall detection** for duplicated state, leaking subscriptions, and template-heavy business logic.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `standalone_components` | Modern standalone Angular composition — `bootstrapApplication`, feature-local routes, provider boundaries, lazy loading. |
| `ngrx_state_management` | NgRx store architecture — reducers, selectors, effects, action boundaries, and store ownership discipline. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=angular
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=angular/standalone_components
@aecf run skill=refactor stack=angular/ngrx_state_management
```