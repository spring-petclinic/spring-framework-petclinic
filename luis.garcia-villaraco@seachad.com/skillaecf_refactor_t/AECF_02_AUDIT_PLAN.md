# AECF_02_AUDIT_PLAN — Auditoría del Plan: Eager Loading Fix

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
| Skill Executed            | aecf_refactor / AUDIT_PLAN                                                            |
| Sequence Position         | 02 / AUDIT_PLAN                                                                       |
| Total Prompts Executed    | 2                                                                                     |
| Artifact Auditado         | AECF_01_REFACTOR.md (PLAN)                                                            |

---

## Veredicto

> ## ⛔ NO-GO
> El plan tiene **2 brechas críticas** que producirían `LazyInitializationException` en producción si se implementara tal como está. Se requiere FIX_PLAN antes de continuar.

---

## Checklist de Auditoría

| Criterio | Estado | Detalle |
|----------|--------|---------|
| ¿El plan preserva todos los contratos públicos? | ⚠️ Parcial | Se preserva `Pet.getVisits()` pero hay un access point de producción no cubierto |
| ¿Existe estrategia de rollback? | ✅ Sí | `git revert` del commit de LAZY; pasos ordenados permiten rollback incremental |
| ¿Los pasos son atómicos y verificables? | ✅ Sí | Cada paso tiene su checkpoint de tests |
| ¿Los riesgos están identificados y mitigados? | ⛔ No | G-01 y G-02 no están en la tabla de riesgos |
| ¿La secuencia de implementación es segura? | ⚠️ Parcial | El orden es correcto, pero faltan pasos |
| ¿El scope está acotado al EAGER/LAZY fix? | ✅ Sí | No se expande innecesariamente |
| ¿Existe checkpoint de tests por paso? | ✅ Sí | Comandos `mvn test` por clase indicados |

---

## Brechas Identificadas

### G-01 — CRÍTICA: Segundo JSP de producción no cubierto: `createOrUpdateVisitForm.jsp:58`

**Evidencia:**
```jsp
<!-- src/main/webapp/WEB-INF/jsp/pets/createOrUpdateVisitForm.jsp:58 -->
<c:forEach var="visit" items="${visit.pet.visits}">
```

Este JSP accede a `visit.pet.visits`, donde `visit` es el objeto `Visit` inyectado en el modelo por el `@ModelAttribute` `loadPetWithVisit()` en `VisitController.java:61`:

```java
@ModelAttribute("visit")
public Visit loadPetWithVisit(@PathVariable("petId") int petId) {
    Pet pet = this.clinicService.findPetById(petId);  // sesión abierta aquí
    Visit visit = new Visit();
    pet.addVisit(visit);
    return visit;                                       // sesión cerrada al retornar
}
```

**Ruta completa del problema con LAZY:**
```
GET /owners/*/pets/{petId}/visits/new
  → loadPetWithVisit() [sesión JPA abierta]
      → findPetById(petId) carga Pet (visits = proxy LAZY, no inicializado)
      → sesión JPA se cierra al salir del @Transactional de findPetById()
  → initNewVisitForm() retorna "pets/createOrUpdateVisitForm"
  → JSP renderiza ${visit.pet.visits}
      → BOOM: LazyInitializationException (sesión cerrada)
```

**Impacto:** `GET /owners/*/pets/{petId}/visits/new` — formulario de nueva visita — **produce HTTP 500 en producción** con LAZY.

El plan (AECF_01) identificó únicamente `VisitController.java:87` como punto de acceso, pero `loadPetWithVisit()` (línea 61) es un segundo punto crítico que alimenta este JSP. **No está en el plan.**

---

### G-02 — ALTA: Pérdida de ordenación en `findVisitsByPetId()` (Paso 3 del plan incompleto)

El plan (Paso 3) propone sustituir:
```java
// ANTES
model.put("visits", this.clinicService.findPetById(petId).getVisits());
// DESPUÉS
model.put("visits", this.clinicService.findVisitsByPetId(petId));
```

`Pet.getVisits()` ordena las visitas descendentemente por fecha:
```java
// Pet.java:99-103
sortedVisits.sort(Comparator.comparing(Visit::getDate).reversed());
```

Verificación directa de `JpaVisitRepositoryImpl.findByPetId()`:
```java
// JpaVisitRepositoryImpl.java:60
Query query = this.em.createQuery("SELECT v FROM Visit v where v.pet.id= :id");
// Sin ORDER BY → orden no determinista
```

Verificación directa de `JdbcVisitRepositoryImpl.findByPetId()`:
```sql
-- JdbcVisitRepositoryImpl.java:86-88
SELECT id as visit_id, visit_date, description FROM visits WHERE pet_id=:id
-- Sin ORDER BY → orden dependiente del motor de base de datos
```

**Impacto:** La vista `visitList` mostraría las visitas en orden no determinista tras el Paso 3. Esto es una **regresión de comportamiento observable** para el usuario.

---

## Evaluación de la Estrategia de Rollback

✅ La estrategia es correcta y suficiente:
- Los pasos previos al cambio de FetchType son aditivos y no rompen el comportamiento EAGER existente
- `git revert` del commit de LAZY restaura el estado anterior de forma inmediata
- El orden `Paso 2 → Paso 3 → Paso 4 → Paso 1` permite rollback incremental

