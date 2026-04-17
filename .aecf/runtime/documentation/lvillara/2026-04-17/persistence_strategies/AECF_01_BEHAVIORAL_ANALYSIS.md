# AECF_01 — Behavioral Analysis: Persistence Strategies
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
| Sequence Position | 1 of 3 |
| Total Prompts Executed | 3 |
| Phase | PHASE 1 — BEHAVIORAL ANALYSIS |

---

## WORKING_CONTEXT

### 1) TARGET_BEHAVIOR
- El sistema expone 4 interfaces de repositorio (`OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository`) con exactamente **3 implementaciones intercambiables** activadas por Spring profile: `jpa` (default), `jdbc`, `spring-data-jpa`.
- El comportamiento observable: `ClinicServiceImpl` llama siempre al mismo contrato de interfaz, pero la implementación concreta del repositorio inyectada en tiempo de arranque varía completamente según el profile activo.
- Scope: arranque del contexto Spring → inyección de repositorios → ejecución de queries → mapeo de resultados.

### 2) ENTRY_POINTS
- `PetclinicInitializer.java:52` — `SPRING_PROFILE = "jpa"` — profile por defecto codificado en Java
- `PetclinicInitializer.java:55-58` — `rootAppContext.getEnvironment().setDefaultProfiles(SPRING_PROFILE)` — establece el default
- `src/main/resources/spring/business-config.xml:35` — `<beans profile="jpa,spring-data-jpa">` — activa EntityManagerFactory + JpaTransactionManager
- `src/main/resources/spring/business-config.xml:66` — `<beans profile="jdbc">` — activa JdbcClient + DataSourceTransactionManager
- `src/main/resources/spring/business-config.xml:84` — `<beans profile="jpa">` — component-scan de `repository.jpa`
- `src/main/resources/spring/business-config.xml:94` — `<jpa:repositories base-package="...repository.springdatajpa"/>` — activa Spring Data JPA

### 3) EXECUTION_PATHS
**Path A — Activación del profile:**
```
JVM start
  → PetclinicInitializer (Servlet 3.0+ SPI)
  → XmlWebApplicationContext("classpath:spring/business-config.xml", "classpath:spring/tools-config.xml")
  → setDefaultProfiles("jpa")  [o -Dspring.profiles.active=jdbc sobreescribe]
  → business-config.xml evalúa bloques <beans profile="...">
  → Solo el bloque del profile activo registra sus beans
  → ClinicServiceImpl recibe las implementaciones concretas via constructor injection
```

**Path B — Query con profile `jpa` (default):**
```
OwnerController.showOwner(ownerId)
  → ClinicService.findOwnerById(id)
  → ClinicServiceImpl.findOwnerById(id)
  → ownerRepository.findById(id)          ← JpaOwnerRepositoryImpl (bean activo)
  → em.createQuery("SELECT owner FROM Owner owner left join fetch owner.pets WHERE owner.id =:id")
  → Hibernate genera SQL: SELECT + JOIN con pets en una sola query
  → ResultSet → Hibernate mapea automáticamente a Owner + Set<Pet>
  → retorna Owner con pets ya cargados (eager via join fetch)
```

**Path C — Query con profile `jdbc`:**
```
OwnerController.showOwner(ownerId)
  → ClinicService.findOwnerById(id)
  → ClinicServiceImpl.findOwnerById(id)
  → ownerRepository.findById(id)          ← JdbcOwnerRepositoryImpl (bean activo)
  → JdbcClient.sql("SELECT id, first_name, last_name, address, city, telephone FROM owners WHERE id = :id")
      .param("id", id).query(BeanPropertyRowMapper.newInstance(Owner.class)).single()
  → SQL#1 retorna Owner sin pets
  → loadPetsAndVisits(owner)              ← SQL#2 explícito
      → JdbcClient.sql("SELECT pets.id, name, birth_date, type_id, owner_id, visits.id as visit_id, ...")
          .query(new JdbcPetVisitExtractor())
      → OneToManyResultSetExtractor construye manualmente List<JdbcPet> con sus visits
  → getPetTypes()                          ← SQL#3 siempre (no cacheado en JDBC path)
  → EntityUtils.getById() resuelve PetType por id
  → owner.addPet(pet) para cada pet
  → retorna Owner con pets y visits reconstituidos manualmente
```

