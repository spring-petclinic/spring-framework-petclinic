# AECF Surface Context Model

LAST_REVIEW: 2026-04-06
OWNER SEACHAD

---

## 1. Objetivo

Definir un modelo de contexto escalable para `aecf_prompts` en repositorios grandes o con muchos equipos.

La idea es evitar un `AECF_PROJECT_CONTEXT.md` monolitico y sustituirlo por una estructura por capas:

1. contexto global minimo del proyecto,
2. inventario de `surfaces`,
3. contexto reutilizable por `surface`,
4. resolucion por `TOPIC` de las `surfaces` que deben cargarse en cada ejecucion.

`surface` se usa aqui como termino canonico para evitar conflicto con `domain`, que en AECF ya describe stack, knowledge packs y semantic profiles.

## 2. Que es una surface

Una `surface` es una particion operativa de contexto sobre una parte del sistema.

No representa necesariamente un modulo fisico unico ni un bounded context formal.

Su objetivo es contestar esta pregunta:

> Que contexto estable y reutilizable debo cargar cuando el trabajo afecta a esta parte del sistema.

Una `surface` puede ser:

1. `business_surface`: reglas de negocio, flujos funcionales, invariantes y ownership funcional.
2. `technical_surface`: arquitectura tecnica, integraciones, infraestructura, componentes compartidos y restricciones de plataforma.

## 2.1 Principio de decision humana

Las `surfaces` no deben quedar decididas solo por deteccion automatica.

La IA puede:

1. proponer `surfaces` candidatas,
2. sugerir nombre, tipo, rutas y dependencias,
3. explicar por que cree que esa particion es util.

Pero la decision final debe seguir siendo humana.

El flujo recomendado en `aecf_prompts` es:

1. `aecf_project_context_generator` pregunta si hacen falta `surfaces`,
2. si hacen falta, pregunta si son de tipo negocio, tecnico o mixto,
3. la IA propone una primera lista candidata,
4. la persona confirma, renombra, fusiona, divide, elimina o añade `surfaces`,
5. solo despues se consolida el indice y los documentos por `surface`.

## 2.2 Criterios para definir una surface

Una `surface` buena no se decide por carpetas bonitas ni por la intuicion del modelo.

Debe cumplir la mayoria de estos criterios:

1. representa una capacidad de negocio o una responsabilidad tecnica reconocible,
2. concentra cambios que suelen ocurrir juntos,
3. tiene invariantes, riesgos o reglas locales distinguibles,
4. tiene ownership claro o al menos una frontera operativa razonable,
5. permite reducir contexto sin perder comprension real del trabajo.

Si una particion solo sirve para una tarea puntual, probablemente no es una `surface`, sino un alcance temporal.

## 3. Cuando usar surfaces

El modelo de `surface` se recomienda cuando ocurre al menos una de estas condiciones:

1. `AECF_PROJECT_CONTEXT.md` empieza a crecer demasiado para reutilizarse en sesiones repetidas.
2. El repositorio tiene varias areas funcionales o tecnicas con reglas distintas.
3. No todos los equipos necesitan el mismo contexto base.
4. Los flujos reales suelen tocar una zona concreta del sistema y no el repositorio completo.
5. El contexto global contiene demasiado ruido para skills como `new_feature`, `refactor`, `hotfix` o `new_test_set`.

## 4. Capas de contexto recomendadas

### 4.1 Contexto global

Archivo:

- `.aecf/documentation/AECF_PROJECT_CONTEXT.md`

Debe contener solo lo transversal y estable:

1. objetivo del sistema,
2. stack principal,
3. reglas globales de arquitectura,
4. politicas de testing y release,
5. zonas sensibles,
6. restricciones globales del proyecto.

### 4.2 Indice de surfaces

Archivos:

- `.aecf/documentation/AECF_SURFACES_INDEX.md`
- `.aecf/documentation/AECF_SURFACES_INDEX.json`

Estos archivos describen:

1. que `surfaces` existen,
2. su tipo,
3. sus rutas principales,
4. dependencias entre `surfaces`,
5. señales para decidir cuando aplican.

### 4.3 Contexto por surface

Carpeta recomendada:

- `.aecf/documentation/surfaces/`

Archivo recomendado por `surface`:

- `.aecf/documentation/surfaces/AECF_SURFACE_<surface_id>.md`

