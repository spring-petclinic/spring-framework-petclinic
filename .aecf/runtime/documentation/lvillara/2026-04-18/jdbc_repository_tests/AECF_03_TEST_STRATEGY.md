---
# AECF_03_TEST_STRATEGY — jdbc_repository_tests

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
| Sequence Position | 3 of 3 (TEST_STRATEGY) |
| Total Prompts Executed | 1 |

---

## AUDIT GATE: GO ✅ (from AECF_02_AUDIT_PLAN)

---

## Fixture Data (H2 `data.sql` — verified)

| Owner | Name | Pets | Visits per Pet |
|-------|------|------|---------------|
| 1 | George Franklin | 1 (Leo, cat, no visits) | 0 |
| 3 | Eduardo Rodriquez | 2 (Rosy dog, Jewel dog) | 0 each |
| 6 | Jean Coleman | 2 (Samantha cat pet7, Max cat pet8) | 2 each (pet7: visits 1+4; pet8: visits 2+3) |
| 10 | Carlos Estaban | 2 (Lucky dog pet12, Sly cat pet13) | 0 each |
| Types | 6 total | bird(5), cat(1), dog(2), hamster(6), lizard(3), snake(4) — ordered by name |

---

## Infrastructure Confirmed

| Fact | Value |
|------|-------|
| Mockito | ✅ mockito-core 5.23.0 + mockito-junit-jupiter on test classpath |
| JUnit | JUnit 5 (junit-jupiter 6.0.2) |
| Spring test | `@SpringJUnitConfig`, `@ActiveProfiles("jdbc")` |
| H2 data | `spring/datasource-config.xml` via `@SpringJUnitConfig(locations={"classpath:spring/business-config.xml"})` |
| Output language | Spanish (consistent with project prior artifacts) |

---

## New Test Classes

### Class 1: `JdbcRowMapperTests`
**Location**: `src/test/java/org/springframework/samples/petclinic/repository/jdbc/JdbcRowMapperTests.java`  
**Type**: Unit — no Spring context, Mockito `@ExtendWith(MockitoExtension.class)`  
**Dependencies**: `mockito-core`, `JdbcPetRowMapper`, `JdbcVisitRowMapper`

### Class 2: `JdbcPetVisitExtractorTests`
**Location**: `src/test/java/org/springframework/samples/petclinic/repository/jdbc/JdbcPetVisitExtractorTests.java`  
**Type**: Unit — no Spring context, Mockito  
**Dependencies**: `JdbcPetVisitExtractor`, `OneToManyResultSetExtractor`, mock `ResultSet`

### Class 3: `JdbcOwnerRepositoryIntegrationTests`
**Location**: `src/test/java/org/springframework/samples/petclinic/repository/jdbc/JdbcOwnerRepositoryIntegrationTests.java`  
**Type**: Integration — `@SpringJUnitConfig`, `@ActiveProfiles("jdbc")`, `@Transactional`  
**Dependencies**: `JdbcOwnerRepositoryImpl` autowired, H2

### Class 4: `JdbcPetRepositoryIntegrationTests`
**Location**: `src/test/java/org/springframework/samples/petclinic/repository/jdbc/JdbcPetRepositoryIntegrationTests.java`  
**Type**: Integration — `@SpringJUnitConfig`, `@ActiveProfiles("jdbc")`, `@Transactional`  
**Dependencies**: `JdbcPetRepositoryImpl` autowired, H2

---

## Test Catalogue

### CLASS 1 — JdbcRowMapperTests

---

#### T01 — JdbcPetRowMapper: mapeo correcto de todas las columnas
**Risk**: R1 🔴 (table-qualified column name `"pets.id"`)  
**Category**: RowMapper correctness  
**Mandatory**: YES

**Setup**: Mock `ResultSet` con Mockito.
- `rs.getInt("pets.id")` → 42
- `rs.getString("name")` → "Leo"
- `rs.getObject("birth_date", LocalDate.class)` → `LocalDate.of(2010, 9, 7)`
- `rs.getInt("type_id")` → 1
- `rs.getInt("owner_id")` → 1

