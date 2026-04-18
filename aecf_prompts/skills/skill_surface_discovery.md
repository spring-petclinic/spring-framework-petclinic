# AECF SKILL — Surface Discovery

------------------------------------------------------------

## MANDATORY CONTEXT LOAD

This skill operates under the following mandatory contexts:

- aecf_prompts/AECF_SYSTEM_CONTEXT.md
- aecf_prompts/SKILL_DISPATCHER.md (execution protocol)
- <workspace_root>/AECF_PROJECT_CONTEXT.md (if present anywhere in the active workspace)

**REQUIRED inputs from `aecf_codebase_intelligence`** (BLOCKING — see Entry Gate below):

- `.aecf/context/AECF_MODULE_MAP.json`
- `.aecf/context/AECF_ARCHITECTURE_GRAPH.json`
- `.aecf/context/AECF_CODE_HOTSPOTS.json`

**Optional enrichment inputs** (consumed when present, not blocking):

- `.aecf/context/STACK_JSON.json`
- `.aecf/context/AECF_SYMBOL_INDEX.json`
- `.aecf/context/AECF_ENTRY_POINTS.json`
- `.aecf/context/AECF_CONTEXT_KEYS.json`
- `.aecf/context/AECF_DYNAMIC_PROJECT_CONTEXT.md`

Governance:
- aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md

If any of these contexts exist, they MUST be considered active constraints.

Execution is INVALID if these contexts are not acknowledged.

------------------------------------------------------------

## ENTRY GATE — MANDATORY NO-GO CHECK

**This gate is BLOCKING. The skill MUST NOT proceed past this point if any required artifact is missing.**

Before any analysis begins, the AI MUST verify the existence of ALL of the following files:

| Required Artifact | Expected Path |
|---|---|
| Module Map | `.aecf/context/AECF_MODULE_MAP.json` |
| Architecture Graph | `.aecf/context/AECF_ARCHITECTURE_GRAPH.json` |
| Code Hotspots | `.aecf/context/AECF_CODE_HOTSPOTS.json` |

### Gate evaluation procedure

1. For each required artifact, check if the file exists in the workspace.
2. If **ALL** three files exist → verdict is **GO** → proceed to execution.
3. If **ANY** file is missing → verdict is **NO-GO** → execute the NO-GO protocol below.

### NO-GO protocol

When the gate verdict is NO-GO, the AI MUST:

1. **STOP** all analysis — do NOT attempt partial execution.
2. **EMIT** the artifact using the `===SURFACE_DISCOVERY===` delimiter containing ONLY a NO-GO report:

```markdown
# AECF Surface Discovery — NO-GO

## Gate Verdict: NO-GO

The following required artifacts from `aecf_codebase_intelligence` are missing:

- [ ] `.aecf/context/AECF_MODULE_MAP.json` — <PRESENT or MISSING>
- [ ] `.aecf/context/AECF_ARCHITECTURE_GRAPH.json` — <PRESENT or MISSING>
- [ ] `.aecf/context/AECF_CODE_HOTSPOTS.json` — <PRESENT or MISSING>

## Action Required

Run `aecf_codebase_intelligence` first to produce the required artifacts:

```
@aecf run skill=codebase_intelligence topic=<your_topic>
```

Then re-run `aecf_surface_discovery`.

## Reason

Surface Discovery requires the module map to cluster paths, the architecture graph to
measure import density and cross-module coupling, and the code hotspots to annotate
high-risk files within each proposed surface. Without these inputs, any surface proposal
would be based on directory names alone — insufficient for evidence-based decisions.
```

3. **WRITE** the NO-GO report to `.aecf/context/AECF_SURFACE_DISCOVERY.md`.
4. **INFORM** the user in chat that the skill cannot proceed and which artifacts are missing.
5. **COMPLETE** post-execution governance (TOPICS_INVENTORY, CHANGELOG) recording the NO-GO outcome.

------------------------------------------------------------

## EXECUTION MANDATE (IMPERATIVE)

When this skill is invoked AND the Entry Gate verdict is GO, the AI MUST:

1. **AUTO-RESOLVE** all parameters per SKILL_DISPATCHER
2. **EXECUTE** the skill workflow producing TWO artifacts:
   - `.aecf/context/AECF_SURFACE_DISCOVERY.md` — the authoritative surface manifest
   - `.aecf/context/surfaces_draft.md` — the human-facing validation & refinement document
