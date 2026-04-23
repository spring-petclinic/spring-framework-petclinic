# AECF Dynamic Project Context — spring-framework-petclinic

> **Machine-generated architectural intelligence layer** — produced by `aecf_codebase_intelligence`.
> Downstream skills load this file instead of re-scanning the repository.
> Regenerate: `@aecf skill=aecf_codebase_intelligence topic=codebase_intelligence`

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
| Root Prompt | `@aecf skill=aecf_codebase_intelligence topic=codebase_intelligence` |
| Skill Executed | aecf_codebase_intelligence |
| Sequence Position | 1 |
| Total Prompts Executed | 1 |
| Exclusion Manifest | `aecf_prompts/ci_exclusions.json` (applied) |

---

## 1. Project Overview

| Field | Value |
|-------|-------|
| **Name** | spring-framework-petclinic |
| **Version** | 7.0.3 |
| **Packaging** | WAR (`petclinic.war`) |
| **GroupId** | `org.springframework.samples` |
| **Description** | Spring Framework sample app — veterinary practice management using JSP, Spring MVC, Spring Data JPA, Hibernate and JDBC |
| **Java Version** | 21 |
| **Spring Version** | 7.0.6 |

---

## 2. Detected Stack

| Layer | Technology |
|-------|------------|
| Language | Java 21 |
| Web framework | Spring MVC 7.0.6 |
| ORM | Hibernate 7.3.0.Final (default: jpa profile) |
| Alternative ORM | Spring Data JPA 2025.1.2 (spring-data-jpa profile) |
| JDBC layer | Spring JdbcClient (jdbc profile) |
| Connection pool | Tomcat JDBC Pool 11.0.18 |
| Default DB | H2 2.4.240 (in-memory) |
| Alt DBs | HSQLDB, MySQL, PostgreSQL |
| Cache | Caffeine 3.2.3 (Spring Cache abstraction) |
| AOP | AspectJ 1.9.25.1 |
| Logging | SLF4J 2.0.17 + Logback 1.5.32 |
| JSON | Jackson 3.1.1 |
| View layer | JSP + JSTL 3.0.2 + Bootstrap 5.3.8 |
| Build | Maven (mvnw 3.8.4+) + JaCoCo 0.8.14 |
| Container | Docker via Jib 3.5.1 (jetty:11.0-jdk21) |
| CI/CD | GitHub Actions + SonarCloud |

**Language distribution (src/main/java)**:
- Java: 100% (61 files, ~3,114 LOC)
- XML configs: 6 files
- SQL scripts: 8 files
- JSP views: 10 files
- SCSS: 4 files
- Properties: 7 files

---

## 3. Project Structure

```
spring-framework-petclinic/
├── pom.xml                          # Maven build (Java 21, Spring 7.0.6)
├── mvnw / mvnw.cmd                  # Maven wrapper
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── org/springframework/samples/petclinic/
│   │   │       ├── PetclinicInitializer.java   ← bootstrap entry point
│   │   │       ├── model/                      ← JPA entities (11 files)
│   │   │       ├── service/                    ← facade (2 files)
│   │   │       ├── repository/                 ← interfaces + 3 impls
│   │   │       │   ├── OwnerRepository.java
│   │   │       │   ├── PetRepository.java
│   │   │       │   ├── VetRepository.java
│   │   │       │   ├── VisitRepository.java
│   │   │       │   ├── jdbc/                   ← 10 files (Spring JdbcClient)
│   │   │       │   ├── jpa/                    ← 5 files (Hibernate/JPA)
│   │   │       │   └── springdatajpa/          ← 4 files (Spring Data JPA)
│   │   │       ├── web/                        ← controllers (8 files)
│   │   │       └── util/                       ← AOP + utilities (2 files)
│   │   ├── resources/
│   │   │   ├── spring/                         ← XML Spring configs (6 files)
│   │   │   ├── db/{h2,hsqldb,mysql,postgresql}/ ← SQL scripts
│   │   │   ├── messages/                       ← i18n (de, en, es)
│   │   │   └── logback.xml
│   │   └── webapp/
│   │       └── WEB-INF/
│   │           ├── jsp/                        ← JSP views (9 files)
│   │           └── tags/                       ← JSP tag files (9 files)
│   └── test/
│       ├── java/
│       │   └── .../petclinic/
│       │       ├── model/                      ← unit tests (4 files)
│       │       ├── service/                    ← integration tests (4 files)
│       │       └── web/                        ← MockMvc tests (6 files)
│       ├── resources/spring/                   ← test Spring configs
│       └── jmeter/petclinic_test_plan.jmx
└── .github/workflows/               ← GitHub Actions CI
```

