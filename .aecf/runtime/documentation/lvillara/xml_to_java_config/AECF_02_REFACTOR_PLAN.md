# AECF — Refactor Plan: XML → Java Config (business-config.xml)

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
| Sequence Position | 2 |
| Total Prompts Executed | 7 |

---

## 1. Changes Inventory

**Files to review**: [business-config.xml](src/main/resources/spring/business-config.xml), [datasource-config.xml](src/main/resources/spring/datasource-config.xml)

**Problems to resolve**: Migrate Spring XML configuration to type-safe Java `@Configuration` classes, preserving all `@Profile` conditions and observable behavior.

### Files to Create

| New File | Replaces | Profile |
|----------|----------|---------|
| `config/BusinessConfig.java` | Global section of `business-config.xml` | all |
| `config/JpaSharedConfig.java` | `<beans profile="jpa,spring-data-jpa">` | jpa, spring-data-jpa |
| `config/JpaRepositoryConfig.java` | `<beans profile="jpa">` component-scan | jpa |
| `config/JdbcConfig.java` | `<beans profile="jdbc">` | jdbc |
| `config/SpringDataJpaConfig.java` | `<beans profile="spring-data-jpa">` | spring-data-jpa |
| `config/DataSourceConfig.java` | `datasource-config.xml` _(Phase 2)_ | all |

### Files Modified (Phase 3+, after validation)

| File | Change |
|------|--------|
| `PetclinicInitializer.java` | Switch `XmlWebApplicationContext` → `AnnotationConfigWebApplicationContext` |
| `ClinicServiceJpaTests.java` | Switch `locations=` → `classes=` |
| `ClinicServiceJdbcTests.java` | Switch `locations=` → `classes=` |
| `ClinicServiceSpringDataJpaTests.java` | Switch `locations=` → `classes=` |

### Files Deleted (Phase 4, only after all tests pass with Java Config)

| File | When |
|------|------|
| `business-config.xml` | After Phase 3 tests pass |
| `datasource-config.xml` | After Phase 2+3 complete |

---

## 2. Behavior Preservation Guarantees

| Guarantee | Mechanism |
|-----------|-----------|
| Same `transactionManager` bean name | Explicit `@Bean("transactionManager")` in JpaSharedConfig / JdbcConfig |
| Same `entityManagerFactory` bean name | Explicit `@Bean("entityManagerFactory")` in JpaSharedConfig |
| Profile conditions identical | `@Profile({"jpa","spring-data-jpa"})`, `@Profile("jpa")`, `@Profile("jdbc")`, `@Profile("spring-data-jpa")` |
| `system-properties-mode=OVERRIDE` | `StandardEnvironment` already prioritizes system properties over `@PropertySource` — behavior equivalent |
| `PersistenceExceptionTranslationPostProcessor` | Explicit `@Bean` in JpaSharedConfig |
| Component-scan packages identical | `@ComponentScan` in BusinessConfig (service), JpaRepositoryConfig (jpa repos), JdbcConfig (jdbc repos) |
| `EnableJpaRepositories` base-package | `@EnableJpaRepositories("...springdatajpa")` in SpringDataJpaConfig |
| `@Transactional` processing active | `@EnableTransactionManagement` on BusinessConfig |

---

## 3. Risk Assessment