3. **ENRICHMENT CHECK**: if `.aecf/context/surfaces_draft.md` already exists, the skill MUST NOT delete or overwrite it — it MUST enrich it (see Enrichment Mode below)
4. **DRIFT CHECK**: if `.aecf/context/AECF_SURFACE_DISCOVERY.md` already exists, run drift detection before overwriting

**MANDATORY POST-EXECUTION GOVERNANCE (per SKILL_DISPATCHER)**:
- **UPDATE** `aecf_prompts/<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.json` for TOPIC lifecycle and **REGENERATE** `aecf_prompts/<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.md`
- **APPEND** one execution entry to `aecf_prompts/<DOCS_ROOT>/<user_id>/AECF_CHANGELOG.md`

**FORBIDDEN**:
- ❌ Responding only in chat without creating files
- ❌ Modifying any source code in the repository
- ❌ Executing project code or build scripts
- ❌ Accessing external networks
- ❌ Asking the user for execution mode, output path, or AECF conventions
- ❌ Overwriting an existing `AECF_SURFACE_DISCOVERY.md` that has been human-edited without emitting a DRIFT report first
- ❌ Deleting or replacing an existing `surfaces_draft.md` — enrichment only
- ❌ Including ownership decisions in the draft (that is a human team decision)
- ❌ Including knowledge-pack assignments in the draft (that belongs to the final validated artifact)
- ❌ Including skill execution recommendations in the draft (that is operational, not discovery)

------------------------------------------------------------

## Skill ID
`aecf_surface_discovery`

## Description

Analyze the project repository and produce:

1. **`AECF_SURFACE_DISCOVERY.md`** — the authoritative surface manifest that clusters paths, modules,
   scripts, and classes into named **technical surfaces** and **business surfaces**. This artifact acts
   as **guardrails for all other AECF skills**: each skill that accepts a `surface=` parameter reads
   this file to know which files are in scope and which are out of bounds.

2. **`surfaces_draft.md`** — an evidence-based working document designed for human teams (technical
   and functional) to validate, refine, split, merge, or reject each surface proposal. The draft
   contains the data and signals that justify each grouping so that decisions are made with evidence,
   not opinions.

**Dependency**: This skill REQUIRES the artifacts produced by `aecf_codebase_intelligence`
(`AECF_MODULE_MAP.json`, `AECF_ARCHITECTURE_GRAPH.json`, `AECF_CODE_HOTSPOTS.json`). If these
are not present, the skill exits with a NO-GO verdict (see Entry Gate).

**Enrichment mode**: If `surfaces_draft.md` already exists when the skill runs, it is NOT replaced.
The skill reads the existing draft, detects new or changed evidence from the repo, and appends or
updates sections — preserving all prior human annotations, decisions, and conversation notes.

## Execution Phase

This skill is a **Phase 0 Bootstrap skill** — it runs independently of any PLAN or IMPLEMENT step and
its output enriches all downstream skills.

It MUST be run AFTER `aecf_codebase_intelligence` and BEFORE any skill that uses `surface=` scoping.

------------------------------------------------------------

## PHASE_DEFINITION

### AECF_SURFACE_DISCOVERY
output_file: .aecf/context/AECF_SURFACE_DISCOVERY.md
secondary_output: .aecf/context/surfaces_draft.md
requires_prompt: false
entry_gate: codebase_intelligence_artifacts_present
gate: none
loop_to: none
requires_plan_go: false

### Entry Gate: codebase_intelligence_artifacts_present
type: entry
required_files:
  - .aecf/context/AECF_MODULE_MAP.json
  - .aecf/context/AECF_ARCHITECTURE_GRAPH.json
  - .aecf/context/AECF_CODE_HOTSPOTS.json
verdict_on_missing: NO-GO
recovery: "Run aecf_codebase_intelligence first"

---

## TAXONOMY

skill_tier: TIER2
requires_determinism: true

------------------------------------------------------------

## Output Artifact

### AECF_SURFACE_DISCOVERY.md

Location: `.aecf/context/AECF_SURFACE_DISCOVERY.md`

This is the **single authoritative surface manifest** for the project. It MUST be human-editable Markdown
and MUST follow the structure defined below.

#### Required document structure

The output Markdown MUST contain the following sections in this order:

