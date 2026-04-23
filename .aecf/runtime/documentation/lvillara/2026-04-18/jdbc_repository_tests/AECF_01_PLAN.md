---
# AECF_01_PLAN — jdbc_repository_tests

## METADATA

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-04-18T00:00:00Z |
| Executed By | lvillara |
| Executed By ID | lvillara |
| Execution Identity Source | git config user |
| Repository | spring-framework-petclinic |
| Branch | appmod/java-upgrade-20260417115818 |
| Root Prompt | `@aecf run skill=aecf_new_test_set TOPIC=jdbc_repository_tests` |
| Skill Executed | aecf_new_test_set |
| Sequence Position | 1 of 3 (PLAN) |
| Total Prompts Executed | 1 |

---

## WORKING_CONTEXT (Execution-Scoped)

### TARGET_SCOPE
- `JdbcOwnerRepositoryImpl` — JDBC impl of `OwnerRepository` (7 methods)
- `JdbcPetRepositoryImpl` — JDBC impl of `PetRepository` (4 methods + 1 private)
- `JdbcPetVisitExtractor` — `ResultSetExtractor` for pet+visit JOIN (extends `OneToManyResultSetExtractor`)
- `JdbcPetRowMapper` — `RowMapper<JdbcPet>` (5 column mappings)
- `JdbcVisitRowMapper` — `RowMapper<Visit>` (3 column mappings)
- `OneToManyResultSetExtractor` — abstract base class with 4 `ExpectedResults` modes
- `JdbcPet` — internal `Pet` subclass with `typeId` and `ownerId`

Spring profile: `jdbc` | Database: H2 in-memory (`jdbc:h2:mem:petclinic`) | Config: `spring/business-config.xml`

---

### DISCOVERED_MODULES_AND_ROUTINES

**JdbcOwnerRepositoryImpl** (`src/main/java/.../repository/jdbc/JdbcOwnerRepositoryImpl.java`):
| Method | Key Logic |
|--------|-----------|
| `findByLastName(String)` | LIKE `lastName%` query → `BeanPropertyRowMapper<Owner>` → `loadOwnersPetsAndVisits` |
| `findByLastName(String, int, int)` | LIMIT/OFFSET pagination → same loading pipeline |
| `countByLastName(String)` | `COUNT(*)` → `Integer.class` single result |
| `findById(int)` | single-result query, throws `ObjectRetrievalFailureException` on `EmptyResultDataAccessException` |
| `save(Owner)` | branch: `isNew()` → `SimpleJdbcInsert.executeAndReturnKey`; else UPDATE via `JdbcClient` |
| `loadPetsAndVisits(Owner)` | LEFT OUTER JOIN pets+visits → `JdbcPetVisitExtractor` → resolves `PetType` via `EntityUtils.getById` |
| `getPetTypes()` | `SELECT id, name FROM types ORDER BY name` |

**JdbcPetRepositoryImpl** (`src/main/java/.../repository/jdbc/JdbcPetRepositoryImpl.java`):
| Method | Key Logic |
|--------|-----------|
| `findPetTypes()` | `BeanPropertyRowMapper<PetType>` ordered by name |
| `findById(int)` | lookups ownerId first → throws `ObjectRetrievalFailureException`; then owner → `EntityUtils.getById` |
| `save(Pet)` | branch: new → `SimpleJdbcInsert`; existing → UPDATE with `MapSqlParameterSource` |
| `createPetParameterSource(Pet)` | maps: id, name, birth_date, type_id, owner_id — JDBC column names (not Java property names) |

**JdbcPetRowMapper** (`...JdbcPetRowMapper.java`):
- Uses `rs.getInt("pets.id")` — **table-qualified column name** (risk area)
- Uses `rs.getObject("birth_date", LocalDate.class)` — JDBC 4.2 LocalDate direct mapping
- Maps: typeId, ownerId, name

