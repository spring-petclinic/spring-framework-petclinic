# Tasks: Add Pet Photo

**Input**: Design documents from `specs/003-add-pet-photo/`
**Prerequisites**: plan.md ✅, spec.md ✅

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Verify `mvn compile` passes on current codebase (baseline check)
- [X] T002 Review existing `pets` table schema in all 4 DB scripts (h2, hsqldb, mysql, postgresql) under `src/main/resources/db/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add `photoUrl` column to all DB schemas and `photoUrl` field to `Pet` entity — required before any layer above can work

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Add `photo_url VARCHAR(255) NULL` column to `src/main/resources/db/h2/schema.sql` in the `pets` table definition
- [X] T004 [P] Add `photo_url VARCHAR(255) NULL` column to `src/main/resources/db/hsqldb/schema.sql` in the `pets` table definition
- [X] T005 [P] Add `photo_url VARCHAR(255) NULL` column to `src/main/resources/db/mysql/schema.sql` in the `pets` table definition
- [X] T006 [P] Add `photo_url VARCHAR(255) NULL` column to `src/main/resources/db/postgresql/schema.sql` in the `pets` table definition
- [X] T007 Add `photoUrl` field to `src/main/java/org/springframework/samples/petclinic/model/Pet.java` with `@Column(name = "photo_url")` annotation; add getter and setter
- [X] T008 Verify `mvn compile` passes after entity + schema changes

**Checkpoint**: Foundation ready — Pet entity has photoUrl field, all DB schemas updated

---

## Phase 3: User Story 1 - Upload Pet Photo (Priority: P1) 🎯 MVP

**Goal**: Staff can upload a photo for a pet via the edit form, and it is saved and displayed

**Independent Test**: Open pet edit form, upload a valid image file, save, and verify it appears on the owner details page

### Implementation for User Story 1

- [X] T009 [US1] Add `<input type="file" name="photoUrl" accept="image/*"/>` to the pet form in `src/main/webapp/WEB-INF/jsp/pets/createOrUpdatePetForm.jsp` (after other fields)
- [X] T010 [US1] Add photo display to `src/main/webapp/WEB-INF/jsp/owners/ownerDetails.jsp` inside the pet info block (e.g., `<c:if test="${not empty pet.photoUrl}"><img src="${pet.photoUrl}" alt="Pet photo" style="max-width:200px;"/></c:if>`)
- [X] T011 [US1] Run `mvn test` and fix any failures; confirm all 3 profiles pass (JPA, JDBC, Spring Data JPA)

**Checkpoint**: US1 complete — staff can upload a photo and see it on the pet profile

---

## Phase 4: User Story 2 - Update or Remove Pet Photo (Priority: P2)

**Goal**: Staff can update or remove a photo on an existing pet

**Independent Test**: Edit a pet's photo to a new valid image, save, verify updated image shown; then remove it, save, verify it no longer appears

### Implementation for User Story 2

- [X] T012 [US2] Verify the existing pet edit form (T009) already supports update/clear — no new form changes needed; confirm the file input allows selecting a new file or clearing by not selecting a file
- [X] T013 [US2] Test clearing a photo: submit the form without selecting a file, verify the photoUrl is cleared in the database and not displayed in ownerDetails.jsp
- [X] T014 [US2] Run `mvn test` and fix any failures

**Checkpoint**: US2 complete — staff can update or remove pet photos without errors

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, SpotBugs check, and build verification

- [X] T015 [P] Run `mvn spotbugs:check` and fix any reported issues (0 bugs required)
- [X] T016 Run `mvn package` (full build) and confirm it succeeds
- [X] T017 [P] Manual smoke test: start app with `./mvnw jetty:run-war`, navigate to a pet edit form, upload a photo, save, verify display

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **Phase 3 (US1)**: Depends on Phase 2 — can start once entity + schemas ready
- **Phase 4 (US2)**: Depends on Phase 3 (form must exist)
- **Phase 5 (Polish)**: Depends on all story phases complete

### Within Each Phase

- Schema tasks T003–T006 are fully parallel (different files)
- T009, T010 (UI modifications) are parallel (different JSP files)

### Parallel Opportunities

```bash
# Phase 2 — all 4 schema files in parallel:
T003: h2/schema.sql
T004: hsqldb/schema.sql
T005: mysql/schema.sql
T006: postgresql/schema.sql

# Phase 3 — UI modifications in parallel:
T009: createOrUpdatePetForm.jsp
T010: ownerDetails.jsp
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T002)
2. Complete Phase 2: Foundational (T003–T008)
3. Complete Phase 3: User Story 1 (T009–T011)
4. **STOP and VALIDATE**: Upload a photo in browser, verify it saves and displays
5. Demo if ready — basic photo upload functionality is functional

### Incremental Delivery

1. Setup + Foundational → entity + DB ready
2. US1 → upload + display photo (MVP)
3. US2 → confirm update/clear works
4. Polish → spotbugs, full build, smoke test

---

## Notes

- [P] tasks = different files, no dependencies — safe to run in parallel
- The photoUrl field stores a URL/path to the image file; actual file storage would require additional infrastructure (file upload handling) which may be addressed in a separate feature
- For MVP, we focus on the data model and UI display; actual file upload processing may require additional controller/service work
- Existing seed data (`data.sql`) needs no changes as the column is nullable
