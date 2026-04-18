# AECF_03 — Test Strategy: VetRestController + OpenAPI Documentation

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
| Sequence Position | 3 of 6 |
| Total Prompts Executed | 1 |

---

## Test Class: `VetRestControllerTests`

**Location**: `src/test/java/org/springframework/samples/petclinic/web/VetRestControllerTests.java`

**Strategy**: MockMvc standalone setup (matches `VetControllerTests` pattern). No Spring context load — fast, isolated, mocked `ClinicService`.

**Fixture**: 2 vets (James Carter with no specialties, Helen Leary with radiology) — same fixture used in `VetControllerTests` for consistency.

---

## Test Inventory

| # | Test name | Method | Accept | Expected status | Assertions |
|---|---|---|---|---|---|
| T1 | `testListVetsJson_returns200` | GET `/api/vets` | `application/json` | 200 | `Content-Type: application/json`, `$.vetList[0].id == 1` |
| T2 | `testListVetsJson_firstVetFields` | GET `/api/vets` | `application/json` | 200 | `$.vetList[0].firstName == "James"`, `$.vetList[0].lastName == "Carter"` |
| T3 | `testListVetsJson_secondVetHasSpecialty` | GET `/api/vets` | `application/json` | 200 | `$.vetList[1].specialties[0].name == "radiology"` |
| T4 | `testListVetsJson_vetListSize` | GET `/api/vets` | `application/json` | 200 | `$.vetList.length() == 2` |
| T5 | `testListVetsXml_returns200` | GET `/api/vets` | `application/xml` | 200 | `Content-Type: application/xml` or `text/xml` |
| T6 | `testListVetsXml_containsVetId` | GET `/api/vets` | `application/xml` | 200 | XPath `/vets/vet[id=1]/id` present |
| T7 | `testListVets_noAcceptHeader_returnsDefault` | GET `/api/vets` | (none) | 200 or 406 | Documents behavior — if no Accept, returns first `produces` (JSON) |
| T8 | `testListVets_unsupportedMediaType_returns406` | GET `/api/vets` | `text/html` | 406 | Not-acceptable response |

**Total**: 8 tests (all mandatory).

---

## Regression Guard

| Existing test class | Action |
|---|---|
| `VetControllerTests.testShowVetListHtml()` | NOT modified — must still pass |
| `VetControllerTests.testShowResourcesVetList()` | NOT modified — must still pass |
| `VetControllerTests.testShowVetListXml()` | NOT modified — must still pass |

---

## Coverage Target

- `VetRestController.listVets()`: 100% line coverage (single method, no branches)
- `OpenApiConfiguration.petclinicOpenAPI()`: not required (factory method, no logic)

---

## Notes

- T7 behavior: when no `Accept` header is sent, Spring MVC picks the first `produces` value (JSON) → expected 200 with JSON. This should be verified.
- T8 verifies that `text/html` is explicitly rejected (406), confirming the REST controller does NOT return HTML, enforcing the separation from `VetController`.
- XML tests use XPath assertions via `hamcrest-xml` (already on classpath via `testShowVetListXml` in `VetControllerTests`).