```markdown
# AECF Surface Discovery

> This file is the authoritative surface manifest for your repository.
> Edit it freely — it is designed to be modified by humans.

## Metadata

| Field | Value |
|-------|-------|
| Schema Version | aecf_surface_discovery_v1 |
| Version | 1.0 |
| Generated | <ISO 8601 timestamp> |
| Repository | <repository root name or path> |

## How to Use This File

- Add, rename, or remove surfaces freely.
- Each surface defines the paths (dirs, files, globs) that belong to it.
- Paths are relative to the repository root.
- Glob patterns are supported (e.g. `workers/invoice_*.py`).

### How Other Skills Use This File

- Pass `surface=<id>` when invoking any AECF skill to scope it to that surface.
- Example: `@aecf run skill=security_review surface=authentication`
- Skills will only inspect paths listed under the specified surface.
- Skills will warn if a surface id does not exist in this file.

### Drift Detection

- Re-run `@aecf run skill=surface_discovery` to check if the repo has drifted.
- The **Drift Detection** section below records the last check result.

## Technical Surfaces

### <surface_id>

**Description**: <human-readable description>

**Paths**:
- `<path relative to repo root>`
- `<dir/>`
- `<glob pattern>`

**Owners**: <optional — team names, GitHub handles, email aliases>
**Tags**: <optional — e.g. security, critical, pii, revenue>
**Notes**: <optional — free-form notes for human editors>

(repeat for each technical surface)

## Business Surfaces

### <surface_id>

**Description**: <human-readable description>
**Inference Confidence**: HIGH | MEDIUM | LOW

**Paths**:
- `<path relative to repo root>`

**Owners**: <optional>
**Tags**: <optional>
**Notes**: <optional>

(repeat for each business surface)

## Shared Paths

| Path | Appears In | Recommendation |
|------|-----------|----------------|
| <path> | <surface_id_1>, <surface_id_2> | <suggested resolution> |

## Drift Detection

| Field | Value |
|-------|-------|
| Last Checked | <ISO 8601 timestamp> |
| Status | CLEAN or DRIFT_DETECTED |

### Missing Paths
(paths declared in surfaces that no longer exist — empty list if none)

### New Paths
(significant new paths not covered by any surface — empty list if none)

### Drift Summary
(human-readable summary when DRIFT_DETECTED — omit when CLEAN)
```

#### Inference confidence values (business surfaces only)

- `HIGH` — direct naming match AND cohesive import cluster
- `MEDIUM` — naming match but sparse imports, OR import cluster without naming match
- `LOW` — heuristic-only inference; human review strongly recommended

------------------------------------------------------------

### surfaces_draft.md

Location: `.aecf/context/surfaces_draft.md`

This is the **evidence-based working document** for human teams to validate, refine, and enrich the
surface proposals. It is designed to be read by both technical and functional stakeholders so that
decisions to accept, reject, split, or merge surfaces are backed by data.

**Lifecycle rule**: This file is NEVER deleted or replaced by the skill. On re-run, the skill reads
the existing draft, identifies new evidence or repo changes, and appends enrichment sections marked
with the re-run timestamp. All prior human annotations, decisions, and notes are preserved.

#### Required document structure

