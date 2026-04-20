# AECF Prompts - Start Here

LAST_REVIEW: 2026-04-20
OWNER SEACHAD

---

## Step 1 — Set up your user identity

Define the `AECF_PROMPTS_USER_ID` environment variable with your email or identifier. AECF uses it to attribute every topic and artifact.

```powershell
# Windows (persistent for the current user)
setx AECF_PROMPTS_USER_ID "your.email@company.com"
# Open a new terminal for the change to take effect.
```

```bash
# Linux / macOS
echo 'export AECF_PROMPTS_USER_ID="your.email@company.com"' >> ~/.bashrc
source ~/.bashrc
```

> If you skip this step the system auto-generates a random ID prefixed with `user_` that you will not be able to trace back. To check what the bundle sees: `aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --diagnose-env`

---

## Step 2 — Verify your LLM is operational

AECF is model-agnostic: it works with any LLM that can read workspace files (Copilot Chat, Claude, Codex, ChatGPT…).

Check before continuing:

- **VS Code + Copilot Chat / GitHub Copilot**: open the chat panel and confirm it responds.
- **Claude CLI**: run `claude --version` and verify you have an active session.
- **Codex CLI**: run `codex --version`.
- **ChatGPT web**: open a conversation and confirm access.

If your host cannot read workspace files directly, you will need to paste prompt contents manually.

---

## Step 3 — Copy the bundle and sync instructions

1. Copy the `aecf_prompts/` folder to the root of your target project.
2. Run the bootstrap to create the instruction files your LLM needs:

```powershell
# From the target project root
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --sync-instructions
```

This generates `aecf_forced_instructions.md` and host-specific instruction files (`.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, `.codex/instructions.md`).

---

## Step 4 — Generate the project context

Ask the LLM to run the context skill. No need to write it by hand:

```
@aecf run skill=project_context_generator prompt="Generate project context"
```

The skill scans the workspace and generates `AECF_PROJECT_CONTEXT.md` with the project structure, stack, standards, and team information.

Next, if the repository is medium or large, also run:

```
@aecf run skill=codebase_intelligence
```

This skill produces 8 analysis artifacts in `documentation/context/` (including `STACK_JSON.json`) that enrich every subsequent skill.

> **Fast path**: if you prefer to create the context manually, just write `.aecf/documentation/AECF_PROJECT_CONTEXT.md` with the sections Project, Team, Standards, and Scoring Thresholds.

---

## Step 5 — Launch your first skill

You are ready. Start your first real flow, typically with `new_feature`, `refactor`, or `hotfix`:

```
@aecf run skill=new_feature TOPIC=my_first_feature prompt="Description of what I want to implement"
```

See [QUICK_START.md](QUICK_START.md) for the full phase detail and how to iterate through them.

---

## Complementary guides

| Need | Guide |
|---|---|
| Full step-by-step flow | [QUICK_START.md](QUICK_START.md) |
| `@aecf` syntax without the component | [AECF_PROMPT_ONLY_COMMANDS.md](AECF_PROMPT_ONLY_COMMANDS.md) |
| Cross-session project memory | [AECF_MEMORY_MODEL.md](AECF_MEMORY_MODEL.md) |
| Large or multi-team repos (surfaces) | [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md) |
| Extend a skill with project-local rules | [AECF_EXTERNAL_SKILLS.md](AECF_EXTERNAL_SKILLS.md) |
| Token savings per session | [AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md](AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md) |
| Skills catalog | [../skills/README_SKILLS.md](../skills/README_SKILLS.md) |
| Full methodology | [../AECF_METHODOLOGY.md](../AECF_METHODOLOGY.md) |
| Mapping to project management methods | [AECF_APPLICATION_LIFECYCLE_GUIDE.md](AECF_APPLICATION_LIFECYCLE_GUIDE.md) |
| General guide index | [AECF_GUIDES_MASTER.md](AECF_GUIDES_MASTER.md) |

### Host-specific guide

| Host | Guide |
|---|---|
| ChatGPT / Copilot Chat web | [QUICK_START.md](QUICK_START.md) |
| Claude CLI | [AECF_PROMPTS_CLAUDE_CLI.md](AECF_PROMPTS_CLAUDE_CLI.md) |
| Codex CLI | [AECF_PROMPTS_CODEX_CLI.md](AECF_PROMPTS_CODEX_CLI.md) |

---

## Knowledge packs

Knowledge packs and semantic profiles live in `aecf_prompts/knowledge/domains/<domain>/pack.md` and `.../semantic_profiles/<profile>.md`. They load automatically when you use `stack=` in a skill invocation.

---

> `START_HERE.md` orients. [QUICK_START.md](QUICK_START.md) drives execution. When in doubt, always start with QUICK_START.