| Risk ID | Risk | Severity | Mitigation |
|---------|------|----------|------------|
| R1 | `@EnableTransactionManagement` proxy mode defaults may differ from XML `<tx:annotation-driven/>` | LOW | Both default to `PROXY` mode (not `ASPECTJ`). Explicit `@EnableTransactionManagement(mode=AdviceMode.PROXY)` to lock. |
| R2 | `PropertySourcesPlaceholderConfigurer` must be `static @Bean` to resolve `@Value` in `@Configuration` classes | HIGH | Declare `static @Bean PropertySourcesPlaceholderConfigurer` in BusinessConfig. Non-static causes early-init failure in BeanFactory. |
| R3 | `<jpa:repositories>` XML vs `@EnableJpaRepositories` — different default `entityManagerFactoryRef` | LOW | Both default to bean named `entityManagerFactory`. Explicit `entityManagerFactoryRef="entityManagerFactory"` + `transactionManagerRef="transactionManager"` in `@EnableJpaRepositories` to be safe. |
| R4 | `persistenceUnitName` wins over `packagesToScan` — must not add `setPackagesToScan()` in Java Config | LOW | Java Config sets only `persistenceUnitName`. Drop `packagesToScan` — it was already inactive per XML comment. |
| R5 | Test bootstrap changes — `@SpringJUnitConfig(locations=...)` → `classes=` can expose hidden context differences | MEDIUM | Phase 2 adds parallel test variants (XML + Java Config both present). Java Config tests must pass before removing XML tests. |
| R6 | `DataSourceConfig.java` for `datasource-config.xml` is Phase 2 — tests in Phase 1 still require XML datasource | LOW | Phase 1 Java Config imports `datasource-config.xml` via `@ImportResource` as bridge. Phase 2 replaces it. |

---

## 4. Rollback Strategy

- **Phase 1** (Java Config classes created, XML still present): Delete new `.java` config files. Zero impact.
- **Phase 2** (Test variants added): Delete new test classes. Zero impact on existing tests.
- **Phase 3** (Existing tests switched to Java Config): `git revert` the test file changes. XML classes still present.
- **Phase 4** (XML deleted): `git revert` the deletion commit.

All phases are independently reversible via Git. No destructive step until Phase 4.

---

## 5. Incremental Migration Steps

```
Step 1:  Create BusinessConfig.java + JpaSharedConfig.java + JpaRepositoryConfig.java
         + JdbcConfig.java + SpringDataJpaConfig.java
         [Bridge: @ImportResource("classpath:spring/datasource-config.xml") in DataSourceConfig placeholder]

Step 2:  Create parallel test variants that load Java Config instead of XML
         ClinicServiceJpaConfigTests, ClinicServiceJdbcConfigTests, ClinicServiceSpringDataJpaConfigTests
         Run: mvn test  → all 87 existing tests must still pass
         Run: new config tests must also pass

Step 3:  Switch existing test classes from locations= to classes=
         Run: mvn test  → 87/87 must pass

Step 4:  Update PetclinicInitializer to AnnotationConfigWebApplicationContext
         Run: mvn test + manual smoke test

Step 5:  Migrate datasource-config.xml → DataSourceConfig.java (Phase 2)

Step 6:  Delete XML files, run full test suite
```

---

## 6. Target Java @Configuration Classes

### 6.1 `BusinessConfig.java`

```java
package org.springframework.samples.petclinic.config;

/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Root application context configuration — replaces the global section of business-config.xml.
 * Activates @Transactional processing, scans service beans, loads data-access.properties.
 * DataSource is imported from DataSourceConfig (bridge: @ImportResource until datasource-config.xml is migrated).
 */
@Configuration
@EnableTransactionManagement(mode = AdviceMode.PROXY)
@ComponentScan("org.springframework.samples.petclinic.service")
@Import(DataSourceConfig.class)
public class BusinessConfig {

    /**
     * Replaces <context:property-placeholder system-properties-mode="OVERRIDE"/>.
     * Must be static so Spring can process @Value annotations before instantiating @Configuration beans.
     * StandardEnvironment already prioritizes system properties, preserving OVERRIDE semantics.
     */
    @Bean
    public static PropertySourcesPlaceholderConfigurer propertySourcesPlaceholderConfigurer() {
        PropertySourcesPlaceholderConfigurer pspc = new PropertySourcesPlaceholderConfigurer();
        pspc.setLocation(new ClassPathResource("spring/data-access.properties"));
        pspc.setSystemPropertiesMode(PropertySourcesPlaceholderConfigurer.SYSTEM_PROPERTIES_MODE_OVERRIDE);
        return pspc;
    }
}
```

### 6.2 `DataSourceConfig.java` (Phase 1 bridge — imports XML, Phase 2 full migration)

