> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 00_DISCOVERY_LEGACY |

MODO: LEGACY

------------------------------------------------------------

## MANDATORY CONTEXT LOAD

This prompt operates under the following mandatory contexts:

- aecf_prompts/AECF_SYSTEM_CONTEXT.md
- <workspace_root>/AECF_PROJECT_CONTEXT.md (if present anywhere in the active workspace)

Governance:
- aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md

If any of these contexts exist, they MUST be considered active constraints.

Execution is INVALID if these contexts are not acknowledged.

------------------------------------------------------------

HARD PRECONDITION: Load and enforce context with hierarchy:
1. SYSTEM_CONTEXT: aecf_prompts/AECF_SYSTEM_CONTEXT.md
2. PROJECT_CONTEXT (workspace): <workspace_root>/AECF_PROJECT_CONTEXT.md (if exists, overrides defaults)

FASE: DISCOVERY

Objective:
Localizar y enumerar todo el code relacionado con una funcionalidad concreta
dentro del proyecto.

────────────────────────
📌 TOPIC MANAGEMENT (AUTOMATIC)
────────────────────────

1. IF user explicitly provides TOPIC:
   - Use it as-is
   - Truncate to max 20 characters if needed (Windows path limits)
   - Replace spaces with underscores
   - Convert to lowercase
   - Store as {{TOPIC}} for this entire session

2. IF user does NOT provide TOPIC:
   - Infer a short, descriptive name from the functionality description
   - Max 20 characters
   - Use snake_case format
   - Examples: "user_login", "pdf_export", "cache_mgmt"
   - Inform user: "TOPIC inferred as: <topic>"
   - Store as {{TOPIC}} for this entire session

3. All outputs will be stored in:
   documentation/{{TOPIC}}/

────────────────────────
📄 TEMPLATE ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and strictly follow:

./aecf/templates/DISCOVERY_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure and headings of the template.
- You may only add content inside sections.
- You may NOT modify headings.
- You may NOT remove sections.
- Missing sections invalidate the DISCOVERY output.

────────────────────────

Funcionalidad a analizar:
<"funcionalidad a buscar">

Tu tarea:
1. Buscar en el proyecto todos los files, modules o funciones
   relacionados con esta funcionalidad.
2. Identificar:
   - Endpoints
   - Funciones auxiliares
   - Accesos a base de data
   - Logica de seguridad
3. Enumerar los files encontrados y describir brevemente su papel.
4. Delimitar el alcance exacto de la funcionalidad.

REGLAS ESTRICTAS (PHASE VIOLATION DETECTION):
- PROHIBIDO modificar code.
- PROHIBIDO generar code nuevo.
- PROHIBIDO refactorizar, corregir o “mejorar” nada.
- PROHIBIDO proponer soluciones tecnicas.
- PROHIBIDO actualizar docstrings, ejemplos o comentarios.
- PROHIBIDO crear metodos, funciones o APIs.
- PROHIBIDO asumir autoridad de implementacion.

Cualquier incumplimiento invalida la respuesta.

Si detectas:
- inconsistencias
- duplicidades
- posibles errores
- problemas de sincronizacion

DEBES:
- Limitarlos a una enumeracion descriptiva
- SIN proponer como resolverlos

Formato de salida obligatorio:
Follow exactly the structure defined in DISCOVERY_TEMPLATE.md

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
documentation/{{TOPIC}}/AECF_<NN>_DISCOVERY.md

Where:
- {{TOPIC}} = the topic established at the beginning (or inferred)
- <NN> = next sequential number (01, 02, 03...)

Output de esta fase:
- genera el documento md que servira de entrada para la siguiente fase: PLAN

Finaliza con EXACTAMENTE:
FUNCIONALIDAD DELIMITADA PARA AECF

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check

