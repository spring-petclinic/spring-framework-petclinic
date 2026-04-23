---
profile_id: xpp_extension
title: Dynamics 365 Finance and Operations X++ Extension
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - d365fo
requires: []
precedence: 85
fallback_mode: warn_continue
compatibility:
  - d365fo
  - dotnet
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - extension=.xpp
  - keyword=finance and operations
  - keyword=x++
  - keyword=d365fo
max_lines_per_section: 6
tags:
  - xpp
  - d365fo
  - dynamics365
  - financeandoperations
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

Dynamics 365 Finance and Operations X++ work should use extension-based customization with Visual Studio, respecting the layered model architecture and avoiding overlayering of standard objects.

## ARCHITECTURE RULES

- Prefer extension classes with `[ExtensionOf]` over overlayering base application objects.
- Keep business logic in classes and services, separate from form and data source event handlers.
- Respect model and package boundaries; declare dependencies explicitly in model metadata.
- Use data entities for integration surfaces and OData exposure.
- Separate data access, business logic, and UI concerns across tables, classes, and forms.

## DESIGN PATTERNS

- Chain of Command (CoC) for augmenting standard business methods.
- Event handler subscription for decoupled pre/post-processing.
- Data entity wrappers for clean integration contracts.
- Number sequence and configuration key patterns for extensible setup.
- Batch framework usage for long-running or schedulable operations.

## CODING RULES

- Always use `[ExtensionOf]` and `next` for method augmentation; never copy-paste base methods.
- Keep form logic thin; delegate to service or helper classes.
- Use labels for all user-facing strings; never hardcode text.
- Respect `ttsbegin`/`ttscommit` boundaries and keep transactions as short as possible.
- Validate configuration key availability before using gated features.

## SECURITY RULES

- Assign explicit security privileges and duties to new menu items and data entities.
- Review security role grants for least-privilege access on every new entry point.
- Protect data entity fields that expose sensitive financial or personal data.
- Do not bypass security context in batch or service operations without explicit justification.

## TESTING RULES

- Use SysTest framework for unit and component tests inside Visual Studio.
- Cover posting logic, validation rules, and data entity round-trips.
- Test extension behavior in isolation to confirm CoC augmentation is additive and non-breaking.
- Validate security role assignments block unauthorized access.
- Keep test data creation deterministic and independent of environment state.

## COMMON MISTAKES

- Overlayering standard objects instead of using extension classes.
- Burying reusable business rules in form event handlers.
- Ignoring configuration key or license code dependencies.
- Creating data entities without proper field-level security and validation.
- Opening long-running transactions that block other operations.

## AECF AUDIT CHECKS

- Verify extension pattern is used over overlay where available.
- Verify business logic lives in classes and services, not UI event handlers.
- Verify security privileges, duties, and roles are explicitly defined.
- Verify data entities validate input and respect field-level security.
- Verify test coverage includes posting, validation, and security paths.
