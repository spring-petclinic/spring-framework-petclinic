# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Summary

[Extract from feature spec: primary requirement + technical approach]

---

## Technical Context

**Language/Version**: Java 17
**Primary Dependencies**: Spring Framework, JPA/Hibernate
**Storage**: H2 (default), MySQL, PostgreSQL  
**Testing**: JUnit, Mockito, Playwright
**Target Platform**: Web (JSP)

**Project Type**: Web application (Spring MVC)
**Performance Goals**: [domain-specific]
**Constraints**: Must maintain 3-layer architecture; backward-compatible schema
**Scale/Scope**: [single feature, low complexity]

---

## Data Model

### Modified Entities

| Entity | New Attributes | Location |
|--------|---------------|----------|
| Pet | photoUrl | src/main/java/.../model/Pet.java |
| [Other] | [+newField: Type] | [Location] |

### Database Changes

| File | Change |
|------|--------|
| schema.sql (hsqldb, h2, mysql, postgresql) | ADD COLUMN photo_url VARCHAR(255) |

---

## UI Layer (REQUIRED)

### JSP Files to Modify

| File | Purpose | Change |
|------|---------|--------|
| createOrUpdatePetForm.jsp | Pet form | Add input field for photoUrl |
| ownerDetails.jsp | Owner details | Add photo display |
| [Other JSP] | [Purpose] | [Change] |

**Location**: `src/main/webapp/WEB-INF/jsp/pets/` and `src/main/webapp/WEB-INF/jsp/owners/`

---

## Implementation Phases

### Phase 1: Data Layer

- [ ] Modify entity: src/main/java/.../model/Pet.java
- [ ] Update schema.sql (all DB variants)
- [ ] Test: mvn compile (must pass)

**Files**: `src/main/java/.../model/`, `src/main/resources/db/`

### Phase 2: Service Layer

- [ ] Add getter/setter if needed to service
- [ ] Add business logic

**Files**: `src/main/java/.../service/`

### Phase 3: UI Layer (REQUIRED)

- [ ] Modify createOrUpdatePetForm.jsp - add photoUrl field
- [ ] Modify ownerDetails.jsp - display photo
- [ ] Verify in browser

**Files**: `src/main/webapp/WEB-INF/jsp/pets/`, `src/main/webapp/WEB-INF/jsp/owners/`

### Phase 4: Testing (REQUIRED)

- [ ] Run: mvn test (must pass)
- [ ] Run: mvn spotbugs:check (0 bugs)
- [ ] Run: pytest E2E tests (must pass)
- [ ] Fix any failures and re-run until ALL pass

---

## Constitution Check

| Principle | Required | Status |
|-----------|----------|--------|
| Full-stack (data+service+UI+tests) | MANDATORY | [ ] |
| UI Layer included | REQUIRED | [ ] |
| Tests pass before PR | REQUIRED | [ ] |
| Schema backward-compatible | REQUIRED | [ ] |

---

## Dependencies

| Task | Depends On |
|------|------------|
| UI Layer | Data Layer |
| Tests | All layers |

---

## Risks & Open Questions

- [Risk/Question description]