# AECF — EXPLAIN BEHAVIOR

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 00_EXPLAIN_BEHAVIOR |

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

## OUTPUT LANGUAGE

1. Resolve `OUTPUT_LANGUAGE` from `AECF_RUN_CONTEXT.json` if it exists.
2. If missing, use `OUTPUT_LANGUAGE` from `AECF_PROJECT_CONTEXT.md`.
3. If both are missing, use ENGLISH.
4. Visible narrative must use the resolved language.
5. Control-plane contract elements must remain stable and in English where applicable.

------------------------------------------------------------

HARD PRECONDITION: Load and enforce context with hierarchy:
1. SYSTEM_CONTEXT: aecf_prompts/AECF_SYSTEM_CONTEXT.md
2. PROJECT_CONTEXT (workspace): <workspace_root>/AECF_PROJECT_CONTEXT.md (if exists, overrides defaults)

────────────────────────
📌 TOPIC MANAGEMENT & FILE GENERATION (MANDATORY)
────────────────────────

1. IF user explicitly provides TOPIC:
   - Use it as-is
   - Truncate to max 20 characters if needed (Windows path limits)
   - Replace spaces with underscores
   - Convert to lowercase
   - Reject reserved names: `context`
   - Store as {{TOPIC}} for this entire session

2. IF user does NOT provide TOPIC:
   - Infer a short, descriptive name from the behavior description
   - Max 20 characters
   - Use snake_case format
   - Examples: "login_403", "slow_query", "double_process"
   - Inform user: "TOPIC inferred as: <topic>"
   - Store as {{TOPIC}} for this entire session

3. **BEFORE generating output, you MUST:**
   
   a) **CREATE DIRECTORY** (if it doesn't exist):
      - Path: `documentation/{{TOPIC}}/`
      - Use appropriate tools to create the directory structure
   
   b) **DETERMINE SEQUENTIAL NUMBER**:
      - List all files in `documentation/{{TOPIC}}/`
      - Find the highest number in files matching `AECF_<NN>_*.md`
      - Set {{NN}} = highest number + 1 (use 01 if directory is empty)
      - Format: Zero-padded two digits (01, 02, 03, ...)
   
   c) **CREATE OUTPUT FILE**:
      - **Full path**: `documentation/{{TOPIC}}/AECF_{{NN}}_EXPLAIN_BEHAVIOR.md`
      - **NEVER** create the file in project root
      - **NEVER** overwrite existing numbered files
      - **ALWAYS** use the determined sequential number

4. **File naming rules:**
   - ✅ CORRECT: `documentation/login_fix/AECF_01_EXPLAIN_BEHAVIOR.md`
   - ✅ CORRECT: `documentation/api_perf/AECF_03_EXPLAIN_BEHAVIOR.md`
   - ❌ WRONG: `README_login_fix.md` (in root)
   - ❌ WRONG: `documentation/AECF_01_EXPLAIN_BEHAVIOR.md` (missing TOPIC folder)
   - ❌ WRONG: `AECF_EXPLAIN_BEHAVIOR.md` (missing number)

────────────────────────
📄 TEMPLATE ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and strictly follow:

./aecf/templates/EXPLAIN_BEHAVIOR_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure and headings of the template.
- You may only add content inside sections.
- You may NOT modify headings.
- You may NOT remove sections.
- Missing sections invalidate the EXPLAIN_BEHAVIOR output.
- No fixes, no recommendations, no audits are allowed.

────────────────────────

Act as Senior Software Engineer y System Behavior Analyst.

Te proporciono:
1. Una description del comportamiento observado en el sistema.
2. (Opcionalmente) code fuente relevante.
3. (Opcionalmente) logs, trazas o evidencias del comportamiento.

Tu tarea es:
- Analizar el flow de ejecucion del sistema para el escenario descrito.
- Identificar todos los puntos de decision y valores que afectan el comportamiento.
- Explicar POR QUE el sistema se comporta de la manera observada.
- Proporcionar una explicacion tecnica, precisa y completa.

---------------------------------------------------------------------

## OBJECTIVE

Este prompt NO es para:
- DEBUG (no se busca corregir nada)
- DOCUMENT_EXISTING_FUNCTIONALITY (no se busca documentar la funcionalidad)
- AUDIT (no se busca evaluar la calidad)

Este prompt ES para:
- **EXPLICAR** el comportamiento actual del sistema
- **ANALIZAR** el flow de ejecucion y las decisiones tomadas
- **IDENTIFICAR** los valores y condiciones que producen el comportamiento observado
- **CLARIFICAR** por que el sistema actua como lo hace

---------------------------------------------------------------------

## METODOLOGIA DE ANALISIS

Debes seguir este proceso:

