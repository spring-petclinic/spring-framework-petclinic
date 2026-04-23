# AECF Surface Selection Intake

LAST_REVIEW: 2026-04-06
OWNER SEACHAD

---

## 1. Objetivo

Definir un intake minimo para resolver la `surface` o `surfaces` activas antes de arrancar un flujo real en `aecf_prompts`.

Este intake existe para evitar dos fallos comunes:

1. cargar demasiado contexto por defecto,
2. dejar que cada fase vuelva a interpretar el alcance desde cero.

## 2. Cuando usarlo

Usar este intake cuando ocurra alguna de estas condiciones:

1. el repo es grande o multi-equipo,
2. existe `AECF_SURFACES_INDEX.md` o `.json`,
3. el `TOPIC` no deja claro por si solo que contexto cargar,
4. el trabajo puede tocar mas de una parte del sistema.

## 2.1 Regla de autoridad

La IA puede proponer `surfaces`, pero no debe imponerlas.

La salida final del intake debe quedar validada por una persona cuando:

1. se va a crear el primer indice de `surfaces`,
2. la particion propuesta cambia nombres o fronteras existentes,
3. el trabajo es transversal y la seleccion tiene impacto en varios equipos o areas.

## 3. Preguntas canonicas

Haz solo estas preguntas, en este orden, salvo que el contexto ya las responda con claridad.

1. Este workspace necesita realmente `surfaces` o basta contexto global?
2. Si hay `surfaces`, son principalmente de negocio, tecnicas o mixtas?
3. Que modulo, carpeta, componente o area del sistema parece estar implicado?
4. El cambio es localizado o transversal?
5. Necesita sobre todo contexto de negocio, de arquitectura tecnica o ambos?
6. La propuesta inicial de `surfaces` de la IA se acepta tal cual o hay que renombrar, fusionar, dividir, eliminar o anadir alguna?

## 3.1 Acciones de confirmacion humana

La persona debe poder responder con estas acciones, sin tener que redactar un documento largo:

1. aceptar una `surface`,
2. renombrar una `surface`,
3. fusionar dos `surfaces`,
4. dividir una `surface`,
5. eliminar una `surface` propuesta,
6. anadir una `surface` no detectada.

## 4. Regla de minimizacion

El intake debe ser corto.

Si `AECF_PROJECT_CONTEXT.md`, el `TOPIC` y el indice de `surfaces` ya permiten resolver con suficiente confianza, no repetir preguntas innecesarias.

## 5. Salida esperada

La salida del intake no es una solucion del negocio ni un plan tecnico completo.

Debe producir solo una resolucion de contexto con estos campos:

1. `context_mode`
2. `primary_surface`
3. `active_surfaces`
4. `selection_rationale`
5. `surface_selection_confidence`
6. `missing_context`
7. `context_files_to_load`

Ademas, antes de congelar la resolucion, conviene dejar constancia breve de si la seleccion fue:

1. propuesta por la IA y confirmada por humano,
2. propuesta por la IA y modificada por humano,
3. definida manualmente por humano.

## 6. Heuristica de decision

### 6.1 Si el trabajo es localizado

Usar:

- `context_mode = global_plus_surface`
- una sola `primary_surface`

### 6.2 Si el trabajo implica una integracion directa

Usar:

- `context_mode = global_plus_surfaces`
- una `primary_surface`
- una o dos `related_surfaces`

### 6.3 Si el trabajo es transversal pero ambiguo

1. priorizar la `surface` con mas evidencia textual o de rutas,
2. dejar `missing_context` explicito,
3. no activar mas `surfaces` de las necesarias.

### 6.4 Si no hace falta surface

Usar:

- `context_mode = global_only`
- `primary_surface = null`
- `active_surfaces = []`

### 6.5 Si la IA detecta candidatas pero la persona no confirma

Usar:

- `context_mode = global_only` o dejar la seleccion en borrador,
- `missing_context` explicito,
- sin consolidar aun el indice final de `surfaces`.

## 7. Mini ejemplo

Entrada:

- `TOPIC`: "ajustar validaciones del checkout y su integracion con pagos"

Resolucion tentativa de la IA:

1. `checkout` como `business_surface`,
2. `payments_platform` como `technical_surface` relacionada.

Confirmacion humana posible:

1. aceptar `checkout`,
2. renombrar `payments_platform` a `payment_gateway`,
3. dejar fuera cualquier otra zona no necesaria.

Salida congelada:

1. `primary_surface = checkout`
2. `active_surfaces = [checkout, payment_gateway]`
3. `selection_rationale` explica que el cambio es local al flujo de checkout con dependencia tecnica directa del gateway.

## 8. Artefacto recomendado de salida

Si quieres dejar la resolucion por escrito antes de actualizar `AECF_RUN_CONTEXT.json`, usa la plantilla:

- `aecf_prompts/templates/SURFACE_SELECTION_BRIEF_TEMPLATE.md`

## 9. Relacion con AECF_RUN_CONTEXT.json

Una vez resuelta la seleccion, la misma informacion debe congelarse en:

- `<DOCS_ROOT>/<user_id>/<TOPIC>/AECF_RUN_CONTEXT.json`

Contrato de referencia:

- `aecf_prompts/guides/AECF_RUN_CONTEXT_CONTRACT.md`