**Assertions**:
```java
assertThat(pet.getId()).isEqualTo(42);
assertThat(pet.getName()).isEqualTo("Leo");
assertThat(pet.getBirthDate()).isEqualTo(LocalDate.of(2010, 9, 7));
assertThat(pet.getTypeId()).isEqualTo(1);
assertThat(pet.getOwnerId()).isEqualTo(1);
```

**Why critical**: The column name `"pets.id"` (table-qualified) is only valid in a JOIN query context. If refactored to `"id"`, data loads silently broken. This test pins the contract.

---

#### T02 — JdbcPetRowMapper: birth_date null devuelve null (LocalDate nullable)
**Risk**: R8 🟡  
**Category**: Edge case — null handling  
**Mandatory**: YES

**Setup**: Mock RS donde `rs.getObject("birth_date", LocalDate.class)` → `null`

**Assertions**:
```java
assertThat(pet.getBirthDate()).isNull();
```

---

#### T03 — JdbcVisitRowMapper: mapeo correcto de visit_id, visit_date y description
**Risk**: R7 🟡  
**Category**: RowMapper correctness  
**Mandatory**: YES

**Setup**: Mock RS:
- `rs.getInt("visit_id")` → 7
- `rs.getObject("visit_date", LocalDate.class)` → `LocalDate.of(2013, 1, 1)`
- `rs.getString("description")` → "rabies shot"

**Assertions**:
```java
assertThat(visit.getId()).isEqualTo(7);
assertThat(visit.getDate()).isEqualTo(LocalDate.of(2013, 1, 1));
assertThat(visit.getDescription()).isEqualTo("rabies shot");
```

---

#### T04 — JdbcVisitRowMapper: description null no lanza excepción
**Risk**: R7 🟡  
**Category**: Edge case  
**Mandatory**: NO (optional — defensive)

**Setup**: Mock RS donde `rs.getString("description")` → `null`

**Assertions**:
```java
assertThat(visit.getDescription()).isNull();
```

---

### CLASS 2 — JdbcPetVisitExtractorTests

Mock strategy for ResultSet: use `Mockito.when(rs.next())` to control row iteration. Each `when(rs.getInt("pets.id"))` returns the current pet id; `when(rs.getObject("visits.pet_id"))` returns the FK or null.

> **Note**: Mockito mock ResultSet requires careful sequencing of `rs.next()` answers using `thenReturn(true, true, ..., false)`.

---

#### T05 — Extractor con ResultSet vacío devuelve lista vacía
**Risk**: R10 🟡  
**Category**: Edge case — empty RS  
**Mandatory**: YES

**Setup**: `rs.next()` returns `false` immediately.

**Assertions**:
```java
assertThat(result).isEmpty();
```

---

#### T06 — Extractor: mascota sin visitas usa rama null del FK (mapForeignKey retorna null)
**Risk**: R2 🔴 (HIGHEST — silent data loss if null branch broken)  
**Category**: Null FK path  
**Mandatory**: YES

**Setup**: 1 row — pet id=1, FK=null (simulating LEFT JOIN with no visit).
- `rs.next()` → true, then false
- `rs.getInt("pets.id")` → 1
- `rs.getObject("visits.pet_id")` → null (triggers null check in `mapForeignKey`)

**Assertions**:
```java
assertThat(result).hasSize(1);
assertThat(result.get(0).getId()).isEqualTo(1);
assertThat(result.get(0).getVisits()).isEmpty();
```

**Why critical**: The `mapForeignKey` null check (`rs.getObject("visits.pet_id") == null`) prevents visit from being attached to pet. If broken, the `while` loop fails silently or throws NPE.

---

#### T07 — Extractor: mascota con múltiples visitas agrupa correctamente todos los hijos
**Risk**: R2 🔴 / R6 🟠  
**Category**: Child grouping  
**Mandatory**: YES