```markdown
# AECF Surface Discovery — Draft for Validation

> This document is a working artifact for human teams. Edit it freely.
> Decisions recorded here will feed the final `AECF_SURFACE_DISCOVERY.md`.
>
> **DO NOT delete sections you disagree with** — mark them with your decision
> (✅ ACCEPTED / ❌ REJECTED / 🔀 MERGE / ✂️ SPLIT) and add a note explaining why.

## Metadata

| Field | Value |
|-------|-------|
| Generated | <ISO 8601 timestamp> |
| Repository | <repository root name or path> |
| Codebase Intelligence Run | <timestamp of the CI artifacts used> |
| Draft Version | 1 (incremented on each enrichment) |

## How to Use This Document

1. Review each proposed surface below.
2. For each one, check the **Signals**, **Metrics**, and **Dependencies** sections.
3. Record your decision using the status markers: ✅ ❌ 🔀 ✂️
4. Answer the **Open Questions** — your answers guide the next refinement.
5. Add any surface you think is missing in the **Surfaces Proposed by Team** section at the end.
6. When the team is satisfied, run `aecf_surface_discovery` again to produce the final validated manifest.

---

## Proposed Surface: <tentative_name>

> **Status**: 🔲 PENDING REVIEW

### Identification

**Tentative Name**: `<descriptive_name>` *(will be renamed during refinement)*
**Paths**:
- `<path or glob>`
- `<path or glob>`

### Signals Justifying This Grouping

Why these paths form a unit — citing evidence from `aecf_codebase_intelligence`:

- <signal 1: e.g., "These 4 directories share a dedicated `pom.xml`">
- <signal 2: e.g., "The architecture graph shows 47 cross-imports among these modules and only 3 towards the rest">
- <signal 3: e.g., "All files follow the controller/service/repository pattern">
- <signal 4: e.g., "Independent `package.json` with its own dependency tree">

**Evidence Source**: `AECF_MODULE_MAP.json` clusters [X, Y, Z] / `AECF_ARCHITECTURE_GRAPH.json` edge count: N

### Size Metrics

| Metric | Value |
|--------|-------|
| Files | <count> |
| Approximate LOC | <count> |
| Main Classes/Functions | <count> |
| Dominant Language | <language> |

*A surface too large defeats the purpose (the repo is too big to attack at once). A surface too small creates unnecessary overhead.*

### Dependencies with Other Proposed Surfaces

| Target Surface | Direction | Import Count | Key Coupling Points |
|---------------|-----------|-------------|---------------------|
| `<other_surface>` | outbound | <N> | `<file>` → `<file>` |
| `<other_surface>` | inbound | <N> | `<file>` → `<file>` |

*If two proposed surfaces have 200+ cross-imports, they probably should be one. If they have <5, the separation is well justified.*

### Internal Hotspots

Files flagged by `AECF_CODE_HOTSPOTS.json` that fall within this surface:

| File | Hotspot Reason | LOC | Coupling Score |
|------|---------------|-----|----------------|
| `<path>` | <large file / high coupling / high reference count> | <N> | <score> |

*The team needs this to decide if a hotspot warrants its own surface or stays as an attention zone within the current one.*

### Open Questions for Refinement

> Every surface MUST have at least one open question. If the discovery has no doubts, it is not looking deeply enough.

1. <question: e.g., "The `shared/` folder is used by 5 surfaces — should it be its own surface or replicated?">
2. <question: e.g., "The `legacy-adapter` module has patterns very different from the rest of this surface — should it be separated?">
3. <question: e.g., "There are no tests for this zone — is this intentional?">

**Team Response**: *(to be filled by reviewers)*

---

(repeat `## Proposed Surface: <tentative_name>` for each proposed surface)

---

## Cross-Surface Dependency Summary

| Surface A | Surface B | A→B Imports | B→A Imports | Total | Assessment |
|-----------|-----------|-------------|-------------|-------|-----------|
| `<surface>` | `<surface>` | <N> | <N> | <N> | <TIGHT / LOOSE / NEGLIGIBLE> |

Assessment criteria:
- **TIGHT** (>50 total): strong candidate for merging
- **LOOSE** (10–50): review coupling points — may need interface boundaries
- **NEGLIGIBLE** (<10): separation is well justified

## Global Hotspot Distribution

| Hotspot File | Proposed Surface | Hotspot Reason |
|-------------|-----------------|----------------|
| `<path>` | `<surface>` | <reason> |

Files that appear as hotspots but do NOT fall in any proposed surface:

| Orphan Hotspot | Nearest Surface | Recommendation |
|---------------|----------------|----------------|
| `<path>` | `<surface>` | <include / create new surface / investigate> |

## Surfaces Proposed by Team

> Add surfaces that the automated discovery missed. Use the same structure as above,
> or a simplified version — the next enrichment run will fill in metrics and signals.

*(empty until team fills it in)*

## Enrichment Log

