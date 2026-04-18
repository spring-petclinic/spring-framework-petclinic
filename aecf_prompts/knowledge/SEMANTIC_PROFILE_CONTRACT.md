# Semantic Profile Contract

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

This document defines the canonical file contract for AECF semantic profiles.

## Purpose

Semantic profiles are deterministic, local-first knowledge assets that refine prompt guidance for a resolved stack.

They are not executable skills.

They must never block a run. If a profile is missing, malformed, deprecated, or incompatible, AECF must emit a warning and continue.

## Scope

Semantic profiles are intended to:

- refine language, framework, library, database, architecture, security, or tool guidance,
- remain stable across projects and companies,
- avoid project-specific assumptions,
- stay concise enough to embed safely into prompts.

Semantic profiles must not:

- contain customer code,
- contain examples copied from a target repository,
- override AECF governance, phase gates, or testing enforcement,
- require network access at runtime.

## Canonical Path Convention

- Base pack: `domains/<domain>/pack.md`
- Semantic profile: `domains/<domain>/semantic_profiles/<profile_id>.md`
- Cross-cutting profile: `domains/security/semantic_profiles/<profile_id>.md`
- Optional composed profile: `domains/<domain>/semantic_profiles/composed/<profile_id>.md`

## Required File Structure

Each semantic profile file must contain:

1. YAML frontmatter with the required metadata keys.
2. A `LAST_REVIEW` line in the body for export metadata compatibility.
3. The eight required Markdown sections in the exact order defined below.

## Required Metadata

The frontmatter must define at least these keys:

- `profile_id`: stable unique identifier.
- `title`: human-readable title.
- `version`: editorial version for the profile.
- `status`: `active`, `beta`, or `deprecated`.
- `owner`: owner of the profile, normally `AECF`.
- `last_review`: ISO date.
- `profile_type`: `language`, `framework`, `library`, `database`, `architecture`, `security`, or `tool`.
- `stack_nodes`: stack graph nodes to which the profile applies.
- `requires`: prerequisite nodes.
- `precedence`: integer used for prompt composition ordering.
- `fallback_mode`: currently `warn_continue`.
- `compatibility`: explicit compatibility list.
- `conflicts_with`: explicit incompatibility list.
- `activation_mode`: `explicit_only`, `detected_only`, `explicit_or_detected`, or `always_include`.
- `max_lines_per_section`: editorial size cap.

Optional keys:

- `evidence_hint`
- `tags`
- `notes`

## Required Sections

Each file must contain these sections in this exact order:

1. `## STACK`
2. `## ARCHITECTURE RULES`
3. `## DESIGN PATTERNS`
4. `## CODING RULES`
5. `## SECURITY RULES`
6. `## TESTING RULES`
7. `## COMMON MISTAKES`
8. `## AECF AUDIT CHECKS`

## Canonical Template

```md
---
profile_id: example_profile
title: Example Profile
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: framework
stack_nodes:
  - example-node
requires:
  - example-language
precedence: 90
fallback_mode: warn_continue
compatibility:
  - example-language
conflicts_with: []
activation_mode: explicit_or_detected
max_lines_per_section: 6
---

# Example Profile

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK
Short deterministic stack description.

## ARCHITECTURE RULES
- Rule 1
- Rule 2

## DESIGN PATTERNS
- Pattern 1
- Pattern 2

## CODING RULES
- Rule 1
- Rule 2

## SECURITY RULES
- Rule 1
- Rule 2

## TESTING RULES
- Rule 1
- Rule 2

## COMMON MISTAKES
- Mistake 1
- Mistake 2

## AECF AUDIT CHECKS
- Check 1
- Check 2
```

## Validation Rules

Validation is deterministic and non-blocking.

- Missing file: warning and continue.
- Missing mandatory metadata: warning and skip profile.
- Missing required section: warning and skip profile.
- Invalid section order: warning and skip profile.
- `status=deprecated`: warning and skip profile.
- `precedence <= 0`: warning and skip profile.
- Oversized section: warning and either editorial truncation or skip, but never hard fail.

## Logging Contract

The component log should surface, at minimum:

- semantic profiles enabled or disabled,
- requested stack,
- explicit nodes,
- detected nodes,
- loaded profiles,
- skipped profiles,
- warning reason for each skipped profile,
- completion summary.

## Fallback Contract

Semantic profiles are enrichment only.

If profile resolution fails for any reason, AECF must fall back to the base domain pack and any remaining valid profiles. The run continues with warnings recorded in the component log.
