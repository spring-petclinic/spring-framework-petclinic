# AECF Prompts

LAST_REVIEW: 2026-04-16
OWNER SEACHAD

---

`aecf_prompts/` is the prompt-only version of AECF for working inside the client repository without installing the automated component. The bundle provides methodology, skills, prompts, templates, checklists, and scoring so teams can run manual workflows with the LLM host they already use.

Inside this repository, `aecf_prompts/` is also the full source surface for prompt-only prompts, skills, and support assets. The client bundle does not have to ship that full surface: the bundle task filters distributable skills according to `aecf_prompts/skills/SKILL_RELEASE.json`, the client policy file `aecf_prompts_release_data/<client>.json`, and the selected `bundle-mode`. In `release`, the bundle ships only the client-authorized `released` skills and only the allowed knowledge domains; in `god`, it ships the full published bundle surface.

This README should be read as a quick deployment guide for end users: what to copy, what to prepare in the repository, and how to start the first workflow.

The Spanish equivalent is available in `README.md`.

If you want to extend a base skill with project-specific criteria or knowledge without putting anything into the AECF base, use the guide [guides/AECF_EXTERNAL_SKILLS.md](guides/AECF_EXTERNAL_SKILLS.md).

For quick access, open [../index.html](../index.html). That repo-root landing page links to [../guias/SKILL_CATALOG.html](../guias/SKILL_CATALOG.html) for skills, [../guias/AECF_COMMANDS.html](../guias/AECF_COMMANDS.html) for prompt-only commands, and [../guias/GUIDE_VIEWER.html?doc=START_HERE.md](../guias/GUIDE_VIEWER.html?doc=START_HERE.md) for the rest of the markdown guides without exposing downloadable repo links in the published surface. The interactive guides still read their canonical `.md` files from `aecf_prompts/guides/`, so any markdown change is reflected automatically without rebuilding the published HTML.

In a target workspace with the prompt-only MCP enabled, the `aecf_show_guide` tool can serve guides in the effective `output_language`. If no human-maintained localized copy exists for that language, the host LLM must render a derived translation while preserving paths, commands, AECF ids, and code fences.

That landing page and the skill catalog now also expose deterministic version stamps sourced from [guides/AECF_ASSET_VERSIONS.md](guides/AECF_ASSET_VERSIONS.md) and `AECF_ASSET_VERSIONS.json`. Each stamp is derived from the canonical markdown content, so any skill or prompt edit changes the published value on the next sync.

## What it is

With `aecf_prompts/`, work is organized into predefined phases. The LLM does not decide the process on the fly: each skill defines which steps to follow, and each phase prompt tells the model which context to read, which output to generate, and where to save it.

In code-generation flows, blocking static analysis can now be gated in a dedicated `AUDIT_STATIC_ANALYSIS` phase before the code/tests audit.

Typical use cases:

1. Design and implement a new feature.
2. Audit security or coding standards.
3. Document an existing system or explain how code works when the team does not know it well.
4. Work manually with Claude, Copilot, Codex, or another compatible host.

## What you need before starting

You need these three pieces:

1. A client repository where `aecf_prompts/` will be copied.
2. An LLM host that is already installed and authenticated.

Common hosts:

1. GitHub Copilot in VS Code.
2. GitHub Copilot CLI.
3. Claude Code / Claude CLI.
4. Codex CLI.
5. A web chat with file upload support or, if that is not available, manual copy-paste of the required files.

## Install the host your team will use

Choose one of these paths before starting with `aecf_prompts`.

### GitHub Copilot in VS Code

If the team is going to work inside VS Code, this is the most direct path.

