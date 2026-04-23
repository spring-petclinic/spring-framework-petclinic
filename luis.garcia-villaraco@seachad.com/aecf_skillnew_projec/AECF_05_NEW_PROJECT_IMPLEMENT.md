# NEW PROJECT — IMPLEMENT

## Materialized Files

All files below were physically written to `D:\SEACHAD\BANNA_ReadAuditJson\banna_read_audit_json\`.

| File | Description |
|------|-------------|
| `src/banna_read_audit_json/__init__.py` | Package init, version `0.1.0` |
| `src/banna_read_audit_json/cli.py` | Click root group, registers `read` and `audit` |
| `src/banna_read_audit_json/commands/read.py` | `read file` and `read keys` commands |
| `src/banna_read_audit_json/commands/audit.py` | `audit validate` and `audit report` commands |
| `src/banna_read_audit_json/core/config.py` | Env-var settings dataclass |
| `src/banna_read_audit_json/core/reader.py` | `load_json_file`, `top_level_keys`, `click_echo_err` |
| `src/banna_read_audit_json/core/auditor.py` | `AuditResult`, `audit_structure`, `_is_empty` |
| `tests/conftest.py` | `sample_json_file` and `invalid_json_file` fixtures |
| `tests/test_cli.py` | 5 CliRunner-based tests covering all four commands |
| `pyproject.toml` | Hatch build config, `banna-audit` entrypoint, ruff config |
| `requirements.txt` | Runtime deps: click, rich, pydantic |
| `requirements-dev.txt` | Dev deps: pytest, ruff, hatch |
| `.env.example` | Template env vars |
| `.gitignore` | Python + Hatch + ruff ignore patterns |
| `.github/workflows/ci.yml` | GitHub Actions CI — lint + test on Python 3.12 |
| `documentation/README.md` | Documentation folder placeholder |
| `README.md` | Full project README |
| `AECF_PROJECT_CONTEXT.md` | Bootstrapped AECF context for this project |

## AECF_META Compliance

Every source function and class carries a full `AECF_META` block with:
`skill`, `topic`, `run_time`, `generated_at`, `generated_by`,
`last_modified_skill`, `last_modified_at`, `last_modified_by`, `touch_count=1`.

---

## METADATA

| Field                     | Value                                                          |
|---------------------------|----------------------------------------------------------------|
| Timestamp (UTC)           | 2026-04-22T08:32:00Z                                           |
| Executed By               | Claude Sonnet 4.6                                              |
| Executed By ID            | claude-sonnet-4-6                                              |
| Execution Identity Source | AECF MCP dispatcher                                            |
| Repository                | D:\SEACHAD\BANNA_ReadAuditJson                                 |
| Branch                    | main                                                           |
| Root Prompt               | @aecf run skill=new_project topic=BANNA_ReadAuditJson          |
| Skill Executed            | aecf_new_project                                               |
| Sequence Position         | 05 / IMPLEMENT                                                 |
| Total Prompts Executed    | 6                                                              |
