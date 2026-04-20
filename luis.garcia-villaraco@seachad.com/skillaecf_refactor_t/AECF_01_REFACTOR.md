# AECF_01_REFACTOR — PLAN: Eager Loading Fix (Pet → Visit)

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
| Skill Executed            | aecf_refactor                                                                         |
| Sequence Position         | 01 / PLAN                                                                             |
| Total Prompts Executed    | 1                                                                                     |

---

## 1. Archivos a Revisar

| Archivo | Rol |
|---------|-----|
| [`src/main/java/org/springframework/samples/petclinic/model/Pet.java`](../../../src/main/java/org/springframework/samples/petclinic/model/Pet.java) | Entidad JPA — contiene la anotación `FetchType.EAGER` a cambiar |
| [`src/main/java/org/springframework/samples/petclinic/model/Visit.java`](../../../src/main/java/org/springframework/samples/petclinic/model/Visit.java) | Entidad JPA del lado inverso |
| [`src/main/java/org/springframework/samples/petclinic/web/VisitController.java`](../../../src/main/java/org/springframework/samples/petclinic/web/VisitController.java) | Único punto de producción que llama a `pet.getVisits()` (línea 87) |
| [`src/main/java/org/springframework/samples/petclinic/web/OwnerController.java`](../../../src/main/java/org/springframework/samples/petclinic/web/OwnerController.java) | Carga Owner → Pet → Visits a través de JSP (línea 126) |
| [`src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java`](../../../src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java) | `findVisitsByPetId()` (línea 106) y `findPetById()` (línea 87) |
| [`src/main/java/org/springframework/samples/petclinic/service/ClinicService.java`](../../../src/main/java/org/springframework/samples/petclinic/service/ClinicService.java) | Interfaz de servicio — firma `findVisitsByPetId(int petId)` (línea 50) |
| [`src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaPetRepositoryImpl.java`](../../../src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaPetRepositoryImpl.java) | `em.find(Pet.class, id)` — sin FETCH JOIN explícito |
| [`src/main/webapp/WEB-INF/jsp/owners/ownerDetails.jsp`](../../../src/main/webapp/WEB-INF/jsp/owners/ownerDetails.jsp) | JSP que accede a `${pet.visits}` (línea 67) fuera de sesión JPA |
| [`src/test/java/org/springframework/samples/petclinic/service/AbstractClinicServiceTests.java`](../../../src/test/java/org/springframework/samples/petclinic/service/AbstractClinicServiceTests.java) | Tests de servicio que usan `pet.getVisits()` (líneas 180, 188) |
| [`src/test/java/org/springframework/samples/petclinic/model/PetTests.java`](../../../src/test/java/org/springframework/samples/petclinic/model/PetTests.java) | Tests unitarios del modelo (líneas 24, 43, 62) |

---

## 2. Problemas a Resolver

### P-01 — Carga EAGER innecesaria en Pet.visits
**Localización:** `Pet.java:60`
```java
@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.EAGER)
private Set<Visit> visits;
```
**Impacto:** Cada llamada a `findPetById()`, `findOwnerById()` (que carga la colección de pets) o cualquier lista de mascotas genera un JOIN adicional hacia `visits`, incluso cuando el contexto no necesita esos datos (e.g., formulario de edición de mascota).

### P-02 — Acoplamiento fuerte en VisitController
**Localización:** `VisitController.java:87`
```java
model.put("visits", this.clinicService.findPetById(petId).getVisits());
```
El controlador carga la entidad `Pet` completa sólo para navegar al getter de visitas. Ya existe `clinicService.findVisitsByPetId(petId)` que resuelve exactamente ese caso de uso sin necesitar la entidad Pet.

### P-03 — findVisitsByPetId() sin @Transactional
**Localización:** `ClinicServiceImpl.java:106`
```java
public Collection<Visit> findVisitsByPetId(int petId) {
    return visitRepository.findByPetId(petId);  // sin @Transactional
}
```
Todos los demás métodos de lectura del servicio tienen `@Transactional(readOnly = true)`. Esta omisión es incoherente y puede provocar problemas con proxies Hibernate si se añaden relaciones lazy en el futuro.

### P-04 — JSP ownerDetails accede a ${pet.visits} fuera de contexto transaccional
**Localización:** `ownerDetails.jsp:67`
```jsp
<c:forEach var="visit" items="${pet.visits}">
```
Si `FetchType` se cambia a LAZY sin que el controlador proporcione los datos ya inicializados, la plantilla provocará `LazyInitializationException` porque la sesión JPA ya se habrá cerrado al renderizar la vista.

### P-05 — Owner → Pets → Visits: N+1 queries en producción
**Localización:** `OwnerController.java:126`, `JpaPetRepositoryImpl.java:52`
Con EAGER, al mostrar `ownerDetails` se ejecuta: 1 query de Owner + 1 JOIN para Pets + N queries de Visits (una por cada mascota). No hay FETCH JOIN explícito.

