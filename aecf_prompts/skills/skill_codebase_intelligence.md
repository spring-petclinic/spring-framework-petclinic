# AECF SKILL — Codebase Intelligence

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
2. **EXECUTE** the skill workflow according to this definition
3. **CREATE FILES** inside `.aecf/context/` (8 structured artifacts)
4. **MATERIALIZE ALL OUTPUTS**: every artifact MUST be created before the skill is considered complete

**MANDATORY POST-EXECUTION GOVERNANCE (per SKILL_DISPATCHER)**:
- **UPDATE** `aecf_prompts/<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.json` for TOPIC lifecycle and **REGENERATE** `aecf_prompts/<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.md` (Step 4.1)
- **APPEND** one execution entry to `aecf_prompts/<DOCS_ROOT>/<user_id>/AECF_CHANGELOG.md` (Step 4.2)

**FORBIDDEN**:
- ❌ Responding only in chat without creating files
- ❌ Modifying any source code in the repository
- ❌ Executing project code or build scripts
- ❌ Accessing external networks
- ❌ Asking the user for execution mode, output path, or AECF conventions

------------------------------------------------------------

## Skill ID
`aecf_codebase_intelligence`

## Description

Generate a complete dynamic intelligence context of the current workspace.

This skill analyzes the project repository and produces structured artifacts
that serve as **input context for other AECF skills** (PLAN, IMPLEMENT, AUDIT,
REFACTOR, DOCUMENT). The goal is to build a **machine-readable understanding of
the project** so that subsequent skills operate with reliable architectural
knowledge instead of raw code scanning.

The generated artifacts act as **context keys** for later skill executions.

## Execution Phase

This skill MUST run in **AECF PHASE 0** — before any PLAN or IMPLEMENT step.

------------------------------------------------------------

## PHASE_DEFINITION

### AECF_CODEBASE_INTELLIGENCE
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

## Output Artifacts

All outputs MUST be written inside: `.aecf/context/`

### 1. STACK_JSON.json

Machine-readable stack detection artifact used by downstream stack-aware skills.

**Minimum fields**:
- `language`
- `framework`
- `database`
- `orm`
- `testing`
- `platform`
- `architecture`

### 2. AECF_DYNAMIC_PROJECT_CONTEXT.md

Human-readable architectural overview of the repository.

**Required sections**:
- Project Overview
- Detected Stack
- Project Structure
- Entry Points
- Core Modules
- Core Classes
- Core Functions
- Architecture Style
- Code Hotspots
- Configuration Areas
- Testing Structure
- Risk Areas

### 3. AECF_ARCHITECTURE_GRAPH.json

Machine-readable dependency graph.

**Structure**:
```json
{
  "nodes": {
    "files": [],
    "classes": [],
    "functions": [],
    "modules": []
  },
  "edges": {
    "imports": [],
    "calls": [],
    "dependencies": []
  }
}
```

**Used by later skills to detect**: impact of modifications, module coupling, dependency chains.

### 4. AECF_SYMBOL_INDEX.json

Complete symbol index of the repository.

**Must include**: functions, classes, methods, interfaces, structs.

**Example**:
```json
{
  "UserService": {
    "type": "class",
    "file": "services/user_service.py",
    "line": 12
  },
  "calculate_limits": {
    "type": "function",
    "file": "services/license_service.py",
    "line": 45
  }
}
```

### 5. AECF_ENTRY_POINTS.json

Detected system entry points.

**Patterns to detect**: `main.*`, `app.*`, `server.*`, `index.*`, `Application.*`, `cli.*`, Python `__main__` blocks, Java main methods.

### 6. AECF_MODULE_MAP.json

Logical grouping of modules.

**Example**:
```json
{
  "api": [],
  "services": [],
  "repositories": [],
  "models": [],
  "utils": []
}
```

### 7. AECF_CODE_HOTSPOTS.json

Files and modules with structural risk.

**Detection criteria**:
- Files > 500 LOC
- Files with many imports
- Files with high call frequency

### 8. AECF_CONTEXT_KEYS.json

Context keys used by other skills as **structured context secrets**.

**Example**:
```json
{
  "core_modules": [],
  "core_classes": [],
  "core_functions": [],
  "entry_points": [],
  "critical_files": []
}
```

Other skills MUST reference these keys instead of scanning the repository again.

------------------------------------------------------------

## Analysis Scope

The skill MUST analyze the **entire workspace**.

The skill MUST apply the effective Codebase Intelligence exclusions **before**
building the directory tree, counting files, extracting symbols, or generating
dependency/hotspot artifacts.

Effective exclusion manifest resolution order:

1. `.aecf/custom/ci_exclusions.json` when present in the client workspace.
2. `aecf_prompts/ci_exclusions.json` when the prompt bundle was copied into a
  client repository without the full component runtime.
3. Built-in exclusions explicitly listed in this skill when neither manifest is
  available.

If an exclusion manifest is present, the AI MUST treat its entries as
authoritative scope constraints for repository enumeration and MUST NOT inspect
excluded files or directories except to confirm that they are excluded.

It MUST work **independently of programming language**.

**Supported languages** include but are not limited to:
Python, Java, JavaScript, TypeScript, Go, Rust, C, C++, C#, Kotlin, Ruby, PHP.

------------------------------------------------------------

## Analysis Steps

### Step 1 — Project Structure
Generate a directory tree of the project.
**Exclude**: `.git`, `node_modules`, `dist`, `build`, `target`, `venv`, `__pycache__`.