**Setup**: 2 rows for same pet (pet id=7), with 2 different visit FKs.
- Row 1: pets.id=7, visits.pet_id=7, visit_id=1
- Row 2: pets.id=7, visits.pet_id=7, visit_id=4

**Assertions**:
```java
assertThat(result).hasSize(1);
assertThat(result.get(0).getVisits()).hasSize(2);
```

---

#### T08 — Extractor: múltiples mascotas cada una con sus visitas, agrupación correcta
**Risk**: R6 🟠  
**Category**: Multi-root grouping  
**Mandatory**: YES

**Setup**: 4 rows — pet 7 with 2 visits, pet 8 with 2 visits (like owner 6 Jean Coleman).
- Row 1: pets.id=7, visits.pet_id=7, visit_id=1
- Row 2: pets.id=7, visits.pet_id=7, visit_id=4
- Row 3: pets.id=8, visits.pet_id=8, visit_id=2
- Row 4: pets.id=8, visits.pet_id=8, visit_id=3

**Assertions**:
```java
assertThat(result).hasSize(2);
assertThat(result.get(0).getId()).isEqualTo(7);
assertThat(result.get(0).getVisits()).hasSize(2);
assertThat(result.get(1).getId()).isEqualTo(8);
assertThat(result.get(1).getVisits()).hasSize(2);
```

---

#### T09 — OneToManyResultSetExtractor: ONE_AND_ONLY_ONE con 2 roots lanza excepción
**Risk**: R3 🟠  
**Category**: ExpectedResults constraint  
**Mandatory**: YES

**Setup**: Concrete anonymous subclass con `expectedResults=ONE_AND_ONLY_ONE`, RS con 2 root rows.

**Assertions**:
```java
assertThatThrownBy(() -> extractor.extractData(rs))
    .isInstanceOf(IncorrectResultSizeDataAccessException.class);
```

---

#### T10 — OneToManyResultSetExtractor: AT_LEAST_ONE con RS vacío lanza excepción
**Risk**: R3 🟠  
**Category**: ExpectedResults constraint  
**Mandatory**: YES

**Setup**: Concrete subclass con `expectedResults=AT_LEAST_ONE`, RS vacío.

**Assertions**:
```java
assertThatThrownBy(() -> extractor.extractData(rs))
    .isInstanceOf(IncorrectResultSizeDataAccessException.class);
```

---

### CLASS 3 — JdbcOwnerRepositoryIntegrationTests

Context: `@SpringJUnitConfig(locations={"classpath:spring/business-config.xml"})`, `@ActiveProfiles("jdbc")`, `@Transactional`.  
Autowired: `JdbcOwnerRepositoryImpl ownerRepository`.

---

#### T11 — findById con ID inexistente lanza ObjectRetrievalFailureException
**Risk**: R4 🟠  
**Category**: Exception path  
**Mandatory**: YES

**Assertions**:
```java
assertThatThrownBy(() -> ownerRepository.findById(9999))
    .isInstanceOf(ObjectRetrievalFailureException.class);
```

---

#### T12 — loadPetsAndVisits para owner 6 (Jean Coleman): 2 mascotas, 2 visitas cada una, tipo resuelto
**Risk**: R6 🟠  
**Category**: Multi-pet correctness, PetType resolution via EntityUtils  
**Mandatory**: YES

**Fixture**: Owner 6 (Jean Coleman): pet 7 (Samantha, cat, visits 1+4), pet 8 (Max, cat, visits 2+3).

**Assertions**:
```java
Owner jean = ownerRepository.findById(6);
assertThat(jean.getPets()).hasSize(2);

Pet samantha = jean.getPets().stream()
    .filter(p -> p.getName().equals("Samantha")).findFirst().orElseThrow();
assertThat(samantha.getVisits()).hasSize(2);
assertThat(samantha.getType()).isNotNull();
assertThat(samantha.getType().getName()).isEqualTo("cat");

Pet max = jean.getPets().stream()
    .filter(p -> p.getName().equals("Max")).findFirst().orElseThrow();
assertThat(max.getVisits()).hasSize(2);
assertThat(max.getType().getName()).isEqualTo("cat");
```

