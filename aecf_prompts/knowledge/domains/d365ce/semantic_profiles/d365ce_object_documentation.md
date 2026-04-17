---
profile_id: d365ce_object_documentation
title: Dynamics 365 CE Object Documentation
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-16
profile_type: framework
stack_nodes:
  - d365ce
requires: []
precedence: 82
fallback_mode: warn_continue
compatibility:
  - d365ce
  - dotnet
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=dynamics crm
  - keyword=customer engagement
  - keyword=dataverse
  - keyword=d365ce
  - keyword=entity
max_lines_per_section: 8
tags:
  - d365ce
  - dynamics365
  - documentation
  - dataverse
  - objects
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## STACK

Dynamics 365 Customer Engagement is built on the Dataverse platform. Development involves defining and extending entities, forms, views, dashboards, plugins, workflows, custom actions, custom APIs, and web resources. This profile provides documentation rules for each component type.

## ARCHITECTURE RULES

- **Entity (Table)**: the core data structure. Document the schema name, display name, ownership type (User, Organization), primary key and name, and the business concept it represents. Note custom vs system entities.
- **Attribute (Column)**: fields on an entity. Document the data type (String, Integer, Lookup, OptionSet, DateTime, Currency, etc.), required level, display name, and business semantics. For lookups, document the target entity and relationship type (1:N, N:1, N:N).
- **Form**: the UI layout for entity records. Document the form type (Main, Quick Create, Quick View, Card), target audience (role-specific forms), tabs, sections, and the business workflow supported. Note JavaScript event handlers attached to form/field events.
- **View**: saved queries for listing records. Document the filter criteria, columns displayed, sort order, and the business scenario (active records, my records, pipeline, etc.).
- **Dashboard**: aggregated views. Document the chart types, source views, and the KPI or business insight the dashboard provides.

## DESIGN PATTERNS

- **Plugin**: server-side .NET assembly. Document the registered message (Create, Update, Delete, Associate, etc.), entity, pipeline stage (PreValidation, PreOperation, PostOperation), execution mode (Sync/Async), filtering attributes, and the business rule enforced.
- **Custom Action / Custom API**: reusable operations. Document input/output parameters with types, the business operation performed, and whether it is bound to an entity or global.
- **Workflow / Power Automate flow**: orchestration. Document the trigger event, conditions, actions, and the business process automated.
- **Business Rule**: declarative logic. Document the entity, scope (Entity, All Forms, specific form), conditions, and actions (set field, show error, set default, lock/unlock).
- **Web Resource**: client-side assets. Document the type (JavaScript, HTML, CSS, Image, SVG), registration context (form/ribbon), and the UI behavior it implements.

## CODING RULES

- Document all plugin classes with XML doc comments describing the registered message, entity, and pipeline stage.
- Document custom action and custom API request/response classes with parameter descriptions.
- Document web resource JavaScript functions with JSDoc comments including `@param`, `@returns`, and usage context.
- Document entity relationships (1:N, N:1, N:N) with their cascade behavior (Assign, Share, Delete, Reparent, Merge).
- Document OptionSet values with their integer value, label, and business meaning.

## SECURITY RULES

- Document security roles that grant access to each custom entity and their CRUD permission levels.
- Document privilege assignments for custom actions and custom APIs.
- Note field-level security profiles applied to sensitive attributes.
- Document team vs user ownership implications for record-level security.
- Note when plugins require system-user context elevation and the justification.

## TESTING RULES

- Document test cases for plugins including the message, entity, expected behavior, and assertions.
- Document custom action tests with input/output contract verification.
- Document JavaScript web resource test coverage with mock object descriptions.
- When explaining coverage, reference specific entities, plugins, or actions under test.

## COMMON MISTAKES

- Undocumented plugin registrations — registered steps without explaining the business rule.
- Missing OptionSet value descriptions — consumers cannot interpret integer values without labels.
- Undocumented relationship cascade behavior — unexpected deletes or reassignments.
- Forms without documented field visibility logic and event handler purpose.
- Custom actions without documented input/output parameter contracts.
- Security roles without documented entity/privilege mapping.

## AECF AUDIT CHECKS

- Verify all custom entities have documented schema name, display name, ownership type, and purpose.
- Verify all custom attributes have documented data type, required level, and business meaning.
- Verify all plugin registrations have documented message, entity, stage, and business rule.
- Verify custom actions and APIs have documented parameter contracts.
- Verify OptionSet values have labels and business context.
- Verify relationship cascade behavior is explicitly documented.
- Verify security roles are documented with entity/privilege mappings.