**Path D — Query con profile `spring-data-jpa`:**
```
OwnerController.showOwner(ownerId)
  → ClinicService.findOwnerById(id)
  → ClinicServiceImpl.findOwnerById(id)
  → ownerRepository.findById(id)          ← SpringDataOwnerRepository proxy (bean activo)
  → @Query("SELECT owner FROM Owner owner left join fetch owner.pets WHERE owner.id =:id")
  → Spring Data genera proxy → delega a Hibernate (misma JPQL que jpa profile)
  → Hibernate genera SQL idéntico al path B
  → retorna Owner con pets ya cargados
```

### 4) DATA_INPUTS_AND_STATE
- **Spring profile activo**: string — "jpa" (default), "jdbc", "spring-data-jpa"
- **Mecanismo de override**: `-Dspring.profiles.active=jdbc` (JVM property toma precedencia sobre `setDefaultProfiles()`)
- **DB profile Maven**: H2 (default), HSQLDB, MySQL, PostgreSQL — independiente del persistence profile
- **`data-access.properties:8-9`**: `jdbc.initLocation`, `jdbc.dataLocation` → schema.sql + data.sql por DB profile
- **`data-access.properties:11`**: `jpa.showSql=true` → Hibernate loguea SQL en consola (solo profiles jpa/spring-data-jpa)
- **`data-access.properties:19`**: `jpa.database=${jpa.database}` → dialecto Hibernate derivado del Maven DB profile
- **Estado de `owner.id`**: null → INSERT; non-null → UPDATE (governa `BaseEntity.isNew()`)

### 5) DECISION_POINTS
| Punto de decisión | Archivo:Línea | Condición | Consecuencia |
|-------------------|--------------|-----------|--------------|
| Profile por defecto | `PetclinicInitializer.java:52` | `SPRING_PROFILE = "jpa"` | Default si no hay -D property |
| EntityManagerFactory | `business-config.xml:35` | `profile="jpa,spring-data-jpa"` | Solo activo para JPA/SD-JPA — JDBC no tiene Hibernate |
| JPA beans | `business-config.xml:84` | `profile="jpa"` | Activa `JpaOwnerRepositoryImpl` et al. |
| Spring Data beans | `business-config.xml:94` | `profile="spring-data-jpa"` | Activa proxy interfaces SD-JPA |
| JDBC beans | `business-config.xml:66` | `profile="jdbc"` | Activa `JdbcClient` + `DataSourceTransactionManager` |
| INSERT vs UPDATE (JPA) | `JpaOwnerRepositoryImpl.java:73` | `owner.getId() == null` | `em.persist()` vs `em.merge()` |
| INSERT vs UPDATE (JDBC) | `JdbcOwnerRepositoryImpl.java:122` | `owner.isNew()` | `SimpleJdbcInsert` vs UPDATE SQL |
| Load de pets en JDBC | `JdbcOwnerRepositoryImpl.java:89,106` | Siempre | `findById` → SQL#1 owner, SQL#2 pets+visits, SQL#3 types |

### 6) DEPENDENCIES
**Internas:**
- `ClinicServiceImpl` → `OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository` (constructor injection)
- `JdbcPetRepositoryImpl:51-53` → `OwnerRepository` (cross-aggregate dependency — única violación de boundary)
- `OneToManyResultSetExtractor` (genérico) → `JdbcPetVisitExtractor` (extiende)
- `EntityUtils.getById()` → usado en JDBC path para resolver `PetType` por id

**Externas:**
- `javax.sql.DataSource` (Tomcat JDBC Pool) — compartido por los 3 profiles
- `EntityManager` (Hibernate 7.3) — solo profiles jpa y spring-data-jpa
- Spring Data JPA proxy infrastructure — solo spring-data-jpa
- `JdbcClient` / `NamedParameterJdbcTemplate` — solo jdbc
- DB: H2/HSQLDB/MySQL/PostgreSQL (Tomcat JDBC Pool connection)