```java
package org.springframework.samples.petclinic.config;

/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Phase 1 bridge: delegates to datasource-config.xml via @ImportResource.
 * Phase 2 will replace this class body with full Java Config (DataSource bean + DataSourceInitializer).
 */
@Configuration
@ImportResource("classpath:spring/datasource-config.xml")
public class DataSourceConfig {
    // Phase 1: empty body — datasource-config.xml provides all DataSource beans
    // Phase 2: replace @ImportResource with explicit @Bean DataSource + DataSourceInitializer
}
```

### 6.3 `JpaSharedConfig.java`

```java
package org.springframework.samples.petclinic.config;

/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * JPA shared infrastructure for profiles "jpa" and "spring-data-jpa".
 * Replaces <beans profile="jpa,spring-data-jpa"> in business-config.xml.
 * Provides EntityManagerFactory, JpaTransactionManager, and exception translation.
 */
@Configuration
@Profile({"jpa", "spring-data-jpa"})
public class JpaSharedConfig {

    @Autowired
    private DataSource dataSource;

    @Value("${jpa.database}")
    private Database jpaDatabase;

    @Value("${jpa.showSql}")
    private boolean showSql;

    /**
     * Replaces LocalContainerEntityManagerFactoryBean XML bean.
     * Note: persistenceUnitName wins over packagesToScan per Spring contract —
     * packagesToScan is intentionally omitted (was already inactive in XML).
     */
    @Bean("entityManagerFactory")
    public LocalContainerEntityManagerFactoryBean entityManagerFactory() {
        LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
        em.setDataSource(dataSource);
        HibernateJpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
        vendorAdapter.setDatabase(jpaDatabase);
        vendorAdapter.setShowSql(showSql);
        em.setJpaVendorAdapter(vendorAdapter);
        em.setPersistenceUnitName("petclinic");
        return em;
    }

    /** Replaces JpaTransactionManager XML bean. Bean name "transactionManager" matches tx:annotation-driven default. */
    @Bean("transactionManager")
    public PlatformTransactionManager transactionManager(EntityManagerFactory emf) {
        return new JpaTransactionManager(emf);
    }

    /** Replaces PersistenceExceptionTranslationPostProcessor XML bean. */
    @Bean
    public PersistenceExceptionTranslationPostProcessor exceptionTranslation() {
        return new PersistenceExceptionTranslationPostProcessor();
    }
}
```

### 6.4 `JpaRepositoryConfig.java`

```java
package org.springframework.samples.petclinic.config;

/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Scans JPA repository implementations for the "jpa" profile.
 * Replaces <beans profile="jpa"><context:component-scan.../> in business-config.xml.
 */
@Configuration
@Profile("jpa")
@ComponentScan("org.springframework.samples.petclinic.repository.jpa")
public class JpaRepositoryConfig {
    // No explicit beans — JpaXxxRepositoryImpl classes carry @Repository and are discovered by scan
}
```

### 6.5 `JdbcConfig.java`

```java
package org.springframework.samples.petclinic.config;

/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * JDBC infrastructure for the "jdbc" profile.
 * Replaces <beans profile="jdbc"> in business-config.xml.
 * Provides DataSourceTransactionManager, JdbcClient, NamedParameterJdbcTemplate, and JDBC repo scan.
 */
@Configuration
@Profile("jdbc")
@ComponentScan("org.springframework.samples.petclinic.repository.jdbc")
public class JdbcConfig {

    @Autowired
    private DataSource dataSource;

    /** Bean name "transactionManager" matches tx:annotation-driven default. */
    @Bean("transactionManager")
    public PlatformTransactionManager transactionManager() {
        return new DataSourceTransactionManager(dataSource);
    }

    /** Replaces <bean id="jdbcClient" factory-method="create"> */
    @Bean
    public JdbcClient jdbcClient() {
        return JdbcClient.create(dataSource);
    }

    @Bean
    public NamedParameterJdbcTemplate namedParameterJdbcTemplate() {
        return new NamedParameterJdbcTemplate(dataSource);
    }
}
```