### Step 1.1 — Exclusion Manifest Resolution
Before scanning the repository, resolve exclusions from `.aecf/custom/ci_exclusions.json`
or, in prompt-only/client-copy mode, from `aecf_prompts/ci_exclusions.json`.
Honor the manifest for directory exclusion, file exclusion, and vendor-path
filtering across all later analysis steps.

### Step 2 — Language Detection
Detect languages based on file extensions. Compute distribution percentage.

### Step 3 — Stack Detection
Inspect known dependency files: `requirements.txt`, `pyproject.toml`, `package.json`, `pom.xml`, `go.mod`, `Cargo.toml`, `Dockerfile`.
Extract frameworks and runtime technologies.

### Step 4 — Entry Point Detection
Search for entry patterns and runtime entrypoints (Python `__main__`, Java `main`, etc.).

### Step 5 — Symbol Extraction
Detect all symbols: functions, classes, interfaces, methods, modules.
Index them with file path and line number.

### Step 6 — Dependency Graph
Analyze import relationships between modules.
Infer module dependencies. Build the architecture graph.

### Step 7 — Core Component Detection
Identify most referenced classes, most referenced functions, most imported modules.
These represent the **core domain components**.

### Step 8 — Hotspot Detection
Detect files with large size, high coupling, or many references.
These represent architectural risk areas.

### Step 9 — Configuration Detection
Detect configuration files: `.env`, `config.*`, `settings.*`, `*.yaml`, `*.json`.

### Step 10 — Testing Detection
Locate test directories: `tests`, `__tests__`, `test_*`.
Map test coverage areas.

------------------------------------------------------------

## Security Constraints

The skill MUST:
- NOT modify source code
- NOT execute project code
- NOT run build scripts
- NOT access external networks

Only repository inspection is allowed.

------------------------------------------------------------

## Usage by Other Skills

Other AECF skills MUST use the generated context artifacts instead of performing expensive repository scans.

Prompt-only execution is INCOMPLETE if any of the 8 artifacts listed in this skill is missing from `.aecf/context/` after the run.

| Downstream Skill | Uses Artifact |
|------------------|---------------|
| Stack-aware generation/audit/refactor skills | `STACK_JSON.json` as detected default stack evidence |
| PLAN | `AECF_CONTEXT_KEYS.json` |
| IMPLEMENT | `AECF_SYMBOL_INDEX.json` |
| AUDIT | `AECF_ARCHITECTURE_GRAPH.json` |
| REFACTOR | `AECF_CODE_HOTSPOTS.json` + `AECF_MODULE_MAP.json` |
| DOCUMENT | `AECF_DYNAMIC_PROJECT_CONTEXT.md` |

Prompt-only practical rule:

1. `STACK_JSON.json` is the default stack evidence for later executions unless a later run passes an explicit `stack=` override;
2. `AECF_CONTEXT_KEYS.json` is the lightweight planning bridge so prompts do not need to reopen the whole repository map;
3. `AECF_SYMBOL_INDEX.json` and `AECF_ARCHITECTURE_GRAPH.json` are the reusable technical evidence for implementation and audit reasoning;
4. `AECF_CODE_HOTSPOTS.json` and `AECF_MODULE_MAP.json` are the reusable evidence for refactor and test-hardening scope;
5. `AECF_DYNAMIC_PROJECT_CONTEXT.md` is the readable dynamic context layer for documentation and architecture-oriented downstream prompts.

### Stack override examples

- Detected stack only: `@aecf run skill=codebase_intelligence topic=repo_map`
- Reuse detected stack implicitly in later executions: `@aecf run skill=new_feature topic=orders prompt="Implement retry policy"`
- Override detected stack for a specific generation run: `@aecf run skill=new_feature topic=orders prompt="Implement retry policy" stack=python-flask`
- Override detected stack for a specific audit run: `@aecf run skill=code_standards_audit topic=orders_audit prompt="Audit retry module" stack=java-spring`

If an explicit `stack=` is provided later, it overrides the detected `STACK_JSON.json` only for that execution.

------------------------------------------------------------

## Output Requirements

The generated artifacts MUST be:
- Deterministic
- Reproducible
- Language independent
- Machine readable

------------------------------------------------------------

## OUTPUT CONTRACT (MANDATORY DELIMITED FORMAT)

The AI MUST produce ALL 8 artifacts in a **single output** using delimited sections.

Each section is preceded by an `===ARTIFACT_NAME===` delimiter on its own line.

**Required delimiters in order:**

```
===STACK_JSON===
{ ... valid JSON for STACK_JSON.json ... }

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
7. Ignore generic AECF document conventions about executive summaries for this skill's model output; the only valid output is the delimited artifact set.
8. FORBIDDEN anywhere in the output: `Resumen Ejecutivo`, `Executive Summary`, `Hallazgos`, `Recomendaciones`, `Compliance Score`, scoring tables, or audit severities.

------------------------------------------------------------

## AI_METADATA

AI_USED: TRUE
MODEL: Any
DECISION_AUTOMATION: YES
DATA_SENSITIVITY: INTERNAL

## AI_EXPLAINABILITY

- Model used: Any LLM with code analysis capability
- Data inputs: Repository file system (read-only)
- Decision logic summary: Static analysis of file extensions, AST parsing, import graph construction, LOC counting, pattern matching for entry points and config files
- Deterministic components: File counting, extension mapping, import graph, LOC measurement
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

**END OF skill_codebase_intelligence.md**