- Installation: GitHub indicates that in VS Code the required extension is installed automatically during the initial setup.
- Official reference: [Installing the GitHub Copilot extension in your environment](https://docs.github.com/en/copilot/how-tos/set-up/installing-the-github-copilot-extension-in-your-environment)
- VS Code guide: [Set up Copilot in VS Code](https://code.visualstudio.com/docs/copilot/setup)

### GitHub Copilot CLI

If the team wants to work in the terminal with Copilot, the official documentation recommends these options:

```powershell
npm install -g @github/copilot
```

On Windows there is also a WinGet path:

```powershell
winget install GitHub.Copilot
```

Then start it with:

```powershell
copilot
```

And authenticate with `/login` when prompted.

- Official installation: [Installing GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli)
- Usage and configuration: [Using GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)

### Claude Code / Claude CLI

Install it like this:

```powershell
npm install -g @anthropic-ai/claude-code
```

Then start it with:

```powershell
claude
```

And follow the browser login flow when requested.

- Official setup: [Claude Code setup](https://code.claude.com/docs/en/setup)
- Official quickstart: [Claude Code quickstart](https://code.claude.com/docs/en/quickstart)
- Authentication: [Claude Code authentication](https://code.claude.com/docs/en/authentication)

Windows note: Claude Code requires Git for Windows or WSL. Anthropic documents this in the same setup guide.

### Codex CLI

For Codex CLI, OpenAI publishes this quick start:

```powershell
npm install -g @openai/codex
```

Then start it with:

```powershell
codex
```

You can authenticate with your ChatGPT account at startup or configure API-key access according to the official documentation.

- Official repository and quickstart: [openai/codex](https://github.com/openai/codex)
- Official documentation: [Codex documentation](https://developers.openai.com/codex)
- Authentication: [Codex auth](https://developers.openai.com/codex/auth)

## Minimal deployment in the client repository

### 1. Copy the bundle into the project

Expected minimal structure:

```text
my-project/
├── aecf_prompts/
├── src/
└── ...
```

### 2. Identify who is performing the work

Before starting a real workflow, define the identifier AECF will use to know who is executing that topic.

Canonical priority:

1. `AECF_PROMPTS_USER_ID`
2. `AECF_PROMPTS_MODEL_ID` or `MODEL_ID`
3. `AECF_PROMPTS_AGENT_ID` or `AGENT_ID`

Example in Windows PowerShell:

```powershell
setx AECF_PROMPTS_USER_ID "ana.garcia@empresa.com"
```

Then open a new console.

If you want to check exactly what the bundle can see without relying on the chat host, run:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --diagnose-env
```

For `@aecf init` in hosts with tools, this is also the recommended route: the host must use the `--diagnose-env` output instead of trying to read variables with system shell commands.

### 3. Generate or refresh the default instructions

From the client repository root:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --sync-instructions
```

If you are working on a source copy instead of the bundle delivered to the client, you can use the equivalent `.py` script.

That command creates or updates:

At the client repository root, not inside `aecf_prompts/`:

1. `aecf_forced_instructions.md`
2. `.github/copilot-instructions.md`
3. `copilot-instructions.md`
4. `CLAUDE.md`
5. `AGENTS.md`
6. `.codex/instructions.md`

If any of those folders or files does not exist yet, the bootstrap creates them automatically.

The load line is not inserted as loose text: AECF leaves it inside a managed, visible AECF block so it is easy to identify which part of the file is controlled by the bootstrap.

The idea is simple: the host loads one entry line and from there AECF injects its canonical instruction block.

### 3.b Install the bundled MCP for the packaged host

The bundle delivered to the client includes one host-specific MCP at a time. The builder packages `claude` by default, but it can also package `copilot` or `codex`.

The path depends on the host selected when the bundle was built:

```text
aecf_prompts/mcp/claude/aecf-mcp.exe
aecf_prompts/mcp/copilot/aecf-mcp.exe
aecf_prompts/mcp/codex/aecf-mcp.exe
```

It also includes local quick-start guides at:

```text
aecf_prompts/QUICK_START_ES.md
aecf_prompts/QUICK_START_EN.md
```

Those guides are delivered at the bundle root, next to `README.md` and `README_EN.md`, so they stay visible without entering the selected `mcp/<host>/` folder.

The exact registration depends on the packaged host:

- `claude`: use `QUICK_START_ES.md` to register `aecf_prompts\mcp\claude\aecf-mcp.exe` in `.mcp.json`.
- `copilot`: use the same guide to register `aecf_prompts\mcp\copilot\aecf-mcp.exe` in `.vscode/mcp.json`.
- `codex`: use the same guide to register `aecf_prompts\mcp\codex\aecf-mcp.exe` in the Codex MCP configuration surface.

Minimal example for Claude in `.mcp.json`:

```json
{
	"mcpServers": {
		"aecf": {
			"type": "stdio",
			"command": "C:\\path\\to\\your\\project\\aecf_prompts\\mcp\\claude\\aecf-mcp.exe",
			"args": [],
			"env": {
				"AECF_WORKSPACE": "C:\\path\\to\\your\\project"
			}
		}
	}
}
```

The executable path lives inside the bundle so MCP installation stays decoupled from the host and the builder can choose which variant to publish.

In the normal flow you should not run the packaged `aecf-mcp.exe` manually in a separate terminal. The selected MCP host should start it directly from its own configuration.

When the host has this MCP registered, `@aecf` commands that have an equivalent tool should resolve through MCP first and only fall back to the manual `aecf_prompts` router if the tool does not exist, is disconnected, or fails. Examples: `@aecf list commands` should go through `aecf_list_commands` and `@aecf show commands` through `aecf_show_commands`, not through a textual repository search.

### 4. Prepare the minimum project context

You must have this file:

```text
.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md
```

If it does not exist yet, create a first minimal version or follow the guide [guides/AECF_PROJECT_CONTEXT_BOOTSTRAP.md](guides/AECF_PROJECT_CONTEXT_BOOTSTRAP.md).

### 5. Initialize each real topic before the first phase

When you are about to execute real work, freeze the execution context for the topic:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --topic user_auth --prompt-text "Implement JWT authentication with refresh tokens"
```

If you are working on a source copy instead of the bundle delivered to the client, you can use the equivalent `.py` script.

That step creates the topic run context and fixes:

1. `user_id`
2. `RUN_DATE`
3. `output_language`
4. The effective path where artifacts will be written

If the work will depend on repository context, it is best to ensure two additional layers first:

1. `aecf_project_context_generator` to refresh `AECF_PROJECT_CONTEXT.md`;
2. `aecf_codebase_intelligence` to materialize `.aecf/context/*`.

In the prompt-only bundle, those `.aecf/context/*` artifacts should not be copied wholesale into every phase by default. They are reused to derive context filtered by `TOPIC` and, for search-first skills, to freeze a `WORKING_CONTEXT` scoped to that execution.

By default, outputs live in:

```text
<workspace>/.aecf/runtime/documentation
```

Full canonical artifact pattern per phase:

```text
.aecf/runtime/documentation/<user_id>/<TOPIC>/<NN>_<skill_name>_<ARTEFACT_NAME>.md
```

If you need another location, use `AECF_PROMPTS_DOCUMENTATION_PATH`. If a legacy environment already uses `AECF_PROMPTS_DIRECTORY_PATH`, the bundle also accepts it as a legacy alias.

## How the bundle works

Normal usage is this:

1. Choose a skill in `aecf_prompts/skills/`.
2. Read its phase flow.
3. Paste the skill invocation into the host.
4. Then paste the corresponding phase prompt from `aecf_prompts/prompts/`.
5. Save the output to the indicated path.
6. Move forward or enter a fix loop according to the GO or NO-GO verdict.

Base invocation:

```text
use skill=<skill_name> TOPIC=<topic> prompt=<work description>
```

Example:

```text
use skill=new_feature TOPIC=user_auth prompt=Implement JWT authentication with refresh tokens
```

## Recommended first workflow

If this is the first time the team uses the bundle, the practical order is this:

1. Read [guides/QUICK_START.md](guides/QUICK_START.md).
2. Choose an initial skill, usually `new_feature`, `refactor`, or `hotfix`.
3. Open `skills/skill_<skill>.md` to see the flow.
4. Execute the first phase with `prompts/00_PLAN.md`.
5. Continue with the remaining phases one by one until VERSION is closed.

## Which host to use and where to look

### Use with GitHub Copilot in VS Code

Use the client repo in VS Code and run `--sync-instructions` so loading through `.github/copilot-instructions.md` is ready.

If the bundle was generated with `--mcp-host copilot`, also register `aecf_prompts/mcp/copilot/aecf-mcp.exe` in `.vscode/mcp.json` following `QUICK_START_ES.md`.

Reference: [guides/LLM_INSTRUCTIONS_SETUP.md](guides/LLM_INSTRUCTIONS_SETUP.md)

### Use with Claude Code / Claude CLI

Work from the client repository root with `CLAUDE.md` as the loading surface.

If you want native MCP tools inside Claude Code, also use the executable included in `aecf_prompts/mcp/claude/aecf-mcp.exe` and register the server with `AECF_WORKSPACE` pointing to the project root.

If the executable is launched from the bundled path inside the project root, it can also infer the workspace by itself, but `AECF_WORKSPACE` remains the recommended configuration for Claude Code.

Reference: [guides/AECF_PROMPTS_CLAUDE_CLI.md](guides/AECF_PROMPTS_CLAUDE_CLI.md)

### Use with Codex CLI

Work from the client repository root with `AGENTS.md` or `.codex/instructions.md`.

If the bundle was generated with `--mcp-host codex`, also register `aecf_prompts/mcp/codex/aecf-mcp.exe` in the Codex MCP configuration following `QUICK_START_ES.md`.

Reference: [guides/AECF_PROMPTS_CODEX_CLI.md](guides/AECF_PROMPTS_CODEX_CLI.md)

### Web chat without local integration

You can also use the bundle manually: paste the skill, the phase prompt, and, if the host cannot read files from the repo, also paste the required files.

Reference: [guides/QUICK_START.md](guides/QUICK_START.md)

## Key bundle files

1. `AECF_METHODOLOGY.md` / `AECF_METHODOLOGY_EN.md`: global methodology rules in Spanish and English.
2. `skills/`: available skills and their flow.
3. `prompts/`: phase prompts.
4. `templates/`: expected output structure.
5. `checklists/`: review criteria per phase.
6. `scoring/SCORING_MODEL.md`: thresholds and scoring.
7. `knowledge/`: knowledge packs and semantic profiles when the flow needs them.
8. `documentation/`: output generated by each execution.
9. `QUICK_START_ES.md` / `QUICK_START_EN.md`: quick start for the packaged host MCP, copied at the bundle root next to `README.md` and `README_EN.md`.

## Recommended reading path

1. [guides/START_HERE.md](guides/START_HERE.md)
2. [guides/AECF_GUIDES_MASTER.md](guides/AECF_GUIDES_MASTER.md)
3. [guides/QUICK_START.md](guides/QUICK_START.md)
4. [guides/AECF_PROJECT_CONTEXT_BOOTSTRAP.md](guides/AECF_PROJECT_CONTEXT_BOOTSTRAP.md)
5. [skills/README_SKILLS.md](skills/README_SKILLS.md)
6. [guides/AECF_APPLICATION_LIFECYCLE_GUIDE.md](guides/AECF_APPLICATION_LIFECYCLE_GUIDE.md)
7. [AECF_METHODOLOGY.md](AECF_METHODOLOGY.md)
8. [AECF_METHODOLOGY_EN.md](AECF_METHODOLOGY_EN.md)
9. [guides/AECF_EXTERNAL_SKILLS.md](guides/AECF_EXTERNAL_SKILLS.md)

## Authorship

> **Methodology author:** Fernando Garcia Varela (youngluke)
> **Framework:** AECF (AI Engineering Compliance Framework)

