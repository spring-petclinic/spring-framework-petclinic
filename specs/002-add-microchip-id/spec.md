# Feature Specification: Add Microchip ID

**Feature Branch**: `[002-add-microchip-id]`
**Created**: 2026-05-06
**Status**: Draft
**Input**: User description: "Requisito #2: Microchip ID
Descripción: Campo microchipId en Pet + validación única. Identificación oficial.
Categoría: Baja"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Register Microchip ID for a Pet (Priority: P1)

As a veterinary staff member, I want to record the official microchip ID of a pet so that the pet has a unique, verifiable identifier for official purposes.

**Why this priority**: Microchip identification is an official legal requirement in many jurisdictions and is the primary method of permanent pet identification. It must be accurate and unique.

**Independent Test**: A staff member can open a pet's form, enter a microchip ID, save it, and see it displayed on the pet's profile.

**Acceptance Scenarios**:

1. **Given** a pet exists without a microchip ID, **When** staff enters a valid microchip ID and saves, **Then** the ID is stored and displayed on the pet's profile
2. **Given** a pet already has a microchip ID, **When** viewing the pet details, **Then** the microchip ID is clearly visible

---

### User Story 2 - Uniqueness Validation (Priority: P1)

As a veterinary staff member, I want the system to prevent duplicate microchip IDs so that each microchip can only be registered to one pet at a time.

**Why this priority**: A microchip is physically unique per animal — allowing duplicates would cause data integrity issues and identity confusion.

**Independent Test**: Attempt to register the same microchip ID on two different pets and verify the system rejects the second registration with a clear error message.

**Acceptance Scenarios**:

1. **Given** microchip ID `123456789012345` is already registered to Pet A, **When** staff tries to register the same ID to Pet B, **Then** the system rejects it with a clear error message indicating the ID is already in use
2. **Given** a microchip ID has a format error (wrong length or invalid characters), **When** staff submits the form, **Then** the system shows a validation error before saving

---

### User Story 3 - Update or Remove Microchip ID (Priority: P2)

As a veterinary staff member, I want to correct or clear a microchip ID in case of data entry errors.

**Why this priority**: Mistakes happen during data entry; staff need to be able to correct them.

**Independent Test**: Change an existing microchip ID to a new valid value and verify the update is saved correctly.

**Acceptance Scenarios**:

1. **Given** a pet has a microchip ID, **When** staff updates it to a new valid and unique ID, **Then** the new ID is saved and the old one is no longer associated
2. **Given** a pet has a microchip ID, **When** staff removes it, **Then** the field is cleared

---

### Edge Cases

- What happens when two staff members try to register the same microchip ID simultaneously?
- What happens if a microchip ID contains special characters or spaces?
- How does the system handle a microchip ID that was previously assigned to a deceased/deleted pet?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Users MUST be able to add a microchip ID to a pet's profile
- **FR-002**: The system MUST enforce uniqueness of microchip IDs across all pets
- **FR-003**: The system MUST validate microchip ID format (15-digit numeric string per ISO 11784/11785 standard)
- **FR-004**: Users MUST receive a clear error message when a duplicate or invalid microchip ID is submitted
- **FR-005**: Users MUST be able to update or remove a pet's microchip ID
- **FR-006**: The microchip ID MUST be displayed on the pet's details page

### Key Entities *(include if feature involves data)*

- **[Pet]**: Extended with a new `microchipId` attribute. The value must be unique across all pets and optional (not all pets may be microchipped).
- **[MicrochipID]**: A 15-digit numeric identifier per ISO 11784/11785. Globally unique per animal.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of microchip ID entries are validated for format before saving
- **SC-002**: 0 duplicate microchip IDs exist in the system at any time
- **SC-003**: Staff can register a microchip ID for a pet in under 60 seconds
- **SC-004**: Duplicate entry attempts result in a clear, user-readable error message within 2 seconds

## Assumptions

- Microchip IDs follow the ISO 11784/11785 standard: 15-digit numeric string
- The microchip ID field is optional — not all pets are microchipped
- Only veterinary staff (not pet owners) register microchip IDs
- The uniqueness constraint applies across all active pets in the system
- No integration with external microchip registries is required in this scope
