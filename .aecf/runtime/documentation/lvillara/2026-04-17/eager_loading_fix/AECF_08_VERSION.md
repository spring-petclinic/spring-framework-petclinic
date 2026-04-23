# AECF_08 — Version Record: Eager Loading Fix
## TOPIC: eager_loading_fix

---

## METADATA

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-04-17T00:00:00Z |
| Executed By | lvillara |
| Repository | spring-framework-petclinic |
| Branch | appmod/java-upgrade-20260417115818 |
| Skill Executed | aecf_refactor |
| Sequence Position | 8 of 8 |
| Phase | PHASE 8 — VERSION |

---

## SemVer

| Field | Value |
|-------|-------|
| Before | 7.1.0 |
| After | 7.1.1 |
| Change Type | PATCH |

**Rationale**: Internal behavior change only. Public API, URL mappings, JSP structure, and ClinicService interface are all unchanged. No new features, no breaking changes.

---

## Summary

Changed `Pet.visits` from `FetchType.EAGER` to `FetchType.LAZY` to eliminate N+1 visit queries on owner list and pet update paths. All three access points that required visit data were fixed:

1. `ownerDetails.jsp` — covered by JPA L1-cache warm (JPA profile) and `@EntityGraph(pets, pets.visits, pets.type)` (Spring Data JPA profile)
2. `createOrUpdateVisitForm.jsp` — controller now explicitly loads visits via `findVisitsByPetId`; JSP uses `${visits}` model attribute
3. `VisitController.showVisits` — replaced `pet.getVisits()` with `findVisitsByPetId(petId)`

Additionally fixed `VisitController.loadPetWithVisit` to use `visit.setPet(pet)` instead of `pet.addVisit(visit)` to avoid touching the LAZY collection outside a transaction.

---

## Query Count Impact

| Scenario | Before (EAGER) | After (LAZY) |
|----------|----------------|--------------|
| `GET /owners?lastName=X` (N owners, M pets each) | 1 + N×M queries | 1 query |
| `GET /owners/{id}` (JPA) | 1 + N queries | 2 queries |
| `GET /owners/{id}` (Spring Data JPA) | 1 + N queries | 1 query (EntityGraph JOIN) |
| `GET /pets/{id}/visits/new` | 1 + 1 (EAGER) | 1 + 1 (explicit findVisitsByPetId) |

---

## Files Changed

6 production files + 1 test file. No DB schema changes. No migration required.
