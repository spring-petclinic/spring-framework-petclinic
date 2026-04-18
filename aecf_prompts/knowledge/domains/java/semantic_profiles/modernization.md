---
profile_id: modernization
title: Java Modernization
version: 1.0.0
status: active
owner: AECF
last_review: 2026-04-07
profile_type: architecture
stack_nodes:
  - modernization
requires:
  - java
precedence: 80
fallback_mode: warn_continue
compatibility:
  - java
  - spring
  - zkoss
  - jpa
  - lombok
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=modernization
  - keyword=migration
  - keyword=incremental migration
  - keyword=strangler
  - keyword=api first
  - keyword=java 21
max_lines_per_section: 6
tags:
  - java
  - modernization
  - migration
---

LAST_REVIEW: 2026-04-07
OWNER SEACHAD

## STACK

Java modernization should be treated as a phased change program that improves maintainability, upgrade posture, and decoupling without breaking critical business behavior.

## ARCHITECTURE RULES

- Prefer incremental modernization behind stable seams instead of wide rewrites.
- Isolate legacy UI, persistence, or integration concerns behind services or adapters before replacing them.
- Keep backward-compatible contracts explicit while new APIs or modules are introduced.

## DESIGN PATTERNS

- Strangler-style extraction for legacy entry points or tightly coupled modules.
- API-first seams when preparing server-side systems for alternate frontends or clients.
- Anti-corruption layers around generated, legacy, or framework-heavy components.

## CODING RULES

- Separate modernization refactors from feature changes whenever possible.
- Replace broad shared utilities with bounded module ownership rather than creating new god-libraries.
- Keep deprecated pathways discoverable until migration exit criteria are met.

## SECURITY RULES

- Re-evaluate auth, session, and data-exposure assumptions when extracting APIs from legacy flows.
- Do not carry forward obsolete libraries or insecure defaults just for short-term migration speed.
- Review generated or legacy integration boundaries for hidden trust assumptions.

## TESTING RULES

- Add characterization or contract tests before replacing legacy behavior.
- Validate old and new execution paths during coexistence periods.
- Include rollback-safe non-regression checks for critical user or integration flows.

## COMMON MISTAKES

- Trying to modernize architecture, runtime, framework, and UX in one uncontrolled step.
- Removing legacy paths before parity or operational readiness is proven.
- Treating modernization as cosmetic cleanup instead of a governed compatibility program.

## AECF AUDIT CHECKS

- Verify modernization is phased, reversible where needed, and bounded by explicit seams.
- Verify parity and coexistence risks are covered with targeted tests.
- Verify legacy-to-modern contract changes are intentional, documented, and operationally safe.