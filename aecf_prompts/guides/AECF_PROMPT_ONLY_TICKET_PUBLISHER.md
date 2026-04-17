# AECF Prompt-Only Ticket Publisher

LAST_REVIEW: 2026-04-08
OWNER SEACHAD

This guide defines the host-agnostic contract for automatic `@aecf send issue` and `@aecf send feature` flows in prompt-only bundles.

## 1. Goal

Use `aecf_prompts/scripts/publish_github_ticket.py` as the single automation surface for GitHub issue publication across CLI hosts such as Claude CLI, Codex CLI, Copilot CLI, or any other tool that can launch a local command.

The host should do exactly two things:

1. Resolve the user request into a canonical ticket payload.
2. Execute the helper and consume the JSON result.

## 2. Preferred Invocation Order

### Option A: direct args wrapper

Use this when the host can pass arguments and optionally pipe stdin.

```bash
python aecf_prompts/scripts/publish_github_ticket.py create-from-args \
  --kind issue \
  --title "Bug: @aecf continue loses state" \
  --body-file - \
  --label Bug
```

Then write the full body to stdin.

### Option B: JSON payload

Use this when the host already works well with structured JSON.

```bash
python aecf_prompts/scripts/publish_github_ticket.py create --payload-file ticket.json
```

Or pipe the payload through stdin:

```bash
cat ticket.json | python aecf_prompts/scripts/publish_github_ticket.py create --payload-file -
```

## 3. Canonical Payload

```json
{
  "kind": "issue",
  "title": "Bug: @aecf continue loses state",
  "body": "User-visible summary, impact, repro notes, topic, skill, and any relevant context.",
  "labels": ["Bug"],
  "owner": "Seachad-TEAM",
  "repo": "AECF_MCP_issues"
}
```

Rules:

1. `kind` must be `issue` or `feature`.
2. `title` is required.
3. `body` is required.
4. `labels` is optional; defaults are `Bug` for `issue` and `feature` for `feature`.
5. `owner` and `repo` are optional; defaults point to `Seachad-TEAM/AECF_MCP_issues`.

## 4. Output Contract

The helper always writes JSON to stdout.

### Created automatically

```json
{
  "ok": true,
  "status": "created",
  "issue_number": 42,
  "issue_url": "https://github.com/Seachad-TEAM/AECF_MCP_issues/issues/42"
}
```

### Manual publish fallback

```json
{
  "ok": false,
  "status": "manual_publish_required",
  "compose_url": "https://github.com/.../issues/new?..."
}
```

Interpretation rules:

1. If `status=created`, report success with the returned number and URL.
2. If `status=manual_publish_required`, do not treat it as a hard failure; show the `compose_url`.
3. The helper keeps exit code `0` for this manual fallback so multi-CLI wrappers can still consume stdout as a valid machine result.

## 5. Credential Resolution

The helper uses this priority:

1. explicit `--token`
2. `AECF_PROMPTS_GITHUB_TOKEN`
3. `AECF_GITHUB_TOKEN`
4. `GITHUB_TOKEN`
5. `GH_TOKEN`
6. `gh auth token` when `gh` is installed

Target repository override:

1. explicit `--owner` / `--repo`
2. payload `owner` / `repo`
3. `AECF_PROMPTS_GITHUB_ISSUES_OWNER` / `AECF_PROMPTS_GITHUB_ISSUES_REPOSITORY`
4. defaults: `Seachad-TEAM/AECF_MCP_issues`

## 6. Host Recipes

### Claude CLI style

1. Build the title in-process.
2. Pipe the body by stdin.
3. Parse stdout JSON.

```bash
printf '%s' "$BODY" | python aecf_prompts/scripts/publish_github_ticket.py create-from-args \
  --kind feature \
  --title "$TITLE" \
  --body-file - \
  --label feature
```

### Codex CLI style

Prefer the same wrapper mode because it avoids a temporary file.

### Copilot or generic tool runner

If the host handles JSON files more reliably than stdin, use `create --payload-file`.

## 7. Recommended LLM Behavior

When the user asks for `@aecf send issue` or `@aecf send feature`:

1. derive `kind`, `title`, and `body`,
2. choose `create-from-args` when stdin/tool piping is available,
3. otherwise choose `create --payload-file`,
4. only fall back to manual instructions when the host truly cannot run local commands.

## 8. Ready-To-Paste Host Blocks

### `CLAUDE.md`

```markdown
## AECF prompt-only ticket publishing

When the user asks for `@aecf send issue` or `@aecf send feature`, resolve the request into:

1. `kind`: `issue` or `feature`
2. `title`: short GitHub title
3. `body`: complete ticket body

Preferred execution:

~~~bash
printf '%s' "$BODY" | python aecf_prompts/scripts/publish_github_ticket.py create-from-args \
  --kind "$KIND" \
  --title "$TITLE" \
  --body-file - \
  --label "$LABEL"
~~~

Use `Bug` as the default label for `issue` and `feature` as the default label for `feature`.

Interpret stdout JSON as follows:

1. if `status=created`, report the created issue number and URL,
2. if `status=manual_publish_required`, show the returned `compose_url`,
3. do not treat `manual_publish_required` as a hard execution failure.
```

### `AGENTS.md`

```markdown
## AECF Prompt-Only Ticket Publisher

For `@aecf send issue` and `@aecf send feature`:

1. derive `KIND`, `TITLE`, `BODY`, and default `LABEL`,
2. prefer this command:

~~~bash
printf '%s' "$BODY" | python aecf_prompts/scripts/publish_github_ticket.py create-from-args \
  --kind "$KIND" \
  --title "$TITLE" \
  --body-file - \
  --label "$LABEL"
~~~

3. if stdin piping is not practical, use `create --payload-file` with a JSON payload,
4. parse stdout JSON and surface either `issue_url` or `compose_url`.
```

### `.codex/instructions.md`

```markdown
## AECF ticket publishing

If the user invokes `@aecf send issue` or `@aecf send feature`, do not stop at generating text.

Build:

1. `kind`
2. `title`
3. `body`
4. `label`

Then run:

~~~bash
printf '%s' "$BODY" | python aecf_prompts/scripts/publish_github_ticket.py create-from-args \
  --kind "$KIND" \
  --title "$TITLE" \
  --body-file - \
  --label "$LABEL"
~~~

If the command returns `manual_publish_required`, show the `compose_url` instead of failing.
```

## 9. Short Corporate Templates

### Claude CLI

```text
1. Derive KIND, TITLE, BODY.
2. Run `printf '%s' "$BODY" | python aecf_prompts/scripts/publish_github_ticket.py create-from-args --kind "$KIND" --title "$TITLE" --body-file - --label "$LABEL"`.
3. If `status=created`, return `issue_number` and `issue_url`.
4. If `status=manual_publish_required`, return `compose_url`.
```

### Codex CLI

```text
1. Derive KIND, TITLE, BODY.
2. Prefer `create-from-args` with stdin; use `create --payload-file` only if stdin is awkward.
3. Parse stdout JSON.
4. Surface `issue_url` or `compose_url`.
```

### Copilot CLI

```text
1. Build KIND, TITLE, BODY.
2. Execute `python aecf_prompts/scripts/publish_github_ticket.py create-from-args ...`.
3. Treat `manual_publish_required` as a valid fallback.
4. Return the created URL or compose URL.
```

### Generic Host

```text
1. Resolve the ticket to KIND, TITLE, BODY, LABEL.
2. Prefer `create-from-args`; fall back to JSON payload mode if needed.
3. Read stdout JSON.
4. Report `issue_url` or `compose_url`.
```
