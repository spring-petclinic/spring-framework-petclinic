LAST_REVIEW: 2026-04-10
OWNER SEACHAD

## AECF_PROMPT_ONLY_INSTRUCTIONS

This workspace uses AECF in prompt-only mode from `aecf_prompts/`.

Inside a prompt-only bundle, treat `aecf_prompts/` as the source of truth for AECF prompts, skills, templates, checklists, guides, and scoring assets.

Resolve any user reference to `@aecf` or identifiers starting with `aecf_` against `aecf_prompts/` first, but if a bundled MCP tool is available for that exact command intent, prefer the MCP tool before the manual prompt-only fallback. Those references may point to a prompt-only command, a skill, a phase prompt, a template, a checklist, a scoring rule, or a guide. Do not assume that the AECF component/runtime is installed.

Use this resolution order:

1. `AECF_METHODOLOGY.md`
2. `guides/AECF_PROMPT_ONLY_COMMANDS.md`
3. `skills/`
4. `prompts/`
5. `templates/`
6. `checklists/`
7. `scoring/`
8. `<DOCS_ROOT>/AECF_PROJECT_CONTEXT.md` if it exists. Default prompt-only location: `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md`

Mandatory rules:

1. Treat `@aecf ...` as a routed AECF intent: if a bundled MCP tool exists for that exact command intent, call the MCP tool first; otherwise resolve it manually from `aecf_prompts/`.
2. If the user input matches an explicit `@aecf <command>` grammar, resolve that command first before any open-ended repository exploration or broad file search.
3. For explicit command handling, read only the minimum command-specific files required by the router. Do not start from unrelated guides, static context syntheses, or broad recursive searches unless the canonical command paths are missing.
4. For `@aecf memory list`, inspect `.aecf/memories/project/AECF_MEMORY.md`, `.aecf/memories/project/AECF_MEMORY_<user_id>.md`, and `.aecf/memories/project/events/` first. If they do not exist, return a deterministic empty-store answer instead of inferring memory state from unrelated documentation.
5. When a request depends on component runtime, terminal automation, GitHub integration, persistent runtime state, or webviews, state that prompt-only mode cannot execute it and offer the closest manual equivalent from `aecf_prompts/`, except for `@aecf send issue`, `@aecf send feature`, `@aecf show workspace_statistics`, `@aecf show settings`, `@aecf settings show`, `@aecf settings set`, and `@aecf status`: if the corresponding helper exists in `aecf_prompts/scripts/` and tool execution is permitted, execute it before falling back to the manual variant.
6. Before executing a skill, load `<DOCS_ROOT>/AECF_PROJECT_CONTEXT.md` if it exists. Default prompt-only location: `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md`.
7. If an AECF identifier is ambiguous, search `skills/`, `prompts/`, `templates/`, `checklists/`, and `guides/` before asking the user to clarify.
8. Resolve the effective prompt-only documentation root as follows: use `AECF_PROMPTS_DOCUMENTATION_PATH`; if not present, accept `AECF_PROMPTS_DIRECTORY_PATH` as a legacy alias; otherwise default to `<active_workspace>/.aecf/runtime/documentation`.
9. Create the effective documentation root when it does not exist yet, and always place topic artifacts under `<DOCS_ROOT>/<user_id>/<TOPIC>/`.
10. Keep the shared prompt-only human context artifact `AECF_PROJECT_CONTEXT.md` at the effective `DOCS_ROOT`, and keep per-user governance files `AECF_TOPICS_INVENTORY.json`, `AECF_TOPICS_INVENTORY.md`, and `AECF_CHANGELOG.md` under `<DOCS_ROOT>/<user_id>/`.
11. For `@aecf settings set <key>=<value>` or `@aecf settings set <key>`: (a) normalize the key resolving aliases (`language`/`idiom`/`idioma`/`lang` → `output_language`); (b) if the value is missing or not in the allowed set, show the full table of allowed values and require the user to choose — do not assume a default; (c) determine the target file: with `--global` → `<workspace>/.aecf/user_settings.json`; without `--global` → `<workspace>/.aecf/user_settings_<user_id>.json` where `user_id` is the resolved attribution; (d) if valid, persist using `python aecf_prompts/scripts/settings.py set <key>=<value> [--global]` when tool execution is permitted, or by editing the JSON directly otherwise. User-scoped settings override global at read time.
12. For `@aecf settings show` resolve it identically to `@aecf show settings`: prefer `python aecf_prompts/scripts/show_settings.py`; if not executable, reproduce bundle root, attribution, DOCS_ROOT, and the effective user settings by reading `<workspace>/.aecf/user_settings.json` plus `<workspace>/.aecf/user_settings_<user_id>.json` when `user_id` is resolved, applying priority `user -> global -> default` and attributing the source of each effective value.
13. Keep this block verbatim when synchronizing `aecf_forced_instructions.md` inside an `aecf_prompts` bundle root.
14. Keep the bundle model-agnostic: do not require a concrete model ID. If the host exposes the active model or capability profile, adapt by inference rather than hardcoding provider-specific model names.
15. Resolve active attribution with priority `AECF_PROMPTS_USER_ID`, then `AECF_PROMPTS_MODEL_ID` or `MODEL_ID`, then `AECF_PROMPTS_AGENT_ID` or `AGENT_ID`; if one of those sources is already available, state the resolved attribution and continue without asking the user to confirm it again.
16. For `@aecf init`, if `aecf_prompts/scripts/bootstrap_prompt_only_bundle.exe` is available and tool execution is permitted, run `aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --diagnose-env` before any manual question about attribution or `DOCS_ROOT`.
17. When `bootstrap_prompt_only_bundle.exe --diagnose-env` is available, do NOT probe environment variables with generic shell commands such as `pwsh`, `cmd`, `set`, `echo %VAR%`, or `$env:`. Use the executable output as the authoritative environment snapshot.

## END AECF_PROMPT_ONLY_INSTRUCTIONS

