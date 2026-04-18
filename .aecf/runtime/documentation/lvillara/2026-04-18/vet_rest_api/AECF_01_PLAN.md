# AECF_01 — Plan: VetRestController + OpenAPI Documentation

## METADATA

| Field | Value |
|-------|-------|
| Timestamp (UTC) | 2026-04-18T00:00:00Z |
| Executed By | lvillara |
| Executed By ID | lvillara |
| Execution Identity Source | git config user |
| Repository | spring-framework-petclinic |
| Branch | appmod/java-upgrade-20260417115818 |
| Root Prompt | `@aecf run skill=aecf_new_feature TOPIC=vet_rest_api` |
| Skill Executed | aecf_new_feature |
| Sequence Position | 1 of 6 |
| Total Prompts Executed | 1 |

---

## 1. Objective

Add OpenAPI documentation (SpringDoc) to the veterinarians area, and expose a clean REST endpoint at `GET /api/vets` that clients can consume with standard `Accept` header content negotiation.

---

## 2. Current State Analysis

| Endpoint | Mapping | Mechanism | Notes |
|---|---|---|---|
| `GET /vets` | `VetController.showVetList()` | JSP view `vets/vetList` | HTML only — no `produces` restriction |
| `GET /vets.json` | `VetController.showJsonVetList()` | `@ResponseBody`, `produces=JSON` | Extension-based, non-standard REST |
| `GET /vets.xml` | `VetController.showXmlVetList()` | `@ResponseBody`, `produces=XML` | Extension-based, non-standard REST |

No OpenAPI/SpringDoc dependency exists in `pom.xml`.

Jackson version is **3.1.1** (group `tools.jackson.core`) — **compatibility risk** with SpringDoc (see §5).

---

## 3. Architectural Decision: Document As-Is vs. Consolidate

### Option A — Document existing `.json`/`.xml` endpoints as-is
- Pros: zero code change, zero regression risk
- Cons: extension-based URLs are non-standard REST; `/vets.json` is not a canonical REST pattern; confusing when mixed with `Accept` header conventions; Swagger UI shows ugly paths

### Option B — Consolidate to a single REST endpoint + keep HTML view (CHOSEN ✅)

**Decision: extract `VetRestController` at `GET /api/vets` with `produces = {JSON, XML}` content negotiation via `Accept` header. Keep `VetController` and its three existing paths fully intact.**

Rationale:
- Extension URLs (`/vets.json`, `/vets.xml`) are a legacy Spring MVC pattern; standard REST uses `Accept` headers
- `VetController.showVetList()` returns an HTML view — mixing view-layer concerns into a REST controller is an antipattern
- Extracting a `VetRestController` gives a clear REST contract with zero HTML/JSP dependencies
- Existing tests and the HTML flow are completely unaffected
- The `/api/vets` prefix is idiomatic and matches the Spring PetClinic REST sibling project

---

## 4. Implementation Scope

### 4.1 New files

| File | Purpose |
|---|---|
| `src/main/java/.../web/VetRestController.java` | `@RestController` at `GET /api/vets`; `@Operation`, `@ApiResponse` annotations |
| `src/main/java/.../web/OpenApiConfiguration.java` | `OpenAPI` bean (title, version, license); imports SpringDoc MVC configuration |

### 4.2 Modified files

| File | Change |
|---|---|
| `pom.xml` | Add `<springdoc.version>` property + `springdoc-openapi-starter-webmvc-ui` dependency |
| `src/main/resources/spring/mvc-core-config.xml` | Add `org.springdoc` to `<context:component-scan>` base packages |

### 4.3 New test files

| File | Purpose |
|---|---|
| `src/test/java/.../web/VetRestControllerTests.java` | MockMvc: JSON response, XML response, content-type, body fields |

### 4.4 Out of scope

- `VetController` — NOT modified (backward compatibility preserved)
- `VetControllerTests` — NOT modified
- Model annotations (`@Schema` on `Vets`, `Vet`, `Specialty`) — deferred to a follow-up topic
- Authentication / API key / CORS — out of scope (PetClinic is a demo app)
- Pagination — out of scope

---

## 5. Risk Register

| ID | Severity | Risk | Mitigation |
|----|----------|------|-----------|
| R1 | 🔴 HIGH | SpringDoc 2.x depends on `com.fasterxml.jackson` (2.x) while project uses `tools.jackson` (3.x). If SpringDoc brings in Jackson 2.x as transitive dep, both coexist. If SpringDoc 3.x targeting Spring 7 + Jackson 3.x is available, prefer it. | Use latest SpringDoc; inspect transitive deps; verify JSON serialization works with both versions present |
| R2 | 🟠 MEDIUM | SpringDoc non-Boot Spring MVC integration requires explicit `org.springdoc` component scan in DispatcherServlet context | Add `org.springdoc` to `<context:component-scan>` in `mvc-core-config.xml` |
| R3 | 🟠 MEDIUM | `/api/vets` XML response: `Vets` has `@XmlRootElement` so `Jaxb2RootElementHttpMessageConverter` handles it, but the OXM marshaller in `mvc-view-config.xml` is view-layer only | Verify with integration test; the message converter path is separate from the view resolver path |
| R4 | 🟡 LOW | `mvc-default-servlet-handler` may intercept `/swagger-ui/` static resources | Ensure `<mvc:resources mapping="/swagger-ui/**" ...>` is NOT needed (SpringDoc registers its own handler) |
| R5 | 🟡 LOW | Swagger UI WebJar served from classpath may conflict with `<mvc:resources mapping="/webjars/**">` already in mvc-core-config.xml | Verify Swagger UI is accessible at `/swagger-ui/index.html` |

---

## 6. SpringDoc Dependency Strategy

```xml
<!-- Property -->
<springdoc.version>2.8.0</springdoc.version>

<!-- Dependency -->
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>${springdoc.version}</version>
</dependency>
```

**Verification required**: confirm `springdoc-openapi-starter-webmvc-ui:2.8.0` is compatible with Spring Framework 7.0.6 and does not hard-require Spring Boot. If SpringDoc 3.x is released for Spring 7, update version accordingly.

---

## 7. Acceptance Criteria

- [ ] `GET /api/vets` with `Accept: application/json` returns 200 with `vetList` JSON array
- [ ] `GET /api/vets` with `Accept: application/xml` returns 200 with `<vets><vet>...` XML
- [ ] `GET /v3/api-docs` returns OpenAPI 3 JSON spec
- [ ] `GET /swagger-ui/index.html` renders Swagger UI
- [ ] Existing `VetControllerTests` still pass (no regression)
- [ ] `GET /vets`, `GET /vets.json`, `GET /vets.xml` unchanged

---

## 8. File Change Summary

```
MODIFIED:
  pom.xml
  src/main/resources/spring/mvc-core-config.xml

NEW PRODUCTION:
  src/main/java/org/springframework/samples/petclinic/web/VetRestController.java
  src/main/java/org/springframework/samples/petclinic/web/OpenApiConfiguration.java

NEW TEST:
  src/test/java/org/springframework/samples/petclinic/web/VetRestControllerTests.java
```

---

*Plan generated — proceeding to AUDIT_PLAN*
