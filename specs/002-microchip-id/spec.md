# Feature Specification: Pet Microchip ID

**Feature Branch**: `002-add-microchip-id`
**Created**: 2026-05-12
**Status**: Draft
**Input**: "Requisito #2: Microchip ID - Campo microchipId en Pet + validación única. Identificación oficial."

---

## Overview

Store and display official microchip identification numbers for pets following ISO 11784/11785 standard. This enables pet recovery services and regulatory compliance for pet identification.

---

## User Stories & Scenarios

### US1: Register Pet Microchip ID (P1 - MVP)

**As a** clinic staff member
**I want to** register a pet's microchip ID
**So that** I can maintain official identification records

**Scenario: Register microchip ID during pet creation**
- Given I am adding a new pet to the system
- When I enter the pet's details
- Then I can optionally enter the microchip ID (15 characters)
- And the system validates the format

**Scenario: Register microchip ID during pet edit**
- Given I am editing an existing pet's information
- When I update the microchip ID field
- Then the system validates uniqueness
- And stores the identifier

**Scenario: Edit pet without microchip**
- Given a pet exists without a microchip ID
- When I edit the pet
- Then the microchip field is empty
- And I can add one later

---

### US2: View Pet Microchip ID (P1 - MVP)

**As a** clinic staff member
**I want to** see a pet's microchip ID on the owner details page
**So that** I can quickly verify pet identification

**Scenario: Display microchip on owner details**
- Given I am viewing a pet's owner details
- When the pet has a microchip ID registered
- Then the microchip ID is displayed in the pet section
- And shows "Not registered" if empty

---

## Functional Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| FR1 | Store microchip ID | System accepts 15-character alphanumeric microchip ID |
| FR2 | Unique constraint | No two pets can have the same microchip ID |
| FR3 | Optional field | Microchip ID is not required; pets can exist without it |
| FR4 | Display microchip | Pet microchip ID appears on owner details page |
| FR5 | Edit capability | Staff can add or update microchip ID via pet form |

---

## Data Model

### Pet Entity Extension

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| microchipId | String(15) | UNIQUE, NULLABLE | ISO 11784/11785 compliant identifier |

**Assumption**: Using ISO 11784/11785 standard means 15 alphanumeric characters. National codes vary by country, but the standard identifier fits in 15 characters.

---

## Success Criteria

| Criterion | Metric |
|-----------|--------|
| Microchip registration works | Staff can save pet with microchip ID in under 30 seconds |
| Uniqueness enforced | System rejects duplicate microchip IDs with clear error |
| Display visible | 100% of pets with microchip show it on owner details |
| Optional field | Pets without microchip save successfully |

---

## Edge Cases

1. **Empty microchip**: Pet saves normally without microchip ID
2. **Duplicate microchip**: System displays validation error
3. **Invalid format**: System accepts any 15 alphanumeric (ISO validation deferred to client country requirements)
4. **Special characters**: System strips non-alphanumeric characters

---

## Out of Scope

- Pet lookup by microchip ID (US2 in next iteration)
- Microchip validation against national databases
- Batch import of microchip data
- QR code generation from microchip

---

## Dependencies

- Pet entity already exists in PetClinic model
- Pet creation/edit form already exists
- Owner details page already displays pets

---

## Assumptions

1. **ISO Standard**: Assuming 15-character alphanumeric format per ISO 11784/11785
2. **Staff users**: Only clinic staff (not pet owners) manage microchip data
3. **No authentication**: System assumes trusted internal network access
4. **Nullable by default**: Microchip is optional to allow existing pets without it