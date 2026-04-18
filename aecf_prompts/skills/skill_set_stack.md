# AECF SKILL — Set Stack

------------------------------------------------------------

## MANDATORY CONTEXT LOAD

This skill operates under the following mandatory contexts:

- aecf_prompts/AECF_SYSTEM_CONTEXT.md
- aecf_prompts/SKILL_DISPATCHER.md (execution protocol)
- <workspace_root>/AECF_PROJECT_CONTEXT.md (if present anywhere in the active workspace)

Governance:
- aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md

If any of these contexts exist, they MUST be considered active constraints.

Execution is INVALID if these contexts are not acknowledged.

------------------------------------------------------------

## EXECUTION MANDATE (IMPERATIVE)

When this skill is invoked, the AI MUST:

1. **AUTO-RESOLVE** all parameters (TOPIC, scope, numbering) per SKILL_DISPATCHER
2. **VALIDATE** the explicit `stack=` argument against available domains and semantic profiles
3. **EXECUTE** the codebase intelligence workflow using the validated stack instead of auto-detecting it
4. **CREATE FILES** inside `.aecf/context/` (8 structured artifacts, same as `aecf_codebase_intelligence`)
5. **MATERIALIZE ALL OUTPUTS**: every artifact MUST be created before the skill is considered complete

**MANDATORY POST-EXECUTION GOVERNANCE (per SKILL_DISPATCHER)**:
- **UPDATE** `aecf_prompts/<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.json` for TOPIC lifecycle and **REGENERATE** `aecf_prompts/<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.md` (Step 4.1)
- **APPEND** one execution entry to `aecf_prompts/<DOCS_ROOT>/<user_id>/AECF_CHANGELOG.md` (Step 4.2)

**FORBIDDEN**:
- ❌ Responding only in chat without creating files
- ❌ Modifying any source code in the repository
- ❌ Executing project code or build scripts
- ❌ Accessing external networks
- ❌ Asking the user for execution mode, output path, or AECF conventions
- ❌ Auto-detecting the stack — the user-provided `stack=` value is the authoritative stack definition
- ❌ Proceeding when `stack=` is missing or empty AND the guided Q&A flow is not active — the skill MUST trigger the guided domain/profile selection

------------------------------------------------------------

## Skill ID
`aecf_set_stack`

## Description

Set the project stack explicitly and generate codebase intelligence artifacts using
the user-provided stack instead of auto-detection.

This skill is functionally equivalent to `aecf_codebase_intelligence` with one
critical difference: the STACK_JSON artifact is derived from the explicit `stack=`
argument, NOT from automatic stack detection. The remaining 7 artifacts
(architecture graph, symbol index, entry points, module map, code hotspots,
context keys, dynamic project context) are generated normally.

This is useful when:
- The project stack is perfectly known and auto-detection is unnecessary.
- The repository contains mixed technologies and the user wants to force a specific stack focus.
- Auto-detection might yield inaccurate results for unusual repo layouts.

### REQUIRE TOPIC

### REQUIRE STACK

The `stack=` argument is REQUIRED for this skill.

**Guided Q&A flow**: When the user invokes `set_stack` **without** providing `stack=`,
the extension activates a two-step guided flow instead of rejecting the invocation:

1. **Step 1 — Domain selection**: AECF lists all available domains from
   `aecf_prompts/knowledge/domains/` and presents them as selectable buttons.
   The user picks a domain or types a custom one.

2. **Step 2 — Semantic profile selection**: AECF lists the semantic profiles
   available for the selected domain under `<domain>/semantic_profiles/`.
   The user picks one or more profiles, chooses "none" for domain-only, or
   types custom profiles.

3. **Execution**: The resolved `stack=` value is assembled from the selections
   and the skill re-dispatches automatically with the complete `stack=` argument.

#### Direct invocation format

When the user already knows the stack, they can provide `stack=` directly:

Format: `stack=<domain>-<profile1>-<profile2>-...`

Examples:
- `stack=python-flask_web-sqlalchemy_orm`
- `stack=java-spring_boot_service-jpa_persistence`
- `stack=dotnet`
- `stack=cobol`
- `stack=react-react_component_app_architecture`
- `stack=node-node_service_base_architecture`

### Stack validation rules

1. The first segment (before the first `-`) is the **domain**. It MUST exist as a directory under `aecf_prompts/knowledge/domains/`.
2. Each subsequent segment is a **semantic profile**. It MUST exist as a `.md` file under `aecf_prompts/knowledge/domains/<domain>/semantic_profiles/`.
3. If the domain does not exist, the skill MUST report the error and list available domains.
4. If a semantic profile does not exist, the skill MUST report the error and list available profiles for the resolved domain.

## Execution Phase

This skill MUST run in **AECF PHASE 0** — before any PLAN or IMPLEMENT step.

------------------------------------------------------------

## PHASE_DEFINITION

### AECF_SET_STACK
output_file: .aecf/context/AECF_DYNAMIC_PROJECT_CONTEXT.md
requires_prompt: false
gate: none
loop_to: none
requires_plan_go: false

---

## TAXONOMY

skill_tier: TIER2
requires_determinism: true

------------------------------------------------------------

## Trigger Phrases

- set the stack to python flask sqlalchemy
- use this stack for the project
- configure project stack as java spring boot
- set stack explicitly without auto-detection
- force stack to dotnet
- set the stack (triggers guided Q&A when no stack= is provided)
- help me configure the project stack

------------------------------------------------------------

## Output Artifacts

