---
profile_id: al_object_documentation
title: Business Central AL Object Documentation
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-16
profile_type: framework
stack_nodes:
  - businesscentral
requires: []
precedence: 82
fallback_mode: warn_continue
compatibility:
  - businesscentral
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - manifest=app.json
  - extension=.al
  - keyword=business central
  - keyword=al object
max_lines_per_section: 8
tags:
  - al
  - businesscentral
  - documentation
  - objects
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## STACK

Business Central AL development is object-centric. Each AL object type has specific semantics, properties, and documentation requirements. This profile provides the taxonomy and documentation rules for explaining and documenting AL objects.

## ARCHITECTURE RULES

- **Table**: the data definition layer. Document the purpose, key fields, relationships (TableRelation), field groups (FieldGroups), and keys. Note FlowFields and FlowFilters as computed values and their CalcFormula.
- **TableExtension**: extends a base table. Document which base table is extended, added fields with their purpose, and any new keys or field groups.
- **Page**: the UI presentation layer. Document the SourceTable, page type (Card, List, ListPart, Worksheet, Document, etc.), promoted actions, and user workflow.
- **PageExtension**: extends a base page. Document the base page, added fields/controls, added actions, and the business reason for the extension.
- **Codeunit**: reusable business logic. Document the public procedures, their parameters, return values, and the business rules they implement. Note SingleInstance and event publisher/subscriber roles.
- **Report**: data extraction and presentation. Document the data items (source tables), request page options, processing logic, and output format (RDLC, Word, Excel).

## DESIGN PATTERNS

- **Enum**: define closed value sets. Document each value with its caption, usage context, and any extensibility intent (Extensible = true/false).
- **EnumExtension**: extends a base enum. Document the base enum, added values, and their business justification.
- **Interface**: defines a polymorphic contract. Document the required procedure signatures, their semantics, and known implementations.
- **XMLport**: data import/export. Document the element structure, direction (Import/Export/Both), encoding, and the business process it supports.
- **Query**: optimized data retrieval. Document the data items, joins, aggregations, and the reporting or integration scenario it serves.
- **PermissionSet / PermissionSetExtension**: security definitions. Document which objects are included, the permission level (Read, Insert, Modify, Delete, Execute), and the role this permission set supports.

## CODING RULES

- Every public procedure must have a summary comment preceding it using `/// <summary>...</summary>`.
- Document table fields with clear `Caption` values that convey business meaning, not technical names.
- Use `ToolTip` property on page fields to provide inline user documentation.
- Document trigger code with inline comments when the behavior is non-obvious (e.g., `OnValidate`, `OnInsert`, `OnAfterGetRecord`).
- Document event publishers with `[IntegrationEvent]` or `[BusinessEvent]` attributes and describe the contract consumers should expect.
- Document subscriber methods with a reference to the published event they handle.

## SECURITY RULES

- Document which permission sets grant access to custom objects.
- Note when a codeunit runs with elevated permissions (`InherentPermissions`) and the justification.
- Document test permission sets used for validating security boundaries.
- Clearly mark procedures or fields that handle sensitive data (PII, financial amounts).

## TESTING RULES

- Document test codeunits with their test category (unit, integration, scenario) and the object being tested.
- Name test procedures to describe the scenario: `[Test] procedure <ObjectName>_<Scenario>_<ExpectedResult>`.
- Document test helper codeunits and what test data they create.
- When documenting coverage, reference specific tables, pages, or codeunits under test.

## COMMON MISTAKES

- Missing `ToolTip` on page fields — required for accessibility and localization.
- Missing `Caption` values on table fields and enum values.
- Undocumented FlowFields without explanation of what they aggregate.
- Undocumented integration events that third-party extensions are expected to subscribe to.
- Codeunit procedures without summary comments when they are part of the public API.
- Object names that do not follow the publisher prefix convention from `app.json`.

## AECF AUDIT CHECKS

- Verify all table fields have meaningful `Caption` values.
- Verify all page fields have `ToolTip` properties.
- Verify all public codeunit procedures have `/// <summary>` documentation.
- Verify enum values have captions and documented business context.
- Verify events are documented with their publisher/subscriber contract.
- Verify report data items and request page options are documented.
- Verify permission sets explicitly list the objects and permission levels they grant.
