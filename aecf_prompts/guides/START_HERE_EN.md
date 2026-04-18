# AECF Prompts - Start Here

LAST_REVIEW: 2026-04-15
OWNER SEACHAD

---

## If you are new, start here

If you are reading the published documentation on GitHub Pages, start from `index.html` at the repository root and use `GUIDE_VIEWER.html` to open this guide and the rest of the markdown set without leaving the HTML surface.

If you are working in a target workspace with the prompt-only MCP enabled, you can request this same guide through `aecf_show_guide` so the host renders it in the effective `output_language` and only falls back to a derived translation when no human-maintained localized copy exists.

If you only need to know where to start with `aecf_prompts`, follow this order:

1. Read [AECF_GUIDES_MASTER.md](AECF_GUIDES_MASTER.md)
2. Read [QUICK_START.md](QUICK_START.md)
3. If you do not want to draft all project context by hand, read [AECF_PROJECT_CONTEXT_BOOTSTRAP.md](AECF_PROJECT_CONTEXT_BOOTSTRAP.md)
4. If you want to save tokens per session, read [AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md](AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md)
5. If you want `@aecf`-like syntax without the component, read [AECF_PROMPT_ONLY_COMMANDS.md](AECF_PROMPT_ONLY_COMMANDS.md)
6. If you want project memory to enrich every skill, read [AECF_MEMORY_MODEL.md](AECF_MEMORY_MODEL.md)
7. If the repository is large or multi-team, read [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md)
8. If you want to extend a base skill with project-local rules, read [AECF_EXTERNAL_SKILLS.md](AECF_EXTERNAL_SKILLS.md)
9. If you need skill detail, read [../skills/README_SKILLS.md](../skills/README_SKILLS.md)
10. If you need the full methodology, read [../AECF_METHODOLOGY.md](../AECF_METHODOLOGY.md)
11. If you want to understand in which way AECF maps with different project management methodologies read [AECF_APPLICATION_LIFECYCLE_GUIDE.md](AECF_APPLICATION_LIFECYCLE_GUIDE.md)

## Which guide to use depending on the LLM host

- ChatGPT / Copilot Chat web: start with [QUICK_START.md](QUICK_START.md)
- Claude CLI: use [AECF_PROMPTS_CLAUDE_CLI.md](AECF_PROMPTS_CLAUDE_CLI.md)
- Codex CLI: use [AECF_PROMPTS_CODEX_CLI.md](AECF_PROMPTS_CODEX_CLI.md)
- Project-local external skills: use [AECF_EXTERNAL_SKILLS.md](AECF_EXTERNAL_SKILLS.md)

## Minimum recommended order

1. Copy `aecf_prompts/` into the project.
2. Define topic attribution with `AECF_PROMPTS_USER_ID` or, if that is missing, with `AECF_PROMPTS_MODEL_ID`/`MODEL_ID` or `AECF_PROMPTS_AGENT_ID`/`AGENT_ID`. If the host is ambiguous, validate what the bundle sees with `aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --diagnose-env`.
3. Prepare context:
   - fast path: create `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md`
   - better path: run `aecf_project_context_generator`
4. If the repo is large or complex, run `aecf_codebase_intelligence`.
5. If the repo is large or multi-team, create `surfaces` with help from [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md).
6. Start your first real flow from [QUICK_START.md](QUICK_START.md), usually with `new_feature`, `refactor`, or `hotfix`.

## Where the knowledge packs live

In this repository, the canonical source for knowledge packs and semantic profiles that `aecf_prompts` can also consume is:

- `aecf_prompts/knowledge/domains/<domain>/pack.md`
- `aecf_prompts/knowledge/domains/<domain>/semantic_profiles/<profile>.md`

Real example:

- `aecf_prompts/knowledge/domains/java/pack.md`
- `aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md`

`aecf_prompts` also publishes the same surface for prompt-only usage in:

- `aecf_prompts/knowledge/domains/java/pack.md`
- `aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md`

If you want to reuse them in prompt-only mode, you can:

1. Reference the canonical source `aecf_prompts/knowledge/...` if you are working inside this repository.
2. Use `aecf_prompts/knowledge/...` if you are working with the prompt-only bundle.
3. If you build a partial distribution, make sure `aecf_prompts/knowledge/` travels with the package.

## Synchronization rule

If you copy those assets to another location inside this repository for prompt-only consumption or distribution, that copy does not become a new canonical source.

The canonical source remains `aecf_prompts/knowledge/`.

In addition, repository rules require any change made in `aecf_prompts/knowledge/` to stay synchronized with:

- `aecf_prompts/knowledge/`
- `aecf_prompts/knowledge/`

If you create an additional copy for a manual bundle, that copy must also stay aligned with the canonical source to avoid documentation and behavior drift.

## Practical rule

`START_HERE.md` orients.

`QUICK_START.md` drives execution.

If you need reusable semantic profiles in prompt-only mode inside this repository, use the canonical source `aecf_prompts/knowledge/domains/...` and the published copy `aecf_prompts/knowledge/domains/...` as your references.

When in doubt, always start with [QUICK_START.md](QUICK_START.md).

