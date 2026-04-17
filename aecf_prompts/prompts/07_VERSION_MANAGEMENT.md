# AECF — VERSION MANAGEMENT

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 07_VERSION_MANAGEMENT |

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

📌 TOPIC: Maintain {{TOPIC}} from previous phase. All outputs in: documentation/{{TOPIC}}/

Act as Release Engineer y Version Manager.

This prompt is subject to audit.
Failure to follow the flow invalidates the response.

---

## CONTEXTO

Trabajas sobre code que ha pasado AUDIT-CODE with GO verdict.

Esta fase se ejecuta DESPUES de AUDIT-CODE y ANTES de deployment a production.

Tu tarea es:
- Determinar el tipo de cambio segun Semantic Versioning
- Actualizar la version en todos los files relevantes
- Generar entrada en CHANGELOG
- Preparar tag de Git

---

## SEMANTIC VERSIONING (SemVer)

Formato: `MAJOR.MINOR.PATCH` (ejemplo: `1.4.2`)

### Reglas de incremento

**MAJOR** (incrementa X.0.0):
- Cambios incompatibles en la API
- Breaking changes
- Reestructuraciones que rompen compatibilidad
- Ejemplos:
  - Eliminar endpoints publicos
  - Cambiar firma de funciones publicas
  - Modificar estructura de respuestas JSON
  - Cambiar comportamiento esperado de APIs

**MINOR** (incrementa 0.X.0):
- Funcionalidad nueva compatible hacia atras
- Anadir endpoints, metodos o features
- Mejoras que no rompen compatibilidad
- Ejemplos:
  - Anadir nuevo endpoint
  - Anadir parametro opcional
  - Nueva feature sin afectar existentes

**PATCH** (incrementa 0.0.X):
- Correcciones de bugs compatibles hacia atras
- Fixes de seguridad
- Mejoras de rendimiento sin cambiar API
- Ejemplos:
  - Corregir bug en validation
  - Fix de seguridad
  - Optimizacion interna

### Versiones especiales

**Pre-release**: `1.2.3-alpha.1`, `1.2.3-beta.2`, `1.2.3-rc.1`
- alpha: desarrollo interno, no estable
- beta: testing externo, relativamente estable
- rc (release candidate): casi listo para production

**Build metadata**: `1.2.3+20260205` (opcional)

---

## REGLAS ESTRICTAS

- NO incrementes version sin justificacion clara
- NO uses versiones arbitrarias
- NO modifiques CHANGELOG de versiones anteriores
- NO hagas commit sin tag correspondiente
- Si hay duda sobre el tipo de incremento, pregunta

---

## INPUTS REQUERIDOS

Debes recibir:
1. Description del cambio implementado
2. Output del PLAN que genero el cambio
3. Verdict GO de AUDIT-CODE
4. Version actual del proyecto

## INPUT / OUTPUT CONTRACT (MANDATORY)

Input artifacts expected:
- documentation/{{TOPIC}}/AECF_<NN_prev>_PLAN.md (o PLAN_LEGACY equivalente)
- documentation/{{TOPIC}}/AECF_<NN_prev>_AUDIT_CODE.md with GO verdict

Output artifact mandatory for traceability:
- documentation/{{TOPIC}}/AECF_<NN>_VERSION.md

The VERSION artifact must include:
- Referenced input artifacts
- SemVer decision path (why MAJOR/MINOR/PATCH)
- Updated files summary

---

## PROCESO DE VERSIONADO

### 1. Analisis del cambio

Revisa el PLAN y el code implementado para determinar:
- Rompe compatibilidad? → MAJOR
- Anade funcionalidad nueva? → MINOR
- Corrige bugs sin anadir features? → PATCH

### 2. Files a actualizar

Actualiza la version en **todos** los files aplicables:

**Python**:
- `pyproject.toml` → `[tool.poetry]` section `version = "X.Y.Z"`
- `setup.py` → `version="X.Y.Z"`
- `src/__init__.py` o similar → `__version__ = "X.Y.Z"`
- `VERSION` o `version.txt` (si existe)

**Node.js / JavaScript**:
- `package.json` → `"version": "X.Y.Z"`
- `package-lock.json` → actualizado automaticamente

**Otros lenguajes**:
- Java: `pom.xml` o `build.gradle`
- .NET: `.csproj` files
- Rust: `Cargo.toml`
- Go: usar tags de Git directamente

### 3. Actualizar CHANGELOG.md

Formato obligatorio (Keep a Changelog):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [X.Y.Z] - YYYY-MM-DD

### Added
- Nueva funcionalidad 1
- Nueva funcionalidad 2

### Changed
- Cambio en funcionalidad existente

### Deprecated
- Funcionalidad marcada para eliminacion futura

### Removed
- Funcionalidad eliminada

### Fixed
- Bug corregido 1
- Bug corregido 2

### Security
- Vulnerabilidad corregida

## [Version anterior] - YYYY-MM-DD
...
```

**Reglas para CHANGELOG**:
- Solo incluir cambios relevantes para usuarios
- No incluir detalles internos de implementacion
- Usar lenguaje claro y conciso
- Agrupar por tipo de cambio (Added, Changed, Fixed, etc.)
- Incluir referencias a issues/PRs si aplica

### 4. Generar comandos Git

Proporciona los comandos exactos para:

```bash
# 1. Hacer commit de cambios de version
git add [files modificados]
git commit -m "chore: bump version to X.Y.Z"

# 2. Crear tag anotado
git tag -a vX.Y.Z -m "Release version X.Y.Z"

