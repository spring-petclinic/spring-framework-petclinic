---
profile_id: cobol_cics_online
title: COBOL CICS Online Transactions
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: legacy_platform
stack_nodes:
  - ibm-zos
requires:
  - cobol
precedence: 72
fallback_mode: warn_continue
compatibility:
  - cobol
  - ibm-zos
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=cics
  - keyword=transaction
  - keyword=mapset
max_lines_per_section: 6
tags:
  - cobol
  - cics
  - mainframe
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

COBOL CICS workloads should be handled as online transactional systems with strict conversational, screen, and transaction integrity assumptions.

## ARCHITECTURE RULES

- Preserve transaction boundaries, terminal interactions, and mapset-driven contracts unless redesign is explicit.
- Keep CICS calls and transaction control visible in the flow, not hidden by broad refactors.
- Separate modernization adapters from the core transactional behavior.

## DESIGN PATTERNS

- Strangler adapters around stable CICS transactions.
- Explicit command or service facades when exposing online capabilities outward.
- Contract mapping between screen/input layouts and external APIs.

## CODING RULES

- Do not alter conversational assumptions casually.
- Keep screen-field, transaction-id, and commarea handling explicit.
- Document transaction side effects and rollback-sensitive operations.

## SECURITY RULES

- Review transaction authorization, terminal exposure, and RACF or equivalent controls.
- Treat screen inputs and external transaction invocations as untrusted entry points.
- Preserve audit trails around sensitive transactional changes.

## TESTING RULES

- Add regression evidence around transaction flow and screen/commarea compatibility.
- Cover invalid input, rollback-sensitive behavior, and one authorization-sensitive scenario.
- Include non-regression checks for transaction contracts consumed by other systems.

## COMMON MISTAKES

- Breaking transaction semantics while chasing superficial refactors.
- Hiding CICS dependencies from the design narrative.
- Ignoring authorization and rollback behavior during modernization.

## AECF AUDIT CHECKS

- Verify transaction boundaries and CICS dependencies remain explicit.
- Verify online input/output contracts are preserved or intentionally remapped.
- Verify tests cover transactional and authorization-sensitive behavior.