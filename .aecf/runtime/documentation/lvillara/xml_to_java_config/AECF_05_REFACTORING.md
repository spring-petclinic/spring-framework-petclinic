# AECF — Refactoring: XML → Java Config (Phase 1 Implementation)

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
| Sequence Position | 5 |
| Total Prompts Executed | 7 |

---

## Files Created

| File | Replaces | Profile |
|------|----------|---------|
| [config/BusinessConfig.java](src/main/java/org/springframework/samples/petclinic/config/BusinessConfig.java) | Global section of `business-config.xml` | all |
| [config/DataSourceConfig.java](src/main/java/org/springframework/samples/petclinic/config/DataSourceConfig.java) | Phase 1 bridge → `datasource-config.xml` | all |
| [config/JpaSharedConfig.java](src/main/java/org/springframework/samples/petclinic/config/JpaSharedConfig.java) | `<beans profile="jpa,spring-data-jpa">` | jpa, spring-data-jpa |
| [config/JpaRepositoryConfig.java](src/main/java/org/springframework/samples/petclinic/config/JpaRepositoryConfig.java) | `<beans profile="jpa">` component-scan | jpa |
| [config/JdbcConfig.java](src/main/java/org/springframework/samples/petclinic/config/JdbcConfig.java) | `<beans profile="jdbc">` | jdbc |
| [config/SpringDataJpaConfig.java](src/main/java/org/springframework/samples/petclinic/config/SpringDataJpaConfig.java) | `<beans profile="spring-data-jpa">` | spring-data-jpa |

**Files modified**: None — existing XML and test files are untouched in Phase 1.

---

## Remediation Applied per File

### `BusinessConfig.java`
- **`@EnableTransactionManagement`** — replaces `<tx:annotation-driven/>`. Defaults to `AdviceMode.PROXY`, identical to XML default.
- **`@ComponentScan("...service")`** — replaces `<context:component-scan base-package="...service"/>`.
- **`@Import(DataSourceConfig.class)`** — replaces `<import resource="datasource-config.xml"/>`.
- **`static PropertySourcesPlaceholderConfigurer`** — replaces `<context:property-placeholder system-properties-mode="OVERRIDE"/>`. Must be `static` to resolve `@Value` early in context lifecycle. `PropertySourcesPlaceholderConfigurer` uses `StandardEnvironment` which already prioritises system properties — no explicit `setSystemPropertiesMode()` call needed (that method belongs to the older `PropertyPlaceholderConfigurer`).

### `DataSourceConfig.java`
- **`@ImportResource("classpath:spring/datasource-config.xml")`** — Phase 1 bridge. Imports the XML `dataSource` bean into the Java Config context without duplicating it. Phase 2 will replace this with explicit `@Bean DataSource` + `DataSourceInitializer`.

### `JpaSharedConfig.java`
- **`@Profile({"jpa", "spring-data-jpa"})`** — preserves the multi-profile condition from `<beans profile="jpa,spring-data-jpa">`.
- **`@Bean("entityManagerFactory")`** — explicit name ensures `@PersistenceContext` injection in repositories finds the correct EMF. `persistenceUnitName="petclinic"` set; `packagesToScan` omitted (was already inactive per XML comment).
- **`@Value("${jpa.database}") private Database jpaDatabase`** — Spring converts the `String` property value to the `org.springframework.orm.jpa.vendor.Database` enum via `ConversionService`, same as XML property binding.
- **`@Bean("transactionManager")`** — explicit name matching `@EnableTransactionManagement` convention.
- **`PersistenceExceptionTranslationPostProcessor`** — explicit `@Bean` preserves exception translation for `@Repository` classes.

### `JpaRepositoryConfig.java`
- **`@Profile("jpa")`** + **`@ComponentScan("...repository.jpa")`** — direct equivalent of `<beans profile="jpa"><context:component-scan .../></beans>`.

### `JdbcConfig.java`
- **`@Profile("jdbc")`** + **`@ComponentScan("...repository.jdbc")`** — replaces jdbc profile component-scan.
- **`@Bean("transactionManager") DataSourceTransactionManager`** — replaces `<bean id="transactionManager" class="DataSourceTransactionManager" p:dataSource-ref="dataSource"/>`.
- **`@Bean JdbcClient.create(dataSource)`** — replaces `<bean id="jdbcClient" factory-method="create">`.
- **`@Bean NamedParameterJdbcTemplate`** — direct constructor equivalent.

### `SpringDataJpaConfig.java`
- **`@Profile("spring-data-jpa")`** + **`@EnableJpaRepositories(...)`** — replaces `<jpa:repositories base-package="...springdatajpa"/>`. Added explicit `entityManagerFactoryRef` and `transactionManagerRef` to avoid convention-based defaults that could fail if bean names ever change.

---

## Deviations from Plan

| Deviation | Reason |
|-----------|--------|
| `PropertySourcesPlaceholderConfigurer.setSystemPropertiesMode()` not called | This method does not exist on `PropertySourcesPlaceholderConfigurer` — it belongs to the older `PropertyPlaceholderConfigurer`. `PropertySourcesPlaceholderConfigurer` achieves the same OVERRIDE semantics via `StandardEnvironment` automatically. |
| `@EnableTransactionManagement` without explicit `mode=` | `AdviceMode` is a top-level enum (`org.springframework.transaction.annotation.AdviceMode`), not an inner type of `@EnableTransactionManagement`. Default mode is `PROXY`, which matches XML `<tx:annotation-driven/>` default. Leaving it to the default is cleaner and equivalent. |

---

## Pending (Next Phases)

| Phase | Work Remaining |
|-------|---------------|
| Phase 2 | Add parallel test classes (`ClinicServiceJpaConfigTests`, etc.) per TEST_STRATEGY |
| Phase 2 | Run `mvn test` — all 87 existing + 45 new Java Config tests must pass |
| Phase 3 | Switch `ClinicServiceXxxTests` from `locations=` to `classes=` |
| Phase 4 (after tools-config.xml migration) | Update `PetclinicInitializer` to `AnnotationConfigWebApplicationContext` |
| Phase 5 | Migrate `datasource-config.xml` → full `DataSourceConfig.java` body |
| Phase 6 | Delete XML files |

---

_Document generated by `aecf_refactor` | Phase 5/7 | TOPIC: xml_to_java_config_
