# AECF_03 — Explain Behavior: Estrategias de Persistencia en spring-framework-petclinic
## TOPIC: persistence_strategies

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
| Root Prompt | `@aecf run skill=aecf_explain_behaviour TOPIC=persistence_strategies` |
| Skill Executed | aecf_explain_behavior |
| Sequence Position | 3 of 3 |
| Total Prompts Executed | 3 |
| Phase | PHASE 3 — STRUCTURED OUTPUT & DECISION |
| Sources | AECF_01_BEHAVIORAL_ANALYSIS.md, AECF_02_GOVERNANCE_GATES.md |

---

## 1. EXECUTIVE SUMMARY

El sistema de repositorios de spring-framework-petclinic implementa el **patrón Strategy sobre la capa de datos**, con propósito didáctico explícito: demostrar que la misma interfaz de repositorio puede satisfacerse con tres estrategias de persistencia completamente distintas sin tocar ninguna capa superior.

Las cuatro interfaces de repositorio (`OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository`) son el contrato único. Cada Spring profile activo en arranque registra exclusivamente las implementaciones concretas de esa estrategia, y `ClinicServiceImpl` recibe los beans correspondientes por inyección de constructor sin saber cuál es.

La equivalencia funcional entre los tres profiles está **formalmente garantizada** por `AbstractClinicServiceTests` — la misma batería de 11 tests pasa en los tres. Los trade-offs son de eficiencia, no de funcionalidad.

El profile por defecto es `jpa` (hardcoded en `PetclinicInitializer.java:52`) y puede sobreescribirse con `-Dspring.profiles.active=<profile>` sin modificar código.

---

## 2. DETAILED FLOW

### 2.1 Cómo se activa cada profile

```
╔══════════════════════════════════════════════════════════════════╗
║  JVM START                                                       ║
║    PetclinicInitializer.java:52                                  ║
║    SPRING_PROFILE = "jpa"  ← DEFAULT HARDCODED                  ║
║    [sobreescribible: -Dspring.profiles.active=jdbc]              ║
╚══════════════════════════════════════════════════════════════════╝
                        ↓
╔══════════════════════════════════════════════════════════════════╗
║  XmlWebApplicationContext                                        ║
║  → carga business-config.xml                                     ║
║  → evalúa <beans profile="..."> según profile activo            ║
╚══════════════════════════════════════════════════════════════════╝
                        ↓
     ┌──────────────────┬──────────────────┬──────────────────┐
     ▼                  ▼                  ▼
  profile=jpa    profile=spring-data-jpa  profile=jdbc
     │                  │                  │
  EntityManagerFactory  EntityManagerFactory  DataSourceTxManager
  JpaTransactionManager JpaTransactionManager JdbcClient
  JpaOwnerRepositoryImpl SpringDataOwnerRepo  JdbcOwnerRepositoryImpl
  JpaPetRepositoryImpl  SpringDataPetRepo    JdbcPetRepositoryImpl
  JpaVetRepositoryImpl  SpringDataVetRepo    JdbcVetRepositoryImpl
  JpaVisitRepositoryImpl SpringDataVisitRepo JdbcVisitRepositoryImpl
     │                  │                  │
     └──────────────────┴──────────────────┘
                        ↓
╔══════════════════════════════════════════════════════════════════╗
║  ClinicServiceImpl (constructor injection)                       ║
║  private final OwnerRepository ownerRepository;  ← activo       ║
║  private final PetRepository petRepository;      ← activo       ║
║  private final VetRepository vetRepository;      ← activo       ║
║  private final VisitRepository visitRepository;  ← activo       ║
╚══════════════════════════════════════════════════════════════════╝
```

### 2.2 Flujo de query por profile — `findOwnerById(id)`

#### Profile `jpa` (default)
```
OwnerController → ClinicService.findOwnerById(id)
  → JpaOwnerRepositoryImpl.findById(id)
      → em.createQuery("SELECT owner FROM Owner owner
                        left join fetch owner.pets WHERE owner.id =:id")
      → Hibernate → SQL: SELECT owners.*, pets.*
                          FROM owners LEFT OUTER JOIN pets ON pets.owner_id = owners.id
                          WHERE owners.id = ?
      ← ResultSet → Hibernate mapea automáticamente → Owner + Set<Pet>
  ← Owner completo en 1 SQL query
```

