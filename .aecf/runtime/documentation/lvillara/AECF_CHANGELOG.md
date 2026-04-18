# AECF Changelog — lvillara

---

## 2026-04-18

### aecf_new_feature | TOPIC: i18n_locale_selector

- **Skill**: `aecf_new_feature`
- **Status**: COMPLETE — Gate: GO (AUDIT_PLAN + AUDIT_CODE)
- **Artifacts generated**:
  - `.aecf/runtime/documentation/lvillara/2026-04-18/i18n_locale_selector/AECF_01_PLAN.md`
  - `.aecf/runtime/documentation/lvillara/2026-04-18/i18n_locale_selector/AECF_02_AUDIT_PLAN.md` (Gate: GO)
  - `.aecf/runtime/documentation/lvillara/2026-04-18/i18n_locale_selector/AECF_03_TEST_STRATEGY.md`
  - `.aecf/runtime/documentation/lvillara/2026-04-18/i18n_locale_selector/AECF_04_IMPLEMENTATION.md`
  - `.aecf/runtime/documentation/lvillara/2026-04-18/i18n_locale_selector/AECF_05_AUDIT_CODE.md` (Gate: GO)
  - `.aecf/runtime/documentation/lvillara/2026-04-18/i18n_locale_selector/AECF_06_VERSION.md`
  - `src/main/resources/spring/mvc-core-config.xml` — CookieLocaleResolver + LocaleChangeInterceptor + mvc:interceptors added
  - `src/main/resources/messages/messages.properties` — 4 lang.* keys added (EN)
  - `src/main/resources/messages/messages_es.properties` — 4 lang.* keys added (ES)
  - `src/main/resources/messages/messages_de.properties` — 4 lang.* keys added (DE)
  - `src/main/webapp/WEB-INF/tags/menu.tag` — fmt taglib + Bootstrap 5 language dropdown
  - `src/test/java/.../web/LocaleChangeInterceptorTests.java` — 6 integration tests (created)
- **Summary**: Implementación completa del selector de idioma runtime en PetClinic. Sin LocaleResolver previo — Spring usaba `AcceptHeaderLocaleResolver` (no programable). `CookieLocaleResolver` añadido con `id=localeResolver` (convención fija Spring MVC), `cookieName=PETCLINIC_LOCALE`, `defaultLocale=en`. `LocaleChangeInterceptor` global (sin restricción de path) intercept parámetro `lang`. Dropdown Bootstrap 5 en navbar con 3 idiomas (EN/ES/DE) usando `${pageContext.request.requestURI}?lang=XX`. 6 tests via `webAppContextSetup(wac)` — necesario para incluir interceptores del contexto; `standaloneSetup` los bypasaría. 87 tests existentes sin regresión + 6 nuevos = 93 total. SemVer 7.1.0 → 7.2.0 (MINOR). R1🟡: lang switch pierde query params existentes (p.ej. ?page=2 en paginación).

---

### aecf_refactor | TOPIC: xml_to_java_config

- **Skill**: `aecf_refactor`
- **Status**: PHASE1_COMPLETE — Gate: GO (AUDIT_PLAN + AUDIT_CODE)
- **Artifacts generated**:
  - `.aecf/runtime/documentation/lvillara/xml_to_java_config/AECF_01_DOCUMENT_EXISTING.md`
  - `.aecf/runtime/documentation/lvillara/xml_to_java_config/AECF_02_REFACTOR_PLAN.md`
  - `.aecf/runtime/documentation/lvillara/xml_to_java_config/AECF_03_AUDIT_PLAN.md` (Gate: GO, 3 WARNINGs non-blocking)
  - `.aecf/runtime/documentation/lvillara/xml_to_java_config/AECF_04_TEST_STRATEGY.md`
  - `.aecf/runtime/documentation/lvillara/xml_to_java_config/AECF_05_REFACTORING.md`
  - `.aecf/runtime/documentation/lvillara/xml_to_java_config/AECF_06_AUDIT_CODE.md` (Gate: GO)
  - `.aecf/runtime/documentation/lvillara/xml_to_java_config/AECF_07_VERSION.md`
  - `src/main/java/.../config/BusinessConfig.java` — global beans + @EnableTransactionManagement + static PSPC
  - `src/main/java/.../config/DataSourceConfig.java` — Phase 1 bridge via @ImportResource
  - `src/main/java/.../config/JpaSharedConfig.java` — @Profile({"jpa","spring-data-jpa"}): EMF + JpaTransactionManager + PETP
  - `src/main/java/.../config/JpaRepositoryConfig.java` — @Profile("jpa") @ComponentScan(repository.jpa)
  - `src/main/java/.../config/JdbcConfig.java` — @Profile("jdbc"): DataSourceTxManager + JdbcClient + NPJT + scan
  - `src/main/java/.../config/SpringDataJpaConfig.java` — @Profile("spring-data-jpa") @EnableJpaRepositories
