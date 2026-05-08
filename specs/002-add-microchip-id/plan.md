# Implementation Plan: Add Microchip ID

**Branch**: `002-add-microchip-id` | **Date**: 2026-05-06 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-add-microchip-id/spec.md`

## Summary

Add a `microchipId` field to the `Pet` entity for official pet identification. The field must be optional, globally unique across all pets, and validated for the ISO 11784/11785 format (15-digit numeric string). Implementation covers all layers: data (entity + schema), service (uniqueness validation), UI (form input + display), and tests.

---

## Technical Context

**Language/Version**: Java 17
**Primary Dependencies**: Spring Framework, JPA/Hibernate, Jakarta Bean Validation
**Storage**: H2 (default), MySQL, PostgreSQL
**Testing**: JUnit, Mockito, Playwright
**Target Platform**: Web (JSP + Spring MVC)

**Project Type**: Web application (Spring MVC)
**Performance Goals**: Standard web app — validation response within 1 second
**Constraints**: Must maintain 3-layer architecture; backward-compatible schema; uniqueness enforced at DB + service level
**Scale/Scope**: Single feature, low complexity

---

## Phase 0: Research

### Decision: Uniqueness Enforcement Strategy

- **Decision**: Enforce uniqueness at both the database level (UNIQUE constraint on `microchip_id` column) and the service level (check before save)
- **Rationale**: DB constraint is the safety net; service-level check provides a user-friendly error message before hitting the DB
- **Alternatives considered**: Only DB constraint (no user-friendly error), only service check (race condition risk)

### Decision: microchipId Format

- **Decision**: 15-digit numeric string per ISO 11784/11785; stored as `VARCHAR(15)` (not integer to preserve leading zeros)
- **Rationale**: Microchip IDs can have leading zeros; storing as integer would lose them
- **Alternatives considered**: `BIGINT` (leading zero loss), `VARCHAR(255)` (too permissive)

### Decision: Validation Approach

- **Decision**: Use Jakarta Bean Validation `@Pattern(regexp = "\\d{15}")` on the entity field, plus `@Column(unique = true)`. Custom validator in `PetValidator` for duplicate check.
- **Rationale**: Consistent with existing project validation patterns (e.g., `ValidatorTests`)
- **Alternatives considered**: Custom `ConstraintValidator` class (overkill for this scope)

---

## Data Model

### Modified Entities

| Entity | New Attributes | Location |
|--------|----------------|----------|
| Pet | `microchipId: String` (nullable, unique) | `src/main/java/org/springframework/samples/petclinic/model/Pet.java` |

### Database Changes

| File | Change |
|------|--------|
| `src/main/resources/db/h2/schema.sql` | Add `microchip_id VARCHAR(15) UNIQUE` to `pets` table |
| `src/main/resources/db/hsqldb/schema.sql` | Add `microchip_id VARCHAR(15) UNIQUE` to `pets` table |
| `src/main/resources/db/mysql/schema.sql` | Add `microchip_id VARCHAR(15) UNIQUE` to `pets` table |
| `src/main/resources/db/postgresql/schema.sql` | Add `microchip_id VARCHAR(15) UNIQUE` to `pets` table |

> All columns are nullable (no default needed) — existing seed data remains valid.

---

## UI Layer (REQUIRED)

### JSP Files to Modify

| File | Purpose | Change |
|------|---------|--------|
| `src/main/webapp/WEB-INF/jsp/pets/createOrUpdatePetForm.jsp` | Pet create/edit form | Add `<petclinic:inputField label="Microchip ID" name="microchipId"/>` |
| `src/main/webapp/WEB-INF/jsp/owners/ownerDetails.jsp` | Owner details / pet list | Add `<dd><c:out value="${pet.microchipId}"/></dd>` in pet info section |

---

## Implementation Phases

### Phase 1: Data Layer

- [ ] Add `microchipId` field to `Pet.java` with `@Column(name = "microchip_id", unique = true)` and `@Pattern(regexp = "\\d{15}", message = "Microchip ID must be exactly 15 digits")`
- [ ] Add getter/setter for `microchipId` in `Pet.java`
- [ ] Update `src/main/resources/db/h2/schema.sql` — add `microchip_id VARCHAR(15) UNIQUE NULL`
- [ ] Update `src/main/resources/db/hsqldb/schema.sql`
- [ ] Update `src/main/resources/db/mysql/schema.sql`
- [ ] Update `src/main/resources/db/postgresql/schema.sql`
- [ ] Verify: `mvn compile` must pass

**Files**: `src/main/java/.../model/Pet.java`, `src/main/resources/db/*/schema.sql`

### Phase 2: Service Layer

- [ ] Add uniqueness check in `PetValidator.java` (or equivalent): reject if `microchipId` is non-null and already used by another pet
- [ ] Expose `findPetByMicrochipId(String id)` in `ClinicService` interface and implementations (JPA, JDBC, Spring Data JPA) for the uniqueness check
- [ ] Add corresponding repository query

**Files**: `src/main/java/.../service/`, `src/main/java/.../repository/`, `src/main/java/.../web/PetValidator.java`

### Phase 3: UI Layer (REQUIRED)

- [ ] Add microchip input field in `createOrUpdatePetForm.jsp` using `petclinic:inputField` tag
- [ ] Add microchip display in `ownerDetails.jsp` inside the pet info block
- [ ] Verify form shows microchip ID field and validation errors render correctly

**Files**: `src/main/webapp/WEB-INF/jsp/pets/createOrUpdatePetForm.jsp`, `src/main/webapp/WEB-INF/jsp/owners/ownerDetails.jsp`

### Phase 4: Testing (REQUIRED)

- [ ] Add unit test in `ValidatorTests.java` for `@Pattern` validation on microchipId (valid, invalid length, non-numeric)
- [ ] Add service test in `AbstractClinicServiceTests.java` for uniqueness enforcement
- [ ] Add MVC test in `PetControllerTests.java` for form submission with duplicate microchip ID
- [ ] Run: `mvn test` (must pass on all 3 profiles: JPA, JDBC, Spring Data JPA)
- [ ] Run: `mvn spotbugs:check` (0 bugs)
- [ ] Run: `pytest` E2E tests (must pass)
- [ ] Fix any failures and re-run until ALL pass

---

## Constitution Check

| Principle | Required | Status |
|-----------|----------|--------|
| Full-stack (data + service + UI + tests) | MANDATORY | [x] Planned |
| UI Layer included (JSP forms + display) | REQUIRED | [x] Planned |
| Tests pass before PR | REQUIRED | [ ] To verify |
| Schema backward-compatible (nullable column) | REQUIRED | [x] Nullable — no default needed |
| Convention-First (extends NamedEntity/BaseEntity, uses petclinic tags) | REQUIRED | [x] Planned |
| Uniqueness enforced at DB + service level | REQUIRED | [x] Planned |

---

## Dependencies

| Task | Depends On |
|------|------------|
| Service Layer | Data Layer (entity field must exist) |
| UI Layer | Data Layer (getter/setter must exist) |
| Tests | All layers complete |
| PR | All tests passing |

---

## Risks & Open Questions

- **JDBC mapping**: The JDBC repository (`JdbcPetRepositoryImpl`) uses manual `RowMapper` — `microchip_id` must be explicitly mapped there too (not just JPA).
- **Null uniqueness**: H2 and PostgreSQL treat multiple NULLs as distinct in UNIQUE constraints; MySQL may differ — verify behavior across all three.
- **Race condition**: Two simultaneous registrations with the same ID could both pass the service check before either commits — DB UNIQUE constraint is the final guard.