#### Profile `jdbc`
```
OwnerController → ClinicService.findOwnerById(id)
  → JdbcOwnerRepositoryImpl.findById(id)
      → SQL#1: SELECT id, first_name, last_name, address, city, telephone
               FROM owners WHERE id = :id
               → BeanPropertyRowMapper → Owner (sin pets)
      → loadPetsAndVisits(owner)
          → SQL#2: SELECT pets.id, name, birth_date, type_id, owner_id,
                          visits.id as visit_id, visit_date, description, pet_id
                   FROM pets LEFT OUTER JOIN visits ON pets.id = pet_id
                   WHERE owner_id=:id ORDER BY pet_id
                   → JdbcPetVisitExtractor → List<JdbcPet> con visits
          → SQL#3: SELECT id, name FROM types ORDER BY name
                   → BeanPropertyRowMapper → List<PetType>
          → EntityUtils.getById(petTypes, PetType.class, pet.getTypeId())
          → owner.addPet(pet) × N pets
  ← Owner completo en 3 SQL queries (siempre, sin caché)
```

#### Profile `spring-data-jpa`
```
OwnerController → ClinicService.findOwnerById(id)
  → SpringDataOwnerRepository proxy.findById(id)
      → @Query("SELECT owner FROM Owner owner
                left join fetch owner.pets WHERE owner.id =:id")
      → Spring Data proxy → Hibernate (misma JPQL que profile jpa)
      → SQL idéntico al profile jpa
  ← Owner completo en 1 SQL query
```

### 2.3 Flujo INSERT/UPDATE — `saveOwner(owner)`

| Condición | `jpa` | `jdbc` | `spring-data-jpa` |
|-----------|-------|--------|-------------------|
| `owner.getId() == null` (nuevo) | `em.persist(owner)` | `SimpleJdbcInsert.executeAndReturnKey()` | `SimpleJpaRepository.save()` → `em.persist()` |
| `owner.getId() != null` (existe) | `em.merge(owner)` | `JdbcClient.sql("UPDATE owners SET ...").update()` | `SimpleJpaRepository.save()` → `em.merge()` |

---

## 3. DEPENDENCY GRAPH (TEXTUAL)

```
[OwnerController]
[PetController]       ──────────────────────────────────────────────────────────┐
[VetController]                                                                  │
[VisitController]                                                                │
[PetTypeFormatter]                                                               │
        │ (constructor injection)                                                │
        ▼                                                                        │
[ClinicService «interface»]                                                      │
        ↑                                                                        │
[ClinicServiceImpl] ──────────┬──────────────┬────────────────────┐            │
  @Service @Cacheable         │              │                    │            │
                              ▼              ▼                    ▼            │
              [OwnerRepository «if»]  [PetRepository «if»]  [VetRepository «if»] [VisitRepository «if»]
                              │              │                    │
          ┌───────────────────┤   ┌──────────┤         ┌─────────┘
          │                   │   │          │         │
  profile: jpa    profile: jdbc   profile: spring-data-jpa
          │                   │             │
  [JpaOwnerRepositoryImpl]    │    [SpringDataOwnerRepository]
     → EntityManager          │       → Spring Data Proxy
       (Hibernate)            │         → EntityManager (Hibernate)
                    [JdbcOwnerRepositoryImpl]
                       → JdbcClient
                       → SimpleJdbcInsert
                       → JdbcPetVisitExtractor
                            → OneToManyResultSetExtractor

⚠️ Coupling especial (profile jdbc):
[JdbcPetRepositoryImpl] ──→ [OwnerRepository] (constructor injection — cross-aggregate)
   → JdbcOwnerRepositoryImpl.findById(ownerId) en findById(petId)

[DataSource] (Tomcat JDBC Pool) ←── compartido por los 3 profiles
[Caffeine CacheManager] ←── solo activo en ClinicServiceImpl (@Cacheable)
                             NO accesible directamente desde los repositorios JDBC
```

---

## 4. RISK MATRIX

