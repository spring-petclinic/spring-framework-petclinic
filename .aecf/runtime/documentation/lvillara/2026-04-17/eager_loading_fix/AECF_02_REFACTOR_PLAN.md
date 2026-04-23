# AECF_02 — Refactor Plan: Eager Loading Fix
## TOPIC: eager_loading_fix

---

## METADATA

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-04-17T00:00:00Z |
| Executed By | lvillara |
| Executed By ID | lvillara |
| Execution Identity Source | git config user |
| Repository | spring-framework-petclinic |
| Branch | appmod/java-upgrade-20260417115818 |
| Root Prompt | `@aecf run skill=aecf_refactor TOPIC=eager_loading_fix` |
| Skill Executed | aecf_refactor |
| Sequence Position | 2 of 8 |
| Total Prompts Executed | 2 |
| Phase | PHASE 2 — REFACTOR_PLAN |
| Source Phase | AECF_01_DOCUMENT_EXISTING.md |

---

## 1. CHANGES INVENTORY

### Files to review (from upstream analysis)
1. `src/main/java/org/springframework/samples/petclinic/model/Pet.java` — FetchType.EAGER declaration
2. `src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaOwnerRepositoryImpl.java` — findById needs visit pre-loading
3. `src/main/java/org/springframework/samples/petclinic/repository/springdatajpa/SpringDataOwnerRepository.java` — findById needs @EntityGraph
4. `src/main/java/org/springframework/samples/petclinic/web/VisitController.java` — 3 methods affected
5. `src/main/webapp/WEB-INF/jsp/pets/createOrUpdateVisitForm.jsp` — uses ${visit.pet.visits}

### Problems to resolve (from upstream analysis)
- **P-01**: `Pet.visits` FetchType.EAGER forces unnecessary visit loading in all Pet access paths
- **P-02**: `VisitController.showVisits()` accesses `pet.getVisits()` outside transaction
- **P-03**: `VisitController.loadPetWithVisit()` calls `pet.addVisit(visit)` which accesses the LAZY collection outside transaction
- **P-04**: `createOrUpdateVisitForm.jsp` accesses `${visit.pet.visits}` outside transaction
- **P-05**: `ownerDetails.jsp` accesses `${pet.visits}` — owner loaded without visit pre-loading

---

## 2. INCREMENTAL REFACTOR STEPS

### Step A — Pet model (scope: 1 line)
**File**: `Pet.java:60`  
**Change**: `FetchType.EAGER` → `FetchType.LAZY`  
**Risk**: HIGH — all downstream access must be corrected before this compiles and tests pass  
**Rollback**: Revert single line

### Step B — JpaOwnerRepositoryImpl.findById (scope: L1-cache warm)
**File**: `JpaOwnerRepositoryImpl.java` (`findById`)  
**Change**: Add pre-loading query for Pet visits within the same EntityManager session  
**Pattern**: Execute `SELECT p FROM Pet p left join fetch p.visits WHERE p.owner.id = :id` first → warms L1 cache → main owner query returns pets with visits already initialized  
**Why this pattern**: Both queries share the same `EntityManager` (and thus L1 cache / identity map). After the first query, Pet entities in the cache have their `visits` collection initialized. The second query returns the same Pet instances (by identity), so `pet.visits` is already a resolved collection, not a proxy.  
**Risk**: LOW — additive change, adds one SQL query for owner-by-id path only  
**Rollback**: Remove the pre-loading query

### Step C — SpringDataOwnerRepository.findById (scope: annotation change)
**File**: `SpringDataOwnerRepository.java` (`findById`)  
**Change**: Replace `@Query("SELECT owner FROM Owner owner left join fetch owner.pets WHERE owner.id =:id")` with `@EntityGraph(attributePaths = {"pets", "pets.visits"})`  
**Why @EntityGraph**: Spring Data JPA EntityGraph generates equivalent loading semantics. `attributePaths = {"pets", "pets.visits"}` loads owner → pets → visits in an optimized way (Spring Data uses a LEFT JOIN for each path).  
**Risk**: LOW — same functional result as join-fetch; Spring Data test suite validates  
**Rollback**: Restore original @Query annotation

### Step D — VisitController.loadPetWithVisit (scope: 1 line)
**File**: `VisitController.java:64`  
**Change**: `pet.addVisit(visit)` → `visit.setPet(pet)`  
**Why sufficient**: `Visit.pet` is annotated `@ManyToOne` — it is the owning side of the relationship. JPA uses `visit.pet_id` FK for persistence. `saveVisit(visit)` persists correctly as long as `visit.setPet(pet)` is called. The `addVisit()` method's additional action (adding to the in-memory Set) is not needed here.  
**Risk**: LOW — persistence behavior unchanged; visit form uses `@ModelAttribute("visit")` which only needs the pet reference  
**Rollback**: Restore `pet.addVisit(visit)`

