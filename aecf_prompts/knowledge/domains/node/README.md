# Node.js Domain

## What is this domain?

The **Node.js** domain covers server-side JavaScript/TypeScript development with Node.js. It provides rules for clean service architecture, async boundary management, module side-effect control, and dependency hygiene — keeping HTTP/event transport thin and business logic testable.

## Capabilities

- **Architecture guidance** separating startup wiring, configuration, background jobs, and feature modules.
- **Coding rules** for async/await patterns, centralized error handling, and minimal module side effects.
- **Testing guidance** with focused unit tests for services plus integration tests at the app boundary.
- **Dependency management** reviewing package weight, maintenance posture, and security before adoption.
- **Common pitfall detection** for business logic in route handlers, hidden singleton state, and ad-hoc config reads.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `node_service_base_architecture` | Node.js service architecture — project layout, middleware, error handling, observability. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=node
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=node/node_service_base_architecture
```
