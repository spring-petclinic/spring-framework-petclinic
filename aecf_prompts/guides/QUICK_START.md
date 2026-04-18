# AECF Prompts — Quick Start

LAST_REVIEW: 2026-04-13

---

## 0. Usa esta guia como punto de entrada principal

En la publicacion HTML para GitHub Pages, el entrypoint es `index.html` en la raiz del repo y esta guia se abre desde `GUIDE_VIEWER.html` para mantener la navegacion documental dentro de HTML.

Si eres nuevo en `aecf_prompts`, esta es la guia que debes seguir primero.

Apoyos utiles segun lo que necesites:

- indice maestro de guias: [AECF_GUIDES_MASTER.md](AECF_GUIDES_MASTER.md)
- orientacion general: [START_HERE.md](START_HERE.md)
- bootstrap del contexto: [AECF_PROJECT_CONTEXT_BOOTSTRAP.md](AECF_PROJECT_CONTEXT_BOOTSTRAP.md)
- ahorro de tokens: [AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md](AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md)
- sintaxis tipo `@aecf` sin componente: [AECF_PROMPT_ONLY_COMMANDS.md](AECF_PROMPT_ONLY_COMMANDS.md)
- memoria global y por usuario o agente: [AECF_MEMORY_MODEL.md](AECF_MEMORY_MODEL.md)
- repos grandes o multi-equipo: [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md)
- external skills locales por proyecto: [AECF_EXTERNAL_SKILLS.md](AECF_EXTERNAL_SKILLS.md)
- contrato de `AECF_RUN_CONTEXT.json`: [AECF_RUN_CONTEXT_CONTRACT.md](AECF_RUN_CONTEXT_CONTRACT.md)
- intake de selección de `surfaces`: [AECF_SURFACE_SELECTION_INTAKE.md](AECF_SURFACE_SELECTION_INTAKE.md)
- detalle de skills: [../skills/README_SKILLS.md](../skills/README_SKILLS.md)
- metodologia completa: [../AECF_METHODOLOGY.md](../AECF_METHODOLOGY.md)

## 1. Preparación (5 minutos)

### 1.1 Copiar aecf_prompts al proyecto

```text
mi-proyecto/
├── aecf_prompts/              ← copiar aquí
├── .aecf/
│   └── runtime/
│       └── documentation/
│           └── AECF_PROJECT_CONTEXT.md  ← crear este archivo
├── src/
└── ...
```

> `.aecf/runtime/documentation/` se creará automáticamente para almacenar las salidas de cada skill/topic sin depender de la carpeta del bundle.

Si el repositorio es grande, usa `AECF_PROJECT_CONTEXT.md` como capa global minima y particiona el resto del contexto con el modelo de `surface` descrito en `AECF_SURFACE_CONTEXT_MODEL.md`.

### 1.2 Verificar la atribución del topic

Antes de usar los prompts, verifica qué identificador va a quedar congelado en el topic real.

Prioridad canónica de atribución:

1. `AECF_PROMPTS_USER_ID`
2. `AECF_PROMPTS_MODEL_ID` o `MODEL_ID`
3. `AECF_PROMPTS_AGENT_ID` o `AGENT_ID`

Si necesitas memoria específica, usa el identificador efectivo congelado en `AECF_RUN_CONTEXT.json`. Ver [AECF_MEMORY_MODEL.md](AECF_MEMORY_MODEL.md).

Ejemplos en Windows PowerShell para dejarla persistente:

```powershell
setx AECF_PROMPTS_USER_ID "ana.garcia@empresa.com"
setx AECF_PROMPTS_MODEL_ID "gpt-5.4"
setx AECF_PROMPTS_AGENT_ID "copilot-agent"
```

Si usas `setx`, abre una consola nueva antes de ejecutar el bootstrap del bundle.

