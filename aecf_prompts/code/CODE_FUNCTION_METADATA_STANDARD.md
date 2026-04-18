# AECF — CODE FUNCTION METADATA STANDARD

LAST_REVIEW: 2026-03-06

> **SINGLE SOURCE OF TRUTH** for the mandatory code-level metadata that ALL AECF-generated
> or AECF-modified functions, methods, classes, and modules MUST include in their docstring/comment block.
>
> This standard applies to every skill that touches production code:
> `aecf_new_feature`, `aecf_new_feature_ma`, `aecf_change_feature`,
> `aecf_hotfix`, `aecf_fix_code` (06_FIX_CODE) and any future code-generating skill.

------------------------------------------------------------

## PURPOSE

Every function, method, class, module, or standalone callable created or modified by an AECF skill
MUST carry a traceable metadata block inside its docstring (or equivalent language comment).

This ensures:

- **Origin traceability**: which skill and topic produced or last touched this function.
- **Author accountability**: which user triggered the generation/modification.
- **Temporal auditability**: when the function was created and last changed.
- **Diff readability**: reviewers see AECF context directly in the source code diff.

------------------------------------------------------------

## MANDATORY FIELDS

| Field | Key | Description |
|-------|-----|-------------|
| Generating skill | `skill` | Skill ID that CREATED the function (`aecf_new_feature`, `aecf_hotfix`, etc.) |
| TOPIC | `topic` | AECF TOPIC identifier resolved for this execution chain |
| Active run timestamp | `run_time` | UTC ISO-8601 timestamp of the AECF execution that last touched the callable |
| Generation timestamp | `generated_at` | UTC ISO-8601 timestamp of initial generation |
| Generating user | `generated_by` | `Executed By ID` field from the execution chain (email / account / `N/A`) |
| Last modifying skill | `last_modified_skill` | Skill ID that last touched this function (equals `skill` on first creation) |
| Last modification timestamp | `last_modified_at` | UTC ISO-8601 timestamp of the most recent modification |
| Last modifying user | `last_modified_by` | `Executed By ID` of the most recent modifier |
| AECF touch counter | `touch_count` | Positive integer count of how many AECF write passes created or modified the callable |

Identity rule:
- `generated_by` and `last_modified_by` MUST use the effective execution `user_id` / `Executed By ID`.
- NEVER use generic labels such as `aecf`, `copilot`, `assistant`, the current skill id, or the model name.
- If the execution chain does not provide a user identity, use `N/A`.

Run traceability rule:
- `run_time` MUST represent the current AECF execution timestamp that produced the latest write.
- On creation, `run_time` MUST match `generated_at` and `last_modified_at`.
- On every later AECF modification, `run_time` MUST be updated to the current run timestamp.

Touch counter rule:
- On creation, set `touch_count=1`.
- On every later AECF modification, increment `touch_count` by exactly `1`.

------------------------------------------------------------

## MAINTAINABILITY COMMENT RULE

AECF-generated or AECF-modified code MUST remain maintainable by a human engineer.

- Add enough human-readable comments/docstrings to explain non-obvious intent, invariants,
  fixtures, mocks, teardown/cleanup, or risk-focused assertions.
- Do NOT add redundant narration of trivial lines.
- Human-readable comments and docstring prose MUST use the resolved AECF output language
  (`OUTPUT_LANGUAGE` / `aecf.documentationOutputLanguage`).
- Machine-facing `AECF_META` keys and values remain English-only and stable.

------------------------------------------------------------

## CANONICAL FORMAT BY LANGUAGE

The `AECF_META` line MUST be a **single line** placed as the **last line** of the docstring/comment.
Field separator: ` | `. No line breaks within the block.

### Python (docstring)

```python
def my_function(param: str) -> str:
    """Brief one-line description.

  AECF_META: skill=aecf_new_feature | topic={{TOPIC}} | run_time=2026-03-06T10:00:00Z | generated_at=2026-03-06T10:00:00Z | generated_by=user@example.com | last_modified_skill=aecf_new_feature | last_modified_at=2026-03-06T10:00:00Z | last_modified_by=user@example.com | touch_count=1
    """
```

**Rules:**
- The `AECF_META:` line MUST be the **last line** inside the docstring, after all other content.
- On **creation**: `last_modified_*` equals the `generated_*` values.
- On **modification**: ONLY the `last_modified_*` trio is updated; the `generated_*` values are NEVER changed.
- `generated_by` / `last_modified_by` MUST be the effective execution `user_id`, never `aecf` or similar generic labels.

---

### JavaScript / TypeScript (JSDoc)

```javascript
/**
 * Brief one-line description.
 * @aecf skill=aecf_new_feature | topic={{TOPIC}} | run_time=2026-03-06T10:00:00Z | generated_at=2026-03-06T10:00:00Z | generated_by=user@example.com | last_modified_skill=aecf_new_feature | last_modified_at=2026-03-06T10:00:00Z | last_modified_by=user@example.com | touch_count=1
 */
function myFunction(param) { ... }
```

---

### PowerShell (comment-based help)

```powershell
function My-Function {
    <#
    .SYNOPSIS  Brief description.
  .AECF_META skill=aecf_new_feature | topic={{TOPIC}} | run_time=2026-03-06T10:00:00Z | generated_at=2026-03-06T10:00:00Z | generated_by=user@example.com | last_modified_skill=aecf_new_feature | last_modified_at=2026-03-06T10:00:00Z | last_modified_by=user@example.com | touch_count=1
    #>
}
```