| ID | Severidad | Riesgo | Archivo | Skill recomendado |
|----|-----------|--------|---------|-------------------|
| W-01 | 🟡 WARNING | **N+1 en `jdbc` / `findByLastName`**: `loadOwnersPetsAndVisits()` itera sobre cada owner emitiendo 3 queries por elemento | `JdbcOwnerRepositoryImpl.java:150-153` | `aecf_tech_debt_assessment` |
| W-02 | 🟡 WARNING | **`getPetTypes()` no cacheado en path JDBC**: se ejecuta un `SELECT types` extra en cada `loadPetsAndVisits()` — la caché Caffeine del servicio no se aplica aquí | `JdbcOwnerRepositoryImpl.java:138` | `aecf_refactor` |
| W-03 | 🟡 WARNING | **Cross-aggregate coupling `JdbcPetRepositoryImpl → OwnerRepository`**: violación del boundary entre agregados Pet y Owner | `JdbcPetRepositoryImpl.java:51-53` | `aecf_coupling_assessment` |
| W-04 | 🟡 WARNING | **`jpa.showSql=true` en producción**: overhead de I/O de logging para todo SQL Hibernate — activo por defecto en todos los entornos | `data-access.properties:11` | `aecf_code_standards_audit` |
| I-01 | 💡 WISH | Migrar XML Spring config a Java `@Configuration` | `business-config.xml`, `datasource-config.xml` | `aecf_refactor` |
| I-02 | 💡 WISH | Benchmark parametrizado por profile con JMeter | `petclinic_test_plan.jmx` | `aecf_new_test_set` |
| I-03 | 💡 WISH | Documentar trade-offs de profiles en README | `readme.md` | `aecf_document_legacy` |

---

## 5. RECOMMENDED ACTIONS

> Este skill es READ-ONLY. Las acciones son de análisis, monitoreo y derivación a los skills de implementación adecuados.

### Acción 1 — Investigar impacto N+1 en producción (W-01)
**Si**: La aplicación usa el profile `jdbc` en entornos con listas de owners frecuentes (búsquedas por apellido).
**Hacer**: Ejecutar `aecf_tech_debt_assessment` para cuantificar el impacto del N+1 y evaluar si merece corrección (batch load o cambio a jpa).
**Evidencia**: `JdbcOwnerRepositoryImpl.java:150-153` + `jpa.showSql=true` para comparar en consola.

### Acción 2 — Evaluar caché de PetTypes en path JDBC (W-02)
**Hacer**: En `aecf_refactor` — considerar inyectar `ClinicService.findPetTypes()` en lugar de llamar `getPetTypes()` directamente, para aprovechar la caché Caffeine existente.
**Alternativa**: Mover la caché `@Cacheable` a nivel de repositorio o añadir caché en `JdbcOwnerRepositoryImpl`.

### Acción 3 — Auditar coupling entre JdbcPetRepositoryImpl y OwnerRepository (W-03)
**Hacer**: Ejecutar `aecf_coupling_assessment` para mapear el impacto total del acoplamiento cross-aggregate. La corrección es non-trivial (requiere refactor del modelo de carga de pets en JDBC).

### Acción 4 — Desactivar showSql en production config (W-04)
**Hacer**: Externalizar `jpa.showSql` por entorno (false por defecto, true solo en dev). Puede hacerse con `@Profile` en la config o externalizando la propiedad fuera del archivo commiteado.

### Acción 5 — Confirmar perfil activo en despliegues
**Hacer**: Documentar y verificar qué profile está activo en cada entorno (dev, staging, prod). Si no hay `-Dspring.profiles.active`, el default `jpa` se aplica silenciosamente — puede ser sorpresivo para operaciones.

---

## 6. FINAL DECISION

**COMPORTAMIENTO EXPLICADO**: ✅ Completo y respaldado por evidencia.

El sistema de repositorios implementa el **patrón Strategy** sobre la capa de persistencia mediante Spring Profiles:
- Las **interfaces** son el contrato único e inmutable.
- Los **profiles** determinan cuál implementación concreta se inyecta en `ClinicServiceImpl` al arrancar.
- La **equivalencia funcional** está formalmente verificada por la batería de tests compartida.
- Los **trade-offs de eficiencia** son reales y medibles (especialmente el N+1 del profile `jdbc`), aunque no están benchmarkeados en el codebase.
- El propósito es **pedagógico**: demostrar 3 estrategias válidas de acceso a datos en un mismo proyecto Spring.

---

## Gate Verdict

GO
