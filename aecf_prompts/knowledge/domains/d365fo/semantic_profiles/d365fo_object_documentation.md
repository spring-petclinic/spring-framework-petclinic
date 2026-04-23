---
profile_id: d365fo_object_documentation
title: Dynamics 365 Finance and Operations Object Documentation
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-16
profile_type: framework
stack_nodes:
  - d365fo
requires: []
precedence: 82
fallback_mode: warn_continue
compatibility:
  - d365fo
  - dotnet
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=finance and operations
  - keyword=x++
  - keyword=d365fo
  - keyword=AxClass
  - keyword=AxTable
max_lines_per_section: 8
tags:
  - d365fo
  - dynamics365
  - xpp
  - documentation
  - objects
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## STACK

Dynamics 365 Finance and Operations development uses X++ within a layered model architecture. Objects are defined in models with metadata-driven types including classes, tables, forms, data entities, reports, menus, security artifacts, and enums. This profile provides documentation rules for each object type.

## ARCHITECTURE RULES

- **AxTable**: data storage definition. Document the table group (Group, Main, Transaction, WorksheetHeader, WorksheetLine, Reference, Parameter), primary key and index, field groups, relations, and the business entity it represents. Note delete actions (Cascade, Restricted, None) on relations.
- **AxClass**: business logic container. Document the class purpose, public methods with parameters and return types, extension patterns using `[ExtensionOf]`, and subscription to events. Classify as service class, helper, handler, or entity-specific logic.
- **AxForm**: user interface. Document the form pattern (SimpleList, DetailsTransaction, Dialog, Workspace, ListPage, etc.), data sources with their tables and relationships, action pane structure, and the business process supported.
- **AxDataEntity**: integration and OData surface. Document the root data source, staging table (if applicable), mapped fields including computed and virtual fields, validation methods, and the integration scenario it serves.
- **AxReport**: SSRS report. Document the data provider (RDP class or query), parameters, report design sections, and the business output (invoice, journal list, financial statement, etc.).
- **AxMenu / AxMenuItem**: navigation entry points. Document the menu item type (Display, Output, Action), linked object, security requirements, and user persona.

## DESIGN PATTERNS

- **AxEnum / AxExtensibleEnum**: value sets. Document each value with its integer backing, label, and business meaning. Note if the enum is extensible and which extension scenarios are expected.
- **AxSecurityPrivilege**: atomic permission grant. Document the object type and access level (Read, Update, Create, Delete, Invoke) and the operation it protects.
- **AxSecurityDuty**: aggregated privileges. Document the grouped privileges and the business responsibility this duty represents (e.g., "Maintain customer master data").
- **AxSecurityRole**: user role. Document the associated duties, privileges, and the organizational persona this role serves.
- **AxNumberSequence**: sequence generator. Document the scope (Shared, Company, Legal entity), format, and the transactions that consume it.
- **AxBatch / AxSysOperation**: background processing. Document the contract class, service class, controller, and the business operation executed in batch.

## CODING RULES

- Document all public methods in classes with `/// <summary>` XML-style comments explaining parameters, return values, and business rules.
- Document table field groups with their intended UI and integration usage.
- Document data entity computed/unmapped fields with their derivation logic.
- Document event handler methods referencing the published event they subscribe to and the business rule they enforce.
- Document Chain of Command (CoC) method augmentations explaining what behavior is added before or after `next`.
- Use labels for all user-facing property values; document label IDs and their text for traceability.

## SECURITY RULES

- Document the security privilege, duty, and role chain for each new menu item, data entity, or service operation.
- Note when a class or batch job escalates privileges with `RunAs` or `securitySkipAuthorizationMethodOverride` and justify the escalation.
- Document data entity field-level security where sensitive financial or personal fields are exposed.
- Document configuration key dependencies for objects that should only be available when specific modules are licensed.

## TESTING RULES

- Document SysTest test classes with their test category and the objects under test.
- Name test methods descriptively: `test<Object>_<Scenario>_<ExpectedResult>`.
- Document test data helper classes and the entities they seed.
- When explaining coverage, reference specific tables, classes, data entities, or forms.

## COMMON MISTAKES

- Undocumented table relations and delete actions — causes unexpected cascading deletes.
- Missing documentation on data entity validation methods — integrations fail without clear error context.
- Undocumented configuration key dependencies — objects appear/disappear without explanation.
- Form patterns not following documented Microsoft patterns — causes upgrade friction.
- Extension classes without documented justification for what prior behavior they augment.
- Security artifacts created without documented privilege-duty-role chain.

## AECF AUDIT CHECKS

- Verify all tables have documented table group, primary key, field groups, and delete actions.
- Verify all public class methods have `/// <summary>` documentation.
- Verify data entities have documented root data source, field mappings, and validation logic.
- Verify enums have documented values with labels and business meaning.
- Verify security privilege-duty-role chains are explicitly documented.
- Verify forms follow documented Microsoft form patterns.
- Verify extension classes document the base object and the behavior augmented.
- Verify configuration key dependencies are documented for gated objects.