### 4.4 Resolucion por TOPIC

Archivo existente a extender en las ejecuciones reales:

- `<DOCS_ROOT>/<user_id>/<TOPIC>/AECF_RUN_CONTEXT.json`

Cuando se use el modelo de `surface`, este artefacto debe registrar al menos:

1. `primary_surface`,
2. `active_surfaces`,
3. `selection_rationale`,
4. si el flujo uso solo contexto global o global + surfaces.

Contrato detallado:

- `aecf_prompts/guides/AECF_RUN_CONTEXT_CONTRACT.md`

## 5. Artefactos canonicos del modelo

### 5.1 AECF_SURFACES_INDEX.json

Contrato recomendado:

```json
{
  "version": "1.0",
  "generated_at": "2026-03-27T00:00:00Z",
  "selection_policy": {
    "allow_multiple_surfaces": true,
    "require_primary_surface": true,
    "fallback_to_global_only": true
  },
  "surfaces": [
    {
      "surface_id": "billing_core",
      "surface_type": "business_surface",
      "summary": "Facturacion canonica y reglas de cobro",
      "paths": ["src/billing", "tests/billing"],
      "keywords": ["billing", "invoice", "payment"],
      "upstream_dependencies": ["shared_auth"],
      "related_surfaces": ["reporting_finance"],
      "owners": ["team-billing"],
      "risk_level": "high"
    }
  ]
}
```

### 5.2 AECF_SURFACE_<surface_id>.md

Cada `surface` debe incluir solo el contexto necesario para reutilizacion operativa.

Secciones recomendadas:

1. identificacion y tipo,
2. alcance,
3. invariantes,
4. componentes y rutas clave,
5. integraciones y dependencias,
6. riesgos y limites,
7. testing y validaciones relevantes,
8. heuristicas para decidir cuando cargarla.

## 6. Politica de seleccion de surfaces

Para una ejecucion real, la seleccion recomendada es:

1. cargar siempre `AECF_PROJECT_CONTEXT.md`,
2. preguntar primero si realmente hacen falta `surfaces` si el contexto todavia no lo deja claro,
3. si existe, cargar `AECF_SURFACES_INDEX.md` o `.json`,
4. resolver una `primary_surface`,
5. cargar ademas `related_surfaces` solo si son necesarias,
6. evitar mas de 3 `surfaces` salvo que el trabajo sea realmente transversal.

Regla practica:

1. trabajo localizado -> contexto global + 1 `surface`.
2. trabajo con integracion directa -> contexto global + `primary_surface` + 1 `related_surface`.
3. trabajo transversal fuerte -> contexto global + varias `surfaces`, pero con justificacion explicita en `AECF_RUN_CONTEXT.json`.

## 7. Preguntas minimas para resolver surfaces

Cuando el `TOPIC` no deja clara la `surface`, usar un intake corto.

1. Este workspace necesita realmente `surfaces` o basta contexto global?
2. Si necesita `surfaces`, son principalmente de negocio, tecnicas o mixtas?
3. Que modulo, carpeta o componente parece estar implicado?
4. El cambio es localizado o transversal?
5. Necesita sobre todo contexto de negocio, de arquitectura tecnica o ambos?
6. La lista propuesta por la IA se acepta tal cual o hay que renombrar, fusionar, dividir, eliminar o anadir alguna?

Guia de intake:

- `aecf_prompts/guides/AECF_SURFACE_SELECTION_INTAKE.md`
- `aecf_prompts/guides/AECF_SKILL_SURFACE_CONTRACT.md`

Salida esperada del intake:

1. `primary_surface`,
2. `active_surfaces`,
3. `selection_rationale`,
4. `missing_context` si sigue habiendo ambiguedad.

## 8. Relacion con los skills actuales

Por ahora no hace falta crear un skill nuevo como `aecf_project_context_generator_big`.

La estrategia recomendada en `aecf_prompts` es:

1. `aecf_project_context_generator` genera o refresca el contexto global y es el unico skill que debe decidir con la persona si hay `surfaces`.
2. `aecf_codebase_intelligence` aporta inventario tecnico y señales para proponer `surfaces`.
3. `aecf_set_stack` y `aecf_document_context_ingestion` pueden aportar evidencia adicional, pero no deben cerrar la decision.
4. Los skills repo-dependientes posteriores consumen `primary_surface` y `active_surfaces`; no deben redescubrir alcance desde cero.
5. El modelo de `surface` se consolida como capa de contexto reutilizable para ejecuciones futuras.