**Why critical**: Validates the full JDBC extractor pipeline end-to-end — JdbcPetVisitExtractor grouping + PetType resolution — at integration level with real H2 data.

---

#### T13 — loadPetsAndVisits para owner 1 (George Franklin): 1 mascota sin visitas
**Risk**: R2 🔴  
**Category**: Null FK path — integration confirmation  
**Mandatory**: YES

**Fixture**: Owner 1 (George Franklin): pet 1 (Leo, cat, 0 visits).

**Assertions**:
```java
Owner george = ownerRepository.findById(1);
assertThat(george.getPets()).hasSize(1);
assertThat(george.getPets().get(0).getName()).isEqualTo("Leo");
assertThat(george.getPets().get(0).getVisits()).isEmpty();
assertThat(george.getPets().get(0).getType().getName()).isEqualTo("cat");
```

---

#### T14 — getPetTypes retorna los 6 tipos ordenados por nombre
**Risk**: R — gap in coverage  
**Category**: Query correctness  
**Mandatory**: NO (optional — confirming ORDER BY)

**Assertions**:
```java
Collection<PetType> types = ownerRepository.getPetTypes();
assertThat(types).hasSize(6);
List<String> names = types.stream().map(PetType::getName).toList();
assertThat(names).isSorted(); // ordered by name
assertThat(names).containsExactly("bird", "cat", "dog", "hamster", "lizard", "snake");
```

---

### CLASS 4 — JdbcPetRepositoryIntegrationTests

Context: same Spring config, `@ActiveProfiles("jdbc")`, `@Transactional`.  
Autowired: `JdbcPetRepositoryImpl petRepository`.

---

#### T15 — findById con ID inexistente lanza ObjectRetrievalFailureException
**Risk**: R5 🟠  
**Category**: Exception path  
**Mandatory**: YES

**Assertions**:
```java
assertThatThrownBy(() -> petRepository.findById(9999))
    .isInstanceOf(ObjectRetrievalFailureException.class);
```

---

#### T16 — save nueva mascota: SimpleJdbcInsert genera ID y persiste birth_date, type_id, owner_id
**Risk**: R9 🟡  
**Category**: createPetParameterSource JDBC column names  
**Mandatory**: YES

**Setup**: Owner 6, new pet, type_id=2 (dog), birth_date=2020-01-15.

**Assertions** (after `petRepository.findById(newId)`):
```java
assertThat(saved.getName()).isEqualTo("Buddy");
assertThat(saved.getBirthDate()).isEqualTo(LocalDate.of(2020, 1, 15));
assertThat(saved.getType().getName()).isEqualTo("dog");
assertThat(saved.getOwner().getId()).isEqualTo(6);
```

**Why**: Validates `createPetParameterSource` maps "birth_date"/"type_id"/"owner_id" (JDBC names) correctly, not "birthDate"/"typeId"/"ownerId" (Java property names).

---

#### T17 — findPetTypes retorna 6 tipos ordenados por nombre
**Risk**: gap in direct coverage  
**Category**: Query correctness  
**Mandatory**: NO (optional)

**Assertions**:
```java
List<PetType> types = petRepository.findPetTypes();
assertThat(types).hasSize(6);
assertThat(types.stream().map(PetType::getName).toList())
    .containsExactly("bird", "cat", "dog", "hamster", "lizard", "snake");
```

---

## Test Summary

### Mandatory Tests (must implement)