- **Summary**: Migración Phase 1 de business-config.xml a Java @Configuration completa. 6 clases creadas en `config/` package. XML files intactos — bridge DataSourceConfig via @ImportResource. Correcciones clave: (1) `PropertySourcesPlaceholderConfigurer.setSystemPropertiesMode()` no existe en PSPC — StandardEnvironment maneja OVERRIDE automáticamente; (2) `AdviceMode` es enum standalone, no inner class de `@EnableTransactionManagement`. Pendiente Phase 2 (tests paralelos), Phase 3 (switch tests locations→classes), Phase 4 (AnnotationConfigWebApplicationContext en PetclinicInitializer), Phase 5 (datasource-config.xml), Phase 6 (borrar XML). SemVer 7.0.3→7.0.4 PATCH diferido a Phase 3.

---

### aecf_security_review | TOPIC: controller_security

- **Skill**: `aecf_security_review`
- **Status**: AUDIT_COMPLETE — VERDICT: NO-GO
- **Artifacts generated**:
  - `.aecf/runtime/documentation/lvillara/controller_security/AECF_01_SECURITY_AUDIT.md`
  - `.aecf/runtime/documentation/AECF_SECURITY_REVIEW_SEVERITY_MATRIX.md` (bootstrapped + v1.3 after 3 auto-applied rules)
- **Summary**: Auditoría exhaustiva de la capa web (OwnerController, PetController, VisitController, CrashController, PetclinicInitializer, PetValidator, VetRestController, mvc-core-config.xml). 2 CRITICAL: (1) cero autenticación — todos los endpoints de mutación accesibles sin credenciales (CVSS 9.8 SEC-AUTH-01), (2) IDOR en PetController — petId no validado contra ownerId del path (CVSS 9.1 SEC-AUTHZ-01). 3 HIGH: mass assignment vía @InitBinder blacklist (SEC-INPUT-01), ausencia total de CSRF (SEC-CSRF-01), IDOR en VisitController con wildcard * (SEC-AUTHZ-01). 5 MEDIUM: headers de seguridad ausentes, ruta /oups expuesta en producción, enumeración de owners vía búsqueda vacía, sin logging de seguridad, sin rate limiting. 2 LOW. Severity matrix bootstrapped (v1) + 3 reglas auto-aplicadas (SEC-CSRF-01, SEC-INFO-01, SEC-ENUM-01) → v1.3. MATRIX-PENDING: 3 ADD_RULE ✅, 2 NO_ADD_RULE.

---

### aecf_new_feature | TOPIC: vet_rest_api

- **Skill**: `aecf_new_feature`
- **Status**: COMPLETE — Gate: GO (AUDIT_PLAN + AUDIT_CODE)
- **Artifacts generated**:
  - `.aecf/runtime/documentation/lvillara/2026-04-18/vet_rest_api/AECF_01_PLAN.md`
  - `.aecf/runtime/documentation/lvillara/2026-04-18/vet_rest_api/AECF_02_AUDIT_PLAN.md` (Gate: GO)
  - `.aecf/runtime/documentation/lvillara/2026-04-18/vet_rest_api/AECF_03_TEST_STRATEGY.md`
  - `.aecf/runtime/documentation/lvillara/2026-04-18/vet_rest_api/AECF_04_IMPLEMENTATION.md`
  - `.aecf/runtime/documentation/lvillara/2026-04-18/vet_rest_api/AECF_05_AUDIT_CODE.md` (Gate: GO)
  - `.aecf/runtime/documentation/lvillara/2026-04-18/vet_rest_api/AECF_06_VERSION.md`
- **Summary**: VetController HTML flow preservado intacto. Nuevo `VetRestController` en `GET /api/vets` con produces JSON+XML vía Accept header. SpringDoc `2.8.0` añadido al pom. `OpenApiConfiguration` bean expone `/v3/api-docs` y Swagger UI. 8 tests en `VetRestControllerTests`. SemVer 7.0.3 → 7.1.0 (MINOR). Riesgo R1🔴 (Jackson 3.x / SpringDoc compat) pendiente de verificación en runtime.

---

### aecf_explain_behaviour | TOPIC: aop_monitoring_aspect

- **Skill**: `aecf_explain_behaviour`
- **Status**: COMPLETE — Gate: GO (all 3 phases)
- **Artifacts generated**:
  - `.aecf/runtime/documentation/lvillara/2026-04-18/aop_monitoring_aspect/AECF_01_BEHAVIORAL_ANALYSIS.md`
  - `.aecf/runtime/documentation/lvillara/2026-04-18/aop_monitoring_aspect/AECF_02_GOVERNANCE_GATES.md` (Gate: GO)
  - `.aecf/runtime/documentation/lvillara/2026-04-18/aop_monitoring_aspect/AECF_03_EXPLAIN_BEHAVIOR_FINAL.md` (Gate: GO)
