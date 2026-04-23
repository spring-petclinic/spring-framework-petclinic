# AECF — TEST IMPLEMENTATION

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 09_TEST_IMPLEMENTATION |

------------------------------------------------------------

## MANDATORY CONTEXT LOAD

This prompt operates under the following mandatory contexts:

- aecf_prompts/AECF_SYSTEM_CONTEXT.md
- <workspace_root>/AECF_PROJECT_CONTEXT.md (if present anywhere in the active workspace)
- **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — if present, use `output_language` as the frozen language for the entire execution.

Governance:
- aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md

If any of these contexts exist, they MUST be considered active constraints.

Execution is INVALID if these contexts are not acknowledged.

------------------------------------------------------------

HARD PRECONDITION: Load and enforce context with hierarchy:
1. SYSTEM_CONTEXT: aecf_prompts/AECF_SYSTEM_CONTEXT.md
2. PROJECT_CONTEXT (workspace): <workspace_root>/AECF_PROJECT_CONTEXT.md (if exists, overrides defaults)

📌 TOPIC: Maintain {{TOPIC}} from previous phase. All outputs in: documentation/{{TOPIC}}/

────────────────────────
📄 TEMPLATE ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and strictly follow:

./aecf/templates/TEST_IMPLEMENTATION_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure of TEST_IMPLEMENTATION_TEMPLATE.md.
- All test cases defined in TEST_STRATEGY must be implemented.
- No functional code modifications allowed.
- No additional tests beyond strategy allowed.
- Tests must be deterministic.
- Coverage must be reported.
- Missing sections invalidate TEST_IMPLEMENTATION.

────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/TEST_IMPLEMENTATION_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.

────────────────────────
SCORING ENFORCEMENT (MANDATORY)
────────────────────────

You MUST:

1. Score each checklist item (0,1,2).
2. Apply category weights.
3. Compute normalized score.
4. Declare maturity level.
5. Apply automatic verdict rules.

If scoring is not included → Phase invalid.

Include in AECF_COMPLIANCE_REPORT:

## AECF_SCORE_REPORT

- Raw Score:
- Normalized Score:
- Maturity Level:
- Automatic Verdict:
- Critical Findings Present: YES / NO

---

This prompt is subject to audit.
Failure to follow the flow invalidates the response.

---

## CONTEXTO

Trabajas sobre:
1. Un TEST_STRATEGY aprobado.
2. Code implementado.
3. El PLAN original aprobado.

This phase runs AFTER TEST_STRATEGY.

---

## OBJECTIVE

Implementar los tests definidos en la TEST_STRATEGY de forma completa, ejecutable y mantenible.

---

## ROL

Act as Senior Software Engineer especializado en Testing.

Tu tarea es:
- Implementar TODOS los casos de prueba especificados en TEST_STRATEGY.
- Seguir las convenciones del proyecto.
- Usar los frameworks especificados.
- Generate clear, maintainable, and sufficiently documented test code.
- Ensure tests are deterministic (no flakey).

---

## GROUNDING PRECONDITION (MANDATORY — EXECUTE BEFORE WRITING ANY TEST)

**This block is a hard gate. Any test written without completing it is INVALID.**

Before writing a single line of test code, you MUST:

1. **READ** every implementation file that the tests will import or reference.
   - Use READ_FILE or equivalent to retrieve the actual content.
   - Do NOT rely on the PLAN, TEST_STRATEGY, or prior conversation to infer what exists.

2. **EXTRACT** the actual exported symbols from each file:
   - Public function names (exact spelling, exact casing).
   - Class names and their public methods.
   - Module path as it will be used in `import` statements.

3. **VERIFY** every import statement before writing it:
   - The module path must correspond to an existing file.
   - The symbol name must exist in that file (confirmed from step 2).
   - If a symbol does not exist → STOP. Flag it as `GROUNDING_FAILURE` and do NOT write the test. Instead report: `Symbol '<name>' not found in '<path>'. Test blocked pending implementation.`