Si quieres validar exactamente qué ve el `.exe` en tu máquina, ejecuta:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --diagnose-env
```

### 1.2.b Sincronizar archivos de instrucciones prompt-only

Después de definir la atribución que corresponda, crea o refresca las instrucciones por defecto del bundle:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --sync-instructions
```

Si estás trabajando sobre la copia fuente del repo y no sobre el bundle entregado al cliente, usa el `.py` equivalente.

Esto crea o actualiza `aecf_forced_instructions.md` con el bloque canónico en inglés del bundle y deja `.github/copilot-instructions.md`, `copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md` y `.codex/instructions.md` como superficies mínimas de carga.

### 1.3 Crear .aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md

Crear en `.aecf/runtime/documentation/` con esta estructura mínima:

```markdown
# AECF Project Context

## Project
- Name: Mi Proyecto
- Language: Python / TypeScript / Java / ...
- Framework: Django / React / Spring / ...
- OUTPUT_LANGUAGE: ENGLISH / SPANISH / FRENCH / ...

## Team
- Size: X developers
- Risk tolerance: Low / Medium / High

## Standards
- Testing framework: pytest / jest / junit / ...
- Coverage target: 80%
- Branching strategy: trunk-based / gitflow / ...

## Scoring Thresholds
- Feature: 75
- Hotfix: 70
- Security: 90
```

---

## 2. Tu primera ejecución (10 minutos)

### 2.0 Opcional: conservar sintaxis tipo `@aecf`

Si quieres usar `aecf_prompts/` sin componente pero manteniendo una sintaxis parecida a `@aecf`, carga también `aecf_prompts/guides/AECF_PROMPT_ONLY_COMMANDS.md` en el LLM.

Con esa guía, entradas como estas se resuelven manualmente:

```text
@aecf list skills
@aecf run skill=new_feature TOPIC=user_auth prompt="Implementar autenticación JWT con refresh tokens"
@aecf context
```

No ejecutan comandos reales: el LLM los traduce a skills, prompts y artefactos de `aecf_prompts/`.

### Ejemplo: Nueva feature con `new_feature`

**Paso 1**: Consultar el skill

Leer `aecf_prompts/skills/skill_new_feature.md` → te dice el flujo:

```text
PLAN → AUDIT_PLAN → [FIX_PLAN] → TEST_STRATEGY → IMPLEMENT → AUDIT_CODE → [FIX_CODE] → VERSION
```

Si el repo es grande, antes de ejecutar la primera fase resuelve tambien:

1. `primary_surface`,
2. `active_surfaces`,
3. si basta con contexto global o hace falta contexto por `surface`.

Registra esa resolucion en `AECF_RUN_CONTEXT.json` cuando el flujo sea real.

Si necesitas una salida intermedia corta antes de fijar el JSON, usa `aecf_prompts/templates/SURFACE_SELECTION_BRIEF_TEMPLATE.md`.

**Paso 2**: Ejecutar PLAN

Pegar en tu LLM:

```text
use skill=new_feature TOPIC=user_auth prompt=Implementar autenticación JWT con refresh tokens
```

O, si has cargado la guía de equivalencias prompt-only:

```text
@aecf run skill=new_feature TOPIC=user_auth prompt=Implementar autenticación JWT con refresh tokens
```

Y a continuación pegar el contenido de `aecf_prompts/prompts/00_PLAN.md`.

> El prompt ya contiene las instrucciones de qué archivos debe cargar el LLM (`<DOCS_ROOT>/AECF_PROJECT_CONTEXT.md`) y dónde guardar la salida (`<DOCS_ROOT>/<user_id>/user_auth/01_new_feature_PLAN.md`). Usa `AECF_PROMPTS_DOCUMENTATION_PATH` si necesitas sobrescribir el `DOCS_ROOT` por defecto del workspace. `AECF_PROMPTS_DIRECTORY_PATH` sigue aceptandose como alias legado.