- **Summary**: `within(@Repository *)` selects only concrete classes annotated with `@org.springframework.stereotype.Repository`. Under `spring-data-jpa` profile, Spring Data creates JDK dynamic proxies (`$ProxyXX`) for repository interfaces — neither the interface nor the proxy class carries `@Repository`, so no join points are selected and monitoring is silently absent. Under `jpa`/`jdbc` profiles, CGLIB subclass proxies of annotated concrete classes match correctly. 4 fix options documented: `execution()` by package, `@target()` with explicit annotation, `proxy-target-class="true"`, and `||` pointcut composition. Risks: R1–R3 WARNING (silent gap, no test coverage, hidden profile coupling).

---

### aecf_new_test_set | TOPIC: jdbc_repository_tests

- **Skill**: `aecf_new_test_set`
- **Status**: STRATEGY_COMPLETE — awaiting user approval for implementation
- **Artifacts generated**:
  - `.aecf/runtime/documentation/lvillara/2026-04-18/jdbc_repository_tests/AECF_01_PLAN.md`
  - `.aecf/runtime/documentation/lvillara/2026-04-18/jdbc_repository_tests/AECF_02_AUDIT_PLAN.md` (Gate: GO)
  - `.aecf/runtime/documentation/lvillara/2026-04-18/jdbc_repository_tests/AECF_03_TEST_STRATEGY.md`
- **Summary**: Discovery + gap sweep de 7 clases JDBC. 14 tests de contrato existentes identificados. 10 áreas de riesgo (R1+R2 HIGH). 17 tests nuevos diseñados en 4 clases: JdbcRowMapperTests, JdbcPetVisitExtractorTests, JdbcOwnerRepositoryIntegrationTests, JdbcPetRepositoryIntegrationTests. Gaps clave: columna "pets.id" table-qualified (R1🔴), null FK extractor para mascotas sin visitas (R2🔴), exception paths para IDs inexistentes (R4/R5🟠), carga multi-mascota con fixture owner 6 (R6🟠).

---

## 2026-04-17

### aecf_project_context_generator | TOPIC: project_context

- **Skill**: `aecf_project_context_generator`
- **Status**: COMPLETE
- **Artifacts generated**:
  - `.aecf/runtime/context/AECF_PROJECT_CONTEXT_AUTO.json` (confidence_overall: 0.90)
  - `.aecf/runtime/context/AECF_PROJECT_CONTEXT_HUMAN.yaml` (8 mandatory fields pending)
  - `.aecf/runtime/context/AECF_PROJECT_CONTEXT_RESOLVED.json` (merged, human fields not yet applied)
  - `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md` (human-readable context)
- **Summary**: First bootstrap execution on spring-framework-petclinic v7.0.3. Java 21, Spring Framework 7.0.6, modular monolith, 61 Java files, multi-DB profile support. 8 business fields pending in HUMAN.yaml.

---

## 2026-04-17 (2)

### aecf_codebase_intelligence | TOPIC: codebase_intelligence

- **Skill**: `aecf_codebase_intelligence`
- **Status**: COMPLETE
- **Artifacts generated**:
  - `.aecf/context/STACK_JSON.json`
  - `.aecf/context/AECF_ARCHITECTURE_GRAPH.json` (44 nodes, 35 edges)
  - `.aecf/context/AECF_SYMBOL_INDEX.json` (60+ symbols indexed with line numbers)
  - `.aecf/context/AECF_ENTRY_POINTS.json` (1 bootstrap + 8 route groups)
  - `.aecf/context/AECF_MODULE_MAP.json` (16 module groups)
  - `.aecf/context/AECF_CODE_HOTSPOTS.json` (8 hotspots — no monolithic files)
  - `.aecf/context/AECF_CONTEXT_KEYS.json`
  - `.aecf/context/AECF_DYNAMIC_PROJECT_CONTEXT.md`
- **Summary**: Phase 0 intelligence layer complete.

---

## 2026-04-17 (4)

### aecf_new_feature | TOPIC: owner_pagination

- **Skill**: `aecf_new_feature`
- **Status**: COMPLETE
- **Artifacts generated**:
  - `AECF_01_PLAN.md` — Implementation plan, 9-step ordered, 3-profile coverage
  - `AECF_02_AUDIT_PLAN.md` — Gate: GO (2 minor WARNINGs resolved in impl)
  - `AECF_03_TEST_STRATEGY.md` — 4 test cases, 3-profile coverage
  - `AECF_04_IMPLEMENTATION.md` — 8 source files modified, Spring Data JPA fix documented
  - `AECF_05_AUDIT_CODE.md` — Gate: GO, 87/87 tests pass
  - `AECF_06_VERSION.md` — SemVer 7.0.3 → 7.1.0 (MINOR)
