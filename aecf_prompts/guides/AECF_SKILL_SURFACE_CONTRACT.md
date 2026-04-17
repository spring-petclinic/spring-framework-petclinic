# AECF Skill Surface Contract

LAST_REVIEW: 2026-04-17
OWNER SEACHAD

---

## 1. Objetivo

Definir la convencion comun para los skills de `aecf_prompts` que quieran documentar o consumir `surfaces`.

Estado actual: este documento describe una convencion operativa y un objetivo de integracion futura. El
engine y la extension no aplican hoy este contrato de forma automatica en runtime.

Este contrato no decide `surfaces` nuevas.

Su objetivo es que todos los skills repo-dependientes resuelvan el alcance igual:

1. sin redescubrir fronteras desde cero,
2. sin ampliar alcance en silencio,
3. sin volver a discutir en cada skill algo que ya quedo congelado en bootstrap.

## 2. A que skills aplica

Aplica a los skills con rol `CONSUMES` en `aecf_prompts/guides/SKILL_CATALOG.md`.

Ejemplos comunes:

1. `aecf_new_feature`
2. `aecf_hotfix`
3. `aecf_refactor`
4. `aecf_new_test_set`
5. `aecf_document_legacy`
6. `aecf_explain_behavior`
7. `aecf_code_standards_audit`
8. `aecf_security_review`
9. `aecf_release_readiness`
10. `aecf_executive_summary`

## 3. Parametros canonicos de superficie

Cuando el usuario quiera fijar el alcance de forma explicita, los skills y operadores pueden adoptar estas
formas conceptuales:

1. `surface=<surface_id>`
2. `surfaces=<surface_a,surface_b,...>`

Regla interna:

1. `surface` se normaliza como `primary_surface`,
2. `surfaces` se normaliza como `active_surfaces`,
3. `primary_surface` debe ser el primer elemento de `active_surfaces` cuando exista.

## 4. Precedencia de resolucion

Los skills consumidores deben resolver el alcance en este orden:

1. si existe `<DOCS_ROOT>/<user_id>/<TOPIC>/AECF_RUN_CONTEXT.json` y ya incluye `primary_surface` o `active_surfaces`, esa seleccion congelada es la autoridad por defecto,
2. si no existe seleccion congelada pero el usuario pasa `surface` o `surfaces`, validar contra `AECF_SURFACES_INDEX.md` o `.json` y usar esa resolucion,
3. si existe indice de `surfaces` pero el alcance sigue ambiguo, no decidir en silencio: pedir confirmacion breve o redirigir a `aecf_project_context_generator`,
4. si no hace falta `surface`, usar `context_mode = global_only`.

## 5. Archivos minimos a cargar

Cuando el trabajo use `surfaces`, el skill debe cargar como minimo:

1. `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md`,
2. `.aecf/runtime/documentation/AECF_SURFACES_INDEX.md` o `.json`,
3. cada `AECF_SURFACE_<surface_id>.md` correspondiente a `active_surfaces`,
4. `AECF_RUN_CONTEXT.json` si ya existe para el `TOPIC`.

Si el trabajo es `global_only`, basta con el contexto global y los artefactos normales del skill.

## 6. Reglas obligatorias para skills consumidores

1. No inventar `surfaces` nuevas.
2. No renombrar `surfaces` existentes.
3. No ampliar `active_surfaces` en silencio.
4. Si hace falta ampliar alcance por dependencia directa, dejarlo explicito en el artefacto y pedir confirmacion cuando afecte materialmente al trabajo.
5. Evitar mas de 3 `surfaces` activas salvo justificacion clara.
6. Si no hay suficiente contexto para resolver el alcance, reportar el bloqueo en vez de improvisar.

## 7. Comportamiento cuando falta informacion

Si el skill necesita `surface` pero no puede resolverla con seguridad:

1. no debe actuar como si todo el repo estuviera implicitamente en alcance,
2. debe pedir una confirmacion corta,
3. o debe indicar que el siguiente paso correcto es `aecf_project_context_generator` para fijar `surfaces`.

## 8. Regla de salida

Cuando el skill opere con `surfaces`, su artefacto debe dejar claro el alcance efectivo:

1. `context_mode`,
2. `primary_surface`,
3. `active_surfaces`,
4. cualquier expansion de alcance ocurrida durante la ejecucion.

No hace falta crear un formato nuevo para ello si el skill ya lo deja claro en su bloque de alcance, contexto o metadata operativa.

## 9. Relacion con el bootstrap

`aecf_project_context_generator` decide si hacen falta `surfaces`, propone candidatas y requiere confirmacion humana.

Los skills cubiertos por este contrato no deben repetir esa responsabilidad.

## 10. Regla corta

`aecf_project_context_generator` decide o fija.

Los demas skills comunes consumen.
