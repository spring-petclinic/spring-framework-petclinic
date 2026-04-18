---
profile_id: al_extension_app
title: Business Central AL Extension App
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: framework
stack_nodes:
  - businesscentral
requires: []
precedence: 85
fallback_mode: warn_continue
compatibility:
  - businesscentral
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - manifest=app.json
  - extension=.al
  - keyword=business central
max_lines_per_section: 6
tags:
  - al
  - businesscentral
  - extension
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

Business Central AL work should be treated as extension-centric development with app.json as the authoritative manifest and object-level contracts kept explicit.

## ARCHITECTURE RULES

- Keep business logic in reusable codeunits when it should outlive a page or report trigger.
- Preserve object responsibilities across tables, pages, reports, and codeunits.
- Treat extension boundaries and dependency declarations as part of the architecture.

## DESIGN PATTERNS

- Codeunit-based reusable business rules.
- Explicit setup and permission handling for extension capabilities.
- Clear separation between UI behavior and posting or validation logic.

## CODING RULES

- Do not bury core business rules only in page triggers.
- Keep object IDs, naming, and versioning coherent with app.json.
- Make upgrade and data-change impact explicit when schema evolves.

## SECURITY RULES

- Review permission sets and privileged operations for each new capability.
- Treat setup data, posting routines, and integration endpoints as trust boundaries.
- Avoid assumptions about tenant state or implicit permissions.

## TESTING RULES

- Prefer test codeunits for business behavior and posting flows.
- Cover happy path, invalid business rule, and one permissions or setup regression.
- Keep test data setup explicit and isolated from production configuration.

## COMMON MISTAKES

- Coupling reusable business rules to UI-only objects.
- Changing object IDs or extension identity casually.
- Ignoring upgrade and tenant-state implications of schema changes.

## AECF AUDIT CHECKS

- Verify manifest, object ownership, and extension boundaries are coherent.
- Verify business logic is not trapped only in UI triggers.
- Verify tests cover business rules, setup, and permission-sensitive behavior.