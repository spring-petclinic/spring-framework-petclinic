# AECF Guides Master

LAST_REVIEW: 2026-04-13
OWNER SEACHAD

---

## Purpose

This is the master index for every Markdown guide published under `aecf_prompts/guides/`.

Published HTML surface:

- The GitHub Pages entry point is the repo-root `index.html`.
- `guias/GUIDE_VIEWER.html` is the HTML viewer for the Markdown guides listed here.
- The published surface is documentation-only: it should route readers through HTML pages instead of exposing direct download links from the landing pages.

Rule of coherence:

1. If a new `.md` guide is added under `aecf_prompts/guides/`, this master guide MUST be updated in the same change.
2. If a guide is removed or renamed, this master guide MUST be updated in the same change.
3. The goal is discoverability, coherence, and prompt-only usability without forcing users to inspect the folder manually.

---

## Core Entry Guides

| Guide | Purpose |
|---|---|
| [START_HERE.md](START_HERE.md) | First orientation guide for new users of `aecf_prompts` |
| [QUICK_START.md](QUICK_START.md) | Primary operating entry point for prompt-only execution |
| [AECF_APPLICATION_LIFECYCLE_GUIDE.md](AECF_APPLICATION_LIFECYCLE_GUIDE.md) | Generic application lifecycle model with AECF skill mapping by methodology |
| [SKILL_CATALOG.md](SKILL_CATALOG.md) | Full skill catalog and routing matrix |
| [AECF_ASSET_VERSIONS.md](AECF_ASSET_VERSIONS.md) | Deterministic content version stamps for prompts and skills |

## Context And Bootstrap Guides

| Guide | Purpose |
|---|---|
| [AECF_PROJECT_CONTEXT_BOOTSTRAP.md](AECF_PROJECT_CONTEXT_BOOTSTRAP.md) | How to create or improve project context |
| [AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md](AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md) | Token-saving strategy for static reusable context |
| [AECF_MEMORY_MODEL.md](AECF_MEMORY_MODEL.md) | Memory model for prompt-only usage |
| [AECF_RUN_CONTEXT_CONTRACT.md](AECF_RUN_CONTEXT_CONTRACT.md) | Canonical contract for `AECF_RUN_CONTEXT.json` |

## Surface And Scope Guides

| Guide | Purpose |
|---|---|
| [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md) | Model for `business_surface` and `technical_surface` partitioning |
| [AECF_SURFACE_SELECTION_INTAKE.md](AECF_SURFACE_SELECTION_INTAKE.md) | Intake process to decide when and how to use `surfaces` |
| [AECF_SKILL_SURFACE_CONTRACT.md](AECF_SKILL_SURFACE_CONTRACT.md) | Common contract for skills that consume `surfaces` |
| [AECF_MULTI_REPO_SURFACES.md](AECF_MULTI_REPO_SURFACES.md) | **[PROPOSAL]** Multi-repo surface model with contract boundaries and federation manifests |

## Prompt-Only Operation Guides

| Guide | Purpose |
|---|---|
| [AECF_PROMPT_ONLY_COMMANDS.md](AECF_PROMPT_ONLY_COMMANDS.md) | `@aecf`-style prompt-only command equivalences |
| [AECF_PROMPT_ONLY_INSTRUCTIONS_BLOCK.md](AECF_PROMPT_ONLY_INSTRUCTIONS_BLOCK.md) | Canonical instructions block for prompt-only setups |
| [AECF_PROMPT_ONLY_TICKET_PUBLISHER.md](AECF_PROMPT_ONLY_TICKET_PUBLISHER.md) | Prompt-only ticket publishing and related workflow |
| [AECF_PROMPTS_CLAUDE_CLI.md](AECF_PROMPTS_CLAUDE_CLI.md) | Host-specific quick start for Claude CLI |
| [AECF_PROMPTS_CODEX_CLI.md](AECF_PROMPTS_CODEX_CLI.md) | Host-specific quick start for Codex CLI |
| [LLM_INSTRUCTIONS_SETUP.md](LLM_INSTRUCTIONS_SETUP.md) | How to set up prompt/instruction loading correctly |

## Extension And Advanced Usage Guides

| Guide | Purpose |
|---|---|
| [AECF_EXTERNAL_SKILLS.md](AECF_EXTERNAL_SKILLS.md) | How to extend AECF with local external skills |
| [CONSULTING_PLAYBOOK.md](CONSULTING_PLAYBOOK.md) | Consulting-oriented usage patterns |

---

## Completeness Checklist

The current master guide intentionally references every Markdown guide currently present in `aecf_prompts/guides/`:

- `AECF_APPLICATION_LIFECYCLE_GUIDE.md`
- `AECF_ASSET_VERSIONS.md`
- `AECF_EXTERNAL_SKILLS.md`
- `AECF_GUIDES_MASTER.md`
- `AECF_MEMORY_MODEL.md`
- `AECF_MULTI_REPO_SURFACES.md`
- `AECF_PROJECT_CONTEXT_BOOTSTRAP.md`
- `AECF_PROMPTS_CLAUDE_CLI.md`
- `AECF_PROMPTS_CODEX_CLI.md`
- `AECF_PROMPT_ONLY_COMMANDS.md`
- `AECF_PROMPT_ONLY_INSTRUCTIONS_BLOCK.md`
- `AECF_PROMPT_ONLY_TICKET_PUBLISHER.md`
- `AECF_RUN_CONTEXT_CONTRACT.md`
- `AECF_SKILL_SURFACE_CONTRACT.md`
- `AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md`
- `AECF_SURFACE_CONTEXT_MODEL.md`
- `AECF_SURFACE_SELECTION_INTAKE.md`
- `CONSULTING_PLAYBOOK.md`
- `LLM_INSTRUCTIONS_SETUP.md`
- `QUICK_START.md`
- `SKILL_CATALOG.md`
- `START_HERE.md`

If this list becomes stale, update it immediately in the same request that changed the guides folder.