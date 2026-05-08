# Feature Specification: Add Pet Photo

**Feature Branch**: `003-add-pet-photo`
**Created**: 2026-05-07
**Status**: Draft
**Input**: User description: "Requisito #1: Foto de mascota
Descripción: Añadir campo photoUrl o photo (BLOB) a Pet. CRUD básico.
Categoría: Baja"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Upload Pet Photo (Priority: P1)

As a veterinary staff member, I want to upload a photo for a pet so that I can visually identify the pet in the system.

**Why this priority**: Visual identification helps prevent errors and improves the user experience when managing multiple pets.

**Independent Test**: A staff member can open a pet's edit form, upload an image file, save it, and see the photo displayed on the pet's profile.

**Acceptance Scenarios**:

1. **Given** a pet exists without a photo, **When** staff uploads a valid image file and saves, **Then** the photo is stored and displayed on the pet's profile
2. **Given** a pet already has a photo, **When** viewing the pet details, **Then** the photo is clearly visible

### User Story 2 - Update or Remove Pet Photo (Priority: P2)

As a veterinary staff member, I want to update or remove a pet's photo so that I can keep the pet's information current.

**Why this priority**: Photos may become outdated or incorrect; staff need to be able to replace or remove them.

**Independent Test**: Change an existing pet photo to a new valid image and verify the update is saved correctly; then remove the photo and verify it no longer appears.

**Acceptance Scenarios**:

1. **Given** a pet has a photo, **When** staff uploads a new photo and saves, **Then** the new photo replaces the old one
2. **Given** a pet has a photo, **When** staff removes it and saves, **Then** the photo field is cleared and no image is displayed

### Edge Cases

- What happens when a staff member tries to upload a non-image file?
- How does the system handle very large image files?
- What occurs when two staff members try to upload photos for the same pet simultaneously?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a file upload field in the pet create/edit form
- **FR-002**: System MUST accept common image formats (JPEG, PNG, GIF) for pet photos
- **FR-003**: System MUST store pet photos as BLOB data in the database or as file paths (photoUrl) in the Pet entity
- **FR-004**: System MUST display the pet photo on the pet's profile/owner details page
- **FR-005**: System MUST validate file type and size before saving
- **FR-006**: System MUST allow updating an existing pet photo with a new image
- **FR-007**: System MUST allow removing a pet's photo (setting it to null/empty)

### Key Entities

- **Pet**: Extend with a photo field (either BLOB data or URL string) to store pet photographs

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully upload, view, update, and remove pet photos without errors
- **SC-002**: System validates image files and rejects invalid formats with clear error messages
- **SC-003**: Pet photo storage and retrieval does not degrade system performance significantly

## Assumptions

- The feature will use a URL-based approach (photoUrl) rather than storing binary data directly in the database for simplicity
- Image files will be stored in a dedicated directory within the web application context
- Existing seed data does not require migration as the photo field will be nullable