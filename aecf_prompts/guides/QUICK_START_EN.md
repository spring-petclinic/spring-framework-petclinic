# AECF Prompts - Quick Start

LAST_REVIEW: 2026-04-15

---

## 0. Use this guide as the main entry point

In the HTML publication for GitHub Pages, the entry point is `index.html` at the repository root and this guide is opened through `GUIDE_VIEWER.html` to keep navigation inside the HTML documentation surface.

If you are new to `aecf_prompts`, this is the guide you should follow first.

Useful companion guides depending on what you need:

- guide master index: [AECF_GUIDES_MASTER.md](AECF_GUIDES_MASTER.md)
- general orientation: [START_HERE.md](START_HERE.md)
- context bootstrap: [AECF_PROJECT_CONTEXT_BOOTSTRAP.md](AECF_PROJECT_CONTEXT_BOOTSTRAP.md)
- token savings: [AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md](AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md)
- `@aecf`-like syntax without the component: [AECF_PROMPT_ONLY_COMMANDS.md](AECF_PROMPT_ONLY_COMMANDS.md)
- global and per-user or per-agent memory: [AECF_MEMORY_MODEL.md](AECF_MEMORY_MODEL.md)
- large or multi-team repositories: [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md)
- project-local external skills: [AECF_EXTERNAL_SKILLS.md](AECF_EXTERNAL_SKILLS.md)
- `AECF_RUN_CONTEXT.json` contract: [AECF_RUN_CONTEXT_CONTRACT.md](AECF_RUN_CONTEXT_CONTRACT.md)
- `surface` selection intake: [AECF_SURFACE_SELECTION_INTAKE.md](AECF_SURFACE_SELECTION_INTAKE.md)
- skill detail: [../skills/README_SKILLS.md](../skills/README_SKILLS.md)
- full methodology: [../AECF_METHODOLOGY.md](../AECF_METHODOLOGY.md)

## 1. Preparation (5 minutes)

### 1.1 Copy aecf_prompts into the project

```text
my-project/
├── aecf_prompts/              <- copy here
├── .aecf/
│   └── runtime/
│       └── documentation/
│           └── AECF_PROJECT_CONTEXT.md  <- create this file
├── src/
└── ...
```

> `.aecf/documentation/` will be created automatically to store skill/topic outputs without depending on the bundle folder.

If the repository is large, use `AECF_PROJECT_CONTEXT.md` as the minimum global layer and partition the rest of the context with the `surface` model described in `AECF_SURFACE_CONTEXT_MODEL.md`.

### 1.2 Verify topic attribution

Before using the prompts, verify which identifier will be frozen into the real topic.

Canonical attribution priority:

1. `AECF_PROMPTS_USER_ID`
2. `AECF_PROMPTS_MODEL_ID` or `MODEL_ID`
3. `AECF_PROMPTS_AGENT_ID` or `AGENT_ID`

If you need user-specific memory, use the effective identifier frozen in `AECF_RUN_CONTEXT.json`. See [AECF_MEMORY_MODEL.md](AECF_MEMORY_MODEL.md).

Windows PowerShell examples to persist it:

```powershell
setx AECF_PROMPTS_USER_ID "ana.garcia@empresa.com"
setx AECF_PROMPTS_MODEL_ID "gpt-5.4"
setx AECF_PROMPTS_AGENT_ID "copilot-agent"
```

If you use `setx`, open a new shell before running bundle bootstrap.

If you want to validate exactly what the `.exe` sees on your machine, run:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --diagnose-env
```

### 1.2.b Synchronize prompt-only instruction files

After defining the attribution you need, create or refresh the default instruction surfaces from the bundle:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --sync-instructions
```

If you are working on the repository source copy rather than on the client bundle, use the equivalent `.py` script.

This creates or refreshes `aecf_forced_instructions.md` with the canonical English instruction block from the bundle and keeps `.github/copilot-instructions.md`, `copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, and `.codex/instructions.md` as the minimum instruction-loading surfaces.

### 1.3 Create .aecf/documentation/AECF_PROJECT_CONTEXT.md

Create this file in `.aecf/documentation/` with at least the following structure:

```markdown
# AECF Project Context

## Project
- Name: My Project
- Language: Python / TypeScript / Java / ...
- Framework: Django / React / Spring / ...
- OUTPUT_LANGUAGE: ENGLISH / SPANISH / FRENCH / ...

## Team
- Size: X developers
- Risk tolerance: Low / Medium / High

## Standards
- Testing framework: pytest / jest / junit / ...
- Coverage target: 80%
- Branching strategy: trunk-based / gitflow / ...

