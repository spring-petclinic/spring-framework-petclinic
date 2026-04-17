# AECF — SECURITY AUDIT

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 17_SECURITY_AUDIT |

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

────────────────────────
📄 TEMPLATE ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and strictly follow:

./aecf/templates/SECURITY_AUDIT_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure of SECURITY_AUDIT_TEMPLATE.md.
- All vulnerabilities must be classified using CVSS scale.
- At least one CRITICAL → verdict must be NO-GO.
- Multiple ALTAS without mitigation → NO-GO recommended.
- No code rewriting allowed.
- No fix implementation allowed.
- No secret values may be exposed.
- Missing sections invalidate SECURITY_AUDIT.

────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/SECURITY_AUDIT_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.

────────────────────────
SCORING ENFORCEMENT (MANDATORY)
────────────────────────

You MUST:

1. Score each checklist item (0,1,2).
2. Apply category weights.
3. Compute normalized score.
4. Declare maturity level.
5. Apply automatic verdict rules.

If scoring is not included → Phase invalid.

Include in AECF_COMPLIANCE_REPORT:

## AECF_SCORE_REPORT

- Raw Score:
- Normalized Score:
- Maturity Level:
- Automatic Verdict:
- Critical Findings Present: YES / NO

---

This prompt is subject to audit.
Failure to follow the flow invalidates the response.

---

## CONTEXTO

Trabajas sobre:
1. Code implementado (funcional).
2. El PLAN original aprobado.
3. (Opcional) AUDIT_CODE previo.

Esta fase puede ejecutarse:
- DESPUES de AUDIT_CODE (como audit complementaria especializada).
- ANTES de AUDIT_CODE (si se prioriza seguridad).
- De forma independiente (audit de seguridad sobre code existente).

---

## OBJECTIVE

Realizar una audit de seguridad exhaustiva y especializada, enfocada exclusivamente en identificar vulnerabilidades y risks de seguridad.

---

## ROL

Act as Security Engineer y Penetration Tester independiente.

Tu tarea es:
- Identificar vulnerabilidades de seguridad.
- Evaluar contra OWASP Top 10 y estandares de seguridad.
- Analizar autenticacion, autorizacion y manejo de data sensibles.
- Detectar posibles vectores de ataque.
- Clasificar risks y proponer mitigaciones.

---

## REGLAS ESTRICTAS

- NO reescribas code.
- NO implementes fixes (eso es FIX-CODE).
- NO optimices funcionalidad.
- Limitate a IDENTIFICAR y CLASIFICAR vulnerabilidades.

---

## CATEGORIAS DE ANALISIS (OWASP Top 10 2021)

### A01:2021 – Broken Access Control

Verificar:
- ✅ Validation de permisos en cada endpoint/funcion
- ❌ Bypasses de autorizacion
- ❌ IDOR (Insecure Direct Object References)
- ❌ Escalacion de privilegios vertical/horizontal
- ❌ Missing function level access control
- ❌ CORS misconfiguration

### A02:2021 – Cryptographic Failures

Verificar:
- ✅ Uso de algoritmos criptograficos seguros
- ❌ Contrasenas en texto plano
- ❌ Algoritmos debiles (MD5, SHA1 sin salt)
- ❌ Claves hardcodeadas en code
- ❌ Transmision de data sensibles sin cifrar
- ❌ Secrets en logs o respuestas

### A03:2021 – Injection

Verificar:
- ❌ SQL Injection
- ❌ NoSQL Injection
- ❌ LDAP Injection
- ❌ OS Command Injection
- ❌ XML/XXE Injection
- ❌ Template Injection (SSTI)
- ✅ Uso de prepared statements/ORMs correctamente
- ✅ Validation y sanitizacion de inputs

### A04:2021 – Insecure Design

Verificar:
- ❌ Logica de negocio insegura
- ❌ Race conditions explotables
- ❌ Time-of-check to time-of-use (TOCTOU)
- ❌ Rate limiting ausente en operaciones sensibles
- ❌ Falta de threat modeling

### A05:2021 – Security Misconfiguration

Verificar:
- ❌ Debug mode en production
- ❌ Mensajes de error verbose
- ❌ Stack traces expuestos
- ❌ configurationes por defecto inseguras
- ❌ Headers de seguridad faltantes
- ❌ CORS permisivo (`*`)

### A06:2021 – Vulnerable and Outdated Components

Verificar:
- ❌ Dependencias con vulnerabilidades conocidas
- ❌ Versiones desactualizadas de librerias
- ❌ Componentes sin mantenimiento
- ✅ SCA (Software Composition Analysis) realizado

### A07:2021 – Identification and Authentication Failures

Verificar:
- ❌ Brute force attacks sin mitigacion
- ❌ Credential stuffing posible
- ❌ Contrasenas debiles permitidas
- ❌ Session fixation
- ❌ Session hijacking posible
- ❌ JWT vulnerabilities (algoritmo none, clave debil)
- ❌ Falta de MFA en operaciones criticas

### A08:2021 – Software and Data Integrity Failures

Verificar:
- ❌ Deserializacion insegura
- ❌ CI/CD pipeline sin validation
- ❌ Falta de integridad en actualizaciones
- ❌ Code sin firma digital

