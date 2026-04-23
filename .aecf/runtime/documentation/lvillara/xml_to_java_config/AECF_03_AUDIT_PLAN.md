# AECF — Audit Plan: XML → Java Config Refactor

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
| Sequence Position | 3 |
| Total Prompts Executed | 7 |

---

## Audit Dimensions

### D1 — Does the plan preserve all public contracts?

| Contract | Preserved? | Evidence |
|----------|-----------|---------|
| `transactionManager` bean name | ✅ YES | Explicit `@Bean("transactionManager")` in JpaSharedConfig and JdbcConfig |
| `entityManagerFactory` bean name | ✅ YES | Explicit `@Bean("entityManagerFactory")` in JpaSharedConfig |
| `dataSource` bean name | ✅ YES | Provided by `datasource-config.xml` (via Phase 1 `@ImportResource`) |
| `jdbcClient` bean name | ✅ YES | `@Bean public JdbcClient jdbcClient()` — Spring uses method name as bean name |
| `namedParameterJdbcTemplate` bean name | ✅ YES | Same — method name convention |
| Service package scan | ✅ YES | `@ComponentScan("...service")` in BusinessConfig |
| JPA repo scan (profile=jpa) | ✅ YES | `@ComponentScan("...repository.jpa")` in JpaRepositoryConfig |
| JDBC repo scan (profile=jdbc) | ✅ YES | `@ComponentScan("...repository.jdbc")` in JdbcConfig |
| Spring Data JPA repos (profile=spring-data-jpa) | ✅ YES | `@EnableJpaRepositories(basePackages="...springdatajpa", ...)` in SpringDataJpaConfig |
| `PersistenceExceptionTranslationPostProcessor` | ✅ YES | Explicit `@Bean` in JpaSharedConfig |
| `@Transactional` processing | ✅ YES | `@EnableTransactionManagement(mode=AdviceMode.PROXY)` in BusinessConfig |
| Profile-based bean activation | ✅ YES | `@Profile({"jpa","spring-data-jpa"})`, `@Profile("jpa")`, `@Profile("jdbc")`, `@Profile("spring-data-jpa")` |

**D1 Verdict**: ✅ PASS — All public contracts preserved.

---

### D2 — Is there a rollback strategy?

✅ YES — Fully documented in REFACTOR_PLAN §4:
- Phase 1: Delete new Java config files. XML unchanged. Zero risk.
- Phase 2: Delete parallel test classes. Zero risk.
- Phase 3: `git revert` test file changes.
- Phase 4: `git revert` XML deletion.

Each phase is independently reversible. XML is only deleted in Phase 4, which is the last step and requires all tests to pass first.

**D2 Verdict**: ✅ PASS — Rollback strategy is granular and safe.

---

### D3 — Are the steps truly atomic?

| Step | Atomic? | Verifiable? |
|------|---------|-------------|
| Step 1: Create Java Config classes | ✅ YES | New files only, no existing code modified |
| Step 2: Add parallel test classes | ✅ YES | New test files only, existing tests run unchanged |
| Step 3: Switch test `locations=` → `classes=` | ✅ YES | 3-file change, `mvn test` verifiable |
| Step 4: Update PetclinicInitializer | ✅ YES | 1-file change, smoke test verifiable |
| Step 5: Migrate datasource-config.xml | ✅ YES | Separate phase with independent test gate |
| Step 6: Delete XML files | ✅ YES | Only after Step 5 tests pass |

**D3 Verdict**: ✅ PASS — Steps are atomic and independently verifiable.

---

### D4 — Are risks identified and mitigated?

| Risk | Plan Response | Verdict |
|------|---------------|---------|
| R1: `@EnableTransactionManagement` proxy mode | Explicit `mode=AdviceMode.PROXY` locks it | ✅ MITIGATED |
| R2: `PropertySourcesPlaceholderConfigurer` must be `static @Bean` | Documented + enforced in BusinessConfig | ✅ MITIGATED |
| R3: `@EnableJpaRepositories` default refs | Explicit `entityManagerFactoryRef` + `transactionManagerRef` | ✅ MITIGATED |
| R4: `persistenceUnitName` vs `packagesToScan` conflict | Only `persistenceUnitName` set in Java Config | ✅ MITIGATED |
| R5: Test context differences | Parallel test variants validate before switching | ✅ MITIGATED |
| R6: DataSourceConfig Phase 1 bridge | `@ImportResource("classpath:spring/datasource-config.xml")` as bridge | ✅ MITIGATED |

**D4 Verdict**: ✅ PASS — All 6 risks are identified with concrete mitigations.

---

### D5 — Additional WARN Items

#### ⚠️ WARN-1: `jpa.showSql=true` hardcoded in data-access.properties

This is a pre-existing issue (identified in `persistence_strategies` topic). The refactor preserves the `${jpa.showSql}` property reference — it does NOT fix this. Post-refactor, the issue remains and should be addressed separately.

#### ⚠️ WARN-2: `tools-config.xml` not in scope

`PetclinicInitializer` loads both `business-config.xml` and `tools-config.xml`. This refactor only covers `business-config.xml`. Phase 4's `AnnotationConfigWebApplicationContext` switch requires `ToolsConfig.java` to also exist before PetclinicInitializer can be updated. Phase 5 must migrate `tools-config.xml` before Phase 4 completes.

**Corrected phase order**:
```
Step 4 (Initializer) DEPENDS ON Step 5 (tools-config migration)
→ Reorder: Step 5 (tools-config) BEFORE Step 4 (Initializer)
```

This is a plan amendment — does not affect the Java Config correctness for Steps 1-3.

#### ⚠️ WARN-3: Spring Framework 7.x compatibility

The project uses Spring Framework 7.0.6 and Spring Data JPA 2025.1.2. The Java Config APIs used (LocalContainerEntityManagerFactoryBean, EnableJpaRepositories, etc.) are stable and unchanged in Spring 7.x. No compatibility risk detected.

---

## Gate Decision

| Dimension | Status |
|-----------|--------|
| D1 — Public contracts preserved | ✅ PASS |
| D2 — Rollback strategy | ✅ PASS |
| D3 — Atomic steps | ✅ PASS |
| D4 — Risks mitigated | ✅ PASS |
| D5 — Warnings | ⚠️ 3 WARNINGs (non-blocking) |

### Plan Amendment Required (WARN-2)

Update the incremental migration steps to move tools-config.xml migration (Step 5) before PetclinicInitializer update (Step 4). This amendment does not affect Steps 1-3.

## GATE: ✅ GO

> Conditions: WARN-1 pre-existing (document as accepted), WARN-2 reorder steps 4 and 5, WARN-3 no action needed.

---

_Document generated by `aecf_refactor` | Phase 3/7 | TOPIC: xml_to_java_config_