## Scoring Thresholds
- Feature: 75
- Hotfix: 70
- Security: 90
```

---

## 2. Your first execution (10 minutes)

### 2.0 Optional: keep `@aecf`-like syntax

If you want to use `aecf_prompts/` without the component while keeping syntax similar to `@aecf`, also load `aecf_prompts/guides/AECF_PROMPT_ONLY_COMMANDS.md` into the LLM.

With that guide, inputs like these are resolved manually:

```text
@aecf list skills
@aecf run skill=new_feature TOPIC=user_auth prompt="Implement JWT authentication with refresh tokens"
@aecf context
```

They do not execute real commands: the LLM translates them into skills, prompts, and artifacts from `aecf_prompts/`.

### Example: New feature with `new_feature`

**Step 1**: Inspect the skill

Read `aecf_prompts/skills/skill_new_feature.md` -> it defines the flow:

```text
PLAN -> AUDIT_PLAN -> [FIX_PLAN] -> TEST_STRATEGY -> IMPLEMENT -> AUDIT_CODE -> [FIX_CODE] -> VERSION
```

If the repository is large, before running the first phase also resolve:

1. `primary_surface`,
2. `active_surfaces`,
3. whether global context is enough or per-`surface` context is required.

Record that resolution in `AECF_RUN_CONTEXT.json` when the flow is real.

If you need a short intermediate output before fixing the JSON, use `aecf_prompts/templates/SURFACE_SELECTION_BRIEF_TEMPLATE.md`.

**Step 2**: Execute PLAN

Paste this into your LLM:

```text
use skill=new_feature TOPIC=user_auth prompt=Implement JWT authentication with refresh tokens
```

Or, if you loaded the prompt-only command equivalents guide:

```text
@aecf run skill=new_feature TOPIC=user_auth prompt=Implement JWT authentication with refresh tokens
```

Then paste the contents of `aecf_prompts/prompts/00_PLAN.md`.

> The prompt already contains instructions about which files the LLM must load (`<DOCS_ROOT>/AECF_PROJECT_CONTEXT.md`) and where to save the output (`<DOCS_ROOT>/<user_id>/user_auth/01_new_feature_PLAN.md`). Use `AECF_PROMPTS_DOCUMENTATION_PATH` if you need to override the default workspace `DOCS_ROOT`. `AECF_PROMPTS_DIRECTORY_PATH` is still accepted as a legacy alias.

Before starting a real execution for a `TOPIC`, also freeze the output language for the run:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --topic user_auth --prompt-text "Implement JWT authentication with refresh tokens"
```

If you are working on the repository source copy rather than on the client bundle, use the equivalent `.py` script.

That command creates `<DOCS_ROOT>/<user_id>/user_auth/AECF_RUN_CONTEXT.json` with the resolved `output_language` and the frozen attribution for the whole execution.

If the repository uses `surfaces`, complete that file following the contract from `AECF_RUN_CONTEXT_CONTRACT.md`.

**Step 3**: Execute AUDIT_PLAN

Paste this into your LLM:

```text
use skill=new_feature TOPIC=user_auth prompt=Audit the JWT authentication plan
```

Then paste the contents of `aecf_prompts/prompts/02_AUDIT_PLAN.md`.

> The prompt tells the LLM to load the generated plan, the checklist, and the scoring model automatically. You do not need to paste them yourself.

**Step 4**: Evaluate the verdict

- **GO** -> continue with the next phase (`TEST_STRATEGY`)
- **NO-GO** -> execute `FIX_PLAN` (paste `prompts/03_FIX_PLAN.md`) and then re-audit

**Step 5**: Repeat for each phase in the flow

Each prompt already knows:

- Which previous files must be read
- Which checklist and scoring to apply, when applicable
- Where the output must be stored

---

## 3. Quick skill reference

| Skill | When to use it | Complexity |
| --- | --- | --- |
| `new_feature` | New feature, not urgent | TIER 3 (8 phases) |
| `refactor` | Improve existing code | TIER 3 (8 phases) |
| `hotfix` | Production emergency | TIER 3 (threshold 70) |
| `code_standards_audit` | Review coding standards | TIER 1 (1 phase) |
| `security_review` | Review security | TIER 1 (1 phase) |
| `document_legacy` | Document existing code | TIER 2 (3 phases) |
| `explain_behavior` | Understand a behavior | TIER 1 (1 phase) |
| `executive_summary` | Stakeholder summary | TIER 1 (1 phase) |

---

## 4. Where each output goes

All outputs are stored under `<DOCS_ROOT>/<user_id>/{{TOPIC}}/`.

`<DOCS_ROOT>` uses `artifacts_path` from `.aecf/user_settings.json` (as `.aecf/<artifacts_path>`) if set; otherwise `AECF_PROMPTS_DOCUMENTATION_PATH` if it exists; otherwise it accepts `AECF_PROMPTS_DIRECTORY_PATH` as a legacy alias; if none exists, it defaults to `<workspace>/.aecf/documentation`:

| Phase | Output file |
| --- | --- |
| PLAN | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/01_<skill_name>_PLAN.md` |
| AUDIT_PLAN | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/02_<skill_name>_AUDIT_PLAN.md` |
| FIX_PLAN | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/03_<skill_name>_FIX_PLAN.md` |
| TEST_STRATEGY | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/04_<skill_name>_TEST_STRATEGY.md` |
| IMPLEMENT | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/05_<skill_name>_IMPLEMENT.md` |
| AUDIT_CODE | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/06_<skill_name>_AUDIT_CODE.md` |
| FIX_CODE | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/07_<skill_name>_FIX_CODE.md` |
| VERSION | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/08_<skill_name>_VERSION.md` |

---

## 5. Tips

- **Each prompt already knows what it needs** - you do not need to tell the LLM what to load; the prompt does.
- **Correct attribution depends on the first available identifier** - `AECF_PROMPTS_USER_ID`, then `AECF_PROMPTS_MODEL_ID`/`MODEL_ID`, then `AECF_PROMPTS_AGENT_ID`/`AGENT_ID`.
- **If the chat host cannot see the environment, validate with `--diagnose-env`** - the `.exe` uses `os.environ` directly and tells you exactly which AECF variables are visible to the bundle.
- **Freeze the language per TOPIC** - use `bootstrap_prompt_only_bundle.exe --topic ...` before the first phase of every real execution.
- **If the repo is large, activate a primary `surface`** - avoid loading the entire global context if the task only touches one part of the system.
- **If the LLM cannot read files** (for example in ChatGPT web), paste the required file contents together with the prompt.
- **If the LLM does not follow the template**, explicitly instruct it to follow the structure from `aecf_prompts/templates/`.
- **Save every output** to the path indicated by the prompt before moving to the next phase.

---

## 6. Knowledge Packs and Semantic Profiles

### 6.1 Canonical source in this repository

If you are using `aecf_prompts` inside this same repository, the knowledge packs you must treat as the canonical source are:

- `aecf_prompts/knowledge/domains/<domain>/pack.md`
- `aecf_prompts/knowledge/domains/<domain>/semantic_profiles/<profile>.md`

Real Java + ZKoss example:

- `aecf_prompts/knowledge/domains/java/pack.md`
- `aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md`

The prompt-only package publishes the same surface in:

- `aecf_prompts/knowledge/domains/java/pack.md`
- `aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md`

### 6.2 How to use them with `aecf_prompts`

`aecf_prompts` skills already have a consistent local path because `knowledge/` is part of the published package.

So real usage is one of these two:

1. Inside this repository: reference `aecf_prompts/knowledge/...` as the canonical source.
2. In the prompt-only bundle: reference `aecf_prompts/knowledge/...` as the published copy.

If your LLM can read workspace files, tell it explicitly to load those files as additional domain and stack context.

Conceptual example for a `new_feature` flow:

```text
use skill=new_feature TOPIC=zk_order_screen prompt=Create a ZKoss screen to manage orders

Before answering, also read:
- .aecf/documentation/AECF_PROJECT_CONTEXT.md
- aecf_prompts/knowledge/domains/java/pack.md
- aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md
```

If your LLM cannot read files, paste those Markdown files together with the phase prompt.

### 6.3 Minimal practical example

To document or plan over a Java + ZKoss project:

```text
use skill=document_legacy TOPIC=zk_backoffice prompt=Document the backoffice module built with ZUL and composers

Mandatory additional context:
- .aecf/documentation/AECF_PROJECT_CONTEXT.md
- aecf_prompts/knowledge/domains/java/pack.md
- aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md
```

To implement a new feature:

```text
use skill=new_feature TOPIC=zk_customer_search prompt=Implement customer search in a ZKoss screen

Mandatory additional context:
- .aecf/documentation/AECF_PROJECT_CONTEXT.md
- aecf_prompts/knowledge/domains/java/pack.md
- aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md
```

### 6.4 If you copy them to another path

If you build a partial distribution and move those assets to a folder different from `aecf_prompts/knowledge/`, remember this:

1. In this repository the canonical source remains `aecf_prompts/knowledge/`.
2. `aecf_prompts/knowledge/` is the published prompt-only copy.
3. The copy must not evolve independently.
4. If you change the canonical knowledge, you must keep the copy synchronized.

Repository rule:

- `aecf_prompts/knowledge/`, `aecf_prompts/knowledge/`, and `aecf_prompts/knowledge/` must remain synchronized.

If you create a fourth copy for manual distribution, keep it synchronized as well so you do not introduce drift.

