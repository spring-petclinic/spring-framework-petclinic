# AECF_01 — Document Existing Behavior: Eager Loading Fix
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
| Root Prompt | `@aecf run skill=aecf_refactor TOPIC=eager_loading_fix prompt="El modelo Pet tiene una relación OneToMany con Visit mapeada como FetchType.EAGER..."` |
| Skill Executed | aecf_refactor |
| Sequence Position | 1 of 8 |
| Total Prompts Executed | 1 |
| Phase | PHASE 1 — DOCUMENT_EXISTING |

---

## 1. ENTRY POINTS AND PUBLIC API

### Entity: `Pet.java:60`
```java
@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.EAGER)
private Set<Visit> visits;
```
- **Public contract**: `pet.getVisits()` returns `List<Visit>` sorted by date descending (unmodifiable)
- **Internal accessor**: `pet.getVisitsInternal()` returns `Set<Visit>` (protected, null-safe)
- **Mutator**: `pet.addVisit(Visit)` — adds visit to internal set AND sets `visit.setPet(this)`

### Service: `ClinicService` + `ClinicServiceImpl`
- `findPetById(int id)` → `Pet` — triggers EAGER load of visits in JPA profiles
- `findOwnerById(int id)` → `Owner` with pets → each pet triggers EAGER load of visits
- `findVisitsByPetId(int petId)` → `Collection<Visit>` — explicit visit query, independent of FetchType

---

## 2. CURRENT BEHAVIOR BY PROFILE

### Profile `jpa` — `JpaOwnerRepositoryImpl` / `JpaPetRepositoryImpl`

**findOwnerById(id)**:
```
em.createQuery("SELECT owner FROM Owner owner left join fetch owner.pets WHERE owner.id =:id")
→ Hibernate loads owner + pets via JOIN FETCH
→ For each Pet in the result, visits are loaded EAGERLY (additional SELECT * FROM visits WHERE pet_id IN (...))
→ Total: 1 SQL (owner+pets) + 1 SQL per unique pet (visits) OR 1 batched IN query
```

**findPetById(id)**:
```
em.find(Pet.class, id)
→ Hibernate loads Pet
→ visits loaded EAGERLY immediately
→ Total: 1 SQL (pet) + 1 SQL (visits for that pet)
```

### Profile `jdbc` — `JdbcOwnerRepositoryImpl`
```
findByLastName / findById → loadPetsAndVisits(owner)
→ SQL: SELECT pets.*, visits.* FROM pets LEFT OUTER JOIN visits ON pets.id = pet_id WHERE owner_id=:id
→ Visits ALWAYS loaded via explicit SQL JOIN — FetchType annotation has NO EFFECT
```
JDBC profile behavior is IDENTICAL before and after the refactor.

### Profile `spring-data-jpa` — `SpringDataOwnerRepository`
- `findById`: `@Query("SELECT owner FROM Owner owner left join fetch owner.pets WHERE owner.id =:id")`
- Loads owner+pets explicitly. Pet.visits loaded EAGERLY due to FetchType.EAGER (additional query)
- `findByLastName`: similar pattern; visits loaded EAGERLY for all matching pets

---

## 3. ALL ACCESS POINTS TO `pet.getVisits()` (complete inventory)

| Location | Line | Context | Session state at call |
|----------|------|---------|----------------------|
| `web/VisitController.java` | 87 | `findPetById(petId).getVisits()` → model | Outside JPA transaction |
| `webapp/WEB-INF/jsp/owners/ownerDetails.jsp` | 67 | `${pet.visits}` (EL) | Outside JPA transaction (JSP rendering) |
| `webapp/WEB-INF/jsp/pets/createOrUpdateVisitForm.jsp` | 58 | `${visit.pet.visits}` (EL) | Outside JPA transaction (JSP rendering) |
| `test/.../model/PetTests.java` | 24, 43, 62 | Unit tests on detached Pet object | No JPA transaction (unit test) |
| `test/.../service/AbstractClinicServiceTests.java` | 180, 188 | `pet7.getVisits().size()` in `shouldAddNewVisitForPet` | Inside `@Transactional` test |

---

## 4. WHERE VISITS ARE CURRENTLY LOADED UNNECESSARILY

| Code Path | Reason visits are NOT needed | Current behavior |
|-----------|------------------------------|-----------------|
| `OwnerController.processFindForm()` → `findOwnerByLastName()` | `ownersList.jsp` only shows pet names | EAGER load of ALL visits for ALL result owners |
| `OwnerController.initUpdateOwnerForm()` → `findOwnerById()` | Update form shows owner fields only | EAGER load of ALL visits for ALL owner's pets |
| `OwnerController.processUpdateOwnerForm()` | Same | EAGER triggered on form submit |
| `PetController.initUpdateForm()` → `findPetById()` | Pet update form shows pet fields only | EAGER load of ALL visits for that pet |
| `PetController.processCreationForm()` | Pet creation | EAGER triggered |
| `VisitController.loadPetWithVisit()` → `findPetById()` | Only needs pet identity for new visit; reads visits only to add new item | EAGER load of ALL existing visits |

---

## 5. SIDE EFFECTS OF CURRENT EAGER LOADING

1. **Extra SQL queries**: Every `findPetById()` or `findOwnerById()` (JPA profiles) emits additional SELECT on `visits` table — even when the caller never touches visits
2. **Memory overhead**: All Visit objects deserialized and held in memory for the duration of the request
3. **Performance**: Owner search returning N owners with M pets each → N×M visit queries (pre-pagination: up to 10 owners × ~2 pets = ~20 extra queries per search)
4. **Hibernate comment acknowledged it** (`JpaOwnerRepositoryImpl.java:47-52`): "we load Owners with all their Pets and Visits while we do not need Visits at all"

---

## 6. DEPENDENCIES

- **Internal**: `Pet` ← `Owner` (ManyToOne), `Visit` → `Pet` (ManyToOne, owning side)
- **External to Pet.visits**: `ClinicServiceImpl.findVisitsByPetId()` → `VisitRepository.findByPetId()` — independent path that bypasses FetchType
- **Profiles affected**: JPA, Spring Data JPA (visits load via Hibernate proxy). JDBC: not affected.

---

## 7. CURRENT TEST COVERAGE

| Test | File | Visits usage |
|------|------|-------------|
| `shouldAddNewVisitForPet` | AbstractClinicServiceTests:177 | `pet7.getVisits().size()` — within `@Transactional` |
| `shouldFindVisitsByPetId` | AbstractClinicServiceTests:192 | uses `findVisitsByPetId()` |
| `PetTests.*getVisits*` | PetTests:24,43,62 | Unit tests on detached Pet (no JPA) |
| `VisitControllerTests` | VisitControllerTests | Controller behavior (4 tests) |
