# Security Domain

## What is this domain?

The **Security** domain is a cross-cutting knowledge layer that applies security guardrails across all stack domains. It ensures authentication, authorization, input validation, secret management, and observability are reviewed on every non-trivial change — regardless of the target language or framework.

## Capabilities

- **Cross-cutting security enforcement** for authn/authz, secrets, serialization, and unsafe input handling.
- **Log and trace review** detecting sensitive information leakage in error paths and observability outputs.
- **Dependency and supply-chain** impact assessment when new packages, images, or services are introduced.
- **Stack-adaptive** — security rules apply as a common layer on top of any detected or explicit `stack=` parameter.
- **Override-safe** — security checks persist even when the user specifies a different primary stack.

### Semantic Profiles

| Profile | Description | Activation |
|---------|-------------|------------|
| [`agentic_ai`](semantic_profiles/agentic_ai.md) | OWASP Agentic AI Skills Top 10 (AST01-AST10). Security checklist for systems that build, distribute, or consume AI agent skills — including MCP servers, agent frameworks, and skill registries. | `explicit_or_detected` — activated when workspace shows agentic AI indicators (SKILL.md, agent manifest, MCP definitions, agent framework dependencies). |

## Activation Example

The security domain is typically activated automatically when AECF detects security-relevant changes. To explicitly activate it:

```
@aecf run skill=refactor stack=security
```

Or combine with another domain for layered guidance:

```
@aecf run skill=create_tests stack=python,security
```
