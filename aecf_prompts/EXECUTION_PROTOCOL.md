# AECF EXECUTION PROTOCOL (v1)

> Universal execution contract for all AECF skills. Shared by MCP and prompt-only paths.
> Steps are IN ORDER — no step may be skipped.

---

## Step 1: ACKNOWLEDGE

Display before execution:

```
✅ Skill recognized: <skill_name>
📌 TOPIC: <resolved_topic>
📂 Scope: <resolved_scope>
🔢 Next number: <NN>
🌐 Output language: <resolved_output_language>
📄 Output: <DOCS_ROOT>/<user_id>/<TOPIC>/AECF_<NN>_<DOCUMENT_NAME>.md
```

## Step 2: LOAD CONTEXTS

Load in order (silent — do not narrate to user):

1. `aecf_prompts/AECF_SYSTEM_CONTEXT.md`
2. `<workspace_root>/AECF_PROJECT_CONTEXT.md` (if exists)
3. `aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md`
4. `aecf_prompts/templates/TEMPLATE_HEADERS.md` (universal metadata standard)
5. The resolved `skill_*.md` file
6. Referenced templates, checklists, phase prompts from the skill definition

**`_ext` overlay**: for each file loaded, check for `<name>_ext.<ext>` sibling. If it exists, load and merge (`_ext` wins on conflict).

**Prompt metadata gate**: every prompt from `aecf_prompts/prompts/` MUST contain `@METADATA` header with at least `Document Type` and `Phase`. Missing metadata → execution INVALID.

## Step 3: EXECUTE SKILL

Execute the skill's defined workflow completely:

- Follow the skill's phase sequence as defined in its `skill_*.md` file.
- Apply AECF rules from SYSTEM_CONTEXT (including `_ext` overlays).
- Apply governance from EXECUTIVE_SUMMARY_GOVERNANCE.
- Apply metadata from TEMPLATE_HEADERS.md to ALL generated documents.
- Use prompt-level `@METADATA` as mandatory execution contract per phase.

### Phase-by-phase materialization (MANDATORY)

For multi-phase skills, execution MUST be strictly sequential:

1. Execute the current phase prompt.
2. Create the phase output document(s) **immediately** (no deferred/batch creation).
3. Validate that the artifact includes mandatory metadata.
4. Only then proceed to the next phase.

### Explainability gate (conditional)

If the skill declares `AI_USED = TRUE`, the output MUST include `## AI_EXPLAINABILITY_VALIDATION` with all required fields. Missing block → execution INVALID.

## Step 4: GENERATE OUTPUT

**CRITICAL**: Each document-producing phase MUST create its file at:

```
<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_<NN>_<DOCUMENT_NAME>.md
```

The file MUST include the standard `## METADATA` block per `templates/TEMPLATE_HEADERS.md`. Missing/incomplete metadata → document INVALID.

### 4.1 Update TOPICS_INVENTORY (mandatory, every execution)

After file creation, update `<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.json` and regenerate `.md`. Status logic: OPEN → ACTIVE → CLOSED (by executive_summary) → REOPENED. Create if missing. See SKILL_DISPATCHER §4.1 data model for JSON schema details.

### 4.2 Update CHANGELOG (mandatory, every execution)

Append entry to `<DOCS_ROOT>/<user_id>/AECF_CHANGELOG.md` with date, TOPIC, skill, artifact path, and summary. Create if missing.

## Step 5: CONFIRM COMPLETION

```
✅ Skill execution complete
📄 File created: <DOCS_ROOT>/<user_id>/<TOPIC>/AECF_<NN>_<DOCUMENT_NAME>.md
📊 TOPICS_INVENTORY updated: <TOPIC> → <STATUS>
📝 CHANGELOG updated: <DOCS_ROOT>/<user_id>/AECF_CHANGELOG.md
```

---

## Non-negotiable rules

1. **Execution mode is ALWAYS "AECF STRICT"** — never ask the user.
2. **Every invocation MUST produce files** — chat-only response = INVALID execution.
3. **AECF conventions are mandatory** — never ask if the user wants them.
4. **Templates load automatically** — no user confirmation needed.
5. **Minimal prompts MUST work**: `skill: code_standards_audit. TOPIC: STANDARDS` is sufficient.
6. **Always create the output file** — incomplete file > no file.
7. **AECF naming**: `AECF_<NN>_<DOCUMENT_NAME>.md`, `<NN>` sequential within TOPIC.
8. **Triad enforcement**: `skill` + `TOPIC` + `prompt` → enforced skill invocation, no free-form bypass.
9. **Phase gates are blocking**: each skill defines its own sequential gates (e.g., PLAN → AUDIT → IMPLEMENT). Skipping is a dispatcher violation.