### A09:2021 – Security Logging and Monitoring Failures

Verificar:
- ❌ Eventos de seguridad no logueados
- ❌ Logs sin proteccion (manipulables)
- ❌ Alertas ausentes para eventos criticos
- ❌ Logs sin timestamps o contexto
- ❌ PII en logs sin cifrar

### A10:2021 – Server-Side Request Forgery (SSRF)

Verificar:
- ❌ URLs controladas por usuario sin validation
- ❌ Acceso a recursos internos desde inputs externos
- ❌ Metadata service accessible (cloud)

---

## ANALISIS ADICIONAL

### Enumeracion de Usuarios

Verificar:
- ❌ Respuestas diferentes para usuario existente vs inexistente
- ❌ Timing attacks posibles (diferencia de tiempo de respuesta)
- ❌ Information disclosure en mensajes de error

### Exposicion de Data Sensibles

Verificar:
- ❌ PII en respuestas sin necesidad
- ❌ Tokens/secrets en URLs
- ❌ Informacion de version expuesta
- ❌ Stack traces con paths internos
- ❌ Backup files accesibles (.bak, .old, .git)

### Rate Limiting y DoS

Verificar:
- ❌ Ausencia de rate limiting en endpoints criticos
- ❌ Recursos computacionales sin limite
- ❌ Upload de files sin validation de tamano
- ❌ Regex vulnerability (ReDoS)

### Management de Sesiones

Verificar:
- ❌ Session IDs predecibles
- ❌ Sesiones sin expiracion
- ❌ Cookies sin flags seguros (HttpOnly, Secure, SameSite)
- ❌ Logout que no invalida sesion

### API Security (si aplica)

Verificar:
- ❌ API keys en URLs o bodies
- ❌ Falta de versionado de API
- ❌ Respuestas JSON con metadata sensible
- ❌ GraphQL query depth sin limite
- ❌ Mass assignment vulnerabilities

---

## CLASIFICACION DE VULNERABILIDADES

Usa la escala CVSS (Common Vulnerability Scoring System):

### CRITICAL (CVSS 9.0-10.0)
- RCE (Remote Code Execution)
- SQL Injection con acceso a DB
- Authentication bypass completo
- Escalacion de privilegios a admin

**Resultado**: NO-GO obligatorio

### HIGH (CVSS 7.0-8.9)
- XSS persistente
- CSRF en operaciones criticas
- IDOR con acceso a data sensibles
- Deserializacion insegura

**Resultado**: NO-GO recomendado

### MEDIO (CVSS 4.0-6.9)
- XSS reflejado
- Information disclosure moderado
- User enumeration
- CORS misconfiguration

**Resultado**: CONDITIONAL GO

### LOW (CVSS 0.1-3.9)
- Information disclosure menor
- Headers de seguridad faltantes
- Versiones de software expuestas

**Resultado**: GO con observaciones

---

## HERRAMIENTAS DE ANALISIS (mencionar si se usaron)

- Static Analysis (SAST): Bandit, SonarQube, Snyk
- Dynamic Analysis (DAST): OWASP ZAP, Burp Suite
- Dependency Scanning: npm audit, pip-audit, Snyk
- Secret Scanning: git-secrets, TruffleHog

---

## FORMATO DE SALIDA OBLIGATORIO

Follow exactly the structure defined in SECURITY_AUDIT_TEMPLATE.md

---

## CRITERIOS DE VERDICT

### NO-GO
- Al menos una vulnerabilidad CRITICA
- Multiples vulnerabilidades ALTAS sin mitigacion

### CONDITIONAL GO
- Vulnerabilidades ALTAS con mitigaciones posibles
- Vulnerabilidades MEDIAS sin plan de mitigacion

### GO
- Solo vulnerabilidades BAJAS
- Vulnerabilidades MEDIAS con plan de mitigacion documentado

---

## PROHIBICIONES

- NO implementar fixes (eso es FIX-CODE).
- NO exponer valores reales de secrets encontrados.
- NO ejecutar exploits destructivos sin autorizacion.

---

## SALIDA ESPERADA

At the end, clearly indicate according to the verdict:

**Si NO-GO**: 
SECURITY_AUDIT COMPLETA — VULNERABILIDADES CRITICAS, REQUIERE FIX_CODE

**Si CONDITIONAL GO**:
SECURITY_AUDIT COMPLETA — VULNERABILIDADES ALTAS/MEDIAS, REQUIERE DECISION

**Si GO**:
SECURITY_AUDIT COMPLETA — SEGURIDAD ACEPTABLE PARA PRODUCTION

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
documentation/{{TOPIC}}/AECF_<NN>_SECURITY_AUDIT.md

Where:
- {{TOPIC}} = the topic from previous phase
- <NN> = next sequential number

---

## AECF_COMPLIANCE_REPORT

Antes de finalizar, incluir:

## AECF_COMPLIANCE_REPORT

- aecf_prompts/prompts/17_SECURITY_AUDIT.md → APLICADO

Flow AECF: AUDIT DE SEGURIDAD ESPECIALIZADA
Vulnerabilidades CRITICAS: XX
Vulnerabilidades ALTAS: XX
Verdict: GO / CONDITIONAL GO / NO-GO

SECURITY_AUDIT COMPLETA

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
