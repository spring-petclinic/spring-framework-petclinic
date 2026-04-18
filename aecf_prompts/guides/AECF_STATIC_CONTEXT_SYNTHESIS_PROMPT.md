# AECF Static Context Synthesis Prompt

LAST_REVIEW: 2026-03-24
OWNER SEACHAD

---

## Purpose

This prompt transforms `AECF_STATIC_PROJECT_CONTEXT` into a dense, low-token artifact named `AECF_SYNTHETIC_STATIC_PROJECT_CONTEXT`.

Goal:

- reduce token consumption as much as possible
- preserve all operational information
- preserve all non-negotiable constraints
- remove only repetition, filler prose, and redundant examples

Use this when the source static context is already stable and the main need is session token efficiency.

---

## Expected Output Contract

The model must output a single Markdown artifact with this exact title:

```markdown
# AECF_SYNTHETIC_STATIC_PROJECT_CONTEXT
```

The artifact must be lossless in meaning, deterministic, and optimized for future prompt injection.

Compression rules:

- keep every unique fact, constraint, path, variable, command, module, flag, port, prefix, phase, and document reference
- merge duplicate or equivalent statements into one canonical rule
- convert long prose into dense canonical bullets
- prefer short declarative statements over narrative paragraphs
- keep examples only when they contain unique project facts that would otherwise be lost
- if two statements partially overlap, keep the more restrictive one and append the missing detail
- if something is uncertain in the source, preserve it explicitly as `UNRESOLVED`, never drop it

Forbidden:

- omitting information because it looks minor
- replacing specific paths, commands, variables, or class names with generic wording
- reinterpreting rules into weaker language
- adding new assumptions not present in the source
- generating an executive summary instead of a compressed operational artifact

---

## Prompt

Paste the complete source `AECF_STATIC_PROJECT_CONTEXT` after this prompt.

```text
You are compressing a project static context for AECF.

TASK
Transform the provided `AECF_STATIC_PROJECT_CONTEXT` into a new artifact named `AECF_SYNTHETIC_STATIC_PROJECT_CONTEXT`.

PRIMARY GOAL
Minimize token cost for future sessions without losing operational information, constraints, or project memory references.

NON-NEGOTIABLE RULES
1. Preserve all unique facts.
2. Preserve all mandatory rules, prohibitions, defaults, precedence chains, naming conventions, security constraints, testing obligations, and architecture constraints.
3. Preserve all exact identifiers when present:
   - file paths
   - folder paths
   - environment variables
   - config variables
   - commands
   - ports
   - flags
   - prefixes
   - class names
   - function names
   - module names
   - document ids
4. Preserve all `PROJECT MEMORY` references with their ids, paths, descriptions, and inject phase information.
5. Remove only duplication, explanatory filler, decorative prose, and repeated rationale.
6. Never generalize away project-specific facts.
7. If the source contains ambiguity or pending items, keep them explicitly as `UNRESOLVED`.
8. Do not invent any missing data.
9. Output only the final artifact.

COMPRESSION STRATEGY
Apply these transformations in order:

1. CANONICALIZE
- Normalize repeated statements into one canonical form.
- Prefer the most restrictive or most explicit formulation.

2. DEDUPLICATE
- Merge repeated rules that appear in multiple sections.
- Keep one copy only, but do not lose section-specific detail.

3. STRUCTURE
- Convert narrative prose into compact bullets.
- Use dense labels instead of paragraphs.
- Keep sections stable and deterministic.

4. PRESERVE OPERABILITY
- Keep the artifact usable as direct injected context in later prompts.
- Keep constraints clearer than summaries.

OUTPUT FORMAT
Return exactly one Markdown document with this structure:

# AECF_SYNTHETIC_STATIC_PROJECT_CONTEXT

LAST_REVIEW: <copy or infer from source if explicitly present>
SOURCE_ARTIFACT: AECF_STATIC_PROJECT_CONTEXT
COMPRESSION_MODE: LOSSLESS_SYNTHETIC

## CORE_DIRECTIVES
- Dense canonical rules only.

## ARCHITECTURE_AND_STACK
- Stack, entry points, key modules, architecture rules, configuration precedence.

## IMPLEMENTATION_CONSTRAINTS
- Coding rules, naming conventions, traceability, logging, environment variable rules, forbidden changes.

## SECURITY_CONSTRAINTS
- Input validation, secret handling, SQL rules, session/auth constraints, concurrency or locking constraints.

## TESTING_AND_VALIDATION
- Required tests, execution commands, coverage expectations, non-regression requirements.

## OPERATING_MODEL
- Phase model, output locations, artifact rules, documentation rules, versioning or governance rules.

## PROJECT_MEMORY_INDEX
- Keep each referenced memory document in compact form:
  - `id | path | why_it_matters | inject_phases`

## LOSSLESS_CHECK
- List only information that was compressed by deduplication pattern, not removed.
- If nothing notable, write `NONE`.

STYLE RULES
- Use compact Markdown bullets.
- Prefer one-line bullets.
- No marketing language.
- No long introductions.
- No conclusions.
- No recommendations.
- No examples unless they contain unique project facts.
- Keep the language of the source facts when needed, but prefer short control labels in English.

LOSSLESS VALIDATION
Before finalizing, verify mentally that the synthetic artifact still contains:
- every hard constraint
- every exact path and variable that matters operationally
- every precedence rule
- every architecture prohibition
- every testing obligation
- every project memory reference

If any of those are missing, fix the output before returning it.
```

---

## Minimal Usage

1. Open the current `AECF_STATIC_PROJECT_CONTEXT`.
2. Paste the prompt above into the LLM.
3. Paste the full static context below it.
4. Save the result as `AECF_SYNTHETIC_STATIC_PROJECT_CONTEXT.md`.

---

## Design Notes

This prompt is intentionally not wired to an AECF phase or chat command yet.
It is a standalone compression asset for manual or prompt-only workflows.