---

## 4. Entry Points

| Type | Location | Description |
|------|----------|-------------|
| **Application bootstrap** | `PetclinicInitializer.java:39` | Servlet 3.0+ programmatic bootstrap — loads Spring contexts |
| **Web root** | `GET /` | Mapped to `welcome.jsp` |
| **Owner CRUD** | `OwnerController` | 7 routes under `/owners/**` |
| **Pet CRUD** | `PetController` | 4 routes under `/owners/{ownerId}/pets/**` |
| **Visit CRUD** | `VisitController` | 3 routes under `/owners/*/pets/{petId}/visits/**` |
| **Vet list** | `VetController` | `GET /vets`, `/vets.json`, `/vets.xml` |
| **Error demo** | `CrashController` | `GET /oups` — intentional exception |
| **DB init** | `datasource-config.xml` | `jdbc:initialize-database` runs at startup |

---

## 5. Core Modules

| Module | Files | Purpose |
|--------|-------|---------|
| `model` | 11 | JPA domain entities — Owner, Pet, PetType, Visit, Vet, Specialty, Vets, and base classes |
| `service` | 2 | `ClinicService` interface + `ClinicServiceImpl` facade (single @Service bean) |
| `repository` (interfaces) | 4 | `OwnerRepository`, `PetRepository`, `VetRepository`, `VisitRepository` |
| `repository/jpa` | 5 | Hibernate/JPA implementations (default profile) |
| `repository/jdbc` | 10 | Spring JdbcClient implementations (jdbc profile) |
| `repository/springdatajpa` | 4 | Spring Data JPA interfaces (spring-data-jpa profile) |
| `web` | 8 | Spring MVC controllers + formatter + validator |
| `util` | 2 | `CallMonitoringAspect` (AOP + JMX) + `EntityUtils` |

---

## 6. Core Classes

| Class | File | Role |
|-------|------|------|
| `ClinicService` | `service/ClinicService.java:32` | Central service interface — single entry point for all domain operations |
| `ClinicServiceImpl` | `service/ClinicServiceImpl.java:40` | Only service implementation — @Cacheable on findPetTypes and findVets |
| `Owner` | `model/Owner.java:45` | Primary aggregate root — owns Pet collection (CASCADE ALL) |
| `Pet` | `model/Pet.java:46` | Entity with bidirectional associations to Owner and Visit |
| `PetclinicInitializer` | `PetclinicInitializer.java:39` | Application bootstrap — programmatic Servlet 3.0+ replacement for web.xml |
| `OwnerController` | `web/OwnerController.java:39` | Busiest controller — 7 HTTP endpoints |
| `CallMonitoringAspect` | `util/CallMonitoringAspect.java:39` | AOP around-advice on service calls — tracks count and timing via JMX |

---

## 7. Core Functions

| Method | Signature | Notes |
|--------|-----------|-------|
| `ClinicService.findOwnerById` | `Owner findOwnerById(int id)` | Used by OwnerController, PetController, VisitController |
| `ClinicService.saveOwner` | `void saveOwner(Owner owner)` | Triggers @Transactional write |
| `ClinicService.findVets` | `Collection<Vet> findVets()` | @Cacheable("vets") |
| `ClinicService.findPetTypes` | `Collection<PetType> findPetTypes()` | @Cacheable("default") |
| `Owner.addPet` | `void addPet(Pet pet)` | Maintains bidirectional association |
| `Pet.addVisit` | `void addVisit(Visit visit)` | Maintains bidirectional association |
| `EntityUtils.getById` | `static <T> T getById(Collection<T>, Class<T>, int)` | Shared helper for lookup by ID |
| `CallMonitoringAspect.invoke` | `Object invoke(ProceedingJoinPoint)` | @Around all service calls |

---

## 8. Architecture Style

**Pattern**: Modular Monolith — classic Spring MVC 3-tier

```
HTTP Request
    ↓
DispatcherServlet (mvc-core-config.xml)
    ↓
@Controller (web/) — validates input, binds to model
    ↓
ClinicService (interface) → ClinicServiceImpl (@Service @Transactional)
    ↓
Repository Interface (OwnerRepository / PetRepository / VetRepository / VisitRepository)
    ↓
[profile: jpa]           [profile: spring-data-jpa]    [profile: jdbc]
JpaXxxRepositoryImpl     SpringDataXxxRepository        JdbcXxxRepositoryImpl
    ↓                            ↓                              ↓
Hibernate/JPA            Spring Data JPA            Spring JdbcClient
    ↓                            ↓                              ↓
RDBMS (H2 / HSQLDB / MySQL / PostgreSQL — selected by Maven DB profile)
```

