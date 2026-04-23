# AECF_04_AUDIT_PLAN — Segunda Auditoría del Plan (sobre FIX_PLAN): Eager Loading Fix

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
| Skill Executed            | aecf_refactor / AUDIT_PLAN (ronda 2)                                                  |
| Sequence Position         | 04 / AUDIT_PLAN                                                                       |
| Total Prompts Executed    | 4                                                                                     |
| Artifact Auditado         | AECF_03_FIX_PLAN.md                                                                   |

---

## Veredicto

> ## ⛔ NO-GO
> El FIX_PLAN contiene **2 nuevas brechas** que producirían un error de compilación (G-03) y una regresión de ordenación en el perfil Spring Data JPA (G-04). Se requiere un segundo FIX_PLAN.

---

## Checklist de Auditoría

| Criterio | Estado | Detalle |
|----------|--------|---------|
| ¿Se corrige G-01 (createOrUpdateVisitForm)? | ✅ Sí | Paso 5: `findPetByIdWithVisits()` cubre el JSP |
| ¿Se corrige G-02 (ORDER BY en findByPetId)? | ⚠️ Parcial | Paso 3 cubre JPA y JDBC, pero omite `SpringDataVisitRepository` |
| ¿La implementación de Paso 5 compila? | ⛔ No | `getVisitsInternal()` es `protected` — inaccesible desde `ClinicServiceImpl` |
| ¿Se cubre el tercer acceso `findPetById` en PetController? | ✅ Sí | `createOrUpdatePetForm.jsp` no accede a visits — verificado |
| ¿La estrategia de rollback es válida? | ✅ Sí | Sin cambios al respecto |
| ¿La secuencia de pasos es segura? | ✅ Sí | Orden correcto, LAZY sigue siendo el último |
| ¿El scope está acotado? | ✅ Sí | No hay expansión injustificada |

---

## Brechas Identificadas

### G-03 — CRÍTICA: Error de compilación — `getVisitsInternal()` es `protected`

**Evidencia — FIX_PLAN Paso 5B:**
```java
// ClinicServiceImpl.java (org.springframework.samples.petclinic.service)
@Transactional(readOnly = true)
public Pet findPetByIdWithVisits(int id) {
    Pet pet = petRepository.findById(id);
    Hibernate.initialize(pet.getVisitsInternal());  // ← ERROR DE COMPILACIÓN
    return pet;
}
```

**Causa:** `getVisitsInternal()` está declarado `protected` en `Pet.java:88`:
```java
// Pet.java (org.springframework.samples.petclinic.model)
protected Set<Visit> getVisitsInternal() { ... }
```

En Java, `protected` es accesible desde: (1) el mismo paquete, (2) subclases. `ClinicServiceImpl` está en `org.springframework.samples.petclinic.service` — ni mismo paquete ni subclase de `Pet`. **El código no compilaría.**

**Fix:** Usar `pet.getVisits()` (método `public`) que internamente llama a `getVisitsInternal()`, triggereando la inicialización del proxy Hibernate mientras la sesión está abierta. No se necesita `Hibernate.initialize()`:

```java
@Transactional(readOnly = true)
public Pet findPetByIdWithVisits(int id) {
    Pet pet = petRepository.findById(id);
    pet.getVisits(); // public; fuerza inicialización lazy dentro de la transacción
    return pet;
}
```

El mismo patrón aplica a `findOwnerByIdWithPetsAndVisits()`:
```java
for (Pet pet : owner.getPets()) {
    pet.getVisits(); // en lugar de Hibernate.initialize(pet.getVisitsInternal())
}
```

---

### G-04 — ALTA: `SpringDataVisitRepository` no cubierto por el Paso 3 de ORDER BY

**Evidencia — `SpringDataVisitRepository.java`:**
```java
// org.springframework.samples.petclinic.repository.springdatajpa
public interface SpringDataVisitRepository extends VisitRepository, Repository<Visit, Integer> {
    // Sin métodos declarados — hereda findByPetId(Integer petId) de VisitRepository
}
```

Spring Data JPA auto-deriva la query de `findByPetId` como:
```sql
SELECT v FROM Visit v WHERE v.pet.id = ?1
-- Sin ORDER BY → orden no determinista
```

El FIX_PLAN Paso 3 añade `ORDER BY date DESC` a `JpaVisitRepositoryImpl` y `JdbcVisitRepositoryImpl`, pero **no toca `SpringDataVisitRepository`**. Cuando la aplicación corre con el perfil `spring-data-jpa`, la ordenación de visitas permanece sin garantía.

El proyecto tiene tres perfiles de repositorio:
- `jpa` → `JpaVisitRepositoryImpl` (cubierto ✅)
- `jdbc` → `JdbcVisitRepositoryImpl` (cubierto ✅)
- `spring-data-jpa` → `SpringDataVisitRepository` (**no cubierto ⛔**)

**Fix:** Añadir `@Query` con `ORDER BY` en `SpringDataVisitRepository`:
```java
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface SpringDataVisitRepository extends VisitRepository, Repository<Visit, Integer> {

    @Override
    @Query("SELECT v FROM Visit v WHERE v.pet.id = :petId ORDER BY v.date DESC")
    List<Visit> findByPetId(@Param("petId") Integer petId);
}
```

---

## Validación de Access Points — Estado tras FIX_PLAN

| Access point | Cobertura | Estado |
|-------------|-----------|--------|
| `ownerDetails.jsp:67` — `${pet.visits}` | Paso 6 (findOwnerByIdWithPetsAndVisits) | ✅ Correcto (con fix G-03) |
| `createOrUpdateVisitForm.jsp:58` — `${visit.pet.visits}` | Paso 5 (findPetByIdWithVisits) | ✅ Correcto (con fix G-03) |
| `GET /owners/*/pets/{petId}/visits` — visitList | Paso 4 (findVisitsByPetId) | ✅ Correcto |
| Ordenación descendente — perfil `jpa` | Paso 3A | ✅ Cubierto |
| Ordenación descendente — perfil `jdbc` | Paso 3B | ✅ Cubierto |
| Ordenación descendente — perfil `spring-data-jpa` | Sin paso | ⛔ No cubierto (G-04) |
| `PetController.findPetById()` → `createOrUpdatePetForm.jsp` | Sin acceso a visits | ✅ Seguro |
| Tests integración `@Transactional` | Sesión abierta por test | ✅ Sin impacto |

---

## Acciones para el Segundo FIX_PLAN

| ID | Acción | Impacto |
|----|--------|---------|
| FA-03 | Reemplazar `Hibernate.initialize(pet.getVisitsInternal())` por `pet.getVisits()` en Paso 5B y Paso 6 | Elimina error de compilación |
| FA-04 | Añadir `@Query` con `ORDER BY v.date DESC` en `SpringDataVisitRepository` | Cubre el tercer perfil de repositorio |

---

## AI_USAGE_DECLARATION

```
AI_USED = FALSE
ANALYSIS_SOURCE = Verificación directa: Pet.java (protected), SpringDataVisitRepository.java, Java access control rules
```

## GOVERNANCE VALIDATION BLOCK

- **Data lineage impact:** No
- **Model impact:** No
- **Risk impact:** Alto — G-03 es un error de compilación que bloquea el build
- **Compliance check:** ⛔ Pendiente de segundo FIX_PLAN