| Run | Timestamp | Draft Version | Changes |
|-----|-----------|--------------|---------|
| 1 | <ISO 8601> | 1 | Initial draft |
```

#### Content rules for surfaces_draft.md

**MUST contain per proposed surface**:
1. **Identification** — tentative name + concrete paths (globs or folder/file listing)
2. **Signals justifying the grouping** — citing specific data from `aecf_codebase_intelligence` artifacts (import counts, shared build files, naming patterns, graph edges)
3. **Size metrics** — file count, approximate LOC, main classes/functions count
4. **Dependencies with other proposed surfaces** — import/reference counts and direction, with key coupling points
5. **Internal hotspots** — files from `AECF_CODE_HOTSPOTS.json` within this surface, with reason and scores
6. **Open questions** — at least one per surface; if there are zero questions, the analysis is too shallow

**MUST NOT contain**:
- ❌ Ownership decisions (team/person assignments) — that is a human team decision
- ❌ Knowledge pack assignments — that belongs to the final validated manifest
- ❌ Skill execution recommendations — that is operational, not discovery
- ❌ Technology recommendations — that is out of scope for surface mapping

#### Enrichment mode protocol

When `surfaces_draft.md` already exists:

1. **READ** the existing draft completely, including all human annotations and decisions
2. **COMPARE** current codebase_intelligence artifacts against the evidence cited in the draft
3. **For unchanged surfaces**: add nothing — preserve as-is
4. **For surfaces with new evidence**: append an `#### Enrichment (<timestamp>)` subsection under the affected surface documenting what changed (new files, changed import counts, new hotspots)
5. **For new surfaces detected**: append new `## Proposed Surface:` sections at the end, before the `## Surfaces Proposed by Team` section
6. **For surfaces whose paths no longer exist**: add a `⚠️ DRIFT` marker to the surface header and note which paths are missing
7. **Increment** the `Draft Version` in Metadata
8. **Append** a row to the `Enrichment Log` table

------------------------------------------------------------

## Analysis Scope

The skill MUST analyze the **entire workspace** applying the effective exclusion manifest:

1. `.aecf/custom/ci_exclusions.json` — when present in the client workspace
2. `aecf_prompts/ci_exclusions.json` — when the prompt bundle was copied without the full runtime
3. Built-in defaults when neither manifest is present: `.git`, `node_modules`, `dist`, `build`,
   `target`, `venv`, `__pycache__`, `*.egg-info`, `.aecf/`

Excluded paths MUST NOT appear in any surface's paths list.

------------------------------------------------------------

## Analysis Steps

### Step 0 — Entry Gate Validation

Verify the three required artifacts exist (see Entry Gate section). If any is missing → NO-GO.

### Step 1 — Load Codebase Intelligence Artifacts

Load and parse the mandatory inputs:

- **`AECF_MODULE_MAP.json`** → module clusters, module boundaries, dominant languages
- **`AECF_ARCHITECTURE_GRAPH.json`** → import edges, edge weights, cross-module coupling metrics
- **`AECF_CODE_HOTSPOTS.json`** → files flagged for size, coupling, or reference frequency

Also load optional inputs when present:
- **`STACK_JSON.json`** → technology stack context
- **`AECF_SYMBOL_INDEX.json`** → symbol-level detail for coupling analysis
- **`AECF_ENTRY_POINTS.json`** → entry point grouping for path clustering
- **`AECF_CONTEXT_KEYS.json`** → domain vocabulary for business surface inference

### Step 2 — Repository Structure Scan

Build a directory tree of the project excluding built-in defaults and any active exclusion manifest.

For each directory and significant file, collect:
- Path relative to repo root
- File count and dominant language/type
- Naming patterns (prefixes, suffixes, conventions)
- LOC (approximate — from module map or direct count)

### Step 3 — Existing Draft Check (Enrichment Mode)

If `.aecf/context/surfaces_draft.md` already exists:

1. Load the entire existing draft
2. Parse all human annotations, decisions (✅ ❌ 🔀 ✂️), and team-proposed surfaces
3. Mark this run as an enrichment run — do NOT create a new draft from scratch
4. Proceed to analysis steps, but compare results against existing evidence and only add deltas

### Step 4 — Technical Surface Clustering

Group paths into technical surfaces using the following signals in priority order:

1. **Directory naming conventions**: `auth/`, `api/`, `services/`, `models/`, `repositories/`,
   `workers/`, `jobs/`, `utils/`, `lib/`, `config/`, `migrations/`, `scripts/`, `tests/`
2. **Import density** (from `AECF_ARCHITECTURE_GRAPH.json`): files with heavy mutual imports cluster into the same surface — record exact edge counts as evidence
3. **Naming suffixes**: `*_service.py`, `*_repository.py`, `*_controller.py`, `*_handler.py`,
   `*_middleware.py`, `*Controller.java`, `*Repository.java`, `*Service.java`, `*Router.ts`, `*Store.ts`
