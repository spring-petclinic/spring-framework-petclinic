---
profile_id: lombok
title: Lombok Usage
version: 1.0.0
status: active
owner: AECF
last_review: 2026-04-07
profile_type: tool
stack_nodes:
  - lombok
requires:
  - java
precedence: 65
fallback_mode: warn_continue
compatibility:
  - java
  - spring
  - jpa
  - zkoss
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=lombok
  - keyword=@data
  - keyword=@builder
  - keyword=@getter
  - keyword=@setter
max_lines_per_section: 6
tags:
  - java
  - lombok
  - codegen
---

LAST_REVIEW: 2026-04-07
OWNER SEACHAD

## STACK

Lombok should be treated as a compile-time code generation aid that reduces boilerplate but does not replace explicit domain design, validation, or API clarity.

## ARCHITECTURE RULES

- Keep Lombok annotations as an implementation convenience, not as a substitute for architectural boundaries.
- Be explicit when constructors, builders, or value semantics are part of the public contract.
- Avoid hiding domain invariants behind generated accessors or all-args constructors.

## DESIGN PATTERNS

- Prefer targeted annotations such as `@Getter`, `@RequiredArgsConstructor`, or `@Builder` over broad bundles when intent matters.
- Use immutable or near-immutable models where the domain benefits from predictable state.
- Keep DTO, entity, and domain-model Lombok usage intentionally differentiated.

## CODING RULES

- Do not use `@Data` by default on entities or rich domain models.
- Review generated `equals`, `hashCode`, and `toString` behavior before relying on defaults.
- Keep annotation processing requirements explicit in the existing build configuration.

## SECURITY RULES

- Do not expose secrets or sensitive fields through generated `toString` methods.
- Review builder and setter generation on security-sensitive or authorization-relevant objects.
- Avoid generated mutators that weaken encapsulation of privileged state.

## TESTING RULES

- Cover equality, builder defaults, and constructor invariants when Lombok shapes object semantics.
- Validate serialization, mapping, or persistence behavior where generated methods are involved.
- Include one non-regression test when replacing handwritten boilerplate with Lombok annotations.

## COMMON MISTAKES

- Using `@Data` everywhere and accidentally broadening mutability or equality semantics.
- Assuming generated methods are harmless without reviewing entity lifecycle implications.
- Forgetting annotation-processing or IDE support requirements across modules.

## AECF AUDIT CHECKS

- Verify Lombok use keeps contracts explicit and does not hide invariants.
- Verify generated equality, mutability, and logging behavior are safe for the model type.
- Verify build and test setup covers annotation-driven behavior intentionally.