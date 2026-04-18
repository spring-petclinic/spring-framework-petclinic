# AECF_02 — Governance & Quality Gates: Persistence Strategies
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
| Sequence Position | 2 of 3 |
| Total Prompts Executed | 3 |
| Phase | PHASE 2 — GOVERNANCE & QUALITY GATES |
| Source Phase | AECF_01_BEHAVIORAL_ANALYSIS.md |

---

## Quality Gate Checklist

### 1. Code Clarity ✅

| Check | Result |
|-------|--------|
| La explicación del comportamiento es internamente consistente | ✅ PASS |
| Los 3 paths de ejecución están diferenciados con evidencia concreta | ✅ PASS |
| El mecanismo de activación por profile está explicado sin ambigüedad | ✅ PASS |
| La tabla de trade-offs distingue hechos verificados de inferencias | ✅ PASS |

**Observación**: La claridad es alta. El único punto de opacidad menor es el `save()` de Spring Data JPA, cuya implementación interna (`SimpleJpaRepository`) no está presente en el código del proyecto pero es comportamiento documentado del framework. Se marcó explícitamente como inferido en PHASE 1.

---

### 2. Coupling ✅ / ⚠️

| Check | Result |
|-------|--------|
| `ClinicServiceImpl` depende solo de interfaces, no de implementaciones | ✅ PASS |
| Los 3 profiles son mutuamente excluyentes a nivel de beans Spring | ✅ PASS |
| `JdbcPetRepositoryImpl` depende de `OwnerRepository` (cross-aggregate) | ⚠️ WARNING |
| No hay dependencias entre repository packages de perfiles distintos | ✅ PASS |

**Hallazgo**: `JdbcPetRepositoryImpl.java:51-53` inyecta `OwnerRepository` para resolver el owner al hacer `findById(petId)`. Esto crea un acoplamiento cross-aggregate donde `PetRepository` necesita `OwnerRepository`, violando la separación de agregados. En el profile `jdbc`, el bean inyectado es `JdbcOwnerRepositoryImpl` (único candidato activo), pero no hay qualifier explícito — se confía en que Spring resuelva correctamente por tipo.

---

### 3. Testability ✅

| Check | Result |
|-------|--------|
| Existe path de reproducción para cada profile | ✅ PASS — `@ActiveProfiles` en tests |
| Los 3 profiles tienen cobertura de integración equivalente | ✅ PASS — `AbstractClinicServiceTests` compartida |
| Se puede cambiar de profile sin modificar tests | ✅ PASS — solo la anotación `@ActiveProfiles` cambia |
| Los tests cubren INSERT y UPDATE (no solo SELECT) | ✅ PASS — `shouldInsertOwner`, `shouldUpdateOwner` |
| Existe test de carga (JMeter) | ✅ PASS — `petclinic_test_plan.jmx` (pero no diferencia profiles) |

**Observación**: El diseño de test es especialmente bien estructurado. La clase abstracta comparte el contrato y cada subclase activa el profile correspondiente con una sola anotación. Sin embargo, los tests de carga JMeter no están parametrizados por profile — los trade-offs de rendimiento no están validados con datos empíricos.

---

### 4. Side Effects ✅ / ⚠️

| Check | Result |
|-------|--------|
| `findById` (jdbc) emite siempre 3 queries — side effect explícito | ✅ Documentado |
| `findPetTypes()` en JDBC path no usa caché Caffeine | ⚠️ WARNING |
| `jpa.showSql=true` produce output de consola en producción | ⚠️ WARNING |
| `@Cacheable` en `findVets` y `findPetTypes` solo activo en ClinicServiceImpl | ✅ PASS |
| Los tests son `@Transactional` con rollback automático — no hay side effects en DB | ✅ PASS |

**Hallazgo #1**: `JdbcOwnerRepositoryImpl.java:138` llama `getPetTypes()` en **cada invocación de `loadPetsAndVisits()`**. Esto significa que en el profile `jdbc`, cada `findById` (y cada elemento de `findByLastName`) emite un `SELECT id, name FROM types ORDER BY name` extra. A pesar de que `ClinicServiceImpl.findPetTypes()` está anotada con `@Cacheable("default")`, esa caché no es usada por el path interno de JDBC — la query de types se repite.

**Hallazgo #2**: `jpa.showSql=true` en `data-access.properties:11` está activo para todos los entornos, incluido producción potencial. Esto genera overhead de I/O en el logger.

---

### 5. Determinism ✅

| Check | Result |
|-------|--------|
| La implementación activa está determinada 100% por el profile — sin condicionales en runtime | ✅ PASS |
| El comportamiento de queries es reproducible con las mismas precondiciones de datos | ✅ PASS |
| Los tests lo confirman (AbstractClinicServiceTests pasa con datos predefinidos en data.sql) | ✅ PASS |
| No hay feature flags ni condiciones de entorno dentro de las implementaciones | ✅ PASS |

**Observación**: El comportamiento es completamente determinista dado un profile fijo. No hay lógica condicional dentro de las implementaciones que dependa de estado de runtime distinto a los datos de la base de datos.

---

## Risk Matrix

### 🔴 CRITICAL

Ninguno identificado. El sistema funciona correctamente en sus 3 variantes.

---

### 🟡 WARNING

| ID | Severidad | Hallazgo | Evidencia | Skill recomendado |
|----|-----------|---------|-----------|-------------------|
| W-01 | WARNING | **N+1 estructural en `jdbc` profile para `findByLastName`**: cada owner del resultado requiere una llamada separada a `loadPetsAndVisits()` | `JdbcOwnerRepositoryImpl.java:150-153` — `loadOwnersPetsAndVisits` itera sobre todos los owners | `aecf_tech_debt_assessment` |
| W-02 | WARNING | **Consulta de types no cacheada en path JDBC**: `getPetTypes()` llamada en cada `loadPetsAndVisits()` — bypasa la caché Caffeine de `ClinicServiceImpl.findPetTypes()` | `JdbcOwnerRepositoryImpl.java:138` — llamada directa, no pasa por servicio | `aecf_refactor` |
| W-03 | WARNING | **Cross-aggregate dependency en `JdbcPetRepositoryImpl`**: `PetRepository` depende de `OwnerRepository` en el profile `jdbc` | `JdbcPetRepositoryImpl.java:51-53` | `aecf_coupling_assessment` |
| W-04 | WARNING | **`jpa.showSql=true` globalmente**: genera overhead de logging en producción potencial | `data-access.properties:11` | `aecf_code_standards_audit` |

---

### 💡 WISH

| ID | Hallazgo | Evidencia | Beneficio |
|----|---------|-----------|-----------|
| I-01 | Migrar configuración XML Spring a Java `@Configuration` — más seguro en tiempo de compilación y más mantenible | `business-config.xml`, `datasource-config.xml` | Detecta errores de configuración en compilación |
| I-02 | Añadir benchmark parametrizado por profile para evidenciar empíricamente los trade-offs (JMeter plan actual no diferencia profiles) | `src/test/jmeter/petclinic_test_plan.jmx` | Convierte trade-off teórico en medición real |
| I-03 | Documentar explícitamente en README cuándo usar cada profile y su impacto operacional | Ausente en `readme.md` | Onboarding más rápido |
| I-04 | Añadir qualifier `@Profile` explícito en `JdbcPetRepositoryImpl` para el `OwnerRepository` inyectado | `JdbcPetRepositoryImpl.java:53` | Eliminación de dependencia implícita en ordenación de beans |

---

## Gate Verdict

GO
