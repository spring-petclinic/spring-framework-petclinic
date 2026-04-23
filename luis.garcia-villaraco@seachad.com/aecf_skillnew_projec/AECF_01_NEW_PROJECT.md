# NEW PROJECT — PLAN

## Resolved Parameters

| Parameter            | Value                   |
|----------------------|-------------------------|
| `project_name`       | `banna_read_audit_json` |
| `project_type`       | `cli_tool`              |
| `language_framework` | `python_click`          |
| `database`           | `none`                  |

---

## Operational Skeleton

### Base Approach

A stateless Python 3.12 CLI tool built with Click that reads and audits JSON files from disk.
Two top-level command groups are exposed: `read` (inspect/display JSON content) and `audit`
(validate structure, detect anomalies, produce audit reports). No persistence layer — all
operations are file-in / report-out.

### Runtime Stack

| Component       | Choice                         | Rationale                                          |
|-----------------|--------------------------------|----------------------------------------------------|
| Language        | Python 3.12                    | Catalog minimum; strong JSON stdlib support        |
| CLI framework   | Click 8 + Typer                | Click for routing groups; Rich for styled output   |
| Validation      | Pydantic v2                    | Schema validation, type coercion, error messages   |
| Output styling  | Rich                           | Tables, syntax-highlighted JSON, progress bars     |
| Packaging       | pyproject.toml + Hatch         | PEP 517/518 compliant; editable installs           |
| Testing         | pytest + pytest-click          | CLI invocation testing                             |
| Linting         | ruff                           | Single-tool lint + format                          |
| CI              | GitHub Actions (ubuntu-latest) | Matrix on Python 3.12                              |
| Database        | none                           | Stateless — file-based I/O only                    |

### Command Hierarchy

```
banna-audit [OPTIONS]
├── read
│   ├── file PATH        — Pretty-print a JSON file
│   └── keys PATH        — List top-level keys
└── audit
    ├── validate PATH    — Validate JSON syntax and optional schema
    └── report PATH      — Generate a structural audit report
```

### Key Constraints

- No global state, no database connections.
- All commands accept `--output [text|json|csv]` for machine-readable output.
- Exit code 0 = success, 1 = validation failure, 2 = file/IO error.
- Every source function carries a full `AECF_META` block.

### Project Root

`D:\SEACHAD\BANNA_ReadAuditJson\banna_read_audit_json\`

### Directory Structure

```
banna_read_audit_json/
├── src/
│   └── banna_read_audit_json/
│       ├── __init__.py
│       ├── cli.py                   # Click group entrypoint
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── read.py              # read command group
│       │   └── audit.py             # audit command group
│       └── core/
│           ├── __init__.py
│           ├── config.py            # App settings (env vars)
│           ├── reader.py            # JSON file reading logic
│           └── auditor.py           # JSON auditing / validation logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_cli.py
├── documentation/
│   └── README.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── README.md
└── AECF_PROJECT_CONTEXT.md
```

---

## METADATA

| Field                     | Value                                                          |
|---------------------------|----------------------------------------------------------------|
| Timestamp (UTC)           | 2026-04-22T08:30:00Z                                           |
| Executed By               | Claude Sonnet 4.6                                              |
| Executed By ID            | claude-sonnet-4-6                                              |
| Execution Identity Source | AECF MCP dispatcher                                            |
| Repository                | D:\SEACHAD\BANNA_ReadAuditJson                                 |
| Branch                    | main                                                           |
| Root Prompt               | @aecf run skill=new_project topic=BANNA_ReadAuditJson          |
| Skill Executed            | aecf_new_project                                               |
| Sequence Position         | 01 / PLAN                                                      |
| Total Prompts Executed    | 2                                                              |
