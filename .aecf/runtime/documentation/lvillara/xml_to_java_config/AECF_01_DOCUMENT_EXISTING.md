# AECF — Document Existing: business-config.xml

## METADATA

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-04-18T00:00:00Z |
| Executed By | lvillara |
| Executed By ID | lvillara |
| Execution Identity Source | git config user |
| Repository | spring-framework-petclinic |
| Branch | appmod/java-upgrade-20260417115818 |
| Root Prompt | `@aecf run skill=aecf_refactor TOPIC=xml_to_java_config` |
| Skill Executed | aecf_refactor |
| Sequence Position | 1 |
| Total Prompts Executed | 7 |

---

## Scope

**Primary file**: [business-config.xml](src/main/resources/spring/business-config.xml)
**Imported file**: [datasource-config.xml](src/main/resources/spring/datasource-config.xml) _(Phase 2 — documented here for reference only)_
**Properties**: [data-access.properties](src/main/resources/spring/data-access.properties)

---

## 1. Context Hierarchy

```
PetclinicInitializer (AbstractDispatcherServletInitializer)
│
├── Root ApplicationContext (XmlWebApplicationContext)
│   ├── classpath:spring/business-config.xml    ← TARGET
│   └── classpath:spring/tools-config.xml
│
└── Servlet ApplicationContext (XmlWebApplicationContext)
    └── classpath:spring/mvc-core-config.xml
```

`business-config.xml` is loaded as the **root context**, shared across the entire application. It bootstraps all service beans, repository beans, transaction infrastructure, and JPA persistence.

---

## 2. Entry Points and Public API

### Beans exported to the root context (consumable by child contexts and tests)

| Bean ID | Type | Profile | Consumed By |
|---------|------|---------|-------------|
| `dataSource` | `org.apache.tomcat.jdbc.pool.DataSource` | all | EntityManagerFactory, JdbcClient, TxManager |
| `entityManagerFactory` | `LocalContainerEntityManagerFactoryBean` | jpa, spring-data-jpa | JpaTransactionManager, @PersistenceContext in repos |
| `transactionManager` | `JpaTransactionManager` or `DataSourceTransactionManager` | per profile | `<tx:annotation-driven/>` |
| `jdbcClient` | `JdbcClient` | jdbc | JdbcOwnerRepositoryImpl, JdbcPetRepositoryImpl, etc. |
| `namedParameterJdbcTemplate` | `NamedParameterJdbcTemplate` | jdbc | JdbcOwnerRepositoryImpl |
| All `@Service` beans | ClinicServiceImpl | all | Web layer |
| All `@Repository` beans | Jpa*/Jdbc* impls | per profile | ClinicServiceImpl |

---

## 3. Behavioral Specification — bean-by-bean

### 3.1 Global (all profiles)

#### `<context:property-placeholder>`
- **File**: `classpath:spring/data-access.properties`
- **Mode**: `system-properties-mode="OVERRIDE"` — system properties take precedence over file properties
- **Resolves**: `${jpa.database}`, `${jpa.showSql}`, `${jdbc.driverClassName}`, `${jdbc.url}`, `${jdbc.username}`, `${jdbc.password}`, `${jdbc.initLocation}`, `${jdbc.dataLocation}`, `${db.script}`

#### `<context:component-scan base-package="org.springframework.samples.petclinic.service"/>`
- Scans and registers `ClinicServiceImpl` (annotated `@Service`)
- Also picks up any other `@Component`/`@Service` in the `service` package

#### `<tx:annotation-driven/>`
- Activates `@Transactional` processing on all beans in the container
- Uses default proxy mode (Spring AOP proxy, not AspectJ)
- Looks for a bean named `transactionManager` by convention

#### `<import resource="datasource-config.xml"/>`
- Registers `dataSource` bean (Tomcat JDBC pool)
- Runs `<jdbc:initialize-database>` (schema.sql + data.sql on startup)
- Conditionally registers a JNDI `dataSource` for profile `javaee`

---

### 3.2 Profile `jpa, spring-data-jpa` (JPA shared)

#### `entityManagerFactory` (`LocalContainerEntityManagerFactoryBean`)
| Property | Value | Source |
|----------|-------|--------|
| `dataSource` | ref→`dataSource` | datasource-config.xml |
| `jpaVendorAdapter` | `HibernateJpaVendorAdapter` | inline |
| `database` | `${jpa.database}` (e.g. `H2`, `MYSQL`) | data-access.properties / Maven profile |
| `showSql` | `${jpa.showSql}` (`true` by default) | data-access.properties |
| `persistenceUnitName` | `petclinic` | inline — **wins over packagesToScan** |
| `packagesToScan` | `org.springframework.samples.petclinic` | inline — **superseded by persistenceUnitName** |

> **Invariant**: `persistenceUnitName` takes precedence over `packagesToScan` per Spring's contract. The `META-INF/persistence.xml` with unit name `petclinic` is the effective entity source.

#### `transactionManager` (`JpaTransactionManager`)
- Wraps the `entityManagerFactory`
- Participates in Spring's `@Transactional` AOP chain
- Bean name `transactionManager` matches `<tx:annotation-driven/>` default lookup

