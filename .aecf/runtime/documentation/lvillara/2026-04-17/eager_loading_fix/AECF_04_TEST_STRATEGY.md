# AECF_04 — Test Strategy: Eager Loading Fix
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
| Sequence Position | 4 of 8 |
| Phase | PHASE 4 — TEST_STRATEGY |

---

## 1. EXISTING TESTS THAT COVER THE CHANGE

| Test Class | Test Method | Coverage |
|------------|-------------|----------|
| `AbstractClinicServiceTests` | `shouldFindSingleOwnerWithPet` | Verifies `pet.getType()` accessible after `findOwnerById` (LazyInit risk on `pets.type`) |
| `AbstractClinicServiceTests` | `shouldAddNewVisitForPet` | Verifies `pet.getVisits()` within `@Transactional` — safe with LAZY |
| `ClinicServiceSpringDataJpaTests` | (inherits all 15) | Executes all `AbstractClinicServiceTests` against Spring Data JPA profile |
| `ClinicServiceJpaTests` | (inherits all 15) | Executes all against JPA profile |
| `ClinicServiceJdbcTests` | (inherits all 15) | Executes all against JDBC profile (FetchType irrelevant) |
| `VisitControllerTests` | `testInitNewVisitForm` | Verifies view name |
| `VisitControllerTests` | `testProcessNewVisitFormSuccess` | Verifies redirect |
| `VisitControllerTests` | `testProcessNewVisitFormHasErrors` | Verifies error path returns form view |
| `VisitControllerTests` | `testShowVisits` | Verifies `visits` model attribute present |

---

## 2. TEST GAPS

No new regression tests needed. The existing test suite covers all modified code paths:

- `shouldFindSingleOwnerWithPet`: exercises `findOwnerById` → `@EntityGraph` (Spring Data) / L1-cache warm (JPA)
- `shouldAddNewVisitForPet`: exercises `pet.getVisits()` within transaction — LAZY safe
- `VisitControllerTests`: exercises all 4 modified controller methods with `findVisitsByPetId` stub

---

## 3. STUB UPDATES REQUIRED

| File | Change |
|------|--------|
| `VisitControllerTests.setup()` | Add `given(clinicService.findVisitsByPetId(TEST_PET_ID)).willReturn(Collections.emptyList())` |

---

## 4. PRE-BASELINE VERIFICATION COMMAND

```bash
JAVA_HOME="C:/Users/Ryzen/.jdk/jdk-21.0.8" ./mvnw test
```

Expected pre-baseline (before IMPLEMENT): compile error or `LazyInitializationException` on `Pet.visits` once `FetchType.LAZY` is applied without downstream fixes.

Expected post-implementation: 87 tests pass, 0 failures.

---

## 5. PROFILE COVERAGE

| Profile | Config | LAZY Fix Required |
|---------|--------|-------------------|
| JPA | `JpaOwnerRepositoryImpl` | ✅ L1-cache warm in `findById` |
| Spring Data JPA | `SpringDataOwnerRepository` | ✅ `@EntityGraph({"pets","pets.visits","pets.type"})` |
| JDBC | `JdbcOwnerRepositoryImpl` | ❌ N/A — explicit SQL joins |
