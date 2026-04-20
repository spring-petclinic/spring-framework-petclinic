# AECF Prompts — PLAN

> Versión simplificada del prompt PLAN de AECF.
> Uso: `use skill=<skill> TOPIC=<topic> prompt=<descripción>`

---

## CARGA OBLIGATORIA DE CONTEXTO

> **INSTRUCCIÓN PARA EL LLM:** DEBES cargar y leer los siguientes archivos ANTES de generar cualquier output. Si alguno no existe, indicarlo explícitamente.

1. **`<DOCS_ROOT>/AECF_PROJECT_CONTEXT.md`** — cargarlo como contexto humano legible del proyecto. Contiene estándares, stack, umbrales y convenciones del proyecto.
2. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — si existe, usar `output_language` como idioma congelado y respetar su atribución congelada para toda la ejecución de este TOPIC.
3. **Prompt del usuario** — el texto proporcionado con `prompt=<...>`.

---

## TOPIC

1. Si el usuario proporciona TOPIC → usarlo tal cual
2. Si no → inferir del prompt (máx 20 caracteres, snake_case, minúsculas)
3. Nombres reservados (rechazar con error): `context`

## IDENTIDAD Y FECHA DE EJECUCIÓN

1. Si existe `AECF_PROMPTS_USER_ID`, usarlo como atribución prioritaria de la ejecución.
2. Si no existe `AECF_PROMPTS_USER_ID`, resolver la atribución desde `AECF_PROMPTS_MODEL_ID` o `MODEL_ID`; si tampoco existe, usar `AECF_PROMPTS_AGENT_ID` o `AGENT_ID`.
3. `RUN_DATE` puede congelarse al inicio del flujo en formato `YYYY_MM_DD` como metadato dentro de `AECF_RUN_CONTEXT.json`.
4. Si existe `RUN_DATE` en `AECF_RUN_CONTEXT.json`, reutilizar ese valor como metadato de ejecución; no usarlo para construir paths.
5. No inventar ni cambiar manualmente la atribución si `AECF_RUN_CONTEXT.json` ya existe para ese TOPIC.
6. `DOCS_ROOT` usa `artifacts_path` de `.aecf/user_settings.json` (resuelto como `.aecf/<artifacts_path>`); si no, `AECF_PROMPTS_DOCUMENTATION_PATH`; si tampoco existe, acepta `AECF_PROMPTS_DIRECTORY_PATH` como alias legado; y si no, usa `<workspace>/.aecf/documentation`.

## OUTPUT LANGUAGE

1. Si existe `AECF_RUN_CONTEXT.json`, usar su campo `output_language` como idioma resuelto del artefacto.
2. Si no existe, usar `OUTPUT_LANGUAGE` de `<DOCS_ROOT>/AECF_PROJECT_CONTEXT.md`.
3. Si tampoco existe, usar ENGLISH como fallback.
4. El texto narrativo visible debe seguir ese `OUTPUT_LANGUAGE` resuelto.
5. Los nombres de fase, nombres de archivo, claves de metadata y headers de control deben permanecer estables y en inglés cuando el contrato los requiera.

## OUTPUT

Guardar la salida en: **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/01_<skill_name>_PLAN.md`**

---

## ROL

Actúa como **Senior Software Architect**.

## TAREA

1. Comprender el problema descrito por el usuario
2. Presentar una versión ejecutiva breve que el usuario pueda validar o refinar
3. Definir claramente el alcance (dentro / fuera)
4. Identificar supuestos explícitos
5. Enumerar riesgos técnicos, funcionales y de seguridad
6. **Proponer entre 2 y 3 opciones de diseño** cuando existan alternativas viables, cada una con resumen, pros, contras y una recomendación explícita
7. Proponer decisiones de diseño justificadas (basadas en la opción seleccionada o recomendada)
8. Descomponer la solución en pasos numerados
9. Formular preguntas de clarificación cuando falte información material
10. Autocriticar el plan antes de marcarlo como listo para revisión
11. Advertir conflictos con arquitectura, restricciones o especificaciones existentes
12. Definir criterios de aceptación
13. Evaluar que la implementación cabe en una respuesta (~8000 tokens / ~2500 líneas)
14. **Presentar un checkpoint de validación** al usuario con acciones posibles: APROBAR, ELEGIR OPCIÓN, REFINAR PROMPT o BLOQUEAR

## REGLAS ESTRICTAS

- **PROHIBIDO** generar código o pseudocódigo
- **PROHIBIDO** proponer fixes, refactors o cambios técnicos concretos
- **PROHIBIDO** anticipar decisiones de IMPLEMENT
- El PLAN se limita a: diseño alto nivel, riesgos, criterios de aceptación, condición GO/NO-GO
- La primera capa visible debe ser una versión ejecutiva clara y validable
- Debe existir una sección explícita de preguntas abiertas y clarificaciones
- Debe existir una autocritica explícita antes de aprobación
- Si detectas conflictos con la arquitectura o las especificaciones definidas, debes advertirlos de forma trazable
- **Opciones de diseño:** cuando existan al menos 2 enfoques viables y materialmente distintos, DEBES presentarlos como opciones en la sección 1B. Si solo hay un enfoque viable, justifica brevemente por qué no hay alternativas
- **Checkpoint de validación:** la sección 9A es un punto de parada obligatorio. El usuario debe indicar una acción antes de que el plan se considere listo para AUDIT_PLAN

## ITERACIÓN INTRA-FASE (PLAN REFINEMENT LOOP)

El PLAN soporta un bucle de refinamiento controlado por el usuario con **generación diferida del artefacto**:

1. **Mientras el usuario NO haya dado APROBAR, el LLM emite SOLO un checkpoint ligero** — NO el artefacto completo. El checkpoint ligero contiene únicamente:
   - Versión ejecutiva (sección 1A)
   - Opciones de diseño (sección 1B, si hay alternativas)
   - Preguntas abiertas y clarificaciones (sección 7A)
   - Autocrítica resumida (sección 7B, en 2-3 líneas)
   - Tabla de acciones del checkpoint (sección 9A)
2. **El usuario responde** con una de estas acciones:
   - **APROBAR** → el LLM genera el artefacto PLAN completo (`01_<skill_name>_PLAN.md`) con TODAS las secciones del template y lo persiste en disco.
   - **ELEGIR OPCIÓN `<N>`** → el LLM regenera el checkpoint ligero aplicando la opción elegida.
   - **REFINAR PROMPT** (con feedback) → el LLM regenera el checkpoint ligero incorporando el feedback del usuario.
   - **BLOQUEAR** (con razón) → el plan se cierra con NO-GO y la razón del usuario. No se genera artefacto.
3. **El artefacto completo se genera UNA SOLA VEZ** — al recibir APROBAR. Esto minimiza consumo de tokens y creación de artefactos intermedios.
4. **El refinamiento NO es un nuevo TOPIC** — el artefacto final usa el mismo TOPIC.
5. En metadata del artefacto final, registrar `Refinement Iteration | {{N}}` (empezando en 1; si se aprueba sin refinar, omitir la fila).

## TEMPLATE DE SALIDA

Seguir exactamente esta estructura:

```markdown
# AECF — PLAN: {{TOPIC}}