---

## 3. Análisis de Puntos de Acceso a pet.getVisits()

### Producción

| Punto de acceso | Archivo:Línea | ¿Necesita Pet completo? | Alternativa disponible |
|----------------|--------------|------------------------|------------------------|
| `VisitController.showVisits()` | `VisitController.java:87` | **No** | `clinicService.findVisitsByPetId(petId)` ✅ |
| `ownerDetails.jsp` forEach | `ownerDetails.jsp:67` | Sí (ya tiene el Pet en modelo) | Inicialización explícita en servicio ✅ |

### Tests

| Punto de acceso | Archivo:Línea | Tipo |
|----------------|--------------|------|
| `pet7.getVisits().size()` | `AbstractClinicServiceTests.java:180` | Test de integración de servicio |
| `pet7.getVisits().hasSize(found+1)` | `AbstractClinicServiceTests.java:188` | Test de integración de servicio |
| `pet.getVisits()` × 3 | `PetTests.java:24, 43, 62` | Test unitario del modelo |

Los tests unitarios (`PetTests`) no usan JPA; trabajan con objetos en memoria → no se ven afectados por el cambio de FetchType.

Los tests de integración (`AbstractClinicServiceTests`) operan dentro de un contexto `@Transactional`, por lo que la sesión estará abierta al momento de acceder a `getVisits()` → tampoco generan `LazyInitializationException`. Sin embargo, verifican el comportamiento correcto de carga.

---

## 4. Impacto de Cambiar a FetchType.LAZY

### Escenarios seguros (sesión JPA abierta)
- `AbstractClinicServiceTests` — transaccional por anotación de test ✅
- `VisitController.showVisits()` — si se reemplaza `pet.getVisits()` por `findVisitsByPetId()` ✅
- Cualquier acceso a `getVisitsInternal()` dentro de la misma transacción de servicio ✅

### Escenarios con riesgo de LazyInitializationException
| Escenario | Causa | Solución |
|-----------|-------|----------|
| `ownerDetails.jsp` accede a `${pet.visits}` | Sesión cerrada al renderizar vista | Inicializar visits en el modelo antes del render |
| `VisitController.showVisits()` si no se cambia | Navega `pet.getVisits()` fuera de transacción | Reemplazar por `findVisitsByPetId()` |

---

## 5. Plan de Remediación

### Paso 1 — Cambiar FetchType en Pet.java (LAZY)
**Archivo:** `Pet.java:60`
```java
// ANTES
@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.EAGER)

// DESPUÉS
@OneToMany(cascade = CascadeType.ALL, mappedBy = "pet", fetch = FetchType.LAZY)
```
**Riesgo:** ALTO si no se acompañan los pasos siguientes. **Orden:** debe ser el ÚLTIMO paso.

---

### Paso 2 — Añadir @Transactional(readOnly=true) a findVisitsByPetId()
**Archivo:** `ClinicServiceImpl.java:106`
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
**Riesgo:** BAJO. Alineación de convención; no cambia semántica. **Orden:** primero.

---

### Paso 3 — Desacoplar VisitController del getter de Pet
**Archivo:** `VisitController.java:87`
```java
// ANTES
model.put("visits", this.clinicService.findPetById(petId).getVisits());

// DESPUÉS
model.put("visits", this.clinicService.findVisitsByPetId(petId));
```
**Riesgo:** BAJO. Preserva el contrato de vista (`visitList.jsp` espera una colección de `Visit`). El orden de visitas (descendente por fecha) se perdería al saltar el getter; verificar si la vista o el repositorio ya ordena. Si no, añadir `ORDER BY v.date DESC` en el repositorio o en el servicio.
**Orden:** antes de cambiar FetchType.

---

### Paso 4 — Inicialización explícita de visits en OwnerController
**Archivo:** `OwnerController.java:126`

El patrón actual pasa el Owner completo a la vista y el JSP navega `owner.pets[i].visits`. Con LAZY esto fallará. La solución correcta es hacer la inicialización dentro de la transacción de servicio.

**Opción A (recomendada) — Hibernate.initialize() en servicio:**
Añadir un método en `ClinicService` / `ClinicServiceImpl`:
```java
@Transactional(readOnly = true)
public Owner findOwnerByIdWithPetsAndVisits(int ownerId) {
    Owner owner = ownerRepository.findById(ownerId);
    // Inicializar colección mientras la sesión está abierta
    for (Pet pet : owner.getPets()) {
        Hibernate.initialize(pet.getVisits());
    }
    return owner;
}
```
Y en `OwnerController.java:126`:
```java
mav.addObject(this.clinicService.findOwnerByIdWithPetsAndVisits(ownerId));
```

