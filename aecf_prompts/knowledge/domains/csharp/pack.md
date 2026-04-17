# C# Domain Pack

## Code Generation Rules
- Prefer explicit typing over `var` where the type is not immediately obvious from context.
- Use records for immutable data transfer objects and value-like types.
- Generate classes with clear single-responsibility and explicit dependency injection via constructor.
- Respect nullable reference types and annotate nullability intent explicitly.
- Keep async/await usage consistent; avoid mixing synchronous and asynchronous patterns in the same flow.

## Documentation Rules
- Document public APIs with XML doc comments (`///`) including `<summary>`, `<param>`, `<returns>`, and `<exception>` tags.
- Use `<remarks>` for implementation notes and `<example>` for usage examples on complex APIs.
- Keep internal and private members documented when the logic is non-trivial.
- Use `<inheritdoc/>` on overridden members when the base documentation is sufficient.
- Avoid redundant documentation that merely restates the method signature.

## Testing Rules
- Prefer xUnit or NUnit with Moq, NSubstitute, or similar mocking frameworks.
- Cover happy path, invalid input, edge cases, and one regression per public method or behavior change.
- Test public contracts; avoid testing private implementations directly.
- Use `Theory` / `TestCase` for data-driven test coverage.
- Keep test setup explicit and avoid shared mutable state between tests.

## Packaging And Release Rules
- Keep `.csproj` target framework, package references, and version metadata aligned.
- Use `Directory.Build.props` for shared build configuration across multi-project solutions.
- Treat `AssemblyInfo` attributes and package metadata as release artifacts.
- Avoid hardcoded paths or environment-specific values in project files.

## Common Pitfalls
- Do not suppress nullable warnings without explicit justification.
- Do not use `Task.Result` or `Task.Wait()` in async contexts; use `await` instead.
- Do not catch `Exception` broadly without logging or re-throwing.
- Do not expose mutable collections from public APIs; use `IReadOnlyList<T>` or `IReadOnlyCollection<T>`.
- Do not mix business logic and infrastructure concerns in the same class.
