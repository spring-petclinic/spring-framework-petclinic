# Tasks: Add Microchip ID

**Input**: Design documents from `specs/002-add-microchip-id/`
**Prerequisites**: plan.md ✅, spec.md ✅

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify baseline compiles and schema structure is understood before changes

- [X] T001 Verify `mvn compile` passes on current codebase (baseline check)
- [X] T002 Review existing `pets` table schema in all 4 DB scripts (h2, hsqldb, mysql, postgresql) under `src/main/resources/db/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add `microchip_id` column to all DB schemas and `microchipId` field to `Pet` entity — required before any layer above can work

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Add `microchip_id VARCHAR(15) UNIQUE NULL` column to `src/main/resources/db/h2/schema.sql` in the `pets` table definition
- [X] T004 [P] Add `microchip_id VARCHAR(15) UNIQUE NULL` column to `src/main/resources/db/hsqldb/schema.sql` in the `pets` table definition
- [X] T005 [P] Add `microchip_id VARCHAR(15) UNIQUE NULL` column to `src/main/resources/db/mysql/schema.sql` in the `pets` table definition
- [X] T006 [P] Add `microchip_id VARCHAR(15) UNIQUE NULL` column to `src/main/resources/db/postgresql/schema.sql` in the `pets` table definition
- [X] T007 Add `microchipId` field to `src/main/java/org/springframework/samples/petclinic/model/Pet.java` with `@Column(name = "microchip_id", unique = true)` and `@Pattern(regexp = "\\d{15}", message = "Microchip ID must be 15 digits")` annotations; add getter and setter
- [X] T008 Verify `mvn compile` passes after entity + schema changes

**Checkpoint**: Foundation ready — Pet entity has microchipId field, all DB schemas updated

---

## Phase 3: User Story 1 - Register Microchip ID (Priority: P1) 🎯 MVP

**Goal**: Staff can add a microchip ID to a pet's profile via the edit form, and it is saved and displayed

**Independent Test**: Open pet edit form, enter a valid 15-digit microchip ID, save, and verify it appears on the owner details page

### Implementation for User Story 1

- [X] T009 [US1] Add `findPetByMicrochipId(String microchipId)` method to the `ClinicService` interface in `src/main/java/org/springframework/samples/petclinic/service/ClinicService.java`
- [X] T010 [P] [US1] Implement `findPetByMicrochipId` in the JPA service/repository: add query method to `src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaPetRepositoryImpl.java` (or Spring Data JPA repository interface)
- [X] T011 [P] [US1] Implement `findPetByMicrochipId` in the JDBC repository: add SQL query in `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcPetRepositoryImpl.java` and map `microchip_id` column in the `RowMapper`
- [X] T012 [US1] Add uniqueness validation to `src/main/java/org/springframework/samples/petclinic/web/PetValidator.java`: if `microchipId` is non-null and non-empty, call `clinicService.findPetByMicrochipId(id)` and reject if result belongs to a different pet
- [X] T013 [US1] Add `<petclinic:inputField label="Microchip ID" name="microchipId"/>` to the pet form in `src/main/webapp/WEB-INF/jsp/pets/createOrUpdatePetForm.jsp` (after the Type field)
- [X] T014 [US1] Add microchip ID display to `src/main/webapp/WEB-INF/jsp/owners/ownerDetails.jsp` inside the `<c:forEach var="pet">` block (e.g., `<dt>Microchip ID</dt><dd><c:out value="${pet.microchipId}"/></dd>`)
- [X] T015 [US1] Run `mvn test` and fix any failures; confirm all 3 profiles pass (JPA, JDBC, Spring Data JPA)

**Checkpoint**: US1 complete — staff can register a microchip ID and see it on the pet profile

---

## Phase 4: User Story 2 - Uniqueness Validation (Priority: P1)

**Goal**: System rejects duplicate microchip IDs with a clear user-facing error message

**Independent Test**: Attempt to save two pets with the same microchip ID and verify the second attempt shows a validation error

### Implementation for User Story 2

- [X] T016 [US2] Verify the `PetValidator` uniqueness check from T012 surfaces correctly in the MVC layer — confirm error message appears in the form when a duplicate is submitted (manual test via browser or `mvn test`)
- [X] T017 [US2] Add format validation test to `src/test/java/org/springframework/samples/petclinic/model/ValidatorTests.java`: test that a 14-digit ID, a 16-digit ID, and a non-numeric ID all fail `@Pattern` validation
- [X] T018 [US2] Add uniqueness service test to `src/test/java/org/springframework/samples/petclinic/service/AbstractClinicServiceTests.java`: save a pet with microchipId, attempt to save another pet with the same microchipId, assert exception or validation error
- [X] T019 [US2] Run `mvn test` and fix any failures

**Checkpoint**: US2 complete — duplicates and invalid formats are rejected with clear messages

---

## Phase 5: User Story 3 - Update or Remove Microchip ID (Priority: P2)

**Goal**: Staff can correct or clear a microchip ID on an existing pet

**Independent Test**: Edit a pet's microchip ID to a new valid value, save, verify updated value shown; then clear it, save, verify it no longer appears

### Implementation for User Story 3

- [X] T020 [US3] Verify the existing pet edit form (T013) already supports update/clear — no new form changes needed; confirm the field is pre-populated with current value when editing
- [X] T021 [US3] Test clearing a microchip ID: set microchipId to empty/null in the form, submit, verify the field is cleared in the database and not displayed in ownerDetails.jsp
- [X] T022 [US3] Run `mvn test` and fix any failures

**Checkpoint**: US3 complete — staff can update or remove microchip IDs without errors

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, JDBC mapping check, and build verification

- [X] T023 [P] Verify JDBC `RowMapper` in `JdbcPetRepositoryImpl.java` correctly maps `microchip_id` to `microchipId` (null-safe) — check `rs.getString("microchip_id")` is present
- [X] T024 [P] Run `mvn spotbugs:check` and fix any reported issues (0 bugs required)
- [X] T025 Run `mvn package` (full build) and confirm it succeeds
- [X] T026 [P] Manual smoke test: start app with `./mvnw jetty:run-war`, navigate to a pet edit form, enter a valid microchip ID, save, verify display

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **Phase 3 (US1)**: Depends on Phase 2 — can start once entity + schemas ready
- **Phase 4 (US2)**: Depends on Phase 3 (T012 must exist for uniqueness test)
- **Phase 5 (US3)**: Depends on Phase 3 (form must exist)
- **Phase 6 (Polish)**: Depends on all story phases complete

### Within Each Phase

- Schema tasks T003–T006 are fully parallel (different files)
- T010, T011 (repository implementations) are parallel (different classes)
- T017, T018 (test additions) are parallel (different test files)

### Parallel Opportunities

```bash
# Phase 2 — all 4 schema files in parallel:
T003: h2/schema.sql
T004: hsqldb/schema.sql
T005: mysql/schema.sql
T006: postgresql/schema.sql

# Phase 3 — repository implementations in parallel:
T010: JPA repository
T011: JDBC repository
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T002)
2. Complete Phase 2: Foundational (T003–T008)
3. Complete Phase 3: User Story 1 (T009–T015)
4. **STOP and VALIDATE**: Register a microchip ID in browser, verify it saves and displays
5. Demo if ready — full CRUD for microchip ID is functional

### Incremental Delivery

1. Setup + Foundational → entity + DB ready
2. US1 → register + display microchip (MVP)
3. US2 → add validation tests and uniqueness checks
4. US3 → confirm update/clear works
5. Polish → spotbugs, full build, smoke test

---

## Notes

- [P] tasks = different files, no shared dependencies — safe to run in parallel
- JDBC `RowMapper` must be updated manually (JPA handles it automatically via `@Column`)
- `microchip_id` column is NULL-able — existing seed data (`data.sql`) needs no changes
- Commit after each phase checkpoint
