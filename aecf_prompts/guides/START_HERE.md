# AECF Prompts — Start Here

LAST_REVIEW: 2026-04-13
OWNER SEACHAD

---

## Si eres nuevo, empieza aqui

Si estas leyendo la documentacion publicada en GitHub Pages, empieza por `index.html` en la raiz del repo y usa `GUIDE_VIEWER.html` para abrir esta guia y el resto de markdown sin salir de la superficie HTML.

Si trabajas en un workspace destino con el MCP prompt-only activo, puedes pedir esta misma guía con `aecf_show_guide` para que el host la renderice en el `output_language` efectivo y use traducción derivada solo cuando no exista copia humana localizada.

Si solo quieres saber por donde arrancar con `aecf_prompts`, sigue este orden:

1. Lee [AECF_GUIDES_MASTER.md](AECF_GUIDES_MASTER.md)
2. Lee [QUICK_START.md](QUICK_START.md)
3. Si no quieres redactar todo el contexto a mano, lee [AECF_PROJECT_CONTEXT_BOOTSTRAP.md](AECF_PROJECT_CONTEXT_BOOTSTRAP.md)
4. Si quieres ahorrar tokens por sesion, lee [AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md](AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md)
5. Si quieres usar una sintaxis parecida a `@aecf` sin componente, lee [AECF_PROMPT_ONLY_COMMANDS.md](AECF_PROMPT_ONLY_COMMANDS.md)
6. Si quieres que la memoria del proyecto enriquezca todos los skills, lee [AECF_MEMORY_MODEL.md](AECF_MEMORY_MODEL.md)
7. Si el repo es grande o multi-equipo, lee [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md)
8. Si quieres extender un skill base con reglas locales del proyecto, lee [AECF_EXTERNAL_SKILLS.md](AECF_EXTERNAL_SKILLS.md)
9. Si necesitas detalle sobre skills, lee [../skills/README_SKILLS.md](../skills/README_SKILLS.md)
10. Si necesitas entender la metodologia completa, lee [../AECF_METHODOLOGY.md](../AECF_METHODOLOGY.md)
11. Si quieres entender cómo se mapea AECF con diferentes metodologías de gestión de proyectos lee [AECF_APPLICATION_LIFECYCLE_GUIDE.md](AECF_APPLICATION_LIFECYCLE_GUIDE.md)

## Que guia usar segun el LLM

- ChatGPT / Copilot Chat web: empieza por [QUICK_START.md](QUICK_START.md)
- Claude CLI: usa [AECF_PROMPTS_CLAUDE_CLI.md](AECF_PROMPTS_CLAUDE_CLI.md)
- Codex CLI: usa [AECF_PROMPTS_CODEX_CLI.md](AECF_PROMPTS_CODEX_CLI.md)
- External skills locales de proyecto: usa [AECF_EXTERNAL_SKILLS.md](AECF_EXTERNAL_SKILLS.md)

## Orden minimo recomendado

1. Copia `aecf_prompts/` al proyecto.
2. Define la atribución del topic con `AECF_PROMPTS_USER_ID` o, si no existe, con `AECF_PROMPTS_MODEL_ID`/`MODEL_ID` o `AECF_PROMPTS_AGENT_ID`/`AGENT_ID`. Si el host da dudas, valida lo que ve el bundle con `aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --diagnose-env`
3. Prepara contexto:
   - rapido: crear `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md`
   - mejor: ejecutar `aecf_project_context_generator`
4. Si el repo es grande o complejo, ejecuta `aecf_codebase_intelligence`.
5. Si el repo es grande o multi-equipo, crea `surfaces` con apoyo de [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md).
6. Ejecuta tu primer flujo real desde [QUICK_START.md](QUICK_START.md), normalmente con `new_feature`, `refactor` o `hotfix`.

## Donde estan los knowledge packs

En este repo, la fuente canónica para knowledge packs y semantic profiles que también puede consumir `aecf_prompts` está en:

- `aecf_prompts/knowledge/domains/<domain>/pack.md`
- `aecf_prompts/knowledge/domains/<domain>/semantic_profiles/<profile>.md`

Ejemplo real:

- `aecf_prompts/knowledge/domains/java/pack.md`
- `aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md`

`aecf_prompts` publica además la misma superficie para uso prompt-only en:

- `aecf_prompts/knowledge/domains/java/pack.md`
- `aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md`

Si quieres reutilizarlos en modo prompt-only, puedes:

1. Referenciar la fuente canónica `aecf_prompts/knowledge/...` si trabajas dentro de este repo.
2. Usar `aecf_prompts/knowledge/...` si estás trabajando sobre el bundle prompt-only.
3. Si haces una distribución parcial, asegurarte de que `aecf_prompts/knowledge/` viaja también con el paquete.

## Regla de sincronizacion

Si los copias dentro de este repo a otra ubicación para consumo prompt-only o para distribución, no pasan a ser una nueva fuente canónica.

La fuente canónica sigue siendo `aecf_prompts/knowledge/`.

Además, por las reglas del repo, cualquier cambio hecho en `aecf_prompts/knowledge/` debe mantenerse sincronizado con:

- `aecf_prompts/knowledge/`
- `aecf_prompts/knowledge/`

Si generas una copia adicional para un bundle manual, esa copia también debe mantenerse alineada con la fuente canónica para no introducir deriva documental ni de comportamiento.

## Regla practica

`START_HERE.md` orienta.

`QUICK_START.md` manda.

Si necesitas semantic profiles reutilizables en modo prompt-only dentro de este repo, usa como referencia la fuente canónica `aecf_prompts/knowledge/domains/...` y la copia publicada `aecf_prompts/knowledge/domains/...`.

Si dudas, empieza siempre por [QUICK_START.md](QUICK_START.md).
