---
profile_id: d365marketing_component_documentation
title: Dynamics 365 Marketing Component Documentation
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-16
profile_type: framework
stack_nodes:
  - d365marketing
requires: []
precedence: 82
fallback_mode: warn_continue
compatibility:
  - d365marketing
  - d365ce
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=dynamics marketing
  - keyword=real-time marketing
  - keyword=d365marketing
  - keyword=customer journey
  - keyword=marketing form
max_lines_per_section: 8
tags:
  - d365marketing
  - dynamics365
  - powerplatform
  - documentation
  - components
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## STACK

Dynamics 365 Marketing customization involves Dataverse entities, customer journeys, marketing forms, segments, email templates, event management, PCF controls, Power Automate flows, and custom connectors. This profile provides documentation rules for each component type.

## ARCHITECTURE RULES

- **Customer Journey**: automated marketing workflow. Document the trigger (contact-based, event-based, segment-based), channels used (email, SMS, push), branching conditions, wait steps, and exit criteria. Note which segment provides the audience.
- **Marketing Form**: lead capture or event registration. Document the form type (landing page, embedded, event registration), fields captured, consent handling, and the entity/table where submissions are stored.
- **Segment**: audience definition. Document the segment type (static, dynamic/compound), filter criteria, related entities, and the business audience it represents. Note evaluation frequency for dynamic segments.
- **Email Template**: marketing communication. Document the content blocks, dynamic content (personalization tokens), A/B test variants, and compliance links (unsubscribe, preference center).
- **Event**: event management artifact. Document the event type (webinar, in-person, hybrid), sessions, speakers, registration form, and capacity tracking.

## DESIGN PATTERNS

- **PCF Control**: custom UI component. Document the `ControlManifest.Input.xml` with bound/input/output properties, the framework lifecycle methods (init, updateView, destroy), and the entity or form context where the control is hosted.
- **Power Automate Flow**: orchestration. Document the trigger (Dataverse row change, scheduled, HTTP), input parameters, actions, conditions, error handling (try-scope), and the business process automated. Note child flow references.
- **Custom Connector**: external API integration. Document the OpenAPI definition, authentication type (OAuth, API key), operations, request/response schemas, and security considerations.
- **Custom Channel**: extended channel (SMS, push, custom). Document the contract, message template format, delivery provider, and consent integration.
- **Solution Component**: document the solution publisher prefix, component type, and managed vs unmanaged status.

## CODING RULES

- Document PCF controls with TypeScript JSDoc comments on all public methods and lifecycle implementations.
- Document Power Automate expressions with inline annotations explaining complex conditions.
- Document custom connector operations with parameter descriptions matching the OpenAPI spec.
- Document Dataverse entity customizations (new columns, relationships, business rules) with business justification.
- Document environment variables with their purpose, expected value type, and default value.

## SECURITY RULES

- Document marketing consent requirements (GDPR, CAN-SPAM) for each form and email template.
- Document Power Automate flow connection owners and run-as context.
- Document custom connector authentication type and where secrets are managed.
- Document Dataverse security role requirements for custom marketing entities.
- Note when flows or connectors access external or third-party services and the data shared.

## TESTING RULES

- Document PCF control test setup with mock component framework context.
- Document Power Automate flow test runs with trigger inputs and expected outputs.
- Document custom connector contract tests with expected request/response pairs.
- Document marketing form submission tests with validation and consent scenarios.
- When explaining coverage, reference specific components by solution name and type.

## COMMON MISTAKES

- Undocumented customer journey exit criteria — audiences may receive unintended communications.
- Missing consent documentation on marketing forms — compliance risk.
- Undocumented dynamic segment filter changes — audience scope changes silently.
- PCF controls without documented input/output property contracts.
- Power Automate flows without documented error handling paths.
- Custom connectors without documented authentication and security configuration.

## AECF AUDIT CHECKS

- Verify customer journeys have documented trigger, audience, channels, and exit criteria.
- Verify marketing forms document consent handling and submission storage.
- Verify segments document their filter criteria, type, and evaluation frequency.
- Verify email templates document personalization tokens and compliance links.
- Verify PCF controls document all manifest properties and lifecycle methods.
- Verify Power Automate flows document trigger, actions, and error handling.
- Verify custom connectors document auth type, operations, and security.