### 7) CONFIG_AND_FLAGS
| Variable/Flag | Archivo | Valor | Impacto |
|---------------|---------|-------|---------|
| `-Dspring.profiles.active` | JVM arg | "jpa" / "jdbc" / "spring-data-jpa" | Sobreescribe default |
| `SPRING_PROFILE` | `PetclinicInitializer.java:52` | "jpa" | Default hardcoded en código |
| `jpa.showSql` | `data-access.properties:11` | true | SQL logueado en consola |
| `jpa.database` | `data-access.properties:19` | `${jpa.database}` del Maven profile | Dialecto Hibernate |
| `-P H2 / -P MySQL / ...` | Maven | Db profile | Configura driver, URL, credenciales |

### 8) TEST_AND_LOG_EVIDENCE
- `ClinicServiceJdbcTests.java:30-31`: `@ActiveProfiles("jdbc")` — test de integración completo con perfil jdbc
- `ClinicServiceJpaTests.java:16-17`: `@ActiveProfiles("jpa")` — ídem perfil jpa
- `ClinicServiceSpringDataJpaTests.java:14-15`: `@ActiveProfiles("spring-data-jpa")` — ídem
- `AbstractClinicServiceTests.java:53`: clase abstracta compartida — **los 3 perfiles pasan EXACTAMENTE los mismos 11 tests** → equivalencia funcional contractual verificada
- `jpa.showSql=true` en `data-access.properties:11` → SQL Hibernate visible en consola durante ejecución

### 9) UNCERTAINTIES
- No existen benchmarks de rendimiento en el codebase — los trade-offs de performance se infieren de comportamiento arquitectónico (número de queries, estrategia de carga), no de medición empírica
- `SpringDataXxxRepository` no declara explícitamente `save()` — la implementación es `SimpleJpaRepository.save()` del core Spring Data, delegada al proxy generado en tiempo de arranque
- No hay qualifier explícito en `JdbcPetRepositoryImpl` para garantizar que `OwnerRepository` inyectado sea `JdbcOwnerRepositoryImpl` — se confía en que solo hay un bean `OwnerRepository` activo por profile

### 10) ASSUMPTIONS
- Los 3 profiles son funcionalmente equivalentes (probado por `AbstractClinicServiceTests` compartida)
- `-Dspring.profiles.active` tiene precedencia sobre `setDefaultProfiles()` en el modelo Spring de resolución de profiles
- `SpringDataOwnerRepository.save()` es `SimpleJpaRepository.save()` — no está sobreescrito, delega a Hibernate igual que `JpaOwnerRepositoryImpl.save()`
- La aplicación solo tiene activo un profile de persistencia en cualquier momento (no combinación de profiles)

### 11) SOURCE_REFERENCES
- `src/main/java/org/springframework/samples/petclinic/PetclinicInitializer.java:52-58`
- `src/main/resources/spring/business-config.xml:35,66,84,94`
- `src/main/java/org/springframework/samples/petclinic/repository/OwnerRepository.java:32-62`
- `src/main/java/org/springframework/samples/petclinic/repository/jpa/JpaOwnerRepositoryImpl.java:37-81`
- `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcOwnerRepositoryImpl.java:48-156`
- `src/main/java/org/springframework/samples/petclinic/repository/jdbc/JdbcPetRepositoryImpl.java:44-117`
- `src/main/java/org/springframework/samples/petclinic/repository/springdatajpa/SpringDataOwnerRepository.java:32-41`
- `src/main/resources/spring/data-access.properties:8-19`
- `src/test/java/org/springframework/samples/petclinic/service/AbstractClinicServiceTests.java:53`
- `src/test/java/org/springframework/samples/petclinic/service/ClinicServiceJdbcTests.java:30-31`
- `src/test/java/org/springframework/samples/petclinic/service/ClinicServiceJpaTests.java:16-17`
- `src/test/java/org/springframework/samples/petclinic/service/ClinicServiceSpringDataJpaTests.java:14-15`

---

## PHASE 0 Gate: ✅ GO
> Todos los 11 campos de WORKING_CONTEXT presentes. Referencias concretas y trazables. Incertidumbres declaradas explícitamente.

---

## Behavioral Analysis

### Por qué existen tres implementaciones

El proyecto es **un tutorial académico** cuyo propósito explícito es demostrar que el mismo contrato de repositorio puede satisfacerse con estrategias de persistencia completamente distintas, sin que ninguna capa superior (servicio, controlador) necesite modificarse. La decisión de diseño es **el patrón Strategy aplicado a la capa de datos**, materializado mediante Spring Profiles.