4. **Module map clusters** (from `AECF_MODULE_MAP.json`): respect existing module boundaries as primary clustering input
5. **Entry point proximity** (from `AECF_ENTRY_POINTS.json` if available): files reached from the same entry point cluster together
6. **Configuration scope**: config files that configure a specific subsystem cluster with that subsystem

For each proposed surface, collect and record:
- The **signals** that justify the grouping (citing specific artifact data)
- **File count** and **approximate LOC** (from module map or direct count)
- **Main classes/functions count**
- **Dominant language**

**Minimum surfaces to detect** (only if matching paths exist):

| Surface ID | Signal |
|------------|--------|
| `api_layer` | HTTP endpoints, controllers, routers, view functions |
| `domain_services` | Business logic service classes/modules |
| `data_access` | Repositories, DAOs, ORM models, query builders |
| `workers_and_jobs` | Background tasks, queues, schedulers, cron |
| `authentication` | Auth flows, JWT, sessions, permissions, RBAC |
| `configuration` | Config files, environment loaders, settings modules |
| `infrastructure` | Dockerfile, CI/CD YAML, Kubernetes manifests, deployment scripts |
| `testing` | Test directories, fixtures, factories, test utilities |
| `utilities` | Shared helpers, formatters, validators, constants |

Do NOT create a surface if no paths match the detection signal.

### Step 5 — Business Surface Mapping

Map technical paths to business surfaces using:

1. **Naming semantics**: directories or files named after business domains
   (`billing`, `payments`, `orders`, `users`, `inventory`, `notifications`, `reporting`,
   `analytics`, `compliance`, `subscriptions`, `catalog`, `search`) map directly
2. **PROJECT_CONTEXT.md vocabulary**: if `AECF_PROJECT_CONTEXT.md` exists, extract the business
   domain vocabulary from it and use those terms as surface IDs
3. **Import graph clustering** (from `AECF_ARCHITECTURE_GRAPH.json`): if `billing_service.py` imports from `stripe_client.py` and
   `invoice_repository.py`, all three form a `billing` business surface
4. **Entry point grouping**: all files reachable from `/api/billing/` belong to a `billing` surface

Annotate each business surface with `Inference Confidence` (HIGH / MEDIUM / LOW) as defined above.

### Step 6 — Cross-Surface Dependency Analysis

For every pair of proposed surfaces, use `AECF_ARCHITECTURE_GRAPH.json` to count:
- Outbound imports (A → B)
- Inbound imports (B → A)
- Total coupling intensity

Classify each pair as TIGHT (>50), LOOSE (10–50), or NEGLIGIBLE (<10).

Populate the **Cross-Surface Dependency Summary** table in the draft.

### Step 7 — Hotspot Mapping

For each entry in `AECF_CODE_HOTSPOTS.json`:
1. Determine which proposed surface it falls in
2. Record the hotspot reason, LOC, and coupling score in that surface's **Internal Hotspots** table
3. If a hotspot falls outside all proposed surfaces, add it to the **Orphan Hotspots** table in the draft

### Step 8 — Open Questions Generation

