# Go Domain

## What is this domain?

The **Go** domain covers Go (Golang) service and application development. It provides rules for idiomatic Go project structure, explicit error handling, context propagation, interface design, and table-driven testing — following Go community conventions and standard library patterns.

## Capabilities

- **Architecture guidance** with `cmd/` thin entrypoints, reusable internal packages, and clear import direction.
- **Coding rules** for explicit `context.Context` propagation, error-return patterns, and small interfaces defined near consumers.
- **Testing guidance** with table-driven tests, `httptest` for HTTP boundaries, and `-race` safe deterministic tests.
- **Dependency management** favoring standard library usage over unnecessary frameworks.
- **Common pitfall detection** for orchestration in `main()`, shared mutable globals, and blurred package boundaries.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `go_service_base_architecture` | Go service architecture — project layout, DI patterns, middleware, observability. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests stack=go
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor stack=go/go_service_base_architecture
```