4. **ASSERTION SAFETY RULES** (mandatory, non-negotiable):
   - NEVER assert raw string equality between outputs produced by different serialization formats (e.g., `json_output == yaml_output`). Serialization formats produce structurally equivalent but lexically different strings.
   - For format-equivalence tests: deserialize both outputs to native Python structures (`json.loads`, `yaml.safe_load`, etc.) and compare the resulting dicts/lists.
   - NEVER hard-code expected string output that includes indentation or key ordering unless the function explicitly guarantees it with `sort_keys=True` and fixed `indent`.

5. **GROUNDING SUMMARY** (include in output before first test):
   - List each file read with ✅ or ❌.
   - List each symbol verified with ✅ (exists) or ❌ (not found).
   - Declare: `GROUNDING COMPLETE — all symbols verified` or `GROUNDING FAILED — <list of missing symbols>`.

If GROUNDING fails for any symbol → that test MUST NOT be written. Write a placeholder comment instead:
```python
# GROUNDING_FAILURE: '<symbol>' not found in '<module>'. Test blocked.
```

---

## REGLAS ESTRICTAS

- DO NOT modify functional code (tests only).
- NO implementes tests no especificados en TEST_STRATEGY.
- NO omitas casos de prueba definidos en TEST_STRATEGY.
- NO uses prints (usa logging si necesario en tests).
- Sigue EXACTAMENTE la estructura de directorios de tests del proyecto.
- Every generated or modified test file/module/function/class MUST include a full `AECF_META` line following
    `./aecf/code/CODE_FUNCTION_METADATA_STANDARD.md`, including `run_time` and `touch_count`.
- On creation, set `touch_count=1`; on a later AECF modification, preserve `generated_*`, update
    `last_modified_*`, refresh `run_time`, and increment `touch_count` by exactly `1`.
- Every test generated by AECF MUST include a traceability docstring with at least:
        - `Generated by AECF framework`
        - `TOPIC: {{TOPIC}}` (o el topic resuelto de la sesion)
        - the full `AECF_META` line as the last line of the docstring/comment block
- Human-maintenance comments/docstrings MUST be sufficient to explain non-obvious intent,
    fixtures, mocks, cleanup, risk coverage, and deterministic choices.
- Human-readable comments/docstrings MUST use the resolved `OUTPUT_LANGUAGE` /
    `aecf.documentationOutputLanguage`; machine-facing `AECF_META` keys stay in English.
- Missing `AECF_META`, stale `touch_count`, or sparse maintenance comments INVALIDATE TEST_IMPLEMENTATION.

---

## TECHNICAL OBLIGATIONS

### 1. Estructura de Files

Sigue las convenciones del proyecto:
- Python: `tests/test_<module>.py`
- Organization by type: `tests/unit/`, `tests/integration/`, `tests/e2e/`
- Fixtures en: `tests/fixtures/` o `tests/conftest.py`

### 1.1 Docstring de Trazabilidad AECF (OBLIGATORIO)

Cada file de tests generado y/o cada test function generada debe incluir docstring con trazabilidad AECF.

Minimum valid format:

```python
"""Generated by AECF framework. TOPIC: {{TOPIC}}.

AECF_META: skill=aecf_new_test_set | topic={{TOPIC}} | run_time={{timestamp_utc}} | generated_at={{timestamp_utc}} | generated_by={{Executed By ID o N/A}} | last_modified_skill=aecf_new_test_set | last_modified_at={{timestamp_utc}} | last_modified_by={{Executed By ID o N/A}} | touch_count=1
"""
```

Valid example per function:

```python
def test_example_case():
    """Generated by AECF framework. TOPIC: {{TOPIC}}.

    AECF_META: skill=aecf_new_test_set | topic={{TOPIC}} | run_time={{timestamp_utc}} | generated_at={{timestamp_utc}} | generated_by={{Executed By ID o N/A}} | last_modified_skill=aecf_new_test_set | last_modified_at={{timestamp_utc}} | last_modified_by={{Executed By ID o N/A}} | touch_count=1
    """
    ...
```

### 2. Naming Conventions

```python
# Unitarios
def test_<funcion>_<condicion>_<resultado_esperado>():
    # test_calculate_total_with_discount_returns_correct_amount

# Integration  
def test_<componente_A>_integrates_with_<componente_B>_<resultado>():
    # test_user_service_integrates_with_database_creates_user

# Edge cases
def test_<funcion>_<edge_case>_<comportamiento>():
    # test_divide_by_zero_raises_value_error
```

