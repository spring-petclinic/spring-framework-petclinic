# AECF Project Context — spring-framework-petclinic

> **Prompt-only human-readable context** — consumed by all AECF skills at execution time.
> Source of truth: `.aecf/runtime/context/AECF_PROJECT_CONTEXT_RESOLVED.json`
> Regenerate: `aecf context resolve` → `aecf_project_context_generator`

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
| Root Prompt | `@aecf skill=aecf_project_context_generator topic=project_context` |
| Skill Executed | aecf_project_context_generator |
| Sequence Position | 1 |
| Total Prompts Executed | 1 |

---

## 1. Project Overview

| Field | Value |
|-------|-------|
| **Project Name** | spring-framework-petclinic |
| **Version** | 7.0.3 |
| **Artifact** | `org.springframework.samples:spring-framework-petclinic` (WAR) |
| **Description** | Spring Framework application based on JSP, Spring MVC, Spring Data JPA, Hibernate and JDBC — veterinary practice management demo |
| **License** | Apache License 2.0 |
| **Structural Hash** | `a3f2b1c4d5e6f708` |

---

## 2. Technical Stack (confidence: 0.98 🟢)

### Primary Language
- **Java 21** (compiler source/target = 21)

### Core Frameworks
| Framework | Version |
|-----------|---------|
| Spring Framework | 7.0.6 |
| Spring MVC | 7.0.6 (included) |
| Spring Data JPA | 2025.1.2 |
| Spring Context Support | 7.0.6 |
| Spring JDBC / ORM / OXM | 7.0.6 |
| Hibernate ORM | 7.3.0.Final |
| Hibernate Validator | 9.1.0.Final |
| AspectJ | 1.9.25.1 |
| Jakarta Servlet API | 6.1.0 |
| Jakarta JPA API | 3.2.0 |
| JSTL | 3.0.2 |

### Frontend
- JSP views + JSTL tags
- Bootstrap 5.3.8 (WebJar)
- Font Awesome 4.7.0 (WebJar)
- Flatpickr 4.6.13 (WebJar)
- SCSS compiled via libsass-maven-plugin

### Logging
- SLF4J 2.0.17 + Logback 1.5.32
- Config: `src/main/resources/logback.xml`

### JSON
- Jackson 3.1.1 (jackson-core, jackson-databind)

---

## 3. Architecture Pattern (confidence: 0.97 🟢)

**Style**: Modular Monolith — classic Spring MVC layered application packaged as WAR.

### Layer Map
```
[Browser / REST client]
        ↓
  [Web Layer] — Spring MVC @Controllers (web/)
        ↓
  [Service Layer] — ClinicService interface / ClinicServiceImpl facade (service/)
        ↓
  [Repository Layer] — 3 interchangeable implementations selected by Spring profile:
     ├── jpa (default)          → Hibernate/JPA via LocalContainerEntityManagerFactoryBean
     ├── spring-data-jpa        → Spring Data JPA repositories
     └── jdbc                   → Spring JdbcClient / NamedParameterJdbcTemplate
        ↓
  [Persistence] — Relational DB (H2 default, MySQL, PostgreSQL, HSQLDB)
```

### Entry Point
- `PetclinicInitializer.java` — Servlet 3.0+ programmatic bootstrap (replaces web.xml)
- Default Spring profile: `jpa`

### Spring Configuration
All XML-based:
- `spring/business-config.xml` — service + repository beans + profiles
- `spring/datasource-config.xml` — connection pool, DB initializer
- `spring/mvc-core-config.xml` — DispatcherServlet, MVC beans, formatters
- `spring/mvc-view-config.xml` — JSP ViewResolver
- `spring/tools-config.xml` — AOP, JMX, Spring Cache

---

## 4. Persistence Model (confidence: 0.97 🟢)

| Field | Value |
|-------|-------|
| **Default DB** | H2 in-memory (`jdbc:h2:mem:petclinic`) |
| **ORM** | Hibernate ORM 7.3.0.Final |
| **Connection Pool** | Tomcat JDBC Pool 11.0.18 |
| **Migration** | `Spring jdbc:initialize-database` — schema.sql + data.sql per DB profile |
| **Profiles** | H2 (default), HSQLDB, MySQL, PostgreSQL |

### Database Profiles (Maven)
| Profile ID | Driver | URL |
|------------|--------|-----|
| H2 (default) | `org.h2.Driver` | `jdbc:h2:mem:petclinic` |
| HSQLDB | `org.hsqldb.jdbcDriver` | `jdbc:hsqldb:mem:petclinic` |
| MySQL | `com.mysql.cj.jdbc.Driver` | `jdbc:mysql://localhost:3306/petclinic` |
| PostgreSQL | `org.postgresql.Driver` | `jdbc:postgresql://localhost:5432/petclinic` |

---

## 5. Domain Model (confidence: 0.97 🟢)

**Bounded Context**: PetClinic (single — veterinary practice management)

