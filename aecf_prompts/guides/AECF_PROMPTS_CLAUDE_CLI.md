# AECF Prompts — Guía de Uso con Claude CLI

LAST_REVIEW: 2026-04-06
OWNER SEACHAD

---

## 1. Qué es esto

Guía práctica para ejecutar skills de AECF Prompts usando [Claude CLI](https://docs.anthropic.com/en/docs/claude-code) (`claude`), sin necesidad de VS Code ni del motor `aecf_engine`. Todo funciona con ficheros Markdown que se pegan al LLM como prompts gobernados.

Si quieres mantener una sintaxis parecida a `@aecf` sin componente, combina esta guía con `AECF_PROMPT_ONLY_COMMANDS.md`. Esa guía traduce comandos tipo `@aecf run`, `@aecf list skills` o `@aecf context` a resoluciones manuales sobre `aecf_prompts`, y cuando Claude tenga el MCP de AECF registrado debe preferir el tool MCP equivalente antes del fallback manual.

---

## 2. Requisitos previos

| Requisito | Comando de verificación |
|---|---|
| Claude CLI instalado | `claude --version` |
| Node.js ≥ 18 (para Claude CLI) | `node --version` |
| API key de Anthropic configurada | `echo $ANTHROPIC_API_KEY` |

### Instalar Claude CLI si no lo tienes

```bash
npm install -g @anthropic-ai/claude-code
```

---

## 3. Estructura en el proyecto destino

```bash
# Copiar aecf_prompts al proyecto
cp -r /ruta/a/AECF_MCP/aecf_prompts ./aecf_prompts
```

Resultado:

```
mi-proyecto/
├── aecf_prompts/
│   ├── skills/                 ← definición de cada skill
│   ├── prompts/                ← prompts de fase (PLAN, AUDIT, IMPLEMENT...)
│   ├── templates/              ← plantillas de artefactos
│   ├── checklists/             ← checklists de auditoría
│   ├── scoring/                ← modelo de scoring GO/NO-GO
│   ├── guides/                 ← esta guía y otras
│   ├── knowledge/              ← knowledge packs por dominio (ver sección 7)
│   └── documentation/          ← artefactos generados (creado automáticamente)
├── AECF_PROJECT_CONTEXT.md     ← contexto del proyecto (lo creas tú)
├── src/
└── ...
```

---

## 4. Crear `AECF_PROJECT_CONTEXT.md`

Crear en la raíz del proyecto. Claude lo leerá antes de generar cualquier output:

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
- Code review: merge requests obligatorios

## Architecture
- Pattern: microservicios / monolito modular / hexagonal
- Persistence: JPA + PostgreSQL
- Messaging: Kafka / RabbitMQ / ninguno
- Auth: OAuth2 / JWT / SSO corporativo

## Scoring Thresholds
- Feature: 75
- Hotfix: 70
- Security: 90
```

---

## 5. Ejecutar `document_legacy` con Claude CLI

Sintaxis recomendada:

- base y más portable: `use skill=...`
- opcional si has cargado el router prompt-only: sintaxis `@aecf ...`

### Opción A: Modo interactivo (Claude Code)

```bash
cd mi-proyecto

# Abrir sesión interactiva de Claude con acceso al filesystem
claude

# Dentro de la sesión, pegar:
> Lee el archivo aecf_prompts/skills/skill_document_legacy.md y ejecútalo con:
> TOPIC=payment_service
> prompt=Documentar el servicio de pagos legacy, identificar flujos, dependencias y riesgos
> Antes de documentar, resuelve `DOCS_ROOT` con `aecf_prompts/scripts/bootstrap_prompt_only_bundle.py --topic payment_service --prompt-text "Documentar el servicio de pagos legacy, identificar flujos, dependencias y riesgos"` o, si usas el `.exe` publicado, con `bootstrap_prompt_only_bundle.exe --topic payment_service ...`
> Lee los archivos Java en src/main/java/com/empresa/payments/ como código a documentar
> Si `AECF_PROMPTS_USER_ID` no está definido, declara que Claude Code no expone por sí mismo un `user_id` autenticado reutilizable y que debes usar `AECF_PROMPTS_USER_ID`; como fallback de atribución de modelo acepta `ANTHROPIC_MODEL`
> Guarda el resultado en <DOCS_ROOT>/<user_id>/payment_service/AECF_01_DOCUMENT_LEGACY.md
```

Variante equivalente si has cargado `AECF_PROMPT_ONLY_COMMANDS.md`:

```bash
> @aecf run skill=document_legacy TOPIC=payment_service prompt="Documentar el servicio de pagos legacy, identificar flujos, dependencias y riesgos"
```

Claude Code lee los ficheros directamente del filesystem, ejecuta el skill y escribe el artefacto.

### 5.1 MCP-first para comandos `@aecf` en Claude Code

Si Claude Code tiene registrado `aecf_prompts/mcp/claude/aecf-mcp.exe`, pide los comandos con una formulación que fuerce el uso del tool MCP cuando exista.

Ejemplos recomendados:

```text
Usa el tool MCP `aecf_list_commands` para resolver `@aecf list commands`. Usa `aecf_show_commands` para resolver `@aecf show commands`. Si el tool MCP no está disponible, cae al router manual de `aecf_prompts`.

Usa el tool MCP `aecf_list_skills` para resolver `@aecf list skills`. Si falla, usa el fallback manual.

Usa el tool MCP `aecf_context_examine` para resolver `@aecf context examine`.
```

Regla operativa:

1. `@aecf list commands` debe resolverse con `aecf_list_commands` cuando el MCP esté conectado.
2. `@aecf show commands` debe resolverse con `aecf_show_commands` cuando el MCP esté conectado.
3. Claude no debe tratar `aecf_list_commands` ni `aecf_show_commands` como nombres de archivo ni como texto a buscar en el repo cuando el tool MCP exista.
4. Si el tool MCP falla o no está disponible, Claude debe decir que entra en fallback manual y resolver el comando desde `aecf_prompts`.

### Opción B: Modo pipe (un solo comando)

```bash
cd mi-proyecto

# Construir el prompt completo y enviarlo
claude -p "$(cat aecf_prompts/skills/skill_document_legacy.md)

TOPIC=payment_service
prompt=Documentar el servicio de pagos legacy, identificar flujos, dependencias y riesgos

Contexto del proyecto:
$(cat AECF_PROJECT_CONTEXT.md)

Knowledge pack del dominio:
$(cat aecf_prompts/knowledge/java/pack.md 2>/dev/null || echo 'No domain pack available')

Código a documentar:
--- src/main/java/com/empresa/payments/PaymentService.java ---
$(cat src/main/java/com/empresa/payments/PaymentService.java)

--- src/main/java/com/empresa/payments/PaymentValidator.java ---
$(cat src/main/java/com/empresa/payments/PaymentValidator.java)

--- src/main/java/com/empresa/payments/PaymentRepository.java ---
$(cat src/main/java/com/empresa/payments/PaymentRepository.java)
" | tee .aecf/runtime/documentation/<user_id>/payment_service/AECF_01_DOCUMENT_LEGACY.md
```

### Opción C: Script reutilizable

Guardar como `aecf_prompts/run_skill.sh`:

```bash
#!/bin/bash
# Uso: ./aecf_prompts/run_skill.sh <skill> <topic> "<prompt>" <archivo1> [archivo2] ...
set -euo pipefail

SKILL=$1; TOPIC=$2; PROMPT=$3; shift 3
BUNDLE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOCS_ROOT="${AECF_PROMPTS_DOCUMENTATION_PATH:-${AECF_PROMPTS_DIRECTORY_PATH:-$BUNDLE_ROOT/.aecf/runtime/documentation}}"
USER_ID="${AECF_PROMPTS_USER_ID:-${ANTHROPIC_MODEL:-}}"
if [ -z "$USER_ID" ]; then
  echo "AECF_PROMPTS_USER_ID must be defined for stable user-scoped artifacts. Claude Code does not expose a reusable authenticated user_id env var." >&2
  exit 1
fi
TOPIC_DIR="$DOCS_ROOT/$USER_ID/$TOPIC"

# Construir bloque de código fuente
CODE_BLOCK=""
for f in "$@"; do
  CODE_BLOCK="$CODE_BLOCK
--- $f ---
$(cat "$f")"
done

# Construir bloque de knowledge pack
KNOWLEDGE=""
if [ -f "aecf_prompts/knowledge/java/pack.md" ]; then
  KNOWLEDGE="
Knowledge pack del dominio:
$(cat aecf_prompts/knowledge/java/pack.md)"
fi

# Crear directorio de salida
mkdir -p "$TOPIC_DIR"

# Ejecutar
claude -p "$(cat "aecf_prompts/skills/skill_${SKILL}.md")

TOPIC=$TOPIC
prompt=$PROMPT

Contexto del proyecto:
$(cat AECF_PROJECT_CONTEXT.md)
$KNOWLEDGE

Código a documentar:
$CODE_BLOCK
" | tee "$TOPIC_DIR/AECF_01_DOCUMENT_LEGACY.md"

echo ""
echo "✅ Artefacto: $TOPIC_DIR/AECF_01_DOCUMENT_LEGACY.md"
```

Uso:

```bash
chmod +x aecf_prompts/run_skill.sh

./aecf_prompts/run_skill.sh document_legacy payment_service \
  "Documentar el servicio de pagos, flujos, dependencias y riesgos" \
  src/main/java/com/empresa/payments/PaymentService.java \
  src/main/java/com/empresa/payments/PaymentValidator.java \
  src/main/java/com/empresa/payments/PaymentRepository.java
```

---

## 6. Ejecutar skills multi-fase (new_feature, refactor, etc.)

Los skills TIER 3 tienen múltiples fases. Se ejecutan secuencialmente:

Si prefieres mantener sintaxis `@aecf`, la invocación equivalente del ejemplo sería:

```text
@aecf run skill=new_feature TOPIC=user_auth prompt="Implementar autenticación JWT con refresh tokens"
```

Claude no ejecuta ese comando como runtime del componente: lo resuelve usando `AECF_PROMPT_ONLY_COMMANDS.md` y luego aplica las fases manuales igual que en esta guía.

```bash
TOPIC=user_auth
PROMPT="Implementar autenticación JWT con refresh tokens"

# Fase 1: PLAN
claude -p "use skill=new_feature TOPIC=$TOPIC prompt=$PROMPT

$(cat aecf_prompts/prompts/00_PLAN.md)

Contexto del proyecto:
$(cat AECF_PROJECT_CONTEXT.md)

$(cat aecf_prompts/knowledge/java/pack.md 2>/dev/null)
" > .aecf/runtime/documentation/$TOPIC/AECF_01_PLAN.md

# Fase 2: AUDIT_PLAN
claude -p "use skill=new_feature TOPIC=$TOPIC

$(cat aecf_prompts/prompts/02_AUDIT_PLAN.md)

Plan a auditar:
$(cat .aecf/runtime/documentation/$TOPIC/AECF_01_PLAN.md)

Checklist:
$(cat aecf_prompts/checklists/AUDIT_PLAN_CHECKLIST.md)

Scoring:
$(cat aecf_prompts/scoring/SCORING_MODEL.md)
" > .aecf/runtime/documentation/$TOPIC/AECF_02_AUDIT_PLAN.md

# Verificar veredicto
grep -i "GO\|NO-GO" .aecf/runtime/documentation/$TOPIC/AECF_02_AUDIT_PLAN.md

# Si GO → continuar con TEST_STRATEGY, IMPLEMENT, AUDIT_CODE, VERSION
# Si NO-GO → ejecutar FIX_PLAN (03_FIX_PLAN.md) y repetir AUDIT
```

---

## 7. Knowledge Packs: cómo funcionan con aecf_prompts

### Qué son

Knowledge packs son ficheros Markdown con reglas específicas de un dominio/tecnología que se inyectan en el prompt para que el LLM genere output adaptado al stack real del proyecto.

### Fuente canónica en este repo

Dentro de `AECF_MCP`, la fuente canónica no es `aecf_prompts/knowledge/`.

La fuente canónica está en:

- `aecf_prompts/knowledge/domains/<domain>/pack.md`
- `aecf_prompts/knowledge/domains/<domain>/semantic_profiles/<profile>.md`

`aecf_prompts/knowledge/` es una copia o distribución local para uso prompt-only, no la fuente maestra.

### Estructura

```
aecf_prompts/
└── knowledge/
    └── <dominio>/
        ├── pack.md                    ← reglas base del dominio
        └── semantic_profiles/
            ├── spring_boot_service.md ← perfil específico Spring Boot
            ├── jpa_persistence.md     ← perfil específico JPA
            └── ...
```

### Cómo crear los knowledge packs iniciales

Copiar desde el repositorio AECF_MCP:

```bash
# Copiar el dominio Java (ya incluye Spring Boot, ZKoss, JPA, AWS, Azure)
mkdir -p aecf_prompts/knowledge
cp -r /ruta/a/AECF_MCP/aecf_prompts/knowledge/domains/java aecf_prompts/knowledge/java
```

Ejemplo concreto si quieres usar ZKoss en modo prompt-only:

```bash
cp /ruta/a/AECF_MCP/aecf_prompts/knowledge/domains/java/pack.md aecf_prompts/knowledge/java/pack.md
cp /ruta/a/AECF_MCP/aecf_prompts/knowledge/domains/java/semantic_profiles/zkoss.md aecf_prompts/knowledge/java/semantic_profiles/zkoss.md
```

O crear uno propio desde cero:

```bash
mkdir -p aecf_prompts/knowledge/java/semantic_profiles
```

**`aecf_prompts/knowledge/java/pack.md`** — reglas base:

```markdown
# Java Domain Pack

## Code Generation Rules
- Respetar el build tool existente: Maven → Maven, Gradle → Gradle.
- Mantener package names alineados con el source tree existente.
- Preferir constructor injection e interfaces explícitas cuando el codebase ya usa DI.
- Mantener lógica de negocio fuera de controllers y DTOs de transporte.

## Testing Rules
- Preferir JUnit 5. Integration tests solo donde importa wiring o persistencia.
- Test doubles locales y obvios; evitar reflection-heavy test setups.
- Validar paths de éxito Y contratos de fallo (excepciones, validación).

## Build And Runtime Rules
- Reutilizar la versión de Java y convenciones de plugins del pom.xml/build.gradle.
- No introducir migraciones de framework como parte de trabajo no relacionado.

## Common Pitfalls
- Evitar estado mutable estático.
- No mezclar versiones incompatibles de dependencias entre módulos.
- No tratar package-private como sustituto de API boundaries claros.
```

**`aecf_prompts/knowledge/java/semantic_profiles/spring_boot_service.md`** — profile específico:

```markdown
# Spring Boot Service Profile

## Architecture Rules
- Separar controllers, application services, domain logic e infrastructure.
- Constructor injection y configuración explícita sobre magia del framework.
- Configuración externalizada y endpoints de health/metrics intencionales.

## Design Patterns
- Usar DTOs separados para request/response, no exponer entidades JPA en controllers.
- Mapeo entre capas explícito (MapStruct o manual), no auto-magia.

## Testing Rules
- @SpringBootTest solo para integration tests que necesiten contexto completo.
- @WebMvcTest para controller tests aislados.
- @DataJpaTest para repository tests.
- Mockar servicios externos con WireMock, no con mocks frágiles.

## Security Rules
- Configurar Spring Security explícitamente, no confiar en defaults.
- Validar input con @Valid + Bean Validation en DTOs de entrada.
- No loggear tokens, passwords ni PII.

## Deployment Rules
- Actuator endpoints protegidos en producción.
- Profiles separados para dev/staging/prod.
- Health checks que reflejen dependencias reales (DB, colas, APIs externas).
```

**`aecf_prompts/knowledge/java/semantic_profiles/zkoss.md`** — profile específico ZKoss:

```markdown
# ZKoss Server-Driven UI

## ARCHITECTURE RULES
- Mantener ZUL centrado en presentación y mover los casos de uso a servicios de aplicación.
- Hacer explícito el uso de session, desktop y execution scope.

## CODING RULES
- No poner reglas de negocio en expresiones ZUL ni en handlers de eventos UI.
- Mantener composers o view models finos y trazables.

## TESTING RULES
- Cubrir flows críticos de eventos, validación y autorización.
- Verificar el reinicio correcto del estado de desktop o session.
```

### Cómo se usan en la ejecución

Se concatenan al prompt. En el script `run_skill.sh` (sección 5.C) ya está integrado. Manualmente:

```bash
claude -p "$(cat aecf_prompts/skills/skill_document_legacy.md)

TOPIC=payment_service
prompt=Documentar el servicio de pagos

Contexto del proyecto:
$(cat AECF_PROJECT_CONTEXT.md)

Reglas del dominio Java:
$(cat aecf_prompts/knowledge/java/pack.md)

Reglas específicas Spring Boot:
$(cat aecf_prompts/knowledge/java/semantic_profiles/spring_boot_service.md)

Código a documentar:
$(cat src/main/java/com/empresa/payments/PaymentService.java)
"
```

Ejemplo equivalente para ZKoss:

```bash
claude -p "$(cat aecf_prompts/skills/skill_new_feature.md)

TOPIC=zk_customer_search
prompt=Implementar una pantalla ZKoss para búsqueda de clientes

Contexto del proyecto:
$(cat AECF_PROJECT_CONTEXT.md)

Reglas del dominio Java:
$(cat aecf_prompts/knowledge/java/pack.md)

Reglas específicas ZKoss:
$(cat aecf_prompts/knowledge/java/semantic_profiles/zkoss.md)

Código relevante:
$(cat src/main/java/com/empresa/ui/CustomerComposer.java)
"
```

### Regla de sincronización

Si copias estos knowledge packs dentro de este repo a otra ruta para consumo prompt-only, debes mantenerlos sincronizados con la fuente canónica.

En `AECF_MCP`, la regla obligatoria es:

1. `aecf_prompts/knowledge/` sigue siendo la fuente canónica.
2. `aecf_prompts/knowledge/` debe mantenerse sincronizado con esa fuente.
3. Cualquier copia adicional para `aecf_prompts`, `aecf_prompts` o bundles de cliente debe mantenerse alineada para evitar deriva.

### Crear knowledge packs propios del cliente

Para reglas específicas de la empresa que no son genéricas de Java/Spring:

**`aecf_prompts/knowledge/empresa/pack.md`**:

```markdown
# Reglas Específicas de la Empresa

## Naming Conventions
- Services: <Entity>Service (e.g., PaymentService, InvoiceService)
- Repositories: <Entity>Repository (JPA Spring Data)
- DTOs: <Entity>Request, <Entity>Response
- Tests: <Entity>ServiceTest, <Entity>ControllerIT

## Architecture Mandatory Rules
- Toda comunicación entre microservicios pasa por Kafka (nunca REST directo)
- Logs en formato JSON estructurado (Logback + logstash-encoder)
- Toda entidad JPA tiene campo auditoria (createdAt, updatedAt, createdBy)

## GitLab CI Rules
- Merge requests requieren 2 approvals
- Pipeline debe pasar: build → test → sonar → deploy staging
- No se merges con coverage < 80%
```

Uso:

```bash
claude -p "...
$(cat aecf_prompts/knowledge/java/pack.md)
$(cat aecf_prompts/knowledge/java/semantic_profiles/spring_boot_service.md)
$(cat aecf_prompts/knowledge/empresa/pack.md)
..."
```

---

## 8. Artefactos generados

Después de ejecutar un skill, los artefactos quedan en:

```
.aecf/runtime/documentation/
└── payment_service/
    └── AECF_DOCUMENT_LEGACY.md    ← documentación completa
```

Para skills multi-fase (`new_feature`):

```
.aecf/runtime/documentation/
└── user_auth/
    ├── AECF_01_PLAN.md
    ├── AECF_02_AUDIT_PLAN.md
    ├── AECF_04_TEST_STRATEGY.md
    ├── AECF_05_IMPLEMENT.md
    ├── AECF_06_AUDIT_CODE.md
    └── AECF_08_VERSION.md
```

Estos ficheros se commitean en GitLab junto al código para trazabilidad completa.

---

## 9. Tips para Claude CLI

- **Claude Code (interactivo)** es la mejor opción para explorar proyectos grandes: tiene acceso al filesystem y puede navegar el código por sí mismo.
- **`claude -p`** (pipe) es ideal para scripting y automatización.
- Para proyectos con muchos archivos, usa Claude Code y deja que él explore en vez de concatenar todo en el prompt.
- Si el output se trunca, pide "continúa desde la sección X" en una segunda invocación.
- Usa `--model <configured-model>` solo si necesitas fijar explícitamente el modelo activo; si no, usa el valor por defecto configurado en tu entorno.

---

## 10. Referencia rápida de skills disponibles

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