| ID | Class | Description | Risk |
|----|-------|-------------|------|
| T01 | JdbcRowMapperTests | JdbcPetRowMapper: all columns mapped (table-qualified "pets.id") | 🔴 R1 |
| T02 | JdbcRowMapperTests | JdbcPetRowMapper: null birth_date | 🟡 R8 |
| T03 | JdbcRowMapperTests | JdbcVisitRowMapper: visit_id, visit_date, description | 🟡 R7 |
| T05 | JdbcPetVisitExtractorTests | Empty RS → empty list | 🟡 R10 |
| T06 | JdbcPetVisitExtractorTests | Pet with no visits (null FK path) | 🔴 R2 |
| T07 | JdbcPetVisitExtractorTests | Pet with multiple visits → all grouped | 🔴 R2 |
| T08 | JdbcPetVisitExtractorTests | Multiple pets + multiple visits → correct grouping | 🟠 R6 |
| T09 | JdbcPetVisitExtractorTests | ONE_AND_ONLY_ONE with 2 roots → exception | 🟠 R3 |
| T10 | JdbcPetVisitExtractorTests | AT_LEAST_ONE empty RS → exception | 🟠 R3 |
| T11 | JdbcOwnerRepositoryIntegrationTests | findById non-existent → ObjectRetrievalFailureException | 🟠 R4 |
| T12 | JdbcOwnerRepositoryIntegrationTests | Owner 6: 2 pets × 2 visits each, PetType resolved | 🟠 R6 |
| T13 | JdbcOwnerRepositoryIntegrationTests | Owner 1: 1 pet, 0 visits, PetType resolved | 🔴 R2 |
| T15 | JdbcPetRepositoryIntegrationTests | findById non-existent → ObjectRetrievalFailureException | 🟠 R5 |
| T16 | JdbcPetRepositoryIntegrationTests | save new pet → birth_date, type_id, owner_id persisted | 🟡 R9 |

**Total mandatory**: 14 tests

### Optional Tests

| ID | Class | Description | Risk |
|----|-------|-------------|------|
| T04 | JdbcRowMapperTests | JdbcVisitRowMapper: null description | 🟡 R7 |
| T14 | JdbcOwnerRepositoryIntegrationTests | getPetTypes: 6 types ordered | low |
| T17 | JdbcPetRepositoryIntegrationTests | findPetTypes: 6 types ordered | low |

**Total optional**: 3 tests

**Grand total**: 17 tests across 4 classes

---

## Recommended Execution Commands

```bash
# Ejecutar solo los tests de repositorio JDBC (unit + integration)
./mvnw test -Dspring.profiles.active=jdbc \
  -Dtest="JdbcRowMapperTests,JdbcPetVisitExtractorTests,JdbcOwnerRepositoryIntegrationTests,JdbcPetRepositoryIntegrationTests"

# Ejecutar toda la suite con perfil jdbc (incluye ClinicServiceJdbcTests)
./mvnw test -Dspring.profiles.active=jdbc

# Generar reporte de cobertura JaCoCo
./mvnw test jacoco:report -Dspring.profiles.active=jdbc

# Reporte HTML en target/site/jacoco/index.html
```

---

## Risk Coverage Map

| Risk | # Tests | Covered By |
|------|---------|-----------|
| R1 🔴 JdbcPetRowMapper table-qualified column | 2 | T01, T16 (indirect) |
| R2 🔴 Null FK extractor path | 3 | T06, T07, T13 |
| R3 🟠 ExpectedResults modes | 2 | T09, T10 |
| R4 🟠 findById exception (Owner) | 1 | T11 |
| R5 🟠 findById exception (Pet) | 1 | T15 |
| R6 🟠 Multi-pet loading correctness | 2 | T08, T12 |
| R7 🟡 JdbcVisitRowMapper | 2 | T03, T04 |
| R8 🟡 LocalDate birth_date nullable | 1 | T02 |
| R9 🟡 createPetParameterSource JDBC names | 1 | T16 |
| R10 🟡 Empty RS | 1 | T05 |

---

## Approval Gate

> **Do I implement and execute the proposed tests?**

Please reply:
- `Sí` / `Yes` — procedo con la implementación de los 14 tests obligatorios (+ 3 opcionales si lo deseas)
- `No` — se detiene aquí, queda el diseño documentado para implementación posterior
