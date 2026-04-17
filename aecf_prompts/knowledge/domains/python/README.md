# Python Domain

## What is this domain?

The **Python** domain covers Python application development across web services (Flask), cloud functions (AWS Lambda, Azure Functions), database access (SQLAlchemy, PostgreSQL), and general-purpose scripting. It provides rules for clean module design, type hints, pytest-based testing, and dependency isolation.

## Capabilities

- **Code generation** using `pyproject.toml` conventions, explicit imports, `pathlib`, and type hints on public boundaries.
- **Testing rules** with pytest style, fixtures close to tests, and coverage of happy path, invalid input, and edge cases.
- **Dependency management** separating dev/test tooling from runtime requirements.
- **Module design** favoring small composable functions over monolithic scripts with minimal import-time side effects.
- **Common pitfall detection** for broad `except Exception`, sync/async mixing, and test coupling to internal layout.

### Semantic Profiles

| Profile | Focus |
|---------|-------|
| `flask_web` | Flask web applications — blueprints, request handling, configuration, testing patterns. |
| `aws_lambda_python` | Python on AWS Lambda — handler design, event parsing, cold starts, SAM/CDK deployment. |
| `azure_functions_python` | Python on Azure Functions — bindings, triggers, configuration, deployment. |
| `requests_http_client` | Python Requests HTTP client — sessions, timeouts, retries, TLS, response validation. |
| `sqlalchemy_orm` | SQLAlchemy ORM — models, sessions, migrations (Alembic), query patterns. |
| `postgresql_db` | PostgreSQL database — schema design, indexing, query optimization, connection management. |

## Activation Example

To activate this domain with a skill:

```
@aecf run skill=create_tests domain=python
```

Or use a semantic profile for targeted guidance:

```
@aecf run skill=refactor domain=python semantic_profiles=flask_web
```