Antes de arrancar una ejecución real para un `TOPIC`, congela también el idioma de salida del flujo:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --topic user_auth --prompt-text "Implementar autenticación JWT con refresh tokens"
```

Si estás trabajando sobre la copia fuente del repo y no sobre el bundle entregado al cliente, usa el `.py` equivalente.

Ese comando crea `<DOCS_ROOT>/<user_id>/user_auth/AECF_RUN_CONTEXT.json` con el `output_language` resuelto y la atribución congelada para toda la ejecución.

Si el repo usa `surfaces`, completa ese archivo siguiendo el contrato de `AECF_RUN_CONTEXT_CONTRACT.md`.

**Paso 3**: Ejecutar AUDIT_PLAN

Pegar en tu LLM:

```text
use skill=new_feature TOPIC=user_auth prompt=Auditar el plan de autenticación JWT
```

Y a continuación pegar el contenido de `aecf_prompts/prompts/02_AUDIT_PLAN.md`.

> El prompt instruye al LLM a cargar automáticamente el plan generado, el checklist y el scoring model. No necesitas pegarlos tú.

**Paso 4**: Evaluar el veredicto

- **GO** → continuar con la siguiente fase (TEST_STRATEGY)
- **NO-GO** → ejecutar FIX_PLAN (pegar `prompts/03_FIX_PLAN.md`) y luego re-auditar

**Paso 5**: Repetir para cada fase del flujo

Cada prompt sabe:

- Qué archivos previos debe leer
- Qué checklist y scoring aplicar (si aplica)
- Dónde guardar su salida

---

## 3. Referencia rápida de skills

| Skill | Cuándo usarlo | Complejidad |
| --- | --- | --- |
| `new_feature` | Feature nueva, no urgente | TIER 3 (8 fases) |
| `refactor` | Mejorar código existente | TIER 3 (8 fases) |
| `hotfix` | Emergencia en producción | TIER 3 (umbral 70) |
| `code_standards_audit` | Revisar estándares de código | TIER 1 (1 fase) |
| `security_review` | Revisar seguridad | TIER 1 (1 fase) |
| `document_legacy` | Documentar código existente | TIER 2 (3 fases) |
| `explain_behavior` | Entender un comportamiento | TIER 1 (1 fase) |
| `executive_summary` | Resumen para stakeholders | TIER 1 (1 fase) |

---

## 4. Dónde va cada output

Todas las salidas se guardan dentro de `<DOCS_ROOT>/<user_id>/{{TOPIC}}/`.

`<DOCS_ROOT>` usa `AECF_PROMPTS_DOCUMENTATION_PATH` si existe; si no, acepta `AECF_PROMPTS_DIRECTORY_PATH` como alias legado; si tampoco existe, cae por defecto en `<workspace>/.aecf/runtime/documentation`:

| Fase | Archivo de salida |
| --- | --- |
| PLAN | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/01_<skill_name>_PLAN.md` |
| AUDIT_PLAN | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/02_<skill_name>_AUDIT_PLAN.md` |
| FIX_PLAN | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/03_<skill_name>_FIX_PLAN.md` |
| TEST_STRATEGY | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/04_<skill_name>_TEST_STRATEGY.md` |
| IMPLEMENT | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/05_<skill_name>_IMPLEMENT.md` |
| AUDIT_CODE | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/06_<skill_name>_AUDIT_CODE.md` |
| FIX_CODE | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/07_<skill_name>_FIX_CODE.md` |
| VERSION | `<DOCS_ROOT>/<user_id>/{{TOPIC}}/08_<skill_name>_VERSION.md` |

---

## 5. Tips