#### `PersistenceExceptionTranslationPostProcessor`
- Post-processor that converts JPA/Hibernate native exceptions to Spring's `DataAccessException` hierarchy
- Applied to all `@Repository`-annotated beans in the context

---

### 3.3 Profile `jpa`

#### `<context:component-scan base-package="org.springframework.samples.petclinic.repository.jpa"/>`
- Registers: `JpaOwnerRepositoryImpl`, `JpaPetRepositoryImpl`, `JpaVetRepositoryImpl`, `JpaVisitRepositoryImpl`
- All annotated `@Repository` + use `@PersistenceContext EntityManager`
- All use `@Transactional` at method level

---

### 3.4 Profile `jdbc`

#### `transactionManager` (`DataSourceTransactionManager`)
- Wraps the `dataSource` directly (no JPA)
- Bean name `transactionManager` matches `<tx:annotation-driven/>` default

#### `jdbcClient` (`JdbcClient`)
- Factory: `JdbcClient.create(dataSource)`
- Used by `JdbcOwnerRepositoryImpl`, `JdbcPetRepositoryImpl`, `JdbcVetRepositoryImpl`, `JdbcVisitRepositoryImpl`

#### `namedParameterJdbcTemplate` (`NamedParameterJdbcTemplate`)
- Wraps `dataSource`
- Also used in JDBC repositories (some operations)

#### `<context:component-scan base-package="org.springframework.samples.petclinic.repository.jdbc"/>`
- Registers all `JdbcXxxRepositoryImpl` classes

---

### 3.5 Profile `spring-data-jpa`

#### `<jpa:repositories base-package="org.springframework.samples.petclinic.repository.springdatajpa"/>`
- Activates Spring Data JPA infrastructure
- Creates proxy implementations for: `SpringDataOwnerRepository`, `SpringDataPetRepository`, `SpringDataVetRepository`, `SpringDataVisitRepository`
- Requires `entityManagerFactory` and `transactionManager` from profile `jpa,spring-data-jpa`

---

## 4. Side Effects

| Side Effect | Where | Impact |
|-------------|-------|--------|
| DB schema + data initialization | `datasource-config.xml` via `jdbc:initialize-database` | Runs on every cold start; fails if scripts have errors |
| JPA persistence.xml registration | EntityManagerFactory → `petclinic` PU | All JPA entities in `META-INF/persistence.xml` become managed |
| Hibernate DDL validation | `showSql=true` always in `data-access.properties` | SQL visible in logs across all environments |
| Spring Data JPA proxy infrastructure | `<jpa:repositories>` | Creates JDK proxies; impacts AOP pointcut matching (see `aop_monitoring_aspect` topic) |

---

## 5. Test Coupling (Regression Baseline)

All 3 service integration test classes use the same bootstrap:

```java
@SpringJUnitConfig(locations = {"classpath:spring/business-config.xml"})
@ActiveProfiles("jpa")   // or "jdbc" or "spring-data-jpa"
class ClinicServiceXxxTests extends AbstractClinicServiceTests { }
```

Tests:
- [ClinicServiceJpaTests.java](src/test/java/org/springframework/samples/petclinic/service/ClinicServiceJpaTests.java)
- [ClinicServiceJdbcTests.java](src/test/java/org/springframework/samples/petclinic/service/ClinicServiceJdbcTests.java)
- [ClinicServiceSpringDataJpaTests.java](src/test/java/org/springframework/samples/petclinic/service/ClinicServiceSpringDataJpaTests.java)

**Contract under test** (`AbstractClinicServiceTests`): All ClinicService CRUD operations across all 3 profiles.

---

## 6. Dependencies (Internal)

```
business-config.xml
├── datasource-config.xml          (import — provides dataSource)
│   └── data-access.properties     (JDBC + JPA settings)
├── data-access.properties         (also imported directly for JPA settings)
├── META-INF/persistence.xml       (petclinic PU — entity definitions)
└── repository.{jpa|jdbc|springdatajpa}  (component-scanned per profile)
```

---

## 7. Summary — What Must Be Preserved

| Contract | Must Not Change |
|----------|-----------------|
| `entityManagerFactory` bean name and type | Required by @PersistenceContext injection |
| `transactionManager` bean name | Required by `<tx:annotation-driven/>` convention |
| `dataSource` bean name | Required by EntityManagerFactory + JdbcClient + TxManager refs |
| `jdbcClient` bean name | Required by `@Autowired` in JDBC repos |
| `namedParameterJdbcTemplate` bean name | Required by `@Autowired` in JDBC repos |
| Profile activation conditions | `jpa`, `jdbc`, `spring-data-jpa` must activate identical bean sets |
| `system-properties-mode=OVERRIDE` semantics | System properties must override file properties |
| Exception translation for @Repository | `PersistenceExceptionTranslationPostProcessor` must be registered |

---

_Document generated by `aecf_refactor` | Phase 1/7 | TOPIC: xml_to_java_config_
