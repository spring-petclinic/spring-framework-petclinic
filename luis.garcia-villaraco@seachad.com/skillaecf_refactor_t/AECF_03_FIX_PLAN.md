# AECF_03_FIX_PLAN — Corrección del Plan: Eager Loading Fix

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
| Skill Executed            | aecf_refactor / FIX_PLAN                                                              |
| Sequence Position         | 03 / FIX_PLAN                                                                         |
| Total Prompts Executed    | 3                                                                                     |
| Origen                    | AUDIT_PLAN NO-GO — brechas G-01 y G-02                                                |

---

## Brechas Corregidas

| ID | Brecha | Corrección |
|----|--------|------------|
| G-01 | `createOrUpdateVisitForm.jsp:58` accede a `${visit.pet.visits}` sin cobertura | Nuevo Paso 5: `findPetByIdWithVisits()` en servicio + cambio en `loadPetWithVisit()` |
| G-02 | `findByPetId()` en JPA y JDBC sin `ORDER BY` → pérdida de ordenación descendente | Nuevo Paso 3: añadir `ORDER BY date DESC` en ambas implementaciones |

---

## Plan Completo Corregido

### Paso 1 — `Pet.java` → `FetchType.LAZY` _(diferido al final, sin cambio)_

> Sin modificaciones respecto al plan original. Sigue siendo el **último** paso.

---

### Paso 2 — `ClinicServiceImpl.findVisitsByPetId()` → `@Transactional(readOnly=true)`

**Archivo:** [`src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java`](../../../src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java) — línea 106

```java
// ANTES
@Override
public Collection<Visit> findVisitsByPetId(int petId) {
    return visitRepository.findByPetId(petId);
}

// DESPUÉS
@Override
@Transactional(readOnly = true)
public Collection<Visit> findVisitsByPetId(int petId) {
    return visitRepository.findByPetId(petId);
}
```

**Riesgo:** Bajo. Alineación de convención con todos los demás métodos de lectura.
**Verificación:** `mvn test -Dtest=AbstractClinicServiceTests` → VERDE

---

### Paso 3 — `ORDER BY date DESC` en ambas implementaciones de repositorio _(NUEVO — G-02)_

#### 3A — JPA

**Archivo:** [`src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaVisitRepositoryImpl.java`](../../../src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaVisitRepositoryImpl.java) — línea 60

```java
// ANTES
Query query = this.em.createQuery("SELECT v FROM Visit v where v.pet.id= :id");

// DESPUÉS
Query query = this.em.createQuery("SELECT v FROM Visit v WHERE v.pet.id = :id ORDER BY v.date DESC");
```

#### 3B — JDBC

**Archivo:** [`src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcVisitRepositoryImpl.java`](../../../src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcVisitRepositoryImpl.java) — línea 86

```sql
-- ANTES
SELECT id as visit_id, visit_date, description FROM visits WHERE pet_id=:id

-- DESPUÉS
SELECT id as visit_id, visit_date, description FROM visits WHERE pet_id=:id ORDER BY visit_date DESC
```

**Justificación:** Reproduce exactamente el comportamiento de `Pet.getVisits()`:
```java
// Pet.java:101
sortedVisits.sort(Comparator.comparing(Visit::getDate).reversed()); // desc por fecha
```

**Riesgo:** Bajo. No cambia los datos retornados, sólo su orden; equivalente al comportamiento actual.
**Verificación:** `mvn test -Dtest=AbstractClinicServiceTests,VisitControllerTests` → VERDE

---

### Paso 4 — `VisitController.showVisits()` → `findVisitsByPetId(petId)` _(sin cambio)_

**Archivo:** [`src/main/java/org/springframework/samples/petclinic/web/VisitController.java`](../../../src/main/java/org/springframework/samples/petclinic/web/VisitController.java) — línea 87

```java
// ANTES
model.put("visits", this.clinicService.findPetById(petId).getVisits());

// DESPUÉS
model.put("visits", this.clinicService.findVisitsByPetId(petId));
```