Sin embargo, el orden **debe ampliarse** para incluir el nuevo paso derivado de G-01.

---

## Evaluación de la Preservación de Contratos

| Contrato | Plan cubre | Estado |
|----------|-----------|--------|
| `GET /owners/{id}` → `ownerDetails.jsp` muestra visitas | Paso 4 (Hibernate.initialize) | ✅ Cubierto |
| `GET /owners/*/pets/{petId}/visits` → `visitList` muestra visitas | Paso 3 | ⚠️ Incompleto (G-02: sin ordenación) |
| `GET /owners/*/pets/{petId}/visits/new` → formulario con visitas previas | **Sin paso asignado** | ⛔ No cubierto (G-01) |
| `POST /owners/{ownerId}/pets/{petId}/visits/new` → redirect | No requiere visitas | ✅ Sin impacto |
| `Pet.getVisits()` — API pública del modelo | Sin cambio | ✅ Preservado |

---

## Acciones Requeridas en FIX_PLAN

### FA-01 — Cubrir `createOrUpdateVisitForm.jsp` (G-01)

Añadir un **nuevo Paso 3-bis** en la secuencia, antes del cambio a LAZY:

**Opción recomendada:** En `loadPetWithVisit()`, inicializar explícitamente la colección de visitas del Pet dentro de la misma transacción:

```java
// VisitController.java — loadPetWithVisit()
@ModelAttribute("visit")
public Visit loadPetWithVisit(@PathVariable("petId") int petId) {
    Pet pet = this.clinicService.findPetById(petId);
    // Con LAZY, la colección aún no está inicializada aquí, pero la sesión
    // se cierra al salir del @Transactional de findPetById(). Por eso es
    // necesario cargar las visitas en el propio servicio, no en el controlador.
    Visit visit = new Visit();
    pet.addVisit(visit);
    return visit;
}
```

El problema es que `findPetById()` es `@Transactional(readOnly=true)` — la sesión cierra al retornar. No es posible inicializar el proxy en el controlador después.

**Solución correcta:** crear un método de servicio dedicado `findPetByIdWithVisits(int id)`:

```java
// ClinicService.java — nueva firma
Pet findPetByIdWithVisits(int id);

// ClinicServiceImpl.java
@Transactional(readOnly = true)
public Pet findPetByIdWithVisits(int id) {
    Pet pet = petRepository.findById(id);
    Hibernate.initialize(pet.getVisitsInternal());
    return pet;
}
```

Y en `VisitController.java:62`:
```java
Pet pet = this.clinicService.findPetByIdWithVisits(petId);
```

Este método también resuelve el Paso 3 original (`showVisits()`) — puede reutilizar `findPetByIdWithVisits()` en lugar de `findPetById()`, manteniendo el getter `getVisits()` con su ordenación. O bien se puede mantener el Paso 3 como está y usar `findVisitsByPetId()` directamente (más eficiente).

### FA-02 — Añadir ORDER BY a `findByPetId()` (G-02)

Modificar la query JPQL en `JpaVisitRepositoryImpl.java:60`:
```java
// ANTES
"SELECT v FROM Visit v where v.pet.id= :id"
// DESPUÉS
"SELECT v FROM Visit v WHERE v.pet.id = :id ORDER BY v.date DESC"
```

Modificar la query SQL en `JdbcVisitRepositoryImpl.java:86`:
```sql
-- ANTES
SELECT id as visit_id, visit_date, description FROM visits WHERE pet_id=:id
-- DESPUÉS
SELECT id as visit_id, visit_date, description FROM visits WHERE pet_id=:id ORDER BY visit_date DESC
```

Esto garantiza comportamiento equivalente al `Comparator.comparing(Visit::getDate).reversed()` de `Pet.getVisits()`.

---

## Secuencia Corregida Propuesta (para FIX_PLAN)

```
[PASO 2]  ClinicServiceImpl.findVisitsByPetId()     → @Transactional(readOnly=true)
[PASO 3]  JpaVisitRepositoryImpl / JdbcVisitRepositoryImpl  → ORDER BY date DESC  ← NUEVO (FA-02)
[PASO 4]  VisitController.showVisits()              → findVisitsByPetId(petId)
[PASO 5]  ClinicService/Impl                        → findPetByIdWithVisits(int id)  ← NUEVO (FA-01)
[PASO 6]  VisitController.loadPetWithVisit()         → findPetByIdWithVisits(petId)
[PASO 7]  OwnerController + ClinicService/Impl      → findOwnerByIdWithPetsAndVisits()
              └─ Test: suite completa → VERDE
[PASO 1]  Pet.java                                  → FetchType.LAZY  ← ÚLTIMO
              └─ Test: suite completa + test manual → VERDE
```

---

## AI_USAGE_DECLARATION

```
AI_USED = FALSE
ANALYSIS_SOURCE = Static code exploration + code verification (VisitController, JSPs, repositories)
```

## GOVERNANCE VALIDATION BLOCK

- **Data lineage impact:** No
- **Model impact:** No
- **Risk impact:** Alto — sin FIX_PLAN, implementar causaría HTTP 500 en formulario de visitas
- **Compliance check:** ⛔ Pendiente de FIX_PLAN para garantizar comportamiento externo preservado
