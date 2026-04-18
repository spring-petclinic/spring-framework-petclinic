---
profile_id: maven
title: Java Maven Build Lifecycle
version: 1.0.0
status: active
owner: AECF
last_review: 2026-04-07
profile_type: tool
stack_nodes:
  - maven
requires:
  - java
precedence: 66
fallback_mode: warn_continue
compatibility:
  - java
  - spring
  - jpa
  - lombok
  - lts_compatibility
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - manifest=pom.xml
  - keyword=maven-compiler-plugin
  - keyword=maven-surefire-plugin
  - keyword=dependencymanagement
max_lines_per_section: 6
tags:
  - java
  - maven
  - build
  - tooling
---

LAST_REVIEW: 2026-04-07
OWNER SEACHAD

## STACK

Maven-based Java projects should keep lifecycle phases, plugin ownership, dependency convergence, and compiler settings explicit so builds remain reproducible across modules and CI environments.

## ARCHITECTURE RULES

- Keep parent POM, module POMs, and shared plugin or dependency conventions clearly separated.
- Centralize version alignment through dependency management or BOMs when the existing build already uses them.
- Preserve current packaging and reactor structure unless the task explicitly requires build reorganization.

## DESIGN PATTERNS

- Use the Maven compiler, surefire, failsafe, and enforcer plugins intentionally with explicit ownership.
- Keep annotation processing, generated sources, and profile-driven packaging visible in the build definition.
- Separate unit-test and integration-test concerns through lifecycle-aware plugin configuration.

## CODING RULES

- Prefer `maven.compiler.release` or an equivalent explicit compiler target aligned with the supported runtime floor.
- Avoid ad hoc plugin additions when an existing parent or corporate POM already governs the build.
- Review transitive dependency impact before introducing starters, SDKs, or overlapping BOM imports.

## SECURITY RULES

- Treat new repositories, mirrors, and build extensions as supply-chain decisions requiring justification.
- Review plugin and dependency version pinning before relying on latest or floating ranges.
- Avoid profile-specific packaging or resource filtering that can leak secrets or environment assumptions.

## TESTING RULES

- Keep surefire and failsafe scope intentional and verify the expected tests actually execute in CI.
- Add one non-regression check when changing compiler, plugin, or module wiring.
- Cover happy path, failing build contract, and one compatibility edge when build logic changes.

## COMMON MISTAKES

- Mixing plugin configuration across parent and child POMs until the effective build becomes unclear.
- Hiding Java version constraints in CI only instead of the Maven build definition.
- Treating Maven profiles as a substitute for clear environment or module boundaries.

## AECF AUDIT CHECKS

- Verify plugin ownership, dependency alignment, and compiler settings are explicit.
- Verify test lifecycle configuration matches the intended unit/integration split.
- Verify build changes stay reproducible across modules, local runs, and CI agents.