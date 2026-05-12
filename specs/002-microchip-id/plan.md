# Implementation Plan: Pet Microchip ID

**Feature Branch**: `002-add-microchip-id`
**Created**: 2026-05-11
**Status**: Implementation Ready
**Input**: User description: "Requisito #2: Microchip ID - Campo microchipId"

---

## Context

PetClinic needs to store and display official microchip identification numbers for pets, following ISO 11784/11785 standard. This enables pet recovery and regulatory compliance.

---

## Tech Stack

- **Language**: Java 17
- **Framework**: Spring Framework (non-Boot)
- **Build**: Maven
- **Persistence**: Spring Data JPA, H2 (default), MySQL, PostgreSQL
- **View Layer**: JSP + JSTL + Spring MVC tags
- **E2E Testing**: Playwright via pytest

---

## Project Structure

```
src/main/java/org/springframework/samples/petclinic/
├── model/
│   └── Pet.java                    # Add microchipId field
├── repository/
│   └── PetRepository.java          # No changes needed
├── service/
│   └── ClinicService.java          # No changes needed
└── web/
    └── (controllers unchanged)    # No changes needed

src/main/resources/
├── db/
│   ├── hsqldb/schema.sql
│   ├── h2/schema.sql
│   ├── mysql/schema.sql
│   └── postgresql/schema.sql       # Add microchip_id column

src/main/webapp/WEB-INF/jsp/
├── pets/
│   └── createOrUpdatePetForm.jsp  # Add microchipId input
└── owners/
    └── ownerDetails.jsp           # Display microchip ID

automatizacion/scripts/tests_e2e/
└── test_petclinic_e2e.py          # E2E tests for microchip feature
```

---

## Data Model

### Pet Entity Changes

| Field | Type | Constraints |
|-------|------|-------------|
| microchipId | String | VARCHAR(15), UNIQUE, nullable |

**Validation**: 15 alphanumeric characters (ISO 11784/11785 standard)

---

## Implementation Notes

1. **Entity**: Add `microchipId` field with getter/setter to Pet.java
2. **Schema**: Update all 4 database schemas with `microchip_id` column
3. **Form**: Add microchip ID input to pet creation/edit form
4. **Display**: Show microchip ID on owner details page
5. **Tests**: All 3 test types MUST pass per constitution

---

## Testing Requirements (MANDATORY per Constitution)

After implementation, MUST run and pass ALL three test types:

1. **mvn test**: `./mvnw clean test`
2. **Playwright E2E**: `playwright test automatizacion/scripts/tests_e2e/test_petclinic_e2e.py`
3. **SpotBugs**: `./mvnw spotbugs:check` (threshold=High, ignore Low/Medium)

**Save test results to automatizacion/logs/** after each run.

If any test fails: run `speckit.implement` with error log to fix.