All outputs MUST be written inside: `.aecf/context/`

The 8 artifacts are identical to `aecf_codebase_intelligence`:

### 1. STACK_JSON.json

Machine-readable stack artifact **constructed from the explicit `stack=` argument**.

Unlike `aecf_codebase_intelligence`, this artifact is NOT auto-detected. The AI MUST:
1. Parse the `stack=` value.
2. Map the domain to `language` (and related fields).
3. Map semantic profiles to `framework`, `database`, `orm`, `testing`, `platform`, `architecture`.
4. Fill remaining fields with evidence from manifest files and file extensions (supplementary, NOT primary).

**Minimum fields**:
- `language`
- `framework`
- `database`
- `orm`
- `testing`
- `platform`
- `architecture`
- `_set_by`: `"explicit"` (marks that this stack was set explicitly, not auto-detected)
- `_stack_argument`: the raw `stack=` value provided by the user

### 2–8. Same as `aecf_codebase_intelligence`

The following artifacts follow the same structure and rules:
- `AECF_ARCHITECTURE_GRAPH.json`
- `AECF_SYMBOL_INDEX.json`
- `AECF_ENTRY_POINTS.json`
- `AECF_MODULE_MAP.json`
- `AECF_CODE_HOTSPOTS.json`
- `AECF_CONTEXT_KEYS.json`
- `AECF_DYNAMIC_PROJECT_CONTEXT.md`

Refer to `skill_codebase_intelligence.md` for detailed schemas.

------------------------------------------------------------

## Analysis Scope

Same as `aecf_codebase_intelligence`: the skill MUST analyze the **entire workspace**, language-independent.

All 10 analysis steps from `aecf_codebase_intelligence` apply, with the exception of **Step 3 — Stack Detection**:
- Step 3 is **replaced** by explicit stack resolution from the `stack=` argument.
- The AI MUST NOT override or second-guess the user-provided stack.

------------------------------------------------------------

## Security Constraints

The skill MUST:
- NOT modify source code
- NOT execute project code
- NOT run build scripts
- NOT access external networks

Only repository inspection is allowed.

------------------------------------------------------------

## OUTPUT CONTRACT (MANDATORY DELIMITED FORMAT)

The AI MUST produce ALL 8 artifacts in a **single output** using delimited sections.
Identical format to `aecf_codebase_intelligence`.

Each section is preceded by an `===ARTIFACT_NAME===` delimiter on its own line.

**Required delimiters in order:**

```
===STACK_JSON===
{ ... valid JSON for STACK_JSON.json — with _set_by: "explicit" ... }

===ARCHITECTURE_GRAPH===
{ ... valid JSON for AECF_ARCHITECTURE_GRAPH.json ... }

===SYMBOL_INDEX===
{ ... valid JSON for AECF_SYMBOL_INDEX.json ... }

===ENTRY_POINTS===
{ ... valid JSON for AECF_ENTRY_POINTS.json ... }

===MODULE_MAP===
{ ... valid JSON for AECF_MODULE_MAP.json ... }

===CODE_HOTSPOTS===
{ ... valid JSON for AECF_CODE_HOTSPOTS.json ... }

===CONTEXT_KEYS===
{ ... valid JSON for AECF_CONTEXT_KEYS.json ... }

===DYNAMIC_PROJECT_CONTEXT===
# AECF Dynamic Project Context
... Markdown content for AECF_DYNAMIC_PROJECT_CONTEXT.md ...
```

**Rules:**
1. The first 7 sections MUST contain **valid, parseable JSON** — no trailing commas, no comments.
2. The last section (`DYNAMIC_PROJECT_CONTEXT`) is **Markdown**, not JSON.
3. All artifacts are persisted to `.aecf/context/` by the engine automatically.
4. Do NOT wrap JSON in code fences inside delimited sections — raw JSON only.
5. Every delimiter MUST appear exactly once. Missing delimiters = incomplete execution.
6. Emit NOTHING before `===STACK_JSON===` and NOTHING after the end of `===DYNAMIC_PROJECT_CONTEXT===`.
7. STACK_JSON MUST include `"_set_by": "explicit"` and `"_stack_argument": "<raw_value>"`.
8. FORBIDDEN anywhere in the output: `Resumen Ejecutivo`, `Executive Summary`, `Hallazgos`, `Recomendaciones`, `Compliance Score`, scoring tables, or audit severities.

------------------------------------------------------------

## AI_METADATA

AI_USED: TRUE
MODEL: Any
DECISION_AUTOMATION: YES
DATA_SENSITIVITY: INTERNAL

## AI_EXPLAINABILITY

- Model used: Any LLM with code analysis capability
- Data inputs: Repository file system (read-only), explicit stack= argument
- Decision logic summary: Validates stack= against available domains/profiles, then performs static analysis identical to codebase_intelligence with the stack forced from user input
- Deterministic components: Stack validation, file counting, extension mapping, import graph, LOC measurement
- Probabilistic components: Module grouping heuristics, core component ranking
- User-facing explanation provided? YES (via AECF_DYNAMIC_PROJECT_CONTEXT.md)

## AI_EXPLAINABILITY_VALIDATION

- Explainability level defined? 3
- User explanation rendered? YES
- Model version logged? YES
- Decision trace stored? YES (in artifact metadata)

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact: None (read-only analysis)
- Model impact: NO
- Risk impact: LOW (informational artifacts only)
- Compliance check: N/A

------------------------------------------------------------

**END OF skill_set_stack.md**