**JdbcVisitRowMapper** (`...JdbcVisitRowMapper.java`):
- Maps: `visit_id` (int), `visit_date` (LocalDate), `description` (String)

**JdbcPetVisitExtractor** (`...JdbcPetVisitExtractor.java`):
- `mapPrimaryKey` → `rs.getInt("pets.id")`
- `mapForeignKey` → `rs.getObject("visits.pet_id") == null ? null : rs.getInt("visits.pet_id")` — **null-safe NULL handling for pets with no visits**
- `addChild` → `root.addVisit(child)`

**OneToManyResultSetExtractor** (`...OneToManyResultSetExtractor.java`):
- `extractData` — loops ResultSet, groups children by key equality, handles empty RS
- `ExpectedResults` modes: `ANY`, `ONE_AND_ONLY_ONE`, `ONE_OR_NONE`, `AT_LEAST_ONE`
- Throws `IncorrectResultSizeDataAccessException` when constraints violated

---

### EXISTING_TEST_SURFACE

`ClinicServiceJdbcTests` (inherits `AbstractClinicServiceTests`):

| Test | What It Covers | Gap |
|------|---------------|-----|
| `shouldFindOwnersByLastName` | findByLastName(String) returns 2 Davis owners | ✅ Happy path |
| `shouldFindSingleOwnerWithPet` | findById(1) with 1 pet + type | ✅ But only 1 pet, 0 visits verified |
| `shouldInsertOwner` | new Owner → ID generated | ✅ |
| `shouldUpdateOwner` | existing Owner → lastName updated | ✅ |
| `shouldFindPetWithCorrectId` | findById(7) — name, owner | ✅ |
| `shouldFindAllPetTypes` | findPetTypes() — id=1 cat, id=4 snake | ✅ |
| `shouldInsertPetIntoDatabaseAndGenerateId` | new Pet → ID generated | ✅ |
| `shouldUpdatePetName` | existing Pet → name updated | ✅ |
| `shouldAddNewVisitForPet` | save visit + verify count | ✅ |
| `shouldFindVisitsByPetId` | 2 visits for pet 7 | ✅ |
| `shouldCountOwnersByLastName` | count Davis=2, empty prefix, non-existent | ✅ |
| `shouldFindOwnersByLastNameWithPagination` | page 1+2 of size 5 non-overlapping | ✅ |
| `shouldReturnEmptyPageBeyondRange` | page 99 → empty | ✅ |
| `shouldReturnSingleOwnerOnFirstPage` | Franklin on page 1 | ✅ |

**Total existing JDBC tests**: 14 (all inherited generic contract tests)

---

### RISK_AREAS

| # | Area | Risk Level | Gap |
|---|------|-----------|-----|
| R1 | `JdbcPetRowMapper` — table-qualified `"pets.id"` column name | 🔴 HIGH | 0 unit tests. Wrong column alias breaks entire pet loading silently |
| R2 | `JdbcPetVisitExtractor` — null FK path (pet with no visits) | 🔴 HIGH | Not tested: `mapForeignKey` returns null, extractor takes else branch |
| R3 | `OneToManyResultSetExtractor` — ExpectedResults constraint violations | 🟠 MEDIUM | 0 tests for `ONE_AND_ONLY_ONE`/`AT_LEAST_ONE` throwing `IncorrectResultSizeDataAccessException` |
| R4 | `JdbcOwnerRepositoryImpl.findById` — non-existent ID → exception | 🟠 MEDIUM | Exception path not tested in AbstractClinicServiceTests |
| R5 | `JdbcPetRepositoryImpl.findById` — non-existent ID → exception | 🟠 MEDIUM | Exception path not tested |
| R6 | Owner with multiple pets + multiple visits each | 🟠 MEDIUM | Existing test (owner 1) has 1 pet; multi-pet grouping untested |
| R7 | `JdbcVisitRowMapper` column mapping | 🟡 LOW | 0 unit tests; exercised indirectly |
| R8 | `JdbcPetRowMapper.birth_date` as `LocalDate` via JDBC 4.2 | 🟡 LOW | Exercised indirectly but not unit-verified |
| R9 | `createPetParameterSource` JDBC column names vs Java property names | 🟡 LOW | "birth_date" vs "birthDate" subtle mapping risk |
| R10 | `OneToManyResultSetExtractor` — empty ResultSet → empty list | 🟡 LOW | Not explicitly asserted |

