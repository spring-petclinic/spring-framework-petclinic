# AECF — SCAFFOLD

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Scaffold |
> | Phase | 03_SCAFFOLD |

---

CRITICAL: Your SCAFFOLD output MUST be a markdown document containing **exactly** these `##` headers.
Do NOT use `<AECF_FILE_CHANGES>` or code blocks as the top-level output — produce the planning document below.
Write every header in ENGLISH, exactly as listed, regardless of the conversation language.

## Resolved Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| project_name | `<project_name>` | Path or naming note |
| project_type | `<project_type>` | Why this type fits |
| language_framework | `<language_framework>` | Runtime / framework note |
| database | `<database>` | Stateful/stateless rationale |

## Structure Tree

```text
<full generated project structure tree>
```

## Operational Decisions

- [Decision 1: architecture / packaging]
- [Decision 2: local execution / docker / ci]
- [Decision 3: persistence / observability / test strategy bootstrap]

## Bootstrap Files

| File | Purpose |
|------|---------|
| README.md | [why this file exists] |
| AECF_PROJECT_CONTEXT.md | [what context it seeds] |
| .gitignore | [what it protects] |
| ... | ... |

## Next Steps

1. [Immediate developer action]
2. [Validation or smoke test]
3. [Recommended next AECF skill]
