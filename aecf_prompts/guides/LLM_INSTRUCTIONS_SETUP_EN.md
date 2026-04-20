# Default Instructions Setup for Hosts and LLMs

LAST_REVIEW: 2026-04-20
OWNER SEACHAD

---

> How to configure AECF instructions as default context in each compatible host or provider so that every execution automatically follows the methodology.

---

## 1. Concept

`aecf_prompts/` contains prompts, skills, templates, checklists, and scoring designed for manual execution with any LLM. If the host is configured to load AECF instructions as default context, **every new conversation starts with the methodology active** without needing to paste instructions manually.

The instructions in this bundle must remain **model-agnostic**:

- Do not fix a specific model ID unless the operator does so outside the bundle.
- If the tool exposes the active model or a capabilities profile, adapt behavior to that inferred signal.
- `.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, and `.codex/instructions.md` are loading surfaces, not contracts tied to a specific model.

If you also want to emulate an experience similar to `@aecf` without installing the component, also add `aecf_prompts/guides/AECF_PROMPT_ONLY_COMMANDS.md` to the default context. That guide converts inputs like `@aecf run ...` or `@aecf list skills` into manual resolutions based on `aecf_prompts/`.

For CLI-type hosts, that guide should not be loaded as passive documentation only: inputs with explicit `@aecf <command>` grammar must be resolved first against its prompt-only contract before initiating broad repo searches. This is especially important for commands like `@aecf memory list`, which must first inspect `.aecf/memories/project/` and return a deterministic state if the store does not yet exist.

If you also want persistent memory that enriches all skills sent to the LLM, also add `aecf_prompts/guides/AECF_MEMORY_MODEL.md`. That guide defines a general project memory and a user-specific memory under `.aecf/memories/project/`.

If you run `aecf_project_context_generator` from the root of the `aecf_prompts` bundle, the generator can automatically create or refresh `aecf_forced_instructions.md` with the canonical block from `aecf_prompts/guides/AECF_PROMPT_ONLY_INSTRUCTIONS_BLOCK.md` and leave `.github/copilot-instructions.md`, `copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, and `.codex/instructions.md` as minimal surfaces that only load it.

If you work without that generator, you can achieve the same result by running `aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --sync-instructions` from the root of the bundle delivered to the client. In source mode, the fallback is `python aecf_prompts/scripts/bootstrap_prompt_only_bundle.py --sync-instructions`.

---

## 2. GitHub Copilot (VS Code)

### 2.1 Copilot Instructions (`.github/copilot-instructions.md`)

Copilot automatically loads `.github/copilot-instructions.md` in every chat. To inject AECF instructions:

1. Create or edit `.github/copilot-instructions.md` at the project root.
2. Add a single loading line:

```markdown
Before responding, load and follow the instructions in `aecf_forced_instructions.md`.
```

### 2.2 Prompt files (`.github/copilot-instructions.md` + `.prompt.md`)

For specific skills, you can also create a `.prompt.md` per task:

```markdown
---
mode: agent
description: "Run AECF new_feature skill"
---

Run the `new_feature` skill following the AECF methodology.
Read `aecf_prompts/skills/skill_new_feature.md` for the phase flow.
Apply each prompt from `aecf_prompts/prompts/` in order.
```

---

## 3. Claude (Anthropic)

### 3.1 CLAUDE.md (default context)

Claude Code and Claude in terminal automatically load `CLAUDE.md` from the project root. Create or edit `CLAUDE.md`:

```markdown
Before responding, load and follow the instructions in `aecf_forced_instructions.md`.
```

### 3.2 Claude Projects (system prompt)

In Claude Projects (web UI), paste the content of `aecf_prompts/AECF_METHODOLOGY.md` as the project **system prompt**.

Optionally, upload as knowledge files:
- `aecf_prompts/AECF_METHODOLOGY.md`
- `aecf_prompts/scoring/SCORING_MODEL.md`
- The skill most used by the team (e.g., `aecf_prompts/skills/skill_new_feature.md`)

### 3.3 Claude API (system message)

For integrations with the Claude API, inject the methodology as a `system` message:

```python
response = client.messages.create(
    model="<configured-model>",
    system="Read and apply the AECF methodology. " + methodology_content,
    messages=[{"role": "user", "content": prompt_content}]
)
```

---

## 4. OpenAI Codex / ChatGPT

### 4.1 AGENTS.md (Codex CLI)

Codex CLI loads `AGENTS.md` or `.codex/instructions.md` as default context. Create at the project root:

```markdown
Before responding, load and follow the instructions in `aecf_forced_instructions.md`.
```

### 4.2 Custom GPTs (system instructions)

For OpenAI Custom GPTs, upload as knowledge files:
- `aecf_prompts/AECF_METHODOLOGY.md`
- `aecf_prompts/scoring/SCORING_MODEL.md`
- `aecf_prompts/skills/` (the skills the team uses)

And define the system instructions with AECF rules.

### 4.3 OpenAI API (system message)

```python
response = openai.chat.completions.create(
    model="<configured-model>",
    messages=[
        {"role": "system", "content": "Apply the AECF methodology. " + methodology_content},
        {"role": "user", "content": prompt_content}
    ]
)
```

---

## 5. Other LLMs (Gemini, Mistral, Llama, etc.)

### Generic pattern

1. **If the LLM supports system instructions**: inject `aecf_prompts/AECF_METHODOLOGY.md` as system prompt.
2. **If the LLM supports file loading**: upload the `aecf_prompts/` folder or key files as context.
3. **If the LLM is chat-only**: paste the skill and phase prompt content manually at the start of each conversation (see `guides/QUICK_START.md`).
4. **If the tool exposes the active model**: use that information only to adjust style, limits, or capabilities; never to make the AECF contract depend on a fixed model ID.

---

## 6. Instruction Files Summary by LLM

| LLM / Tool | Instruction file | Location |
|---|---|---|
| GitHub Copilot (VS Code) | `.github/copilot-instructions.md` | Project root |
| Claude Code / Terminal | `CLAUDE.md` | Project root |
| Claude Projects | System prompt (web UI) | Project settings |
| OpenAI Codex CLI | `AGENTS.md` or `.codex/instructions.md` | Project root |
| Custom GPTs | System instructions + knowledge files | GPT configuration |
| API (any) | System message | In integration code |

---

## 7. Agent CLI Installation

Before configuring AECF instructions for a CLI host, the corresponding tool must be installed. Below are the standard installation commands via npm (Node.js 18+ required).

### 7.1 Claude Code (Anthropic)

```bash
npm install -g @anthropic-ai/claude-code
```

After installation, run `claude` at the project root to start an interactive session.

### 7.2 Codex CLI (OpenAI)

```bash
npm install -g @openai/codex
```

Alternative on macOS: `brew install --cask codex`. After installation, run `codex` at the project root.

### 7.3 GitHub Copilot CLI

Copilot CLI is installed as a GitHub CLI (`gh`) extension:

```bash
# 1. Install GitHub CLI (if not already installed)
# Windows (winget):
winget install --id GitHub.cli
# macOS (brew):
brew install gh

# 2. Install the Copilot extension
gh extension install github/gh-copilot
```

After installation, use `gh copilot` to interact with Copilot from the terminal.

> **Note**: All three CLIs require authentication with their respective providers before first use. Refer to each tool's official documentation to complete the authentication flow.