Nota para la copia prompt-only publicada actual:

1. `aecf_codebase_intelligence` y `aecf_set_stack` estan disponibles como `assists`.
2. `aecf_document_context_ingestion` forma parte del catalogo completo en `aecf_prompts/skills`, aunque el bundle cliente puede filtrarlo segun `SKILL_RELEASE.json`.

## 8.1 Roles de los skills respecto a surfaces

Clasificacion recomendada en `aecf_prompts`:

1. `decides`: solo `aecf_project_context_generator`.
2. `assists`: `aecf_codebase_intelligence`, `aecf_set_stack`, `aecf_document_context_ingestion`.
3. `consumes`: el resto de skills repo-dependientes.
4. `not_applicable` o `global_only`: skills como `aecf_new_project` cuando todavia no existe un workspace real que particionar.

Contrato comun para skills `consumes`:

- `aecf_prompts/guides/AECF_SKILL_SURFACE_CONTRACT.md`

Solo deberia aparecer un skill nuevo cuando la capa de `surface` tenga entradas propias estables, artefactos propios bien cerrados y reglas de resolucion que ya no sean solo una extension natural del bootstrap actual.

## 9. Flujo recomendado para repos grandes

1. Crear o refrescar `AECF_PROJECT_CONTEXT.md` con foco global minimo.
2. Preguntar si realmente hacen falta `surfaces` o si el contexto global basta.
3. Si hacen falta, preguntar si el corte es principalmente de negocio, tecnico o mixto.
4. Ejecutar `aecf_codebase_intelligence` para obtener señales estructuradas del repo.
5. Proponer una primera lista de `surfaces` candidatas con nombre, tipo, rutas y justificacion.
6. Pedir confirmacion humana para aceptar, renombrar, fusionar, dividir, eliminar o anadir `surfaces`.
7. Crear `AECF_SURFACES_INDEX.json` y `AECF_SURFACES_INDEX.md`.
8. Crear primero entre 5 y 15 `surfaces` de alto valor.
9. Para cada `TOPIC`, resolver la `primary_surface` antes de arrancar la primera fase gobernada.
10. Registrar la seleccion en `AECF_RUN_CONTEXT.json`.
11. Revisar y refinar las `surfaces` conforme aparezcan nuevos flujos.

## 9.1 Ejemplo de definicion de surfaces

Supongamos un workspace cliente de e-commerce.

La IA detecta estas candidatas:

1. `catalog` como `business_surface`,
2. `checkout` como `business_surface`,
3. `identity_access` como `technical_surface`,
4. `observability` como `technical_surface`.

El skill no debe consolidarlas automaticamente.

Debe preguntar algo como:

> Detecto 4 `surfaces` candidatas. Quieres mantenerlas, renombrarlas, fusionarlas, dividirlas o eliminar alguna?

La persona puede responder, por ejemplo:

1. mantener `catalog`,
2. mantener `checkout`,
3. renombrar `identity_access` a `auth_platform`,
4. no crear `observability` como `surface` separada y dejarla como dependencia transversal.

Solo despues de esa confirmacion se crea el indice final y los borradores por `surface`.

## 10. Limites deliberados de esta primera iteracion

Este modelo en `aecf_prompts`:

1. no cambia aun el componente,
2. no introduce un skill nuevo,
3. no obliga a generar `surfaces` automaticamente,
4. no sustituye el contexto global,
5. no pretende resolver toda la topologia del repo sin validacion humana.

## 11. Consideracion futura para el componente

Cuando se lleve este modelo al componente, convendra mantener el mismo contrato de artefactos si es posible.

La migracion mas limpia seria:

1. conservar `AECF_PROJECT_CONTEXT.md` como capa global,
2. hacer que el runtime pueda leer `AECF_SURFACES_INDEX.json`,
3. persistir `primary_surface` y `active_surfaces` en el estado de ejecucion,
4. decidir por heuristica + confirmacion humana cuando el `TOPIC` sea ambiguo.

Por ahora, en `aecf_prompts`, esto queda solo como contrato prompt-only.

