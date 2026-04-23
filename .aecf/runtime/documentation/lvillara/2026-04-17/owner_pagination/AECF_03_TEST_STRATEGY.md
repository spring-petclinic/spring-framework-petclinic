# AECF_03 — Test Strategy: Owner Pagination
## TOPIC: owner_pagination

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
| Root Prompt | `@aecf run skill=aecf_new_feature TOPIC=owner_pagination` |
| Skill Executed | aecf_new_feature |
| Sequence Position | 3 of N |
| Total Prompts Executed | 3 |
| Phase | PHASE 3 — TEST_STRATEGY |
| Source Phase | AECF_02_AUDIT_PLAN.md (GO) |

---

## 1. TESTING APPROACH

**Strategy**: Integration tests via `AbstractClinicServiceTests` — heredados por los 3 perfiles.

No se requieren unit tests adicionales para `ClinicServiceImpl` (delegación directa sin lógica propia). El `OwnerController` no se testea directamente (no hay MockMvc en el proyecto — sigue el patrón existente de tests de servicio).

**Test data base**: `src/test/resources/db/hsqldb/data.sql` — Los datos existentes incluyen:
- 6 owners en total
- `Davis` aparece 2 veces (Linda Davis, Rafael Ortega) — útil para probar > 1 resultado
- `Franklin` aparece 1 vez — útil para probar redirect (1 resultado)
- `Coleman` aparece 1 vez

Para testear paginación necesitamos ≥6 owners con el mismo apellido (o prefijo). Los datos de test actuales tienen pocos matches de apellido. Estrategia: usar `lastName = ""` para obtener todos los owners (6 total), que con PAGE_SIZE=5 genera 2 páginas.

---

## 2. TEST CASES

### TC-01: `shouldCountOwnersByLastName`

```java
@Test
void shouldCountOwnersByLastName() {
    // "" prefix matches all owners
    int count = this.clinicService.countOwnersByLastName("");
    assertThat(count).isGreaterThan(0);
    
    // "Davis" matches exactly 2 owners in test data
    int davisCount = this.clinicService.countOwnersByLastName("Davis");
    assertThat(davisCount).isEqualTo(2);
    
    // Non-existent name
    int noneCount = this.clinicService.countOwnersByLastName("XxNonExistentXx");
    assertThat(noneCount).isEqualTo(0);
}
```

**Data dependency**: `data.sql` debe tener exactamente 2 owners con `last_name LIKE 'Davis%'`.

### TC-02: `shouldFindOwnersByLastNameWithPagination`

```java
@Test
void shouldFindOwnersByLastNameWithPagination() {
    // Buscar todos (lastName="") — hay 6 owners en test data
    // Page 1, size 5 → debe devolver 5
    Collection<Owner> page1 = this.clinicService.findOwnerByLastName("", 1, 5);
    assertThat(page1).hasSize(5);
    
    // Page 2, size 5 → debe devolver 1 (el restante)
    Collection<Owner> page2 = this.clinicService.findOwnerByLastName("", 2, 5);
    assertThat(page2).hasSize(1);
    
    // Los owners de las 2 páginas no se solapan (IDs distintos)
    java.util.Set<Integer> page1Ids = page1.stream()
        .map(Owner::getId).collect(java.util.stream.Collectors.toSet());
    java.util.Set<Integer> page2Ids = page2.stream()
        .map(Owner::getId).collect(java.util.stream.Collectors.toSet());
    assertThat(page1Ids).doesNotContainAnyElementsOf(page2Ids);
}
```

**Data dependency**: Exactamente 6 owners en `data.sql`.

### TC-03: `shouldReturnEmptyPageBeyondRange`

```java
@Test
void shouldReturnEmptyPageBeyondRange() {
    // Página fuera de rango
    Collection<Owner> beyondPage = this.clinicService.findOwnerByLastName("Davis", 99, 5);
    assertThat(beyondPage).isEmpty();
}
```

### TC-04: `shouldReturnFirstPageSingleResult`

```java
@Test
void shouldReturnFirstPageSingleResult() {
    // "Franklin" = 1 owner. Page 1, size 5 → 1 resultado
    Collection<Owner> results = this.clinicService.findOwnerByLastName("Franklin", 1, 5);
    assertThat(results).hasSize(1);
    assertThat(results.iterator().next().getLastName()).isEqualTo("Franklin");
}
```

---

## 3. VERIFICATION REQUIREMENTS FOR EXISTING TESTS

Los tests existentes en `AbstractClinicServiceTests` NO deben modificarse:
- `shouldFindOwnersByLastName()` → llama `findOwnerByLastName(String)` (firma original, sin paginación) — permanece intacto.

Todos los tests heredados deben seguir pasando en los 3 perfiles tras la implementación.

---

## 4. DATA DEPENDENCIES

| Test | Datos requeridos | Fuente | Verificación |
|------|-----------------|--------|-------------|
| TC-01 | 2 owners con last_name LIKE 'Davis%' | `data.sql` | Leer `data.sql` en IMPLEMENT |
| TC-02 | Exactamente 6 owners totales | `data.sql` | Verificado en fuente |
| TC-03 | N/A — fuera de rango retorna vacío | — | Test de borde |
| TC-04 | 1 owner con last_name LIKE 'Franklin%' | `data.sql` | Verificado en fuente |

---

## 5. PROFILES COVERED

Todos los tests de `AbstractClinicServiceTests` son ejecutados por:
- `ClinicServiceJpaTests` (`@ActiveProfiles("jpa")`)
- `ClinicServiceJdbcTests` (`@ActiveProfiles("jdbc")`)
- `ClinicServiceSpringDataJpaTests` (`@ActiveProfiles("spring-data-jpa")`)

→ Los 4 nuevos TCs se verifican automáticamente en los 3 perfiles.
