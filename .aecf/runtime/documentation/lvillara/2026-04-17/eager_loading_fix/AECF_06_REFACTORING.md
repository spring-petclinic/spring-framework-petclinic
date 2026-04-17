# AECF_06 — Refactoring Record: Eager Loading Fix
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
| Sequence Position | 6 of 8 |
| Phase | PHASE 6 — REFACTORING |

---

## 1. CHANGES APPLIED

### Step A — `Pet.java:60`
```java
// Before:
@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.EAGER)
// After:
@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.LAZY)
```

### Step B — `JpaOwnerRepositoryImpl.java` — `findById`
Added L1-cache warm pre-query. Both queries use `this.em` (same identity map), so Pet entities returned by the main query already have `visits` initialized.
```java
this.em.createQuery(
    "SELECT p FROM Pet p left join fetch p.visits WHERE p.owner.id = :id", Pet.class)
    .setParameter("id", id)
    .getResultList();
```
Added import: `import org.springframework.samples.petclinic.model.Pet;`

### Step C — `SpringDataOwnerRepository.java` — `findById`
Replaced `@Query` join-fetch (pets only) with `@EntityGraph` including `pets`, `pets.visits`, and `pets.type`.
```java
@EntityGraph(attributePaths = {"pets", "pets.visits", "pets.type"})
Owner findById(@Param("id") int id);
```
**Note**: `pets.type` was added after test run revealed that `@EntityGraph` overrides the default EAGER for `@ManyToOne` associations, causing `LazyInitializationException` on `PetType#1` in `shouldFindSingleOwnerWithPet`.

### Step D — `VisitController.java` — `loadPetWithVisit`
```java
// Before:
pet.addVisit(visit);
// After:
visit.setPet(pet);
```

### Step E — `VisitController.java` — `showVisits`
```java
// Before:
model.put("visits", this.clinicService.findPetById(petId).getVisits());
// After:
model.put("visits", this.clinicService.findVisitsByPetId(petId));
```

### Step F — `VisitController.java` — `initNewVisitForm`
```java
// Added:
model.put("visits", this.clinicService.findVisitsByPetId(petId));
```

### Step G — `VisitController.java` — `processNewVisitForm`
Added `@PathVariable int petId, Map<String, Object> model` parameters. Added visits on error path:
```java
if (result.hasErrors()) {
    model.put("visits", this.clinicService.findVisitsByPetId(petId));
    return "pets/createOrUpdateVisitForm";
}
```

### Step H — `createOrUpdateVisitForm.jsp:58`
```jsp
<!-- Before: -->
<c:forEach var="visit" items="${visit.pet.visits}">
<!-- After: -->
<c:forEach var="visit" items="${visits}">
```

---

## 2. DEVIATION FROM PLAN

| Deviation | Reason |
|-----------|--------|
| `@EntityGraph` extended to include `pets.type` | `@EntityGraph` overrides Hibernate's default EAGER fetch for `@ManyToOne`, causing `LazyInitializationException` on `PetType` in `shouldFindSingleOwnerWithPet`. Adding `pets.type` restores the original eager behavior for this association. |

---

## 3. FILES MODIFIED

| File | Change Type |
|------|-------------|
| `src/main/java/.../model/Pet.java` | 1-line annotation change |
| `src/main/java/.../repository/jpa/JpaOwnerRepositoryImpl.java` | findById rewrite + Pet import |
| `src/main/java/.../repository/springdatajpa/SpringDataOwnerRepository.java` | @EntityGraph annotation |
| `src/main/java/.../web/VisitController.java` | 4 method changes |
| `src/main/webapp/WEB-INF/jsp/pets/createOrUpdateVisitForm.jsp` | 1-line EL expression change |
| `src/test/java/.../web/VisitControllerTests.java` | Import + stub in setup() |

---

## 4. FILES NOT MODIFIED (as planned)

- `JdbcOwnerRepositoryImpl.java` — JDBC unaffected by FetchType
- `ClinicService.java` / `ClinicServiceImpl.java` — `findVisitsByPetId` already exists
- `ownerDetails.jsp` — unchanged; visits now loaded correctly by repository layer
- `AbstractClinicServiceTests.java` — no test changes needed
