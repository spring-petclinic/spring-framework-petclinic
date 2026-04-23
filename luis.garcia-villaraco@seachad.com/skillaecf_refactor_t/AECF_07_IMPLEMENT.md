# AECF_07_IMPLEMENT — Implementación: Eager Loading Fix

## METADATA

| Campo                     | Valor                                                                                 |
|---------------------------|---------------------------------------------------------------------------------------|
| Timestamp (UTC)           | 2026-04-20T00:00:00Z                                                                  |
| Executed By               | Claude Sonnet 4.6                                                                     |
| Executed By ID            | claude-sonnet-4-6                                                                     |
| Execution Identity Source | AECF MCP Dispatch                                                                     |
| Repository                | spring-framework-petclinic                                                            |
| Branch                    | claude/brave-rosalind-f8c323                                                          |
| Root Prompt               | eager_loading_fix — refactor FetchType.EAGER → LAZY en Pet.visits                    |
| Skill Executed            | aecf_refactor / IMPLEMENT                                                             |
| Sequence Position         | 07 / IMPLEMENT                                                                        |
| Total Prompts Executed    | 7                                                                                     |
| Plan aprobado             | AECF_06_AUDIT_PLAN.md — GO                                                            |

---

## Scripts Tocados

| Archivo | Cambio |
|---------|--------|
| `src/main/java/.../service/ClinicService.java` | +2 firmas de método |
| `src/main/java/.../service/ClinicServiceImpl.java` | +`@Transactional` en `findVisitsByPetId` + 2 nuevos métodos |
| `src/main/java/.../repository/jpa/JpaVisitRepositoryImpl.java` | ORDER BY en query JPQL |
| `src/main/java/.../repository/jdbc/JdbcVisitRepositoryImpl.java` | ORDER BY en query SQL |
| `src/main/java/.../repository/springdatajpa/SpringDataVisitRepository.java` | `@Query` con ORDER BY |
| `src/main/java/.../web/VisitController.java` | 2 cambios de invocación de servicio |
| `src/main/java/.../web/OwnerController.java` | 1 cambio de invocación de servicio |
| `src/main/java/.../model/Pet.java` | `FetchType.EAGER` → `FetchType.LAZY` |

---

## Detalle de Cambios por Archivo

### Paso 2 — `ClinicServiceImpl.java`

**Remediación:** Añadir `@Transactional(readOnly=true)` a `findVisitsByPetId()` + implementar 2 nuevos métodos.

```java
// findVisitsByPetId — línea 105-108
@Override
@Transactional(readOnly = true)          // ← añadido
public Collection<Visit> findVisitsByPetId(int petId) {
    return visitRepository.findByPetId(petId);
}

// findPetByIdWithVisits — nuevo
@Override
@Transactional(readOnly = true)
public Pet findPetByIdWithVisits(int id) {
    Pet pet = petRepository.findById(id);
    pet.getVisits();  // inicializa proxy LAZY dentro de la transacción
    return pet;
}

// findOwnerByIdWithPetsAndVisits — nuevo
@Override
@Transactional(readOnly = true)
public Owner findOwnerByIdWithPetsAndVisits(int ownerId) {
    Owner owner = ownerRepository.findById(ownerId);
    for (Pet pet : owner.getPets()) {
        pet.getVisits();  // inicializa visits de cada mascota
    }
    return owner;
}
```

**Rationale:** `Owner.getPets()` es seguro porque `OwnerRepository.findById()` usa `LEFT JOIN FETCH owner.pets` en todas las implementaciones. `pet.getVisits()` es el accessor público que accede internamente al proxy Hibernate, forzando su carga con la sesión aún abierta.

---

### Paso 3 — Repositorios de Visit

#### `JpaVisitRepositoryImpl.java:60`
```java
// ANTES
"SELECT v FROM Visit v where v.pet.id= :id"
// DESPUÉS
"SELECT v FROM Visit v WHERE v.pet.id = :id ORDER BY v.date DESC"
```

#### `JdbcVisitRepositoryImpl.java:87`
```sql
-- ANTES
SELECT id as visit_id, visit_date, description FROM visits WHERE pet_id=:id
-- DESPUÉS
SELECT id as visit_id, visit_date, description FROM visits WHERE pet_id=:id ORDER BY visit_date DESC
```

#### `SpringDataVisitRepository.java`
```java
@Override
@Query("SELECT v FROM Visit v WHERE v.pet.id = :petId ORDER BY v.date DESC")
List<Visit> findByPetId(@Param("petId") Integer petId);
```

**Rationale:** Equivalencia con `Pet.getVisits()` que aplica `Comparator.comparing(Visit::getDate).reversed()`.

---

### Paso 4 — `VisitController.java:87`
```java
// ANTES
model.put("visits", this.clinicService.findPetById(petId).getVisits());
// DESPUÉS
model.put("visits", this.clinicService.findVisitsByPetId(petId));
```

---

### Paso 5 — `VisitController.java:62`
```java
// ANTES
Pet pet = this.clinicService.findPetById(petId);
// DESPUÉS
Pet pet = this.clinicService.findPetByIdWithVisits(petId);
```

**Rationale:** `createOrUpdateVisitForm.jsp:58` accede a `${visit.pet.visits}`. Con este cambio las visitas están inicializadas antes de que cierre la transacción.

---

### Paso 6 — `OwnerController.java:128`
```java
// ANTES
mav.addObject(this.clinicService.findOwnerById(ownerId));
// DESPUÉS
mav.addObject(this.clinicService.findOwnerByIdWithPetsAndVisits(ownerId));
```

**Rationale:** `ownerDetails.jsp:67` accede a `${pet.visits}`. Con este cambio todas las colecciones de visitas están inicializadas antes de que cierre la transacción.

---

### Paso 7 — `Pet.java:60` ← ÚLTIMO
```java
// ANTES
@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.EAGER)
// DESPUÉS
@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.LAZY)
```

---

## Verificación Post-Implementación

Ver resultado de `mvn test` en la sección de post-verificación.

---

## AI_USAGE_DECLARATION

```
AI_USED = FALSE
```

## GOVERNANCE VALIDATION BLOCK

- **Data lineage impact:** No
- **Model impact:** No
- **Risk impact:** Bajo — todos los access points cubiertos antes del cambio de FetchType
- **Compliance check:** Pendiente resultado de test suite