# 3. Push con tags
git push origin main --tags

# O crear release con GitHub CLI
gh release create vX.Y.Z --title "Release X.Y.Z" --notes "[CHANGELOG_CONTENT]"
```

---

## FORMATO DE OUTPUT OBLIGATORIO

```markdown
## VERSION MANAGEMENT REPORT

### Version anterior
X.Y.Z

### Nueva version
X.Y.Z

### Tipo de cambio
[MAJOR | MINOR | PATCH]

### Justificacion
[Explicacion de por que este tipo de incremento]

---

## Files modificados

### pyproject.toml
```toml
[tool.poetry]
name = "project-name"
version = "X.Y.Z"
```

### src/__init__.py
```python
__version__ = "X.Y.Z"
```

### CHANGELOG.md
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Nueva funcionalidad X

### Fixed
- Correccion de bug Y
```

---

## Comandos Git

```bash
# Commit de versionado
git add pyproject.toml src/__init__.py CHANGELOG.md
git commit -m "chore: bump version to X.Y.Z"

# Tag
git tag -a vX.Y.Z -m "Release version X.Y.Z

- Nueva funcionalidad X
- Correccion de bug Y"

# Push
git push origin main --tags
```

O usando GitHub CLI:

```bash
gh release create vX.Y.Z \
  --title "Release X.Y.Z" \
  --notes "## Changes

- Nueva funcionalidad X
- Correccion de bug Y

See full CHANGELOG at [link]"
```

---

## Verificacion

Para verificar que --version funcione:

**Python**:
```bash
python -m nombre_proyecto --version
# O
python -c "import nombre_proyecto; print(nombre_proyecto.__version__)"
```

**Node.js**:
```bash
npm version
# O
node -e "console.log(require('./package.json').version)"
```

---

## AECF_COMPLIANCE_REPORT

1. Files seguidos:
   - AECF_PROJECT_CONTEXT.md: APLICADO
   - 07_VERSION_MANAGEMENT.md: APLICADO

2. Flow AECF: COMPLETO (post AUDIT-CODE GO)

3. Version incrementada segun: [MAJOR | MINOR | PATCH]
```

───────────────────────────────
📁 OUTPUT GENERATION (MANDATORY)
───────────────────────────────

Generate document:
documentation/{{TOPIC}}/AECF_<NN>_VERSION.md

Where:
- {{TOPIC}} = topic maintained from previous phases
- <NN> = next sequential number (01, 02, 03...)

---

FINALIZA CON EXACTAMENTE:
VERSION MANAGEMENT COMPLETADO

---

## EJEMPLOS

### Ejemplo 1: Nueva funcionalidad (MINOR)

```
Input:
- PLAN: Anadir exportacion a CSV
- Version actual: 1.2.3

Analisis:
- No rompe compatibilidad ✓
- Anade nueva funcionalidad ✓
- No es solo un fix ✓

Decision: MINOR (1.2.3 → 1.3.0)

CHANGELOG:
## [1.3.0] - 2026-02-05
### Added
- Exportacion de usuarios a formato CSV
- Endpoint GET /api/users/export con soporte de paginacion
```

### Ejemplo 2: Correccion de bug (PATCH)

```
Input:
- PLAN: Corregir validation de email
- Version actual: 2.1.4

Analisis:
- No rompe compatibilidad ✓
- No anade funcionalidad nueva ✓
- Corrige bug existente ✓

Decision: PATCH (2.1.4 → 2.1.5)

CHANGELOG:
## [2.1.5] - 2026-02-05
### Fixed
- Validation de email ahora acepta dominios con multiples puntos
- Corregido error 500 en validation de caracteres especiales
```

### Ejemplo 3: Breaking change (MAJOR)

```
Input:
- PLAN: Cambiar estructura de respuesta de API de autenticacion
- Version actual: 1.8.2

Analisis:
- Rompe compatibilidad con clientes existentes ✗
- Requiere cambios en consumidores de API ✗

Decision: MAJOR (1.8.2 → 2.0.0)

CHANGELOG:
## [2.0.0] - 2026-02-05
### Changed
- **BREAKING**: Estructura de respuesta en /api/auth/login ahora incluye refresh_token como campo separado
- **BREAKING**: Campo `user_data` renombrado a `user` en respuestas de autenticacion

### Migration Guide
Los clientes deben actualizar:
- Antes: `response.user_data.id`
- Ahora: `response.user.id`
```

---

## NOTAS IMPORTANTES

1. **Primera version publica**: Empieza en `3.0.0`
2. **Desarrollo pre-release**: Usa `0.x.y` donde `x` incrementa con features
3. **Version 0.y.z**: No hay garantia de estabilidad
4. **Una vez en 3.0.0+**: Seguir SemVer estrictamente

---

------------------------------------------------------------

## CONTEXT VALIDATION

Confirm:

[ ] AECF_SYSTEM_CONTEXT.md loaded
[ ] Workspace AECF_PROJECT_CONTEXT.md checked (if present)
[ ] Governance rules applied

If confirmation cannot be provided → STOP execution.

------------------------------------------------------------

## VALIDATION FINAL

Antes de finalizar, verifica:
- [ ] Version incrementada correctamente segun tipo de cambio
- [ ] Todos los files de version actualizados consistentemente
- [ ] CHANGELOG.md actualizado con formato correcto
- [ ] Comandos Git proporcionados y correctos
- [ ] Comando --version funciona correctamente
- [ ] Tag sigue formato vX.Y.Z
- [ ] No hay versiones inconsistentes en el proyecto

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