### 6.6 `SpringDataJpaConfig.java`

```java
package org.springframework.samples.petclinic.config;

/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Spring Data JPA repository scanning for the "spring-data-jpa" profile.
 * Replaces <jpa:repositories base-package="...springdatajpa"/> in business-config.xml.
 * entityManagerFactoryRef and transactionManagerRef are explicit to avoid relying on defaults.
 */
@Configuration
@Profile("spring-data-jpa")
@EnableJpaRepositories(
    basePackages = "org.springframework.samples.petclinic.repository.springdatajpa",
    entityManagerFactoryRef = "entityManagerFactory",
    transactionManagerRef = "transactionManager"
)
public class SpringDataJpaConfig {
    // No explicit beans — Spring Data proxies discovered via @EnableJpaRepositories
}
```

---

## 7. PetclinicInitializer Change (Phase 4)

```java
// BEFORE:
protected WebApplicationContext createRootApplicationContext() {
    XmlWebApplicationContext rootAppContext = new XmlWebApplicationContext();
    rootAppContext.setConfigLocations("classpath:spring/business-config.xml",
                                     "classpath:spring/tools-config.xml");
    rootAppContext.getEnvironment().setDefaultProfiles(SPRING_PROFILE);
    return rootAppContext;
}

// AFTER (Phase 4):
protected WebApplicationContext createRootApplicationContext() {
    AnnotationConfigWebApplicationContext rootAppContext = new AnnotationConfigWebApplicationContext();
    rootAppContext.register(BusinessConfig.class, ToolsConfig.class);
    rootAppContext.getEnvironment().setDefaultProfiles(SPRING_PROFILE);
    return rootAppContext;
}
```

> `ToolsConfig.java` (tools-config.xml migration) is out of scope for this refactor — Phase 5.

---

## 8. Test Class Changes (Phase 2 additions, Phase 3 switch)

### Phase 2 — Parallel validation tests (new classes, existing tests untouched)

```java
// NEW: ClinicServiceJpaConfigTests.java
@SpringJUnitConfig(classes = {BusinessConfig.class, JpaSharedConfig.class, JpaRepositoryConfig.class})
@ActiveProfiles("jpa")
class ClinicServiceJpaConfigTests extends AbstractClinicServiceTests { }

// NEW: ClinicServiceJdbcConfigTests.java
@SpringJUnitConfig(classes = {BusinessConfig.class, JdbcConfig.class})
@ActiveProfiles("jdbc")
class ClinicServiceJdbcConfigTests extends AbstractClinicServiceTests { }

// NEW: ClinicServiceSpringDataJpaConfigTests.java
@SpringJUnitConfig(classes = {BusinessConfig.class, JpaSharedConfig.class, SpringDataJpaConfig.class})
@ActiveProfiles("spring-data-jpa")
class ClinicServiceSpringDataJpaConfigTests extends AbstractClinicServiceTests { }
```

### Phase 3 — Switch existing tests to Java Config

```java
// MODIFIED: ClinicServiceJpaTests.java
@SpringJUnitConfig(classes = {BusinessConfig.class, JpaSharedConfig.class, JpaRepositoryConfig.class})
// (remove locations=)
```

---

## 9. Metrics Before/After

| Metric | Before (XML) | After (Java Config) |
|--------|-------------|---------------------|
| Config files | 2 XML (business + datasource) | 6 Java classes (Phase 1+2) |
| Lines of config code | ~97 XML + ~43 XML = ~140 LOC | ~180 Java LOC (more verbose, more type-safe) |
| Compile-time validation | None | Full — missing beans/types caught at compile time |
| IDE navigation | Limited (XML→class) | Full — Ctrl+Click, refactoring, find usages |
| Profile condition clarity | `<beans profile="...">` nested | `@Profile` at class level — explicit |
| Test expressiveness | `locations={"classpath:..."}` | `classes={Config.class}` — type-safe |

---

_Document generated by `aecf_refactor` | Phase 2/7 | TOPIC: xml_to_java_config_