- **Summary**: Paginación server-side (PAGE_SIZE=5) añadida a `OwnerController.processFindForm`. Implementada en los 3 perfiles (jpa: JPQL setFirstResult/setMaxResults, jdbc: LIMIT/OFFSET, spring-data-jpa: Pageable + default method). Vista con controles prev/next Bootstrap. Comportamiento 0/1/N resultados preservado. Fix: `findPagedByLastName` debe retornar `List<Owner>` en Spring Data JPA 2025.1.2+.

---

## 2026-04-17 (6)

### aecf_document_legacy | TOPIC: spring_xml_config

- **Skill**: `aecf_document_legacy`
- **Status**: COMPLETE
- **Artifacts generated**:
  - `AECF_01_DOCUMENT_LEGACY.md` — Full technical documentation of 5 XML config files with Mermaid context hierarchy diagram
- **Key findings**: 2 context levels (root: business-config + tools-config; child: mvc-core-config → mvc-view-config). mvc-core/mvc-view separation is primarily for test isolation — all controller tests load mvc-core but NOT mvc-view. 7 legacy quality findings: `jpa.showSql=true` global (🔴), schema init not idempotent (🔴), deprecated path-extension content negotiation (🟡), JMX unauthenticated (🟡). 4 recommended next skills.

---

## 2026-04-17 (5)

### aecf_refactor | TOPIC: eager_loading_fix

- **Skill**: `aecf_refactor`
- **Status**: COMPLETE
- **Artifacts generated**:
  - `AECF_01_DOCUMENT_EXISTING.md` — Access point analysis + EAGER overhead catalog
  - `AECF_02_REFACTOR_PLAN.md` — 7-step ordered plan (A-G), metrics before/after
  - `AECF_03_AUDIT_PLAN.md` — Gate: GO (2 WARNINGs resolved in impl)
  - `AECF_04_TEST_STRATEGY.md` — Existing test coverage, stub updates required
  - `AECF_05_TEST_IMPLEMENTATION.md` — Stub added to VisitControllerTests.setup()
  - `AECF_06_REFACTORING.md` — 6 production files + 1 test file modified, deviation documented
  - `AECF_07_AUDIT_CODE.md` — Gate: GO, 87/87 tests pass
  - `AECF_08_VERSION.md` — SemVer 7.1.0 → 7.1.1 (PATCH)
- **Summary**: `Pet.visits` changed from `FetchType.EAGER` to `FetchType.LAZY`. JPA profile: L1-cache warm pre-query in `JpaOwnerRepositoryImpl.findById`. Spring Data JPA profile: `@EntityGraph(pets, pets.visits, pets.type)` — `pets.type` was added after discovering `@EntityGraph` overrides `@ManyToOne` default EAGER, causing LazyInitializationException on PetType. Controller: `loadPetWithVisit` uses `visit.setPet(pet)` instead of `pet.addVisit(visit)`; `showVisits` and `initNewVisitForm` use `findVisitsByPetId`. JSP: `${visit.pet.visits}` → `${visits}`. N+1 visit queries eliminated on owner search and all Pet-loading paths except ownerDetails.

---

## 2026-04-17 (3)

### aecf_explain_behavior | TOPIC: persistence_strategies

- **Skill**: `aecf_explain_behavior`
- **Status**: COMPLETE — Gate: GO (all 3 phases)
- **Prompt**: "Explica cómo funciona el sistema de repositorios de este proyecto. Hay tres implementaciones del mismo contrato (JPA, JDBC, Spring Data JPA) activadas por Spring profiles..."
- **Artifacts generated**:
  - `AECF_01_BEHAVIORAL_ANALYSIS.md` — WORKING_CONTEXT (11 secciones) + análisis causal completo
  - `AECF_02_GOVERNANCE_GATES.md` — 5 dimensiones de calidad + 4 WARNINGs + 4 WISHes — Gate: GO
  - `AECF_03_EXPLAIN_BEHAVIOR_FINAL.md` — Flujo detallado + dependency graph + risk matrix — Gate: GO
- **Key findings**: Patrón Strategy sobre capa de datos. Profile `jdbc` tiene N+1 estructural en findByLastName y bypass de caché Caffeine para PetTypes. Cross-aggregate coupling en JdbcPetRepositoryImpl. jpa.showSql=true globalmente. Equivalencia funcional verificada por AbstractClinicServiceTests. Stack: Java 21 / Spring 7.0.6 / Hibernate 7.3 / H2 (default). Architecture: modular monolith, 3-tier MVC. Key risks: no authentication layer, no cache TTL, cross-repository coupling in JdbcPetRepositoryImpl.
