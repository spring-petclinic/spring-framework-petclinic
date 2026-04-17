# AECF Prompts — Guía de Uso con Codex CLI (OpenAI)

LAST_REVIEW: 2026-03-25
OWNER SEACHAD

---

## 1. Qué es esto

Guía práctica para ejecutar skills de AECF Prompts usando [Codex CLI](https://github.com/openai/codex) de OpenAI, sin necesidad de VS Code ni del motor `aecf_engine`. Codex CLI tiene acceso directo al filesystem y puede ejecutar comandos, lo que lo hace especialmente potente para fases de implementación.

Si quieres conservar una sintaxis parecida a `@aecf` sin componente, añade también `AECF_PROMPT_ONLY_COMMANDS.md` al contexto de trabajo. Esa guía convierte entradas tipo `@aecf run ...` o `@aecf list topics` en resoluciones manuales sobre `aecf_prompts`.

---

## 2. Requisitos previos

| Requisito | Comando de verificación |
|---|---|
| Codex CLI instalado | `codex --version` |
| Node.js ≥ 18 | `node --version` |
| API key de OpenAI configurada | `echo $OPENAI_API_KEY` |

### Instalar Codex CLI si no lo tienes

```bash
npm install -g @openai/codex
```

---

## 3. Diferencias clave frente a Claude CLI

| Aspecto | Claude CLI | Codex CLI |
|---|---|---|
| **Acceso a ficheros** | Lee del filesystem (en modo Claude Code) | Lee Y escribe directamente |
| **Ejecución de comandos** | Puede ejecutar (en modo agente) | Puede ejecutar (con approval modes) |
| **Modos de aprobación** | Interactivo o pipe | `suggest` / `auto-edit` / `full-auto` |
| **Proveedor / runtime** | Claude CLI | Codex CLI |
| **Mejor para** | Análisis, documentación, auditoría | Implementación, edición directa de código |

**Implicación para AECF:** Codex CLI puede escribir los artefactos directamente al disco sin necesidad de redirigir stdout. Esto simplifica el flujo, pero hay que tener cuidado con el modo `full-auto` para que no toque archivos fuera del scope.

---

## 4. Estructura en el proyecto destino

Idéntica a la guía de Claude CLI:

```bash
cp -r /ruta/a/AECF_MCP/aecf_prompts ./aecf_prompts
```

```
mi-proyecto/
├── aecf_prompts/
│   ├── skills/
│   ├── prompts/
│   ├── templates/
│   ├── checklists/
│   ├── scoring/
│   ├── guides/
│   ├── knowledge/              ← knowledge packs (ver sección 7)
│   └── documentation/          ← artefactos generados
├── AECF_PROJECT_CONTEXT.md     ← contexto del proyecto
├── src/
└── ...
```

Crear `AECF_PROJECT_CONTEXT.md` en la raíz del proyecto (ver guía Claude CLI sección 4 para la plantilla completa):

```markdown
# AECF Project Context

## Project
- Name: <nombre del proyecto>
- Language: Java
- Framework: Spring Boot 3.x
- Build: Maven

## Team
- Size: X developers
- Risk tolerance: Medium

## Standards
- Testing framework: JUnit 5 + Mockito
- Coverage target: 80%
- Branching strategy: GitLab flow

## Scoring Thresholds
- Feature: 75
- Hotfix: 70
- Security: 90
```

---

## 5. Ejecutar `document_legacy` con Codex CLI

Sintaxis recomendada:

- base y más portable: `use skill=...`
- opcional si Codex ya tiene cargado el router prompt-only: sintaxis `@aecf ...`

### Opción A: Modo interactivo (recomendado para primera vez)

```bash
cd mi-proyecto

# Abrir Codex en modo suggest (pide confirmación antes de escribir)
codex

# Dentro de la sesión, pegar:
> Lee aecf_prompts/skills/skill_document_legacy.md y ejecútalo.
> TOPIC=payment_service
> prompt=Documentar el servicio de pagos legacy, identificar flujos y riesgos.
> Lee los archivos Java de src/main/java/com/empresa/payments/ como código a documentar.
> Lee AECF_PROJECT_CONTEXT.md como contexto del proyecto.
> Si existe aecf_prompts/knowledge/java/pack.md, léelo como reglas del dominio.
> Guarda el resultado en .aecf/runtime/documentation/payment_service/AECF_DOCUMENT_LEGACY.md
```

Variante equivalente si has cargado `AECF_PROMPT_ONLY_COMMANDS.md`:

```bash
> @aecf run skill=document_legacy TOPIC=payment_service prompt="Documentar el servicio de pagos legacy, identificar flujos y riesgos"
```

Codex leerá los ficheros, generará la documentación y pedirá tu aprobación para escribirla.

### Opción B: Modo auto-edit (escribe ficheros sin preguntar, pero no ejecuta comandos)

```bash
cd mi-proyecto

codex --approval-mode auto-edit -q "
Lee aecf_prompts/skills/skill_document_legacy.md y ejecútalo con:
TOPIC=payment_service
prompt=Documentar el servicio de pagos legacy

Lee como contexto:
- AECF_PROJECT_CONTEXT.md
- aecf_prompts/knowledge/java/pack.md (si existe)

Lee como código a documentar:
- src/main/java/com/empresa/payments/PaymentService.java
- src/main/java/com/empresa/payments/PaymentValidator.java
- src/main/java/com/empresa/payments/PaymentRepository.java

Guarda el resultado en .aecf/runtime/documentation/payment_service/AECF_DOCUMENT_LEGACY.md
"
```

### Opción C: Script reutilizable

Guardar como `aecf_prompts/run_skill_codex.sh`:

```bash
#!/bin/bash
# Uso: ./aecf_prompts/run_skill_codex.sh <skill> <topic> "<prompt>" <archivo1> [archivo2] ...
set -euo pipefail

SKILL=$1; TOPIC=$2; PROMPT=$3; shift 3

# Construir lista de archivos
FILES_INSTRUCTION=""
for f in "$@"; do
  FILES_INSTRUCTION="$FILES_INSTRUCTION
- $f"
done

# Knowledge pack si existe
KNOWLEDGE_INSTRUCTION=""
if [ -f "aecf_prompts/knowledge/java/pack.md" ]; then
  KNOWLEDGE_INSTRUCTION="Lee aecf_prompts/knowledge/java/pack.md como reglas del dominio Java."
fi
if [ -f "aecf_prompts/knowledge/java/semantic_profiles/spring_boot_service.md" ]; then
  KNOWLEDGE_INSTRUCTION="$KNOWLEDGE_INSTRUCTION
Lee aecf_prompts/knowledge/java/semantic_profiles/spring_boot_service.md como reglas Spring Boot."
fi

# Ejecutar con Codex
codex --approval-mode auto-edit -q "
Lee aecf_prompts/skills/skill_${SKILL}.md y ejecútalo.

TOPIC=$TOPIC
prompt=$PROMPT

Lee como contexto:
- AECF_PROJECT_CONTEXT.md
$KNOWLEDGE_INSTRUCTION

Lee como código a documentar:
$FILES_INSTRUCTION

Guarda el resultado en .aecf/runtime/documentation/$TOPIC/AECF_DOCUMENT_LEGACY.md
Crea el directorio si no existe.
"

echo ""
echo "✅ Artefacto: .aecf/runtime/documentation/$TOPIC/AECF_DOCUMENT_LEGACY.md"
```

Uso:

```bash
chmod +x aecf_prompts/run_skill_codex.sh

./aecf_prompts/run_skill_codex.sh document_legacy payment_service \
  "Documentar el servicio de pagos, flujos, dependencias y riesgos" \
  src/main/java/com/empresa/payments/PaymentService.java \
  src/main/java/com/empresa/payments/PaymentValidator.java
```

---

## 6. Ejecutar skills multi-fase (new_feature, refactor, etc.)

Codex CLI puede ejecutar cada fase secuencialmente. La ventaja es que puede escribir directamente:

La invocación equivalente en sintaxis prompt-only sería:

```text
@aecf run skill=new_feature TOPIC=user_auth prompt="Implementar autenticación JWT con refresh tokens"
```

Después de esa resolución inicial, el flujo sigue exactamente igual que en esta guía: prompts de fase, artefactos y documentación en disco.

```bash
TOPIC=user_auth

# Fase 1: PLAN
codex --approval-mode auto-edit -q "
Lee aecf_prompts/prompts/00_PLAN.md como instrucciones de fase.
Lee AECF_PROJECT_CONTEXT.md como contexto.
Lee aecf_prompts/knowledge/java/pack.md como reglas del dominio (si existe).

use skill=new_feature TOPIC=$TOPIC prompt='Implementar autenticación JWT con refresh tokens'

Guarda la salida en .aecf/runtime/documentation/$TOPIC/AECF_01_PLAN.md
"

# Fase 2: AUDIT_PLAN
codex --approval-mode auto-edit -q "
Lee aecf_prompts/prompts/02_AUDIT_PLAN.md como instrucciones de fase.
Lee .aecf/runtime/documentation/$TOPIC/AECF_01_PLAN.md como el plan a auditar.
Lee aecf_prompts/checklists/AUDIT_PLAN_CHECKLIST.md como checklist.
Lee aecf_prompts/scoring/SCORING_MODEL.md como modelo de scoring.

use skill=new_feature TOPIC=$TOPIC

Guarda la salida en .aecf/runtime/documentation/$TOPIC/AECF_02_AUDIT_PLAN.md
"

# Verificar veredicto
grep -i "GO\|NO-GO" .aecf/runtime/documentation/$TOPIC/AECF_02_AUDIT_PLAN.md

# Si GO → continuar con TEST_STRATEGY (04), IMPLEMENT (05), AUDIT_CODE (06), VERSION (08)
# Si NO-GO → ejecutar FIX_PLAN (03) y repetir AUDIT
```

### Fase IMPLEMENT con Codex (ventaja clave)

Codex puede **escribir código directamente** en el proyecto:

```bash
# Fase 5: IMPLEMENT (Codex escribe los archivos Java + tests)
codex --approval-mode auto-edit -q "
Lee aecf_prompts/prompts/05_IMPLEMENT.md como instrucciones de fase.
Lee .aecf/runtime/documentation/$TOPIC/AECF_01_PLAN.md como plan aprobado.
Lee .aecf/runtime/documentation/$TOPIC/AECF_04_TEST_STRATEGY.md como estrategia de tests.
Lee aecf_prompts/checklists/IMPLEMENT_CHECKLIST.md como checklist.
Lee aecf_prompts/knowledge/java/pack.md como reglas del dominio.
Lee aecf_prompts/knowledge/java/semantic_profiles/spring_boot_service.md si existe.

use skill=new_feature TOPIC=$TOPIC

Implementa el código según el plan en los archivos Java del proyecto.
Implementa los tests según la estrategia en src/test/java/.
Guarda el artefacto en .aecf/runtime/documentation/$TOPIC/AECF_05_IMPLEMENT.md
"

# Codex habrá creado/modificado los archivos Java directamente
# Verificar con git:
git diff --stat
```

> **Nota de seguridad:** Usa `auto-edit` (no `full-auto`) para poder revisar si ejecuta comandos destructivos. Codex con `auto-edit` puede escribir ficheros pero pide confirmación para ejecutar comandos.

---

## 7. Knowledge Packs

La estructura y contenido de knowledge packs es **idéntica** a la documentada en la guía de Claude CLI. La diferencia está en cómo se inyectan:

Fuente canónica en este repo:

- `aecf_prompts/knowledge/domains/<domain>/pack.md`
- `aecf_prompts/knowledge/domains/<domain>/semantic_profiles/<profile>.md`

Ejemplo real:

- `aecf_prompts/knowledge/domains/java/pack.md`
- `aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md`

**Con Claude CLI (pipe)**: se concatenan en el prompt con `$(cat ...)`.
**Con Codex CLI**: se le dice que lea los ficheros y él los lee del filesystem directamente.

```bash
# Codex los lee nativamente:
codex -q "
Lee aecf_prompts/knowledge/java/pack.md como reglas del dominio.
Lee aecf_prompts/knowledge/java/semantic_profiles/spring_boot_service.md como reglas Spring Boot.
Lee aecf_prompts/knowledge/empresa/pack.md como reglas específicas de la empresa.
...
"
```

Ejemplo equivalente para ZKoss:

```bash
codex -q "
Lee aecf_prompts/knowledge/domains/java/pack.md como reglas del dominio Java.
Lee aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md como reglas específicas de ZKoss.
Lee AECF_PROJECT_CONTEXT.md.
Usa todo eso para ejecutar `new_feature` sobre una pantalla de búsqueda de clientes en ZKoss.
"
```

Si prefieres una copia local prompt-only en `aecf_prompts/knowledge/`, la estructura es la misma, pero recuerda que en este repo la fuente maestra sigue siendo `aecf_prompts/knowledge/`.

Si haces esa copia dentro del repo, mantenla sincronizada con:

- `aecf_prompts/knowledge/`
- `aecf_prompts/knowledge/`

Para crear knowledge packs propios, ver la guía de Claude CLI (sección 7) — la estructura de ficheros es la misma.

---

## 8. Modos de aprobación de Codex (cuándo usar cada uno)

| Modo | Ficheros | Comandos | Cuándo usarlo |
|---|---|---|---|
| `suggest` | Pide permiso | Pide permiso | Primera ejecución, aprendizaje |
| `auto-edit` | Escribe directamente | Pide permiso | Uso habitual — seguro y productivo |
| `full-auto` | Escribe directamente | Ejecuta directamente | Solo si confías al 100% — ojo con side effects |

**Recomendación AECF:** Usar `auto-edit` para fases de documentación y auditoría. Usar `suggest` para fases de IMPLEMENT hasta ganar confianza.

---

## 9. Restricciones de Codex CLI (a tener en cuenta)

| Aspecto | Detalle |
|---|---|
| **No soporta imágenes** | Los diagramas Mermaid se generan como texto, no como renders |
| **Sandbox por defecto** | Codex restringe acceso a red y paths fuera del proyecto |
| **Tamaño de contexto** | Proyectos muy grandes pueden superar la ventana de contexto |
| **Modelo** | Usa el modelo configurado en el runtime; configurable con `--model` |

---

## 10. Comparación rápida: cuándo usar cada CLI

| Tarea | Mejor con Claude CLI | Mejor con Codex CLI |
|---|---|---|
| `document_legacy` | ✅ (buena calidad analítica) | ✅ (escribe directo al disco) |
| `explain_behavior` | ✅ (análisis profundo) | ✅ |
| `security_review` | ✅ | ✅ |
| `new_feature` (PLAN, AUDIT) | ✅ | ✅ |
| `new_feature` (IMPLEMENT) | Necesita script para escribir | ✅ (**escribe código directo**) |
| `refactor` (IMPLEMENT) | Necesita script para escribir | ✅ (**modifica archivos in-place**) |
| Proyectos muy grandes | Claude Code navega bien | Codex sandbox puede limitar |

**Estrategia combinada:** Usar Claude CLI para fases de análisis (PLAN, AUDIT, DOCUMENT) y Codex CLI para fases de implementación (IMPLEMENT, FIX_CODE). Ambos comparten los mismos artefactos en `.aecf/runtime/documentation/`.

---

## 11. Artefactos generados

Idénticos en estructura a la guía de Claude CLI:

```
.aecf/runtime/documentation/
├── payment_service/
│   └── AECF_DOCUMENT_LEGACY.md     ← generado por document_legacy
└── user_auth/
    ├── AECF_01_PLAN.md             ← generado por new_feature fase PLAN
    ├── AECF_02_AUDIT_PLAN.md       ← fase AUDIT_PLAN
    ├── AECF_04_TEST_STRATEGY.md    ← fase TEST_STRATEGY
    ├── AECF_05_IMPLEMENT.md        ← fase IMPLEMENT (+ código escrito)
    ├── AECF_06_AUDIT_CODE.md       ← fase AUDIT_CODE
    └── AECF_08_VERSION.md          ← fase VERSION
```

Commitear en GitLab junto al código para trazabilidad completa.

---

## 12. Referencia rápida de skills disponibles

| Skill | Tier | Fases | Cuándo usarlo |
|---|---|---|---|
| `document_legacy` | 2 | DOCUMENT → FLOW → REVIEW | Código sin documentar |
| `explain_behavior` | 1 | EXPLAIN (una fase) | Entender qué hace un módulo |
| `code_standards_audit` | 1 | AUDIT (una fase) | Verificar estándares |
| `security_review` | 1 | REVIEW (una fase) | Buscar vulnerabilidades |
| `executive_summary` | 1 | SUMMARY (una fase) | Resumen ejecutivo de un topic |
| `new_feature` | 3 | PLAN → AUDIT → TEST → IMPLEMENT → AUDIT → VERSION | Feature nueva completa |
| `refactor` | 3 | PLAN → AUDIT → TEST → IMPLEMENT → AUDIT → VERSION | Refactorizar módulo |
| `hotfix` | 3 | PLAN → AUDIT → IMPLEMENT → AUDIT → VERSION | Corrección urgente |
