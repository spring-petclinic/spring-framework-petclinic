# Python Domain Pack

## Code Generation Rules
- Prefer `pyproject.toml` as the canonical package/config entry point when packaging is needed.
- Use explicit imports, `pathlib`, and type hints on public functions and data boundaries.
- Keep module side effects minimal. Avoid work at import time unless the framework clearly requires it.
- Favor small composable functions over monolithic scripts.

## Testing Rules
- Prefer `pytest` style tests and keep fixtures close to the tests that use them.
- Cover happy path, invalid input, and one edge condition for every new behavior.
- Avoid fragile time/network/file-system dependencies unless the task explicitly needs them.

## Dependency Rules
- Add only justified runtime dependencies.
- Separate dev/test tooling from runtime requirements when the project structure allows it.
- Do not assume global interpreters or system packages; stay environment-aware.

## Common Pitfalls
- Do not hide import errors with broad `except Exception`.
- Do not mix sync and async flows without an explicit boundary.
- Do not couple tests to internal file layout more than necessary.