**Key architectural decisions**:
1. **Strategy pattern for persistence**: 3 interchangeable repository implementations selected by Spring profile at boot time. No code change required to switch persistence strategy.
2. **Service as facade**: `ClinicServiceImpl` aggregates all 4 repositories — controllers never touch repositories directly.
3. **No Spring Security**: No authentication or authorization detected.
4. **XML-based configuration**: All Spring context configuration is XML (not Java @Configuration). This is intentional as a teaching artifact.
5. **Caffeine cache**: Two named caches (`vets`, `default`) with no TTL configured — cache entries persist indefinitely per application lifecycle.

---

## 9. Code Hotspots

| File | LOC | Risk | Reason |
|------|-----|------|--------|
| `ClinicService.java` | 53 | 🔴 HIGH | Referenced by 5 classes — central SPoF |
| `OneToManyResultSetExtractor.java` | 159 | 🟡 MEDIUM | Largest file — complex generic JDBC logic |
| `JdbcOwnerRepositoryImpl.java` | 156 | 🟡 MEDIUM | SQL joins + lazy-loading + object mapping |
| `Owner.java` | 152 | 🟡 MEDIUM | Aggregate root with cascade + bidirectional associations |
| `JdbcPetRepositoryImpl.java` | 117 | 🟡 MEDIUM | Cross-repository dependency on OwnerRepository |
| `ClinicServiceImpl.java` | 111 | 🟡 MEDIUM | Single concrete service — cache invalidation not managed |
| `OwnerController.java` | 132 | 🟡 MEDIUM | 7 endpoints — busiest controller |

> No monolithic files (>500 LOC) detected. All hotspots are coupling/reference based.

---

## 10. Configuration Areas

| Area | File(s) |
|------|---------|
| Spring root context | `src/main/resources/spring/business-config.xml`, `tools-config.xml` |
| Spring MVC context | `src/main/resources/spring/mvc-core-config.xml`, `mvc-view-config.xml` |
| DataSource + DB init | `src/main/resources/spring/datasource-config.xml` |
| Runtime properties | `src/main/resources/spring/data-access.properties` |
| Logging | `src/main/resources/logback.xml` |
| Build + dependencies | `pom.xml` |
| CI/CD | `.github/workflows/maven-build-main.yml`, `maven-build-pull-request.yml` |
| Dev container | `.devcontainer/devcontainer.json` |

---

## 11. Testing Structure

| Level | Files | Framework | Notes |
|-------|-------|-----------|-------|
| Unit (model) | 4 | JUnit Jupiter 6.0.2 + AssertJ | Tests entity validation constraints and behavior |
| Integration (service) | 4 | JUnit Jupiter + Spring Test | `AbstractClinicServiceTests` abstract base — 3 concrete subclasses for jdbc, jpa, spring-data-jpa profiles |
| Web (MockMvc) | 6 | Spring MockMvc + Mockito | Controller tests with mocked ClinicService |
| Load | 1 | JMeter | `src/test/jmeter/petclinic_test_plan.jmx` |
| Coverage | — | JaCoCo 0.8.14 | XML report at `prepare-package` phase, published to SonarCloud |

**Test pattern matched by Surefire**: `**/*Tests.java`

---

## 12. Risk Areas

| Risk | Severity | Details |
|------|----------|---------|
| No authentication/authorization | 🔴 HIGH | No Spring Security or equivalent detected. Any route is publicly accessible. |
| Cache without TTL | 🟡 MEDIUM | `vets` and `default` Caffeine caches have no TTL — stale data risk on long-running instances |
| Cross-repository coupling | 🟡 MEDIUM | `JdbcPetRepositoryImpl` injects `OwnerRepository` — violates aggregate boundary isolation |
| XML Spring configuration | 🟡 MEDIUM | All context wiring is XML-based — harder to refactor, no compile-time type safety |
| Single `ClinicService` concrete implementation | 🟡 MEDIUM | No fallback if `ClinicServiceImpl` fails — no circuit breaker or retry logic |
| No secrets management | 🟡 MEDIUM | DB credentials are in `data-access.properties` (committed) — not externalized |
| Java 21 + Spring 7.0.6 (cutting-edge) | 🟡 MEDIUM | Very new versions — potential for undiscovered compatibility issues |

---

*Generated by `aecf_codebase_intelligence` — prompt-only mode | TOPIC: codebase_intelligence*