---

### TEST_COMMANDS_AND_TOOLING

```bash
# Run all JDBC-profile tests
./mvnw test -Dspring.profiles.active=jdbc

# Run specific test class (once created)
./mvnw test -Dspring.profiles.active=jdbc -Dtest=JdbcRepositoryUnitTests
./mvnw test -Dspring.profiles.active=jdbc -Dtest=JdbcOwnerRepositoryIntegrationTests

# Run all service tests with jdbc profile
./mvnw test -Dtest=ClinicServiceJdbcTests

# Coverage report
./mvnw test jacoco:report -Dspring.profiles.active=jdbc
```

**Test infrastructure**: JUnit 5, Spring TestContext Framework, H2 in-memory, `@SpringJUnitConfig`, `@Transactional` (auto-rollback), no Mockito in current codebase.

---

## PLAN

### Objective
Identify and close test gaps in the JDBC repository layer — specifically in `JdbcOwnerRepositoryImpl`, `JdbcPetRepositoryImpl`, and the three supporting JDBC infrastructure classes (`JdbcPetRowMapper`, `JdbcVisitRowMapper`, `JdbcPetVisitExtractor`, `OneToManyResultSetExtractor`).

### Coverage Goal
- **Current**: 14 tests, all at service-contract level (no JDBC-specific assertions)
- **Target**: Add 12–16 new tests covering:
  - RowMapper correctness (unit, with mock `ResultSet`)
  - Extractor grouping correctness (unit, with mock `ResultSet`)
  - Exception paths in both repositories (integration, jdbc profile)
  - Multi-pet multi-visit owner loading (integration, jdbc profile)

### Test Boundary
- **New test classes**: 2 proposed
  - `JdbcPetRowMapperTests` — unit, no Spring context
  - `JdbcOwnerRepositoryIntegrationTests` — integration, `@ActiveProfiles("jdbc")`
- **No production code changes**: this skill is test-only
- **Not in scope**: VetRepository JDBC impl (separate topic), controller layer

### Implementation Boundaries
- Follow existing test package structure: `src/test/java/org/springframework/samples/petclinic/repository/jdbc/`
- Use `Mockito` for unit tests of RowMappers (mock `ResultSet`) — **requires Mockito already on test classpath** (verify before implementation)
- Use H2 + Spring test context for integration tests (same as `ClinicServiceJdbcTests`)
- Every test MUST include `AECF_META` comment on generation

### Risk Prioritization
1. R1 (JdbcPetRowMapper unit) — highest isolation risk
2. R2 (null FK extractor path) — silent data loss risk
3. R4, R5 (exception paths) — error handling coverage
4. R6 (multi-pet loading correctness) — correctness of JDBC grouping
5. R3 (ExpectedResults modes) — defensive coverage of `OneToManyResultSetExtractor`
6. R7, R8, R9, R10 — low-risk completeness

---

## SCOPE SUMMARY

| Component | Test Type | # Tests Planned |
|-----------|-----------|----------------|
| `JdbcPetRowMapper` | Unit (mock ResultSet) | 2 |
| `JdbcVisitRowMapper` | Unit (mock ResultSet) | 2 |
| `JdbcPetVisitExtractor` / `OneToManyResultSetExtractor` | Unit (mock ResultSet) | 4 |
| `JdbcOwnerRepositoryImpl` — exception + multi-pet | Integration (jdbc+H2) | 4 |
| `JdbcPetRepositoryImpl` — exception + createParameterSource | Integration (jdbc+H2) | 3 |
| **Total new tests** | | **~15** |