**Justificación:** Después del Paso 3, `findVisitsByPetId()` ya devuelve visitas ordenadas descentemente. El getter `Pet.getVisits()` queda en el modelo sin ser invocado en producción para este flujo.
**Riesgo:** Bajo.
**Verificación:** `mvn test -Dtest=VisitControllerTests` → VERDE

---

### Paso 5 — Nuevo método `findPetByIdWithVisits()` en servicio _(NUEVO — G-01)_

Este paso cubre la brecha del `@ModelAttribute loadPetWithVisit()` que alimenta `createOrUpdateVisitForm.jsp:58`.

#### 5A — Interfaz `ClinicService.java`

**Archivo:** [`src/main/java/org/springframework/samples/petclinic/service/ClinicService.java`](../../../src/main/java/org/springframework/samples/petclinic/service/ClinicService.java)

```java
// Añadir después de Pet findPetById(int id);
Pet findPetByIdWithVisits(int id);
```

#### 5B — Implementación `ClinicServiceImpl.java`

**Archivo:** [`src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java`](../../../src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java)

```java
// Añadir después de findPetById()
@Override
@Transactional(readOnly = true)
public Pet findPetByIdWithVisits(int id) {
    Pet pet = petRepository.findById(id);
    Hibernate.initialize(pet.getVisitsInternal());
    return pet;
}
```

**Import necesario:** `org.hibernate.Hibernate`

**Por qué `getVisitsInternal()` y no `getVisits()`:** `getVisitsInternal()` devuelve el `Set<Visit>` raw que es el proxy Hibernate. `Hibernate.initialize()` necesita el proxy directamente para forzar la carga. `getVisits()` devuelve una `List` nueva ya materializada, que no es el proxy — no sirve como argumento de `Hibernate.initialize()` en este contexto.

#### 5C — `VisitController.loadPetWithVisit()` usa el nuevo método

**Archivo:** [`src/main/java/org/springframework/samples/petclinic/web/VisitController.java`](../../../src/main/java/org/springframework/samples/petclinic/web/VisitController.java) — línea 62

```java
// ANTES
Pet pet = this.clinicService.findPetById(petId);

// DESPUÉS
Pet pet = this.clinicService.findPetByIdWithVisits(petId);
```

**Resultado:** Cuando el JSP accede a `${visit.pet.visits}`, la colección ya está inicializada en memoria (no es un proxy Hibernate). No se produce `LazyInitializationException`.

**Riesgo:** Medio. Requiere cambio en interfaz de servicio + nueva implementación. Está completamente dentro del límite transaccional; no cambia el comportamiento externo.
**Verificación:** `mvn test -Dtest=VisitControllerTests,AbstractClinicServiceTests` → VERDE
**Test manual:** `GET /owners/1/pets/1/visits/new` → formulario renderiza con visitas previas.

---

### Paso 6 — `OwnerController` + `findOwnerByIdWithPetsAndVisits()` _(sin cambio respecto al plan original Paso 4)_

**Archivos:** `ClinicService.java`, `ClinicServiceImpl.java`, `OwnerController.java:126`

Sin cambios respecto a la descripción del plan original. Cubre `ownerDetails.jsp:67`.

```java
// ClinicServiceImpl.java — nuevo método
@Override
@Transactional(readOnly = true)
public Owner findOwnerByIdWithPetsAndVisits(int ownerId) {
    Owner owner = ownerRepository.findById(ownerId);
    for (Pet pet : owner.getPets()) {
        Hibernate.initialize(pet.getVisitsInternal());
    }
    return owner;
}
```

```java
// OwnerController.java:126
mav.addObject(this.clinicService.findOwnerByIdWithPetsAndVisits(ownerId));
```

**Verificación:** `mvn test -Dtest=OwnerControllerTests,AbstractClinicServiceTests` → VERDE
**Test manual:** `GET /owners/1` → página muestra visitas de cada mascota.

---

### Paso 7 (antes Paso 1) — `Pet.java` → `FetchType.LAZY` _(ÚLTIMO)_

