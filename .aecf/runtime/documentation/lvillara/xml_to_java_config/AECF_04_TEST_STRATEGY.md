# AECF — Test Strategy: XML → Java Config Regression

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
| Sequence Position | 4 |
| Total Prompts Executed | 7 |

---

## Strategy: Dual-Context Parallel Validation

The migration uses a **parallel validation** approach:

1. **Phase 1 baseline**: Existing tests load `business-config.xml` — must pass 100% before any Java Config code is added.
2. **Phase 2 parallel**: New test classes load Java Config classes for all 3 profiles. Must also pass 100%.
3. **Phase 3 switch**: Existing test classes switch from `locations=` to `classes=`. Must still pass 100%.
4. **Phase 4+ regression gate**: All subsequent phases require `mvn test` passing at each step.

---

## Pre-Refactor Baseline (Phase 1)

No new tests needed. Existing suite covers the full service contract.

| Test Class | Profile | Coverage |
|------------|---------|----------|
| `ClinicServiceJpaTests` | jpa | All 15 service operations via AbstractClinicServiceTests |
| `ClinicServiceJdbcTests` | jdbc | All 15 service operations |
| `ClinicServiceSpringDataJpaTests` | spring-data-jpa | All 15 service operations |

**Verify pre-refactor baseline**:
```bash
mvn test -pl . -Dtest="ClinicServiceJpaTests,ClinicServiceJdbcTests,ClinicServiceSpringDataJpaTests"
```
Expected: 45 tests, 0 failures, 0 errors.

---

## Phase 2 — Parallel Java Config Tests (New Classes)

### Test Class: `ClinicServiceJpaConfigTests`

```java
/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Parallel validation test: loads Java @Configuration classes instead of business-config.xml.
 * Must produce identical behavior to ClinicServiceJpaTests (XML-based).
 */
@SpringJUnitConfig(classes = {BusinessConfig.class, JpaSharedConfig.class, JpaRepositoryConfig.class})
@ActiveProfiles("jpa")
class ClinicServiceJpaConfigTests extends AbstractClinicServiceTests {
}
```

### Test Class: `ClinicServiceJdbcConfigTests`

```java
/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Parallel validation test: loads Java @Configuration classes instead of business-config.xml.
 * Must produce identical behavior to ClinicServiceJdbcTests (XML-based).
 */
@SpringJUnitConfig(classes = {BusinessConfig.class, JdbcConfig.class})
@ActiveProfiles("jdbc")
class ClinicServiceJdbcConfigTests extends AbstractClinicServiceTests {
}
```

### Test Class: `ClinicServiceSpringDataJpaConfigTests`

```java
/**
 * AECF_META: skill=aecf_refactor topic=xml_to_java_config run_time=2026-04-18T00:00:00Z
 * generated_at=2026-04-18T00:00:00Z generated_by=lvillara touch_count=1
 * last_modified_skill=aecf_refactor last_modified_at=2026-04-18T00:00:00Z last_modified_by=lvillara
 *
 * Parallel validation test: loads Java @Configuration classes instead of business-config.xml.
 * Must produce identical behavior to ClinicServiceSpringDataJpaTests (XML-based).
 */
@SpringJUnitConfig(classes = {BusinessConfig.class, JpaSharedConfig.class, SpringDataJpaConfig.class})
@ActiveProfiles("spring-data-jpa")
class ClinicServiceSpringDataJpaConfigTests extends AbstractClinicServiceTests {
}
```

**Verify Phase 2** (90 total tests: 45 XML + 45 Java Config):
```bash
mvn test
```
Expected: All 90 tests pass.

---

## Phase 3 — Switch Existing Tests to Java Config

Modify `ClinicServiceJpaTests`, `ClinicServiceJdbcTests`, `ClinicServiceSpringDataJpaTests`:

```java
// BEFORE
@SpringJUnitConfig(locations = {"classpath:spring/business-config.xml"})

// AFTER
@SpringJUnitConfig(classes = {BusinessConfig.class, JpaSharedConfig.class, JpaRepositoryConfig.class})
```

Remove the parallel Config test classes (they are now redundant).

**Verify Phase 3**:
```bash
mvn test
```
Expected: 45 tests, 0 failures.

---

## Regression Risk Areas and Specific Verification Points

| Risk Area | Test Verification | What to Check |
|-----------|------------------|---------------|
| `transactionManager` bean lookup | All `@Transactional` tests | If TX not found, tests throw `NoSuchBeanDefinitionException` on startup |
| `entityManagerFactory` not found | JPA profile tests | `@PersistenceContext` injection fails on startup |
| `@EnableTransactionManagement` proxy mode | Tests with `@Transactional` rollback | If mode=ASPECTJ, proxy behavior changes |
| Profile `spring-data-jpa` + `entityManagerFactoryRef` | SpringDataJpa tests | Spring Data can't find EMF if ref name differs |
| `PropertySourcesPlaceholderConfigurer` static | Any test with `@Value` property | Non-static PSPC causes `BeanDefinitionParsingException` at context load |
| `PersistenceExceptionTranslationPostProcessor` | JDBC/JPA exception propagation | `DataAccessException` wrapping broken if PPT missing |
| `JdbcClient` bean name `jdbcClient` | Jdbc profile tests | `@Autowired JdbcClient jdbcClient` injection fails |

---

## Integration Verification Matrix

| Phase | Command | Pass Criterion |
|-------|---------|----------------|
| Pre-refactor baseline | `mvn test` | 87 existing tests pass |
| Phase 1 complete | `mvn test` | 87 tests still pass (no new tests yet) |
| Phase 2 complete | `mvn test` | 87 + 45 new = 132 tests pass |
| Phase 3 complete | `mvn test` | 87 tests pass (XML tests replaced by Java Config tests) |
| Phase 4 complete | `mvn test` + smoke test | 87 tests pass + app starts via Jetty |

---

## Test Labeling Convention

New test classes created in Phase 2 carry the suffix `ConfigTests` (vs `Tests` for the XML-based originals) to distinguish them during the parallel validation window. They are deleted in Phase 3 once the originals are switched.

---

_Document generated by `aecf_refactor` | Phase 4/7 | TOPIC: xml_to_java_config_
