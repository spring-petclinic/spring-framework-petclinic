# AECF — VERSION: {{TOPIC}}

## METADATA

| Field | Value |
| --- | --- |
| Skill | {{skill}} |
| Phase | VERSION |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |

## 1. Version Bump

| Field | Value |
| --- | --- |
| Previous version | |
| New version | |
| Change type | Major / Minor / Patch |
| Justification | |

## 2. Changelog Entry

```markdown
## [{{version}}] - {{date}}

### Added
-

### Changed
-

### Fixed
-

### Security
-
```

## 3. Release Artifacts

| Artifact | Status |
| --- | --- |
| Audited code (GO) | ✅ / ❌ |
| Tests passing | ✅ / ❌ |
| Changelog updated | ✅ / ❌ |
| README updated (if applicable) | ✅ / ❌ |
| Version bump applied | ✅ / ❌ |

## 4. AECF Documentation Index

| Phase | Document | Status |
| --- | --- | --- |
| PLAN | <DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_01_PLAN.md | ✅ |
| AUDIT_PLAN | <DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_02_AUDIT_PLAN.md | ✅ |
| TEST_STRATEGY | <DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_04_TEST_STRATEGY.md | ✅ |
| IMPLEMENT | <DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_05_IMPLEMENT.md | ✅ |
| AUDIT_CODE | <DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_06_AUDIT_CODE.md | ✅ |
| VERSION | <DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_08_VERSION.md | ✅ |

## 5. Commit Message

```text
feat({{TOPIC}}): {{short_description}}

AECF Score: ___%
AECF Verdict: GO
Skill: {{skill}}
```

## AECF_COMPLIANCE_REPORT

- [ ] Version bumped according to SemVer
- [ ] Changelog updated
- [ ] All AECF artifacts generated
- [ ] Final audit has GO verdict