**Opción B — Open Session In View (OSIV):**  
Habilitar `spring.jpa.open-in-view=true` (en Spring Boot) o configurar `OpenEntityManagerInViewInterceptor`. **No recomendada** para este proyecto: oculta el problema, genera antipatrón y en Spring MVC clásico la configuración es manual.

**Opción C — DTO/projection con JOIN FETCH en repositorio:**  
Añadir query JPQL con `LEFT JOIN FETCH p.visits` al repositorio de Owner. Más performante pero mayor cambio de scope.

**Decisión:** Opción A. Minimiza scope, es explícita, y mantiene el comportamiento actual visible.
**Riesgo:** MEDIO. Requiere nuevo método de servicio e interfaz. **Orden:** antes de cambiar FetchType.

---

## 6. Evaluación de Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| LazyInitializationException en ownerDetails.jsp | Alta si se omite Paso 4 | Crítico (500 en producción) | Opción A — Hibernate.initialize() |
| LazyInitializationException en VisitController | Alta si se omite Paso 3 | Alto | Reemplazar por findVisitsByPetId() |
| Regresión en tests de servicio | Baja (operan en @Transactional) | Medio | Ejecutar suite completa post-cambio |
| Pérdida de orden en VisitController | Media | Bajo | Verificar ordenación en repositorio |
| N+1 en ownerDetails (ya existente) | Ya presente | Medio | Opción C (fuera de scope actual) |

---

## 7. Estrategia de Rollback

1. El cambio de `FetchType.EAGER` a `LAZY` en `Pet.java` es el único cambio que afecta al esquema de comportamiento JPA.
2. `git revert` de ese commit restaura el comportamiento original inmediatamente.
3. Los pasos 2 y 3 son additive/refactor seguros — no rompen si EAGER sigue activo.
4. El paso 4 (nuevo método de servicio) no afecta el flujo existente hasta que el controlador lo invoque.

**Orden de ejecución seguro (permite rollback incremental):**
```
Paso 2 → Paso 3 → Paso 4 → [tests: OK] → Paso 1 (LAZY)
```

---

## 8. Preservación del Comportamiento Externo

| Comportamiento | ¿Se preserva? | Verificación |
|----------------|--------------|--------------|
| Lista de visitas en `/owners/{id}/pets/{petId}/visits` | ✅ Sí | VisitController — mismos datos, diferente consulta |
| Visitas en ownerDetails.jsp | ✅ Sí | Hibernate.initialize() garantiza datos cargados |
| Ordenación descendente por fecha | ⚠️ Verificar | getVisits() ordena; findVisitsByPetId() no necesariamente |
| Tests de servicio | ✅ Sí | Operan en contexto transaccional |
| API pública de Pet.getVisits() | ✅ Sin cambio | El método no se toca |

---

## 9. Métricas Antes / Después

| Métrica | Antes (EAGER) | Después (LAZY) |
|---------|--------------|----------------|
| Queries al cargar 1 Pet sin visitas necesarias | 2 (Pet + Visits) | 1 (Pet solamente) |
| Queries al mostrar ownerDetails (3 mascotas) | 1+3 JOIN | 1+3 explícitas (Hibernate.initialize) |
| Queries en VisitController | 1 (Pet + Visits JOIN) | 1 (findVisitsByPetId directo) |
| Riesgo LazyInitializationException | Ninguno (todo eager) | Eliminado con pasos 3 y 4 |

---

## 10. Secuencia de Implementación Atómica

```
[PASO 2] ClinicServiceImpl.findVisitsByPetId() → @Transactional(readOnly=true)
    └─ Test: mvn test -pl . -Dtest=AbstractClinicServiceTests → VERDE

[PASO 3] VisitController.showVisits() → findVisitsByPetId(petId)
    └─ Test: mvn test -pl . -Dtest=VisitControllerTests → VERDE
    └─ Verificar ordenación de visitas en vista

[PASO 4] OwnerController + ClinicService/Impl → findOwnerByIdWithPetsAndVisits()
    └─ Test: mvn test -pl . -Dtest=OwnerControllerTests,AbstractClinicServiceTests → VERDE

[PASO 1] Pet.java → FetchType.LAZY  ← ÚLTIMO
    └─ Test: mvn test → suite completa VERDE
    └─ Test manual: navegar /owners/1, /owners/1/pets/1/visits
```

---

## AI_USAGE_DECLARATION

```
AI_USED = FALSE
ANALYSIS_SOURCE = Static code exploration (AECF Explore Agent)
```

## GOVERNANCE VALIDATION BLOCK

- **Data lineage impact:** No — refactor interno, sin cambio de esquema DB
- **Model impact:** No
- **Risk impact:** Medio (LazyInitializationException contenido por el plan de pasos)
- **Compliance check:** ✅ Comportamiento externo preservado; sin cambio de API pública
