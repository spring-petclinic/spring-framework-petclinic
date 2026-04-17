---
profile_id: cobol_batch_mainframe
title: COBOL Batch Mainframe Workloads
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: language
stack_nodes:
  - cobol
requires: []
precedence: 85
fallback_mode: warn_continue
compatibility:
  - cobol
  - ibm-zos
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=batch
  - keyword=jcl
  - keyword=copybook
max_lines_per_section: 6
tags:
  - cobol
  - mainframe
  - batch
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

COBOL batch workloads should be treated as contract-heavy operational systems where copybooks, datasets, schedules, and side effects matter as much as source code.

## ARCHITECTURE RULES

- Preserve job orchestration, dataset conventions, and file interface contracts unless redesign is explicit.
- Treat copybooks as shared contracts and trace their blast radius before changes.
- Prefer adapter or strangler boundaries when exposing batch capabilities to newer services.

## DESIGN PATTERNS

- Stable batch step boundaries with explicit inputs and outputs.
- Wrapper services around legacy programs instead of broad rewrites.
- Contract-first modernization around copybooks and file layouts.

## CODING RULES

- Avoid silent changes to field layouts, truncation behavior, or sorting assumptions.
- Keep I/O and business rules understandable when refactoring sections or paragraphs.
- Document operational dependencies such as datasets, job parameters, and scheduling windows.

## SECURITY RULES

- Review access to datasets, batch credentials, and operational schedulers.
- Treat external file payloads and copied data definitions as trust boundaries.
- Preserve auditability of financial and compliance-sensitive batch effects.

## TESTING RULES

- Add regression evidence around copybook compatibility and key output records.
- Cover happy path, bad-input handling, and one operational edge case such as empty feeds or duplicate records.
- Include one non-regression assertion on downstream batch side effects or generated outputs.

## COMMON MISTAKES

- Rewriting stable legacy seams instead of wrapping them.
- Underestimating copybook blast radius.
- Treating batch scheduling and operational dependencies as external trivia.

## AECF AUDIT CHECKS

- Verify copybook, dataset, and batch-step contracts are preserved or explicitly migrated.
- Verify operational assumptions are documented, not implied.
- Verify regression evidence covers real legacy risk points.