Las tres co-existen no por necesidad operacional, sino como evidencia demostrable de que:
1. Spring MVC + Service layer son agnósticos a la tecnología de persistencia.
2. `OwnerRepository` (interfaz) actúa como el contrato único; las implementaciones son plugins intercambiables.
3. La equivalencia funcional está garantizada por `AbstractClinicServiceTests` — **los mismos 11 tests pasan en los 3 profiles**.

### Cómo se activa cada implementación

**Mecanismo de activación — cascada de resolución:**

```
1. JVM start → PetclinicInitializer.java:52
   SPRING_PROFILE = "jpa"  ← hardcoded default

2. rootAppContext.getEnvironment().setDefaultProfiles("jpa")
   [sobreescribible con -Dspring.profiles.active=<profile>]

3. business-config.xml evalúa bloques <beans profile="...">:
   ┌─────────────────────────────────────────────────────────┐
   │ profile="jpa,spring-data-jpa" → EntityManagerFactory   │
   │                                  JpaTransactionManager  │
   ├─────────────────────────────────────────────────────────┤
   │ profile="jpa"              → component-scan repository.jpa
   │                               JpaOwnerRepositoryImpl    │
   │                               JpaPetRepositoryImpl      │
   │                               JpaVetRepositoryImpl      │
   │                               JpaVisitRepositoryImpl    │
   ├─────────────────────────────────────────────────────────┤
   │ profile="spring-data-jpa"  → <jpa:repositories>        │
   │                               SpringDataOwnerRepository │
   │                               SpringDataPetRepository   │
   │                               SpringDataVetRepository   │
   │                               SpringDataVisitRepository │
   ├─────────────────────────────────────────────────────────┤
   │ profile="jdbc"             → JdbcClient bean            │
   │                               NamedParameterJdbcTemplate│
   │                               DataSourceTransactionManager
   │                               component-scan repository.jdbc
   │                               JdbcOwnerRepositoryImpl   │
   │                               JdbcPetRepositoryImpl     │
   │                               JdbcVetRepositoryImpl     │
   │                               JdbcVisitRepositoryImpl   │
   └─────────────────────────────────────────────────────────┘

4. ClinicServiceImpl recibe por constructor los 4 beans OwnerRepository,
   PetRepository, VetRepository, VisitRepository — siempre la implementación
   del profile activo, nunca las otras.
```

**Para cambiar de implementación:**
- En runtime: `-Dspring.profiles.active=jdbc` (JVM arg o env var)
- En tests: `@ActiveProfiles("spring-data-jpa")`
- Modificando `PetclinicInitializer.java:52` y recompilando

### Qué hace cada implementación concretamente

#### Profile `jpa` — Hibernate directo con EntityManager

```java
// JpaOwnerRepositoryImpl.java:56-58
Query query = this.em.createQuery(
    "SELECT DISTINCT owner FROM Owner owner left join fetch owner.pets WHERE owner.lastName LIKE :lastName");
```
- Escribe JPQL a mano, le pasa el `EntityManager` inyectado vía `@PersistenceContext`
- Hibernate traduce JPQL → SQL nativo en tiempo de ejecución según el dialecto configurado
- `left join fetch` carga Owner + Pets en **una sola query SQL**
- `em.persist()` para INSERT, `em.merge()` para UPDATE (detectado por `owner.getId() == null`)
- El desarrollador controla las queries pero no el SQL generado exacto

#### Profile `jdbc` — SQL puro con JdbcClient

```java
// JdbcOwnerRepositoryImpl.java:89-103
owner = this.jdbcClient.sql("""
    SELECT id, first_name, last_name, address, city, telephone
    FROM owners WHERE id = :id""")
    .param("id", id)
    .query(BeanPropertyRowMapper.newInstance(Owner.class)).single();
loadPetsAndVisits(owner);   // ← SQL separado siempre
```
- SQL explícito, sin ORM entre medio
- `findById` emite **siempre 3 queries**: (1) SELECT owner, (2) SELECT pets LEFT JOIN visits por owner_id, (3) SELECT types
- `BeanPropertyRowMapper` mapea ResultSet → POJO por convención de nombres
- `SimpleJdbcInsert` para INSERT con generación automática de clave
- `JdbcPetVisitExtractor` (extiende `OneToManyResultSetExtractor`) reconstituye manualmente la jerarquía Pets → Visits desde el ResultSet