---

### Generic (any other language — inline comment immediately before the function)

```
# AECF_META: skill=aecf_new_feature | topic={{TOPIC}} | run_time=2026-03-06T10:00:00Z | generated_at=2026-03-06T10:00:00Z | generated_by=user@example.com | last_modified_skill=aecf_new_feature | last_modified_at=2026-03-06T10:00:00Z | last_modified_by=user@example.com | touch_count=1
```

------------------------------------------------------------

## ENFORCEMENT RULES

### On Creation (IMPLEMENT / aecf_new_feature / aecf_hotfix)

1. Every new function/method/class/module MUST include the full `AECF_META` line in its docstring/comment block.
2. `generated_*`, `last_modified_*`, and `run_time` MUST point to the same current UTC run timestamp at creation time.
3. `touch_count` MUST be `1` at creation time.
3. Missing `AECF_META` in any function = **automatic checklist failure** for the IMPLEMENT phase.

### On Modification (FIX_CODE / aecf_change_feature / aecf_hotfix modifying existing functions)

1. The AI MUST locate the existing `AECF_META` line in the function/method/class/module being modified.
2. ONLY the latest-touch fields are updated:
   - `last_modified_skill` → current executing skill ID
   - `last_modified_at` → current UTC timestamp
   - `last_modified_by` → current `Executed By ID`
  - `run_time` → current UTC timestamp for the active AECF run
  - `touch_count` → previous value + `1`
3. The `generated_*` fields MUST remain UNCHANGED — they preserve origin provenance.
4. If a function being modified does NOT have an `AECF_META` line (legacy code):
   - ADD the full line using the current skill/timestamp for all 7 fields,
    plus `run_time=<current UTC timestamp>` and `touch_count=1`,
    AND append `retroactive=true` at the end to flag it as retroactively added.
5. Missing meta update = **automatic checklist failure** for the FIX_CODE phase.

### Scope

- Applies to: all public and private functions/methods, documented classes, and module-level files with executable code produced or modified by AECF skills.
- Does NOT apply to: auto-generated files (migrations, compiled outputs, lock files, `__init__.py`
  containing only imports), or third-party vendored code.
- Class-level `__init__` methods MAY inherit the class docstring AECF_META if the class itself
  is documented; individual methods still require their own block when they are generated or modified.
- Module-level metadata should live in the module docstring when the language supports it, or in a
  leading file comment block immediately before the first executable declaration.

------------------------------------------------------------

## EXAMPLE — CORRECT CREATION (Python)

```python
def build_mock_openapi_spec() -> dict:
    """Return a deterministic deep-copied OpenAPI mock specification.

  AECF_META: skill=aecf_new_feature | topic=api_list_v7_mock | run_time=2026-03-06T10:00:00Z | generated_at=2026-03-06T10:00:00Z | generated_by=dev@seachad.com | last_modified_skill=aecf_new_feature | last_modified_at=2026-03-06T10:00:00Z | last_modified_by=dev@seachad.com | touch_count=1
    """
    return deepcopy(_CANONICAL_SPEC)
```

## EXAMPLE — CORRECT UPDATE AFTER FIX_CODE

```python
def build_mock_openapi_spec() -> dict:
    """Return a deterministic deep-copied OpenAPI mock specification.

  AECF_META: skill=aecf_new_feature | topic=api_list_v7_mock | run_time=2026-03-07T09:15:00Z | generated_at=2026-03-06T10:00:00Z | generated_by=dev@seachad.com | last_modified_skill=aecf_fix_code | last_modified_at=2026-03-07T09:15:00Z | last_modified_by=dev@seachad.com | touch_count=2
    """
    # skill/topic/generated_at/generated_by are UNCHANGED (origin provenance)
  # last_modified_* updated to reflect the fix
  # run_time and touch_count updated to reflect the latest AECF write pass
    return deepcopy(_CANONICAL_SPEC)
```

------------------------------------------------------------

## CHECKLIST ITEMS (to be referenced by IMPLEMENT_CHECKLIST and FIX_CODE_CHECKLIST)

- [ ] Every new function has `AECF_META` line in docstring
- [ ] `skill` matches the currently executing skill ID
- [ ] `topic` matches the resolved TOPIC for this execution
- [ ] `run_time` contains a valid UTC ISO-8601 timestamp for the latest AECF run
- [ ] `generated_at` contains a valid UTC ISO-8601 timestamp
- [ ] `generated_by` contains `Executed By ID` or `N/A`
- [ ] `last_modified_*` fields and `run_time` equal `generated_*` timestamps on first creation
- [ ] `touch_count` starts at `1` and increments by exactly `1` on each later AECF modification
- [ ] On modification: only `last_modified_*`, `run_time`, and `touch_count` fields update; origin fields preserved
- [ ] Legacy functions without `AECF_META` that are modified have retroactive line added with `touch_count=1` and `retroactive=true`

------------------------------------------------------------

## RELATED FILES

- `aecf_prompts/templates/TEMPLATE_HEADERS.md` — document-level metadata standard
- `aecf_prompts/prompts/04_IMPLEMENT.md` — enforces this standard at IMPLEMENT phase
- `aecf_prompts/prompts/06_FIX_CODE.md` — enforces meta update at FIX_CODE phase
- `aecf_prompts/checklists/IMPLEMENT_CHECKLIST.md` — includes function metadata checklist items