### Entity Hierarchy
```
BaseEntity (id, isNew)
├── NamedEntity (name)
│   ├── PetType
│   └── Specialty
└── Person (firstName, lastName)
    ├── Owner → 1:N Pet → 1:N Visit
    └── Vet → N:M Specialty

Vets (JAXB wrapper for Collection<Vet>)
```

### Aggregate Roots
- **Owner** — root aggregate (owns Pets, which own Visits; CASCADE ALL)
- **Vet** — root aggregate (owns Specialties)

### ClinicService facade
Single service interface with: `findOwnerById`, `saveOwner`, `findOwnerByLastName`, `findPetById`, `savePet`, `findPetTypes`, `saveVisit`, `findVisitsByPetId`, `findVets`

---

## 6. Caching Strategy (confidence: 0.95 🟢)

- **Backend**: Caffeine 3.2.3 via `CaffeineCacheManager`
- **Pattern**: `@Cacheable` annotation-driven (`<cache:annotation-driven/>`)
- **Named caches**: `vets`, `default`
- **Config**: `spring/tools-config.xml`

---

## 7. Web Controllers

| Controller | Responsibilities |
|------------|-----------------|
| `OwnerController` | Find / create / update owners |
| `PetController` | Add / edit pets for an owner |
| `VisitController` | Create visits for a pet |
| `VetController` | List vets (JSON + JSP) |
| `CrashController` | Intentional error for exception-handling demo |

---

## 8. Observability & Monitoring (confidence: 0.92 🟢)

| Mechanism | Detail |
|-----------|--------|
| Logging | SLF4J + Logback (`logback.xml`) |
| JMX | `CallMonitoringAspect` exposed via `<context:mbean-export/>` — tracks call count and avg invocation time per service method |
| No APM | No OpenTelemetry / Prometheus / Micrometer detected |

---

## 9. Test Organization (confidence: 0.92 🟢)

| Package | Type | Coverage |
|---------|------|---------|
| `model/` | Unit tests (validation, entity behavior) | OwnerTests, PetTests, ValidatorTests, VetTests |
| `service/` | Integration tests — AbstractClinicServiceTests + 3 concrete subclasses | ClinicServiceJdbcTests, ClinicServiceJpaTests, ClinicServiceSpringDataJpaTests |
| `web/` | MockMvc controller tests | CrashControllerTests, OwnerControllerTests, PetControllerTests, PetTypeFormatterTests, VetControllerTests, VisitControllerTests |
| `jmeter/` | Load test plan | petclinic_test_plan.jmx |

- **Coverage tool**: JaCoCo 0.8.14 (XML report at `prepare-package`)
- **Test pattern**: `**/*Tests.java` (via maven-surefire-plugin)

---

## 10. Build & CI/CD (confidence: 0.92 🟢)

| Tool | Config |
|------|--------|
| Build | Maven (`mvnw` wrapper, minimum 3.8.4) |
| Packaging | WAR (`petclinic.war`) |
| Containerization | Jib 3.5.1 → `docker.io/springcommunity/spring-framework-petclinic` (base: `jetty:11.0-jdk21`) |
| CI | GitHub Actions — matrix Java 17/21 on push/PR |
| Code Quality | SonarCloud (`sonar.organization=spring-petclinic`) |
| Coverage | JaCoCo → SonarCloud |
| Dev server | Jetty 11.0.26 (`mvn jetty:run`) |

---

## 11. Structural Metrics (confidence: 0.97 🟢)

| Metric | Value |
|--------|-------|
| Java source files | 61 |
| Java LOC (estimated) | ~4,295 |
| Total project files | ~120 |
| Total LOC (estimated) | ~6,500 |
| Modules | 7 (model, service, repository×3, web, util) |
| Monolithic files (>1000 LOC) | None detected |
| Complexity hotspots | `JdbcOwnerRepositoryImpl.java`, `OwnerController.java` |

---

## 12. Business Context — PENDING HUMAN INPUT ⚠️

> Edit `.aecf/runtime/context/AECF_PROJECT_CONTEXT_HUMAN.yaml` to provide these values.

| Field | Status |
|-------|--------|
| Business criticality | ⚠️ PENDING |
| Risk tolerance | ⚠️ PENDING |
| Data sensitivity | ⚠️ PENDING |
| Compliance requirements | ⚠️ PENDING |
| Team size | ⚠️ PENDING |
| Release cadence | ⚠️ PENDING |
| Production environment | ⚠️ PENDING |
| Primary use case | ⚠️ PENDING |

---

## 13. Skill Recommendations

Based on the discovered state of this project:

| Situation | Recommended Skill |
|-----------|------------------|
| Assess overall project quality | `aecf_code_standards_audit` |
| Check for security vulnerabilities | `aecf_security_review` |
| Evaluate dependency health/CVEs | `aecf_dependency_audit` |
| Quantify technical debt | `aecf_tech_debt_assessment` |
| Understand legacy code flows | `aecf_document_legacy` |
| Validate before release | `aecf_release_readiness` |
| Assess AECF adoption maturity | `aecf_maturity_assessment` |
| Build structured intelligence layer | `aecf_codebase_intelligence` |

---

*Generated by `aecf_project_context_generator` — prompt-only mode | TOPIC: project_context*