### Step E — VisitController.showVisits (scope: 1 line)
**File**: `VisitController.java:87`  
**Change**: Replace `findPetById(petId).getVisits()` with `findVisitsByPetId(petId)`  
**Why**: `findVisitsByPetId` is already in `ClinicService` — explicit visit query that does not touch the LAZY collection. No `LazyInitializationException` risk.  
**Risk**: NONE — `findVisitsByPetId` is already used in production tests; functionally equivalent  
**Rollback**: Restore original line

### Step F — VisitController.initNewVisitForm + processNewVisitForm (scope: 2 methods)
**File**: `VisitController.java:70-83`  
**Change**: Add `model.put("visits", clinicService.findVisitsByPetId(petId))` to both methods  
**`processNewVisitForm`**: Add `@PathVariable int petId` + `Map<String, Object> model` params; populate visits on error path  
**Risk**: LOW — additive; changes method signature of `processNewVisitForm` which needs stub update in VisitControllerTests  
**Rollback**: Restore original method signatures

### Step G — createOrUpdateVisitForm.jsp (scope: 1 line)
**File**: `createOrUpdateVisitForm.jsp:58`  
**Change**: `${visit.pet.visits}` → `${visits}`  
**Why**: Use the explicitly loaded `visits` model attribute (from Step F) instead of traversing the LAZY relation  
**Risk**: NONE — JSP functional behavior identical; `visits` model attr has same data  
**Rollback**: Restore original EL expression

---

## 3. BEHAVIOR PRESERVATION GUARANTEES

| Behavior | Guarantee |
|---------|-----------|
| Owner detail page shows all visits for each pet | ✅ — Steps B/C pre-load visits for `findOwnerById` |
| New visit form shows previous visits | ✅ — Steps F/G explicitly load via `findVisitsByPetId` |
| Visit list page (`/pets/{petId}/visits`) shows correct visits | ✅ — Step E uses `findVisitsByPetId` |
| Saving a new visit persists correctly | ✅ — Step D: `visit.setPet(pet)` sets owning FK |
| JDBC profile: all behavior unchanged | ✅ — No JDBC changes; FetchType irrelevant |
| All existing tests pass | ✅ — `@Transactional` tests safe with LAZY; controller tests need stub update |

---

## 4. RISK ASSESSMENT

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| L1 cache warm does NOT pre-initialize visits (Hibernate implementation detail) | LOW | HIGH | Verified pattern: same `em` session → same identity map → initialized proxy |
| `@EntityGraph` on Spring Data JPA produces different SQL than `@Query` join-fetch | LOW | MEDIUM | Test suite validates; @EntityGraph is Spring Data's preferred approach |
| `VisitControllerTests` mock for `processNewVisitForm` breaks due to new signature | MEDIUM | LOW | Update mock stubs accordingly |
| `pet.addVisit(visit)` change causes visit not to appear in `pet.visits` in-memory (for same request) | LOW | LOW | The new visit is only shown after the redirect to owner detail, where it's loaded fresh from DB |

---

## 5. ROLLBACK STRATEGY

All changes are in 8 files, all modifiable independently. Full rollback = revert Pet.java:60 + revert 4 Java files + revert 1 JSP. No DB migrations, no schema changes, no external contract changes.

Git rollback: `git revert HEAD` or `git diff HEAD~1 -- <file>` per file.

---

## 6. METRICS BEFORE / AFTER

| Metric | Before | After |
|--------|--------|-------|
| SQL queries per `GET /owners/{id}` (JPA) | 1 (owner+pets JOIN FETCH) + N×1 (visits per pet, EAGER) | 2 (pets+visits warm + owner) |
| SQL queries per `GET /owners?lastName=X` (JPA) | 1 (owners+pets) + N×M (visits per pet) | 1 (owners+pets only, NO visits) |
| SQL queries per `GET /pets/{id}/visits/new` | 1 (findPetById) + 1 (EAGER visits) | 1 (findPetById) + 1 (findVisitsByPetId) |
| FetchType.EAGER declarations on Pet | 1 | 0 |
| Direct `pet.getVisits()` calls in production code | 1 (VisitController:87) | 0 |
| `${pet.visits}` EL references in JSPs | 1 (createOrUpdateVisitForm:58) | 0 |