#### Profile `spring-data-jpa` — Spring Data con @Query declarativa

```java
// SpringDataOwnerRepository.java:35-40
@Query("SELECT owner FROM Owner owner left join fetch owner.pets WHERE owner.id =:id")
Owner findById(@Param("id") int id);
```
- La interfaz extiende `OwnerRepository` Y `Repository<Owner, Integer>` (Spring Data marker)
- No hay clase de implementación — Spring Data genera un proxy JDK en tiempo de arranque
- Las queries JPQL son **idénticas** a las del profile `jpa` (mismo `left join fetch`)
- `save()` no está declarado en la interfaz — Spring Data proxy delega a `SimpleJpaRepository.save()` (isNew() → persist, else merge)
- El desarrollador solo escribe la interfaz; Spring genera toda la lógica de infraestructura

### Trade-offs de rendimiento

| Dimensión | `jpa` | `jdbc` | `spring-data-jpa` |
|-----------|-------|--------|-------------------|
| **Queries por `findById`** | 1 (join fetch) | 3 (owner + pets+visits + types) | 1 (join fetch — idéntico a jpa) |
| **Queries por `findByLastName`** | 1 (join fetch) | N+1 (1 query owners + N loads) | 1 (join fetch) |
| **Control del SQL** | JPQL → SQL generado | SQL explícito y total | JPQL → SQL generado |
| **Overhead ORM** | Hibernate session, 1st-level cache, dirty checking | Ninguno — directo al driver JDBC | Hibernate session + proxy infrastructure |
| **Startup** | Slow (EntityManagerFactory bootstrap, schema validation) | Fast (solo DataSource) | Slower (EMF + SD proxy generation) |
| **Flexibilidad de query** | JPQL portable + criterios Hibernate | SQL nativo total | JPQL + Spring Data query methods |
| **Legibilidad** | Media (JPQL inline strings) | Baja (SQL + mapeo manual) | Alta (solo @Query en interfaz) |
| **Mantenimiento** | Medio | Alto (mapeo manual, SQL strings) | Bajo (framework genera infra) |
| **N+1 risk** | Controlado (join fetch declarado) | Estructural en findByLastName | Controlado (join fetch declarado) |

**Conclusión de trade-offs:**
- **`jdbc`** es el más explícito pero tiene el mayor riesgo de N+1 (cada `findByLastName` → 1 query por owner para cargar pets). Adecuado cuando el control absoluto del SQL y el overhead mínimo de runtime superan al coste de mantenimiento.
- **`jpa`** equilibra control (JPQL) con productividad (Hibernate mapping automático). Apropiado para proyectos donde el SQL generable es aceptable y se quiere portabilidad de dialecto.
- **`spring-data-jpa`** maximiza productividad y minimiza boilerplate, al precio de una capa de abstracción adicional (proxy) y dependencia en el framework para generar la infraestructura. Es la opción más moderna y recomendada para nuevos proyectos Spring.

### Cadena de hechos verificados vs incertidumbre residual

| Afirmación | Verificación |
|------------|-------------|
| Los 3 profiles pasan los mismos 11 tests | ✅ `AbstractClinicServiceTests.java:53` + 3 subclases |
| JDBC emite 3 queries para `findById` | ✅ `JdbcOwnerRepositoryImpl.java:89,106,138` — 3 llamadas a `jdbcClient.sql()` explícitas |
| JPA y SD-JPA emiten 1 query (join fetch) | ✅ `JpaOwnerRepositoryImpl.java:63-66`, `SpringDataOwnerRepository.java:39-40` |
| El default es `jpa` | ✅ `PetclinicInitializer.java:52` |
| JdbcPetRepositoryImpl tiene cross-dependency | ✅ `JdbcPetRepositoryImpl.java:51` |
| SD-JPA `save()` delega a `SimpleJpaRepository` | ⚠️ No hay código fuente visible — inferido de Spring Data internals |
| Benchmark de rendimiento real | ❌ No existe en el codebase |