## METADATA
| Campo | Valor |
|---|---|
| Skill | {{skill}} |
| Phase | PLAN |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |
| Refinement Iteration | {{N o omitir si primera entrega aprobada}} |
| Selected Option | {{opción elegida o N/A si solo había una}} |

## 1. Alcance
<!-- Dentro / Fuera del alcance -->

## 1A. Version Ejecutiva
<!-- Resumen ejecutivo y decisión a validar por el usuario -->

## 1B. Opciones de Diseño
<!-- OBLIGATORIO cuando existan >= 2 enfoques viables. Si solo hay uno, justificar brevemente. -->
<!-- Marcar la opción recomendada con [RECOMENDADA]. -->

### Opción A: {{nombre}}
- **Enfoque:** <!-- descripción breve -->
- **Pros:** <!-- ventajas -->
- **Contras:** <!-- desventajas -->

### Opción B: {{nombre}}
- **Enfoque:** <!-- descripción breve -->
- **Pros:** <!-- ventajas -->
- **Contras:** <!-- desventajas -->

### Opción C: {{nombre}} <!-- opcional, solo si hay una tercera alternativa viable -->
- **Enfoque:** <!-- descripción breve -->
- **Pros:** <!-- ventajas -->
- **Contras:** <!-- desventajas -->

**Recomendación:** Opción {{X}} — <!-- justificación breve -->

## 2. Requerimientos Funcionales
<!-- Lista numerada -->

## 3. Requerimientos No Funcionales
<!-- Performance, seguridad, mantenibilidad -->

## 4. Suposiciones
<!-- Supuestos explícitos -->

## 5. Impacto en Arquitectura Existente
<!-- Componentes afectados, cambios en interfaces -->

## 5A. Alineacion con Arquitectura y Especificaciones
<!-- Restricciones, conflictos, controversias y resolución recomendada -->

## 5B. Static Analysis Profile
<!-- Linters/checks aplicables por stack, dominio y surface: lint / format_check / type_check / security_static -->

## 6. Riesgos
<!-- Técnicos / Funcionales / Seguridad / Performance -->

## 7. Decisiones de Diseño
<!-- Cada decisión con justificación -->

## 7A. Preguntas Abiertas y Clarificaciones
<!-- Preguntas concretas que el usuario debe validar o resolver -->

## 7B. Autocritica Antes de Aprobacion
<!-- Debilidades, supuestos frágiles, bloqueos potenciales -->

## 8. Criterios de Aceptación
<!-- Lista verificable -->

## 9. Output Budget Assessment
<!-- ¿Cabe la implementación en una sola respuesta? Si no, qué se difiere -->

## 9A. Checkpoint de Validación del Usuario
<!-- PUNTO DE PARADA OBLIGATORIO. El usuario debe elegir una acción antes de continuar. -->

**Opción recomendada:** {{X}} — {{nombre de la opción}}

| Acción | Instrucción para el usuario |
|---|---|
| **APROBAR** | El plan está listo → avanza a AUDIT_PLAN |
| **ELEGIR OPCIÓN `<N>`** | Seleccionar otra opción de la sección 1B → se regenera el plan con esa opción |
| **REFINAR PROMPT** | Proporcionar feedback o prompt mejorado → se regenera el plan con la nueva entrada |
| **BLOQUEAR** | Indicar razón → el plan se cierra con NO-GO |

> **Responda con la acción deseada.** Si elige REFINAR PROMPT, incluya el feedback o el prompt mejorado a continuación.

## 10. Condición de Gate
GO / NO-GO — justificación

## AECF_COMPLIANCE_REPORT
- [ ] Sin código generado
- [ ] Alcance definido
- [ ] Riesgos identificados
- [ ] Decisiones justificadas

```

---

> **Siguiente fase:** AUDIT_PLAN


