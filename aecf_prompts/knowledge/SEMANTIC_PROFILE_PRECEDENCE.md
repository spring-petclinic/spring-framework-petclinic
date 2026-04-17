# Semantic Profile Precedence

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

This document defines normative precedence, compatibility, and fallback rules for semantic profile composition.

## Goals

- keep composition deterministic,
- avoid contradictory guidance,
- prevent prompt inflation,
- preserve graceful degradation.

## Precedence Table

| Class | Typical `profile_type` | Precedence | Default load rule |
| --- | --- | ---: | --- |
| Cross-cutting security | `security` | 120 | Load when `always_include` or strong evidence applies |
| Base language | `language` | 100 | Load when explicit or strongly detected |
| Primary framework | `framework` | 90 | Load when explicit or strongly detected |
| Explicit architecture | `architecture` | 80 | Load when explicit or backed by strong evidence |
| Explicit library or database | `library`, `database` | 70 | Load when explicit or backed by strong evidence |
| Explicit tooling | `tool` | 65 | Load when explicit or backed by strong evidence |
| Indirect activation with evidence | any | 60 | Load only if graph activation is confirmed by runtime evidence |
| Indirect activation without evidence | any | 0 | Do not load; keep only as candidate for logging |
| Deprecated profile | any | 0 | Do not load |

## Compatibility Matrix

| `profile_type` | Normally compatible with | Typical conflict | Resolution rule |
| --- | --- | --- | --- |
| `language` | `framework`, `library`, `database`, `security`, `tool`, `architecture` | Multiple incompatible primary languages | Keep explicit node; otherwise prefer strongest evidence |
| `framework` | `language`, `library`, `database`, `security`, `tool`, `architecture` | Competing primary frameworks | Keep explicit node; otherwise highest score wins |
| `library` | `language`, `framework`, `database`, `security`, `tool`, `architecture` | Competing alternative libraries | Respect `conflicts_with`; otherwise keep explicit node |
| `database` | `language`, `framework`, `library`, `security`, `tool`, `architecture` | Multiple primary databases without evidence | Keep explicit node; otherwise highest score wins |
| `architecture` | all types | Contradictory architecture guidance | Explicit node wins over inferred node |
| `security` | all types | Rare; only explicit profile conflict | Merge by default unless `conflicts_with` says otherwise |
| `tool` | most types | Alternative tools for the same role | Respect `conflicts_with` and explicit node priority |

## Deterministic Composition Flow

1. Resolve explicit stack nodes from the requested stack string.
2. Resolve detected nodes from runtime evidence only when they exceed the strong-evidence threshold.
3. Expand graph activations.
4. Filter indirectly activated nodes that lack confirming evidence.
5. Remove deprecated or invalid profiles.
6. Order remaining profiles by descending precedence.
7. Apply `conflicts_with` rules.
8. Load the valid ordered profile set.
9. Emit warnings for anything skipped.
10. Continue execution regardless of warnings.

## Strong-Evidence Rule

Strong evidence means one or more of the following:

- explicit `stack=` request,
- resolved stack node from deterministic repo intelligence,
- matching manifest or dependency declaration,
- matching framework-specific file or path evidence,
- matching runtime stack artifact already persisted by AECF.

Weak hints from prompt wording alone are not enough to activate indirect profiles.

## Prompt Budget Rule

When prompt budget is constrained:

1. Keep the base language profile.
2. Keep the explicit framework profile.
3. Keep the explicit library or database profiles.
4. Keep cross-cutting security if already selected.
5. Drop indirectly activated candidates first.
6. Never block execution because a profile was dropped.

## Logging Expectations

The component log should capture:

- requested stack,
- explicit nodes,
- detected nodes,
- indirectly activated candidates,
- loaded profile order,
- skipped profiles with reasons,
- final summary of warnings.

## Worked Example

For `stack=python-flask-sqlalchemy-postgresql`:

- explicit nodes: `python`, `flask`, `sqlalchemy`, `postgresql`
- always include candidate: `security`
- indirect graph candidates from `flask`: `redis`, `celery`, `microservices`, `observability`, `clean-architecture`
- recommended loaded set without extra evidence: `python`, `flask`, `sqlalchemy`, `postgresql`, `security`
- recommended skipped set without extra evidence: `redis`, `celery`, `microservices`, `observability`, `clean-architecture`

This keeps guidance aligned with the requested stack while avoiding accidental prompt inflation and false assumptions.