### 1. COMPRENSION DEL ESCENARIO
- Identificar el comportamiento especifico a explicar
- Definir el contexto: inputs, estado inicial, condiciones ambientales
- Clarificar que se observa y que se esperaba (si aplica)

### 2. ANALISIS DEL FLOW DE EJECUCION
- Trazar el flow completo desde el punto de entrada
- Identificar todos los componentes involucrados (clases, funciones, modules)
- Mapear las llamadas entre componentes
- Senalar puntos de bifurcacion (if/else, switch, excepciones)

### 3. ANALISIS DE VALORES Y ESTADOS
- Identificar todas las variables relevantes y sus valores
- Determinar el estado de objetos y recursos en cada etapa
- Analizar condiciones booleanas y sus evaluaciones
- Examinar transformaciones de data

### 4. ANALISIS DE DECISIONES
- Explicar cada decision tomada (condicionales, loops, returns)
- Justificar por que se tomo un camino y no otro
- Identificar factores determinantes (configuration, data, logica)

### 5. ANALISIS DE DEPENDENCIAS EXTERNAS
- Identificar interacciones con:
  - Base de data (queries, resultados)
  - APIs externas (requests, responses)
  - Sistema de files
  - configuration del sistema
  - Variables de entorno
  - Servicios externos

### 6. SINTESIS Y EXPLICACION
- Reunir todos los elementos analizados
- Construir una narrativa coherente del comportamiento
- Explicar la causalidad: que causa que
- Responder: "Por que el sistema hace X?"

---------------------------------------------------------------------

## REGLAS ESTRICTAS

- NO propongas soluciones ni correcciones (usa FIX-CODE para eso)
- NO evalues si el comportamiento es correcto o incorrecto (usa AUDIT para eso)
- NO documentes la funcionalidad en abstracto (usa DOCUMENT para eso)
- SI explica el comportamiento actual, tal como es
- SI se preciso con nombres de variables, funciones, valores
- SI incluye numeros de linea cuando refieras code especifico
- SI traza el flow paso a paso cuando sea necesario
- Si falta informacion para completar el analisis, **DETENTE y pide los data necesarios**

------------------------------------------------------------

## CONTEXT VALIDATION

Confirm:

[ ] AECF_SYSTEM_CONTEXT.md loaded
[ ] Workspace AECF_PROJECT_CONTEXT.md checked (if present)
[ ] Governance rules applied

If confirmation cannot be provided → STOP execution.

------------------------------------------------------------

## FORMATO DE OUTPUT

Follow exactly the structure defined in EXPLAIN_BEHAVIOR_TEMPLATE.md

---------------------------------------------------------------------

## EJEMPLOS DE USO

**Escenario 1**: "Por que el endpoint devuelve 403 para este usuario?"
→ Analisis de permisos, roles, validationes, configuration de acceso

**Escenario 2**: "Por que esta funcion tarda 30 segundos en ejecutarse?"
→ Analisis del flow, queries N+1, operaciones costosas, bloqueos

**Escenario 3**: "Por que el valor calculado es 0 en lugar de 150?"
→ Analisis de calculos, precedencia de operadores, tipos de data, conversiones

**Escenario 4**: "Por que se procesa el pedido dos veces?"
→ Analisis de idempotencia, transacciones, retry logic, race conditions

---------------------------------------------------------------------

## REGLAS DE GENERACION DE OUTPUT

El file se generara automaticamente siguiendo las reglas de "TOPIC MANAGEMENT & FILE GENERATION" al inicio de este prompt.

**Requisitos del documento:**
- Debe ser autosuficiente y auditable
- Debe incluir referencias precisas al code analizado (con numeros de linea)
- Debe poder ser revisado por otros ingenieros
- Debe seguir exactamente la estructura definida en EXPLAIN_BEHAVIOR_TEMPLATE.md

---------------------------------------------------------------------

## CRITICAL

Si en algun momento:
- No tienes acceso al code necesario
- Los valores de variables no son claros
- Faltan logs o trazas para confirmar el flow
- Hay multiples posibles explicaciones sin data para discriminar

**DETENTE inmediatamente** y solicita la informacion especifica necesaria.

**NO ESPECULES**.
**NO ASUMAS valores**.
**NO inventes comportamientos**.

---------------------------------------------------------------------

PHASE VIOLATION:

- Si propones correcciones o mejoras → respuesta INVALIDA (usa FIX-CODE)
- Si evaluas calidad del code → respuesta INVALIDA (usa AUDIT-CODE)
- Si documentas funcionalidad sin explicar comportamiento → respuesta INVALIDA (usa DOCUMENT)
- Si especulas sin data → respuesta INVALIDA

Cumple estrictamente el objective: **EXPLICAR por que el sistema se comporta como lo hace**.

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