For each proposed surface, generate at least one open question for human review. Questions should address:
- Ambiguous boundaries (paths that could belong to multiple surfaces)
- Unusual patterns within the surface (files that don't match the dominant pattern)
- Missing test coverage
- Shared dependencies that need a decision (own surface vs. replicate)
- Surfaces with TIGHT coupling to another (merge candidate?)
- Hotspots that might warrant their own surface

### Step 9 — Overlap Detection

Scan all surfaces for paths appearing in more than one surface. Populate the **Shared Paths** table with each
overlap, listing which surfaces include that path and a suggested resolution.

### Step 10 — Draft Population

Using all evidence collected in steps 1–9, populate `surfaces_draft.md` following the document structure defined above.

In enrichment mode: follow the enrichment protocol (see `surfaces_draft.md` section above) instead of creating from scratch.

### Step 11 — Drift Detection (re-run mode)

If `.aecf/context/AECF_SURFACE_DISCOVERY.md` already exists when the skill is invoked:

1. Load the existing manifest
2. For each path entry in every surface, validate it according to its type: literal file or
   directory paths must still exist exactly as declared, and glob patterns must be expanded
   relative to the repository root and match at least one existing path.
3. Populate **Missing Paths** with any literal paths that no longer exist and any glob
   patterns that expand to zero matches.
4. Scan the repo for significant new directories or files not covered by any surface and populate
   **New Paths**.
5. Set the **Status** field to `DRIFT_DETECTED` if either list is non-empty, `CLEAN` otherwise
6. When `DRIFT_DETECTED`, write a human-readable **Drift Summary** and emit a
   `===DRIFT_REPORT===` section BEFORE the `===SURFACE_DISCOVERY===` section in the output

### Step 12 — Manifest Population

Populate `AECF_SURFACE_DISCOVERY.md` with the final surface manifest based on the analysis.
The **How to Use This File** section MUST be included verbatim as defined in the document structure above.

------------------------------------------------------------

## Security Constraints

The skill MUST:
- NOT modify source code
- NOT execute project code
- NOT run build scripts
- NOT access external networks

Only repository inspection and Markdown artifact creation are allowed.

------------------------------------------------------------

## Usage by Other Skills

Skills that support surface-scoped execution read `AECF_SURFACE_DISCOVERY.md` to resolve the `surface=`
parameter at invocation time.

| Downstream Skill | Example `surface=` Usage |
|------------------|--------------------------|
| `aecf_security_review` | `surface=authentication` — scopes audit to auth paths only |
| `aecf_code_standards_audit` | `surface=domain_services` — audits only the service layer |
| `aecf_refactor` | `surface=data_access` — refactors only the repository layer |
| `aecf_document_legacy` | `surface=billing` — documents only the billing business domain |
| `aecf_new_feature` | `surface=api_layer` — constrains code generation to API paths |
| `aecf_new_test_set` | `surface=workers_and_jobs` — scopes test generation to workers |
| `aecf_explain_behavior` | `surface=authentication` — traces behavior within auth paths |

**Surface resolution protocol for downstream skills**:

1. If `surface=<id>` is provided, load `.aecf/context/AECF_SURFACE_DISCOVERY.md`
2. Look up the surface by heading `### <id>`
3. If not found: emit `SURFACE_NOT_FOUND` warning and ask user to check the manifest
   or re-run `aecf_surface_discovery`
4. If found: restrict all file discovery, search, and modification to paths listed under that surface
5. Exclusion manifest entries take precedence over surface paths at all times

### Invocation examples

```
# Generate surface discovery for the first time
@aecf run skill=surface_discovery topic=surface_discovery

# Re-run to check drift after a refactor
@aecf run skill=surface_discovery topic=surface_discovery_refresh

# Use a surface to scope a security audit
@aecf run skill=security_review surface=authentication topic=auth_sec_review

# Use a surface to scope a standards audit
@aecf run skill=code_standards_audit surface=billing topic=billing_audit

# Use a surface to scope a new feature
@aecf run skill=new_feature surface=api_layer topic=orders_endpoint prompt="Add GET /orders/:id endpoint"
```

------------------------------------------------------------

## OUTPUT CONTRACT (MANDATORY DELIMITED FORMAT)

The AI MUST produce the artifacts using the following delimiters:

```
===SURFACE_DISCOVERY===
# Markdown content for .aecf/context/AECF_SURFACE_DISCOVERY.md

===SURFACES_DRAFT===
# Markdown content for .aecf/context/surfaces_draft.md
```

**Rules:**
1. Content MUST be valid Markdown following the document structures defined in this skill.
2. Do NOT wrap content in code fences inside the delimited sections.
3. The `===SURFACE_DISCOVERY===` delimiter MUST appear exactly once.
4. The `===SURFACES_DRAFT===` delimiter MUST appear exactly once.
5. If drift was detected (re-run mode), emit `===DRIFT_REPORT===` BEFORE `===SURFACE_DISCOVERY===`:

```
===DRIFT_REPORT===
# Human-readable drift summary (plain text)
<summary of missing paths, new paths, recommendation>

===SURFACE_DISCOVERY===
<full updated Markdown manifest>

===SURFACES_DRAFT===
<full draft content — new or enriched>
```

6. On NO-GO, emit ONLY `===SURFACE_DISCOVERY===` with the NO-GO report (no draft is produced).

------------------------------------------------------------

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `aecf_codebase_intelligence` artifacts missing | Entry gate blocks with NO-GO — run `aecf_codebase_intelligence` first |
| A surface has more than 30 paths | Split into sub-surfaces with more specific IDs |
| Business surface inference confidence is LOW | Add a **Notes** field explaining the inference basis; human review required |
| A path appears in 3+ surfaces | Move it to a dedicated `shared_utilities` or `cross_cutting` surface |
| `AECF_PROJECT_CONTEXT.md` not found | Business surfaces will be inferred from naming only; expect MEDIUM/LOW confidence |
| Existing manifest has many DRIFT entries | Delete the manifest and re-run to cluster from scratch |
| Repo has no clear business domain separation | Leave **Business Surfaces** section with a note explaining why no surfaces were identified |
| Two surfaces have TIGHT coupling (>50 imports) | Flag in draft with merge recommendation and open question for team |
| `surfaces_draft.md` already exists | Enrichment mode — never replace, only add deltas and increment version |
| Hotspot falls outside all proposed surfaces | Add to Orphan Hotspots table with recommendation |
| No open questions generated for a surface | Analysis is too shallow — dig deeper into boundary ambiguities, test gaps, or coupling patterns |

------------------------------------------------------------

## Success Criteria

### When Entry Gate is GO:
- [ ] `.aecf/context/AECF_SURFACE_DISCOVERY.md` created or updated
- [ ] `.aecf/context/surfaces_draft.md` created or enriched (never replaced)
- [ ] At least one technical surface defined
- [ ] At least one business surface defined (or explicit explanation of why none)
- [ ] All surface paths verified to exist in the repository
- [ ] Each proposed surface in draft has: signals, size metrics, dependencies, hotspots, and at least one open question
- [ ] Cross-Surface Dependency Summary populated in the draft
- [ ] Global Hotspot Distribution populated in the draft
- [ ] **How to Use This File** section present and complete in the manifest
- [ ] **Drift Detection** section populated in the manifest
- [ ] **Shared Paths** table populated (empty table if no overlaps)
- [ ] No excluded paths appear in any surface
- [ ] No ownership decisions in the draft
- [ ] No knowledge-pack assignments in the draft
- [ ] No skill execution recommendations in the draft
- [ ] `AECF_TOPICS_INVENTORY.json` updated
- [ ] `AECF_CHANGELOG.md` updated

### When Entry Gate is NO-GO:
- [ ] `.aecf/context/AECF_SURFACE_DISCOVERY.md` created with NO-GO report
- [ ] NO-GO report lists which specific artifacts are missing
- [ ] User informed in chat about the missing prerequisites
- [ ] `AECF_TOPICS_INVENTORY.json` updated (recording NO-GO)
- [ ] `AECF_CHANGELOG.md` updated (recording NO-GO)

------------------------------------------------------------

## AI_METADATA

AI_USED: TRUE
MODEL: Any
DECISION_AUTOMATION: YES
DATA_SENSITIVITY: INTERNAL

## AI_EXPLAINABILITY

- Model used: Any LLM with code analysis capability
- Data inputs: Repository file system (read-only), AECF codebase intelligence artifacts (AECF_MODULE_MAP.json, AECF_ARCHITECTURE_GRAPH.json, AECF_CODE_HOTSPOTS.json — mandatory; STACK_JSON.json, AECF_SYMBOL_INDEX.json, AECF_ENTRY_POINTS.json, AECF_CONTEXT_KEYS.json — optional)
- Decision logic summary: Module map clustering, architecture graph import density analysis,
  hotspot mapping, directory naming convention matching, semantic domain inference from PROJECT_CONTEXT vocabulary
- Deterministic components: Entry gate validation, path enumeration, import graph edge counting, hotspot file mapping
- Probabilistic components: Business surface domain inference, confidence scoring, open question generation
- User-facing explanation provided? YES (via AECF_SURFACE_DISCOVERY.md instructions section,
  surfaces_draft.md evidence sections, and per-surface confidence annotations)

## AI_EXPLAINABILITY_VALIDATION

- Explainability level defined? 3
- User explanation rendered? YES
- Model version logged? YES
- Decision trace stored? YES (in artifact metadata)

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact: None (read-only analysis + Markdown artifact creation)
- Model impact: NO
- Risk impact: LOW (informational artifact only — no source code modified)
- Compliance check: N/A

------------------------------------------------------------

**END OF skill_surface_discovery.md**