- **Cada prompt sabe qué necesita** — no tienes que decirle al LLM qué cargar, el prompt lo manda
- **La atribución correcta depende del primer identificador disponible** — `AECF_PROMPTS_USER_ID`, luego `AECF_PROMPTS_MODEL_ID`/`MODEL_ID`, y luego `AECF_PROMPTS_AGENT_ID`/`AGENT_ID`
- **Si el host de chat no ve el entorno, valida con `--diagnose-env`** — el `.exe` usa `os.environ` directamente y te dirá exactamente qué variables AECF están visibles para el bundle
- **Congela el idioma por TOPIC** — usa `bootstrap_prompt_only_bundle.exe --topic ...` antes de la primera fase de cada ejecución real
- **Si el repo es grande, activa una `surface` primaria** — evita cargar todo el contexto global si el trabajo toca solo una parte del sistema
- **Si el LLM no puede leer archivos** (por ejemplo en ChatGPT web), pega el contenido de los archivos requeridos junto al prompt
- **Si el LLM no sigue el template**, indicarle explícitamente que siga la estructura de `aecf_prompts/templates/`
- **Guarda cada salida** en la ruta indicada por el prompt antes de pasar a la siguiente fase

---

## 6. Knowledge Packs y Semantic Profiles

### 6.1 Fuente canónica en este repo

Si estás usando `aecf_prompts` dentro de este mismo repo, los knowledge packs que debes tomar como referencia están en:

- `aecf_prompts/knowledge/domains/<domain>/pack.md`
- `aecf_prompts/knowledge/domains/<domain>/semantic_profiles/<profile>.md`

Ejemplo real para Java con ZKoss:

- `aecf_prompts/knowledge/domains/java/pack.md`
- `aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md`

El paquete prompt-only publica la misma superficie en:

- `aecf_prompts/knowledge/domains/java/pack.md`
- `aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md`

### 6.2 Cómo usarlos con `aecf_prompts`

Los skills de `aecf_prompts` ya tienen una ruta local consistente porque `knowledge/` forma parte del paquete publicado.

Por tanto, el uso real es uno de estos dos:

1. Dentro de este repo: puedes referenciar `aecf_prompts/knowledge/...` como fuente canónica.
2. En el bundle prompt-only: puedes referenciar `aecf_prompts/knowledge/...` como copia publicada.

Si tu LLM puede leer ficheros del workspace, dile explícitamente que cargue esos ficheros como contexto adicional del dominio y del stack.

Ejemplo conceptual para un flujo `new_feature`:

```text
use skill=new_feature TOPIC=zk_order_screen prompt=Crear una pantalla ZKoss para gestionar pedidos

Antes de responder, lee también:
- .aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md
- aecf_prompts/knowledge/domains/java/pack.md
- aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md
```

Si tu LLM no puede leer ficheros, pega esos Markdown junto al prompt de fase.

### 6.3 Ejemplo práctico mínimo

Para documentar o planificar sobre un proyecto Java con ZKoss:

```text
use skill=document_legacy TOPIC=zk_backoffice prompt=Documentar el módulo backoffice construido con ZUL y composers

Contexto adicional obligatorio:
- .aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md
- aecf_prompts/knowledge/domains/java/pack.md
- aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md
```

Para implementar una feature nueva:

```text
use skill=new_feature TOPIC=zk_customer_search prompt=Implementar búsqueda de clientes en una pantalla ZKoss

Contexto adicional obligatorio:
- .aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md
- aecf_prompts/knowledge/domains/java/pack.md
- aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md
```

### 6.4 Si los copias a otra ruta

Si montas una distribución parcial y mueves esos assets a otra carpeta distinta de `aecf_prompts/knowledge/`, recuerda esto:

1. En este repo la fuente canónica sigue siendo `aecf_prompts/knowledge/`.
2. `aecf_prompts/knowledge/` es la copia publicada para prompt-only.
3. La copia no debe evolucionar por libre.
4. Si cambias el conocimiento canónico, debes mantener sincronizada la copia.

Regla del repo:

- `aecf_prompts/knowledge/`, `aecf_prompts/knowledge/` y `aecf_prompts/knowledge/` deben mantenerse sincronizados.

Si haces una cuarta copia para distribución manual, mantenla también sincronizada para no introducir deriva.