**Archivo:** [`src/main/java/org/springframework/samples/petclinic/model/Pet.java`](../../../src/main/java/org/springframework/samples/petclinic/model/Pet.java) — línea 60

```java
// ANTES
@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.EAGER)

// DESPUÉS
@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.LAZY)
```

**Verificación:** `mvn test` (suite completa) → VERDE
**Test manual:** navegar `/owners/1`, `/owners/1/pets/1/visits`, `/owners/1/pets/1/visits/new` → sin errores, datos correctos.

---

## Secuencia de Implementación Final

```
[Paso 2] ClinicServiceImpl.findVisitsByPetId()           → @Transactional(readOnly=true)
    └─ mvn test -Dtest=AbstractClinicServiceTests → VERDE

[Paso 3] JpaVisitRepositoryImpl + JdbcVisitRepositoryImpl → ORDER BY date DESC
    └─ mvn test -Dtest=AbstractClinicServiceTests,VisitControllerTests → VERDE

[Paso 4] VisitController.showVisits()                    → findVisitsByPetId(petId)
    └─ mvn test -Dtest=VisitControllerTests → VERDE

[Paso 5] ClinicService/Impl.findPetByIdWithVisits()      → nuevo método
         VisitController.loadPetWithVisit()              → findPetByIdWithVisits()
    └─ mvn test -Dtest=VisitControllerTests,AbstractClinicServiceTests → VERDE

[Paso 6] ClinicService/Impl.findOwnerByIdWithPetsAndVisits()  → nuevo método
         OwnerController.showOwner()                     → findOwnerByIdWithPetsAndVisits()
    └─ mvn test -Dtest=OwnerControllerTests,AbstractClinicServiceTests → VERDE

[Paso 7] Pet.java                                        → FetchType.LAZY  ← ÚLTIMO
    └─ mvn test (suite completa) → VERDE
    └─ Test manual: /owners/1, /owners/1/pets/1/visits, /owners/1/pets/1/visits/new
```

---

## Mapa Completo de Access Points con Cobertura

| JSP / Endpoint | Access point a `visits` | Cubierto por | Estado |
|----------------|------------------------|--------------|--------|
| `ownerDetails.jsp:67` | `${pet.visits}` | Paso 6 (Hibernate.initialize en findOwnerByIdWithPetsAndVisits) | ✅ |
| `createOrUpdateVisitForm.jsp:58` | `${visit.pet.visits}` | Paso 5 (Hibernate.initialize en findPetByIdWithVisits) | ✅ |
| `GET /owners/*/pets/{petId}/visits` | `findVisitsByPetId()` | Paso 4 | ✅ |
| Tests integración `@Transactional` | `pet.getVisits()` | Sesión abierta por test | ✅ |
| Tests unitarios | `pet.getVisits()` en memoria | Sin JPA, no aplica | ✅ |

---

## Preservación de Comportamiento Externo (actualizada)

| Comportamiento | ¿Se preserva? | Verificación |
|----------------|--------------|--------------|
| Lista de visitas en `visitList` — orden desc por fecha | ✅ Sí | ORDER BY date DESC en repositorios (Paso 3) |
| Formulario nueva visita muestra visitas previas | ✅ Sí | findPetByIdWithVisits() + Hibernate.initialize (Paso 5) |
| Visitas en ownerDetails — todas las mascotas | ✅ Sí | findOwnerByIdWithPetsAndVisits() + Hibernate.initialize (Paso 6) |
| API pública `Pet.getVisits()` | ✅ Sin cambio | El método no se toca |
| Tests de servicio y modelo | ✅ Sin regresión | Operan en @Transactional o en memoria |

---

## AI_USAGE_DECLARATION

```
AI_USED = FALSE
ANALYSIS_SOURCE = Verificación directa de código fuente (VisitController, JSPs, repositorios JPA y JDBC)
```

## GOVERNANCE VALIDATION BLOCK

- **Data lineage impact:** No
- **Model impact:** No
- **Risk impact:** Bajo tras este plan — todos los access points cubiertos
- **Compliance check:** ✅ Listo para segunda ronda de AUDIT_PLAN
