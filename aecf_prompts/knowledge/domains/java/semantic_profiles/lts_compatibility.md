---
profile_id: lts_compatibility
title: Java LTS Compatibility
version: 1.0.0
status: active
owner: AECF
last_review: 2026-04-07
profile_type: architecture
stack_nodes:
  - lts_compatibility
requires:
  - java
precedence: 78
fallback_mode: warn_continue
compatibility:
  - java
  - spring
  - jpa
  - zkoss
  - lombok
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=java 8
  - keyword=java 11
  - keyword=java 21
  - keyword=maven.compiler.source
  - keyword=maven.compiler.release
  - keyword=sourcecompatibility
max_lines_per_section: 6
tags:
  - java
  - lts
  - compatibility
---

LAST_REVIEW: 2026-04-07
OWNER SEACHAD

## STACK

Java LTS compatibility should be treated as an explicit compatibility envelope when the estate must coexist across older and newer LTS baselines.

## ARCHITECTURE RULES

- Define the minimum supported Java baseline before selecting language features or dependencies.
- Isolate modules that can move faster from modules constrained by older runtimes.
- Keep compatibility decisions visible in build files, CI, and release notes.

## DESIGN PATTERNS

- Prefer adapter or facade seams when newer APIs must coexist with legacy runtime consumers.
- Use incremental compatibility hardening instead of broad all-at-once rewrites.
- Separate upgrade-only refactors from business changes whenever possible.

## CODING RULES

- Do not use APIs or syntax above the agreed runtime floor in shared modules.
- Review `javax` versus `jakarta`, reflection usage, and dependency baselines explicitly.
- Keep compiler target, release, and toolchain settings aligned with the actual support matrix.

## SECURITY RULES

- Review whether older supported runtimes force outdated transitive dependencies or weaker crypto defaults.
- Track security patches that differ by Java baseline or vendor distribution.
- Do not assume a dependency is safe on every supported LTS without checking compatibility constraints.

## TESTING RULES

- Cover the supported compatibility matrix in CI or targeted validation runs.
- Add regression tests for serialization, time, reflection, or framework wiring differences across baselines.
- Include one explicit test or build assertion proving the declared minimum runtime is respected.

## COMMON MISTAKES

- Letting developers silently use newer Java features in modules that must still run on older LTS versions.
- Upgrading libraries without checking runtime-floor changes.
- Treating compatibility as a compiler setting only instead of an architectural constraint.

## AECF AUDIT CHECKS

- Verify the supported Java baseline and toolchain are explicit.
- Verify code and dependencies do not exceed the declared compatibility envelope.
- Verify tests or CI enforce the intended multi-LTS contract.