---

description: Task list for feature implementation

---

# Tasks: Pet Microchip ID

**Feature Branch**: `002-add-microchip-id`
**Input**: specs/002-microchip-id/

---

## Phase 1: Setup

- [X] T001 Verify project compiles with `./mvnw compile`

---

## Phase 2: Data Layer (Foundational)

- [X] T002 Add microchipId field to Pet.java
- [X] T003 Add getter/setter for microchipId in Pet.java
- [X] T004 Update HSQLDB schema.sql
- [X] T005 Update H2 schema.sql
- [X] T006 Update MySQL schema.sql
- [X] T007 Update PostgreSQL schema.sql

---

## Phase 3: UI Layer (User Story 1 - MVP)

- [X] T008 Add microchipId input to createOrUpdatePetForm.jsp
- [X] T009 Display microchip ID on ownerDetails.jsp

---

## Phase 4: Testing (MANDATORY per Constitution)

- [X] T010 Run mvn test and save results to automatizacion/logs/test_mvn_{timestamp}.md
- [ ] T011 Run Playwright E2E tests and save results to automatizacion/logs/test_playwright_{timestamp}.md
- [X] T012 Run SpotBugs check and save results to automatizacion/logs/test_spotbugs_{timestamp}.md
- [ ] T013 Fix any test failures (re-run speckit.implement with error log if needed)

**Testing Loop**: Repeat T010-T013 until ALL tests pass (max 5 iterations)

**Current Status**:
- mvn test: ✅ PASS (84 tests, 0 failures)
- Playwright: ⏳ SKIPPED (Jetty timeout - manual verification needed)
- SpotBugs: ✅ PASS (0 bugs)

---

## Phase 5: Polish (Optional)

- [ ] T014 Handle duplicate microchip ID errors gracefully
- [ ] T015 Search pets by microchip ID (US2)

---

## Summary

- **Total Tasks**: 15
- **Completed**: 9 (T001-T009)
- **In Progress**: Testing Phase (T010-T013)
- **Pending**: Polish (T014-T015)

**MVP Status**: ✓ Core implementation complete - Now testing required