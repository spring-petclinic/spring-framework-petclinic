# AECF Changelog — lvillara

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