### 3. Estructura de Test (AAA Pattern)

```python
def test_example():
    # Arrange (preparar data)
    user = User(name="Test", email="test@example.com")
    
    # Act (execute action)
    result = user.validate()
    
    # Assert (verificar resultado)
    assert result is True
```

### 4. Fixtures y Mocks

- Usa fixtures reusables en `conftest.py`
- Explicitly mock external dependencies
- Document what is mocked and why

### 5. Assertions Claras

```python
# ❌ MAL
assert result

# ✅ BIEN
assert result.status_code == 200, "Should return OK status"
assert result.data['user_id'] == expected_id, "User ID should match"
```

### 6. Deterministic Tests

- NO uses `time.sleep()` (usa mocks de tiempo)
- DO NOT depend on execution order
- DO NOT use random data without a fixed seed
- Limpia estado entre tests

---

## CASOS DE PRUEBA OBLIGATORIOS

Debes implementar TODOS estos tipos especificados en TEST_STRATEGY:

### 1. Happy Path Tests
Validan el flow exitoso estandar.

### 2. Edge Case Tests
- Boundary values (0, -1, None, "", [], etc.)
- Maximum/minimum inputs
- Casos extremos

### 3. Error Handling Tests
- Excepciones esperadas
- Validation errors
- Manejo de errores de dependencias

### 4. Security Tests
- SQL/NoSQL injection
- XSS (si genera HTML)
- Control de acceso
- User enumeration

### 5. Resource Management Tests
- Cierre de conexiones
- Resource release
- Context managers

---

## CODE COVERAGE

- Usa herramientas de coverage (pytest-cov, coverage.py)
- Genera reporte de cobertura
- Identify uncovered lines
- Justify uncovered code (if any)

---

## FORMATO DE SALIDA OBLIGATORIO

Follow exactly the structure defined in TEST_IMPLEMENTATION_TEMPLATE.md

---

## PROHIBICIONES

- NO modificar code funcional (si necesita cambios, detente y documenta).
- NO implementar tests no especificados en TEST_STRATEGY.
- NO crear tests flakey o no deterministicos.
- NO usar prints para debugging (usa logging si necesario).

---

## SALIDA ESPERADA

Al finalizar, indica claramente:

**TESTS IMPLEMENTADOS — Listos para AUDIT_TESTS**

------------------------------------------------------------

## CONTEXT VALIDATION

Confirm:

[ ] AECF_SYSTEM_CONTEXT.md loaded
[ ] Workspace AECF_PROJECT_CONTEXT.md checked (if present)
[ ] Governance rules applied

If confirmation cannot be provided → STOP execution.

------------------------------------------------------------

───────────────────────────────
📁 OUTPUT GENERATION (MANDATORY)
───────────────────────────────

Generate document:
documentation/{{TOPIC}}/AECF_<NN>_TEST_IMPLEMENTATION.md

Incluir:
- Lista de files de tests creados
- Reporte de cobertura
- Instrucciones de ejecucion
- Output de ejecucion exitosa

Where:
- {{TOPIC}} = the topic from previous phase
- <NN> = next sequential number

---

## AECF_COMPLIANCE_REPORT

Antes de finalizar, incluir:

## AECF_COMPLIANCE_REPORT

- aecf_prompts/prompts/00_PLAN.md → APLICADO
- aecf_prompts/prompts/02_AUDIT_PLAN.md → APLICADO (GO)
- aecf_prompts/prompts/04_IMPLEMENT.md → APLICADO
- aecf_prompts/prompts/08_TEST_STRATEGY.md → APLICADO
- aecf_prompts/prompts/09_TEST_IMPLEMENTATION.md → APLICADO

Flow AECF: PARCIAL (pendiente AUDIT_TESTS)
Tests implementados segun TEST_STRATEGY: SI
Cobertura alcanzada: XX%
All tests pass: YES / NO

TEST_IMPLEMENTATION COMPLETA — LISTA PARA AUDIT_TESTS

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
