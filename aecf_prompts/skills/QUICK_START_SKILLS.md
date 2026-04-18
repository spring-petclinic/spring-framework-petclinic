# 🚀 AECF Skills – Quick Execution Guide

## 📖 What are AECF Skills?

The **AECF Skills** are commands that execute complete sequences of AECF prompts automatically, handling GO/NO-GO loops and generating all the necessary documentation.

Instead of running manually:
```
1. Run 00_PLAN.md
2. Revisar output
3. Run 02_AUDIT_PLAN.md
4. If NO-GO, run 03_FIX_PLAN.md
5. Repeat until GO
6. Run 08_TEST_STRATEGY.md
... (15 more steps)
```

You simply invoke:
```
"Implement [feature]. Use skill: aecf_new_feature TOPIC: [name]"
```

And AI runs the entire flow automatically.

---

## 🎯 Skills Disponibles

| Skill | Use When | Weather | Matrix Auto-Apply |
|-------|------------|--------|:--:|
| `aecf_new_feature` | New functionality | 1.5-4h | — |
| `aecf_hotfix` | Falling production (P1/P2) | 1-3h | — |
| `aecf_document_legacy` | Document old code | 30min-2h | — |
| `aecf_security_review` | Audit security | 45min-6h | ✅ |
| `aecf_explain_behavior` | Explain system behavior | 15-60min | — |
| `aecf_code_standards_audit` | Audit code standards | 30min-4h | ✅ |
| `aecf_maturity_assessment` | Evaluar madurez AECF (L1-L5) | 1-3h | — |
| `aecf_refactor` | Refactor governed code | 2-6h | — |
| `aecf_tech_debt_assessment` | Evaluate technical data | 1-4h | ✅ |
| `aecf_release_readiness` | Validate release preparation | 30min-2h | — |
| `aecf_dependency_audit` | Audit dependencies/supply chain | 30min-2h | ✅ |
| `aecf_data_strategy` | Design ingestion/data strategy | 20min-3h | — |
| `aecf_system_replayability_adaptive` | Replay/traceability adaptivo a arquitectura | 1.5-6h | — |
| `aecf_executive_summary` | Generar executive summary consolidado por TOPIC | 5-30min | — |
| `aecf_project_context_generator` | Generar `AECF_PROJECT_CONTEXT.md` para el workspace | 5-15min | — |

> ✅ = Skill includes **Matrix Auto-Apply Protocol**: `ADD_RULE` decisions are automatically applied to the project severity matrix.
 
---

## 📝 Invocation Syntax

### Formato Simple (Recomendado):
```
skill: [skill_name]. TOPIC: [identifier]
```
  
### Format with Description:
```
[Job Description]. Use skill: [skill_name] TOPIC: [identifier]
```

### Structured Triad Format (enforced):
```
use skill [skill_name] TOPIC: [identifier] prompt: [task description]
```
   
Example:
```
use skill aecf_new_feature TOPIC: login prompt: una pantalla que simule login
```

When `skill` + `TOPIC` + `prompt` are present, execution MUST go through the selected skill flow.
Direct coding outside the skill flow is invalid behavior.

### Natural Format (also works):
```
"audit backend code standards"
"documents the payment module"
"explain why the endpoint returns 403"
```

### Components:
- **Description**: What you want to do (clear and specific) — OPTIONAL, it can be inferred
- **Skill**: One of the available skills
- **TOPIC**: Short identifier (< 20 chars, snake_case) — OPTIONAL, automatically inferred

> **NOTE**: Thanks to **SKILL_DISPATCHER**, you don't need verbose prompts.
> The system auto-resolves TOPIC, scope, numbering and AECF conventions.
> A prompt as simple as `skill: code_standards_audit` is sufficient.

---

## 🆕 Skill 1: aecf_new_feature

### When to Use
✅ Implement new functionality
✅ Add new endpoint/module
✅ Greenfield development
❌ Modify existing functionality
❌ Fix it urgently

### Syntax
```
"[Feature description]. Use skill: aecf_new_feature TOPIC: [name]"
```

### Example 1: New Export Endpoint
```
User: "I need to implement an endpoint /api/reports/export that allows
Export reports in PDF and CSV format with filters by date and user.
Must include permissions and pagination control.
Use skill: aecf_new_feature TOPIC: report_export"
```

**What the skill does**:
1. [00_PLAN] Generate implementation plan
2. [02_AUDIT_PLAN] Audit the plan → If NO-GO: loop [03_FIX_PLAN]
3. [08_TEST_STRATEGY] Define estrategia de testing
4. [04_IMPLEMENT] Implement code according to plan
5. [09_TEST_IMPLEMENTATION] Implementa tests
6. [10_AUDIT_TESTS] Audit tests → If NO-GO: correct tests
7. [05_AUDIT_CODE] Audit code → If NO-GO: loop [06_FIX_CODE]
8. [07_VERSION_MANAGEMENT] Update version (SemVer)

**Output generado**:
```
documentation/report_export/
├── AECF_01_PLAN.md
├── AECF_02_AUDIT_PLAN.md (there may be 03, 04... if there were NO-GOs and FIX_PLAN)
├── AECF_0X_TEST_STRATEGY.md
├── AECF_0Y_IMPLEMENT.md
├── AECF_0Z_TEST_IMPLEMENTATION.md
├── AECF_0A_AUDIT_TESTS.md
├── AECF_0B_AUDIT_CODE.md
└── AECF_0C_VERSION.md
```

**Note**: The numbers (X, Y, Z, A, B, C) are sequential according to the actual order of execution.
If there are NO-GO → FIX iterations, each phase uses the next available number.

**Resultado**: Feature completa, testeada (cobertura >= 80%), auditada, versionada

### Example 2: New Feature with NO-GO
```
User: "Implement push notification system.
Use skill: aecf_new_feature TOPIC: push_notifications"

--- AI ejecuta PLAN → AUDIT_PLAN → NO-GO ---

AI: "Audit detected ambiguity: It is not specified which platforms
(iOS/Android/Web). Running FIX_PLAN..."

--- AI ejecuta FIX_PLAN → AUDIT_PLAN → GO ---

AI: "Plan corrected and approved. Continuing with TEST_STRATEGY..."

[Skill continues until completed...]
```

---

## 🚨 Skill 2: aecf_hotfix

### When to Use
✅ Production completely down (P1)
✅ Critical vulnerability being exploited (P1)
✅ Degraded core functionality (P2)
❌ Bug con workaround  
❌ Performance improvements

### Syntax
```
"🚨 [Severity]: [Incident description]. Use skill: aecf_hotfix TOPIC: [name]"
```

### Example 1: API Crash (P1)
```
User: "🚨 Q1: API /auth/login returns 500. Users cannot log in.
Error en logs: 'Connection pool exhausted'. 
Use skill: aecf_hotfix TOPIC: prod_auth_500"
```

**Typical timeline**:
```
[10:15] Incident detection
        AI ejecuta triage → Confirma P1

[10:17] AI ejecuta DEBUG (RUNTIME mode)
→ Analyze production logs
→ ROOT CAUSE: DB pool size=10 exhausted due to traffic spike

[10:25] AI runs HOTFIX_PLAN
        → FIX: Aumentar pool 10 → 50
        → ROLLBACK: Revertir a 10
        → TESTS: test_pool_size, test_concurrent_logins

[10:35] AI ejecuta HOTFIX_AUDIT → GO

[10:40] AI ejecuta HOTFIX_IMPLEMENT
→ Modified code
→ Tests implemented and passing

[10:55] AI runs HOTFIX_VERIFY
→ Critical Tests: ✅
→ Bug reproduced → Solved: ✅
        → Smoke test staging: ✅

[11:00] AI executes DEPLOY
        → Tag: hotfix-20260210-1100-auth-pool-fix
→ Deploy to production
→ Active monitoring ON

[11:35] AI verifica MONITORING
        → Error rate: 0%
        → API responde 200
→ ✅ INCIDENT SOLVED

[Next day] AI ejecuta POST-MORTEM
→ Documented timeline
→ Solution: TEMPORARY (needs auto-scaling)
→ Action item: Create PLAN for definitive solution
```

**Output generado**:
```
documentation/prod_auth_500/
├── AECF_01_RCA.md (Root Cause Analysis)
└── AECF_01_HOTFIX.md (single document with all phases)
    ├── HOTFIX_PLAN
    ├── HOTFIX_AUDIT
    ├── HOTFIX_IMPLEMENTATION
    ├── HOTFIX_VERIFICATION
    ├── DEPLOYMENT
    └── POST-MORTEM
```

**Result**: Incident resolved in 1h 20min, complete traceability, documented post-mortem

### Example 2: Critical Vulnerability (P1)
```
User: "🚨 P1: SQL Injection detectada en /api/users por security researcher. 
Exploitable without authentication.
Use skill: aecf_hotfix TOPIC: sql_injection_fix"

--- AI prioritizes security fix ---

AI: "CRITICAL vulnerability confirmed. Running hotfix with highest priority..."

[Skill executes accelerated flow]
- HOTFIX_PLAN: Implementar prepared statements
- HOTFIX_AUDIT: Verify that the fix does not introduce new vulnerabilities
- HOTFIX_IMPLEMENT: Corrected code + security tests
- HOTFIX_VERIFY: Attempt exploit → Blocked ✅
- DEPLOY: Urgent deployment
- POST-MORTEM: Document how the vulnerability was introduced

✅ Vulnerability mitigated in 45 min
```

---

## 📚 Skill 3: aecf_document_legacy

### When to Use
✅ You need to modify legacy code without docs
✅ Audit existing functionality
✅ Onboarding of new equipment
❌ New code (should already be documented)

### Syntax
```
"Document [functionality/module]. Use skill: aecf_document_legacy TOPIC: [name]"
```

### Example 1: Documentation Only
```
User: "Document the payment module in app/payments/ for onboarding
of the new team. I'm not going to modify it.
Use skill: aecf_document_legacy TOPIC: payment_docs"
```

**What it does**:
1. [00_DOCUMENT_EXISTING_FUNCTIONALITY] Analyze code
   - Identifica entry points
- Trace flows (high-level + technical)
- Map dependencies
   - Identifica side effects
   - Lista unknowns

**Output**:
```
documentation/payment_docs/
├── AECF_01_DOCUMENTATION.md
├── AECF_01_FLOW_HIGHLEVEL.mmd (diagrama Mermaid)
└── AECF_01_FLOW_TECHNICAL.mmd (diagrama Mermaid)
```

**Result**: Complete documentation ready for the team

### Example 2: Documentation + Modification
```
User: "Document authentication module in app/auth/ because I'm going to
add support for MFA.
Use skill: aecf_document_legacy TOPIC: user_auth_mfa"
```

**What it does**:
1. [00_DOCUMENT_EXISTING_FUNCTIONALITY] Generate complete documentation
2. User reviews and confirms
3. [00_DISCOVERY_LEGACY] Delimits modification scope
4. Question: "Continue with implementation?"
5. If user says YES → Continue with `aecf_new_feature` flow

**Output**:
```
documentation/user_auth_mfa/
├── AECF_01_DOCUMENTATION.md (current code)
├── AECF_01_FLOW_HIGHLEVEL.mmd
├── AECF_01_FLOW_TECHNICAL.mmd
├── AECF_02_DISCOVERY.md (scope of changes)
└── [If you continue with PLAN...]
├── AECF_03_PLAN.md (modification plan)
    ├── ... (flujo normal de aecf_new_feature)
```

---

## 🔒 Skill 4: aecf_security_review

### When to Use
✅ Pre-deployment security check  
✅ Code that handles sensitive data
✅ After AUDIT_CODE if there are questions
✅ Compliance requirement (PCI-DSS, HIPAA)  
❌ Code in PLAN phase (very early)

### Syntax
```
"Security review of [code/module/endpoint]. Use skill: aecf_security_review TOPIC: [name]"
```

### Complete example: Payments API
```
User: "Security review of the /api/payments/ endpoint before deploying to production.
Use skill: aecf_security_review TOPIC: payment_api_security"
```

**Execution**:

**Phase 1: SECURITY_AUDIT**
```
AI: "Running OWASP Top 10 analysis..."

EXECUTIVE SUMMARY:
Total vulnerabilities: 5
CRITICAL: 1  [CRIT-001] SQL Injection
ALTAS: 2     [HIGH-001] Missing auth, [HIGH-002] Amount validation
MEDIAS: 1    [MED-001] Rate limiting
BAJAS: 1     [LOW-001] API version exposed

VERDICT: NO-GO (CRITICAL vulnerability detected)

Output: documentation/payment_api_security/AECF_01_SECURITY_AUDIT.md
```

**Phase 2: FIX_CRITICAL**
```
AI: "Fixing CRITICAL vulnerability [CRIT-001]..."

VULNERABLE CODE:
query = f"SELECT * FROM payments WHERE user_id = {user_id}"  # ❌ SQL Injection

CORRECTED CODE:
query = "SELECT * FROM payments WHERE user_id = ?"
cursor.execute(query, (user_id,))  # ✅ Prepared statement

ADDED TESTS:
def test_payment_history_sql_injection_blocked():
    malicious_input = "1 OR 1=1--"
    response = client.get(f'/api/payments?user_id={malicious_input}')
    assert response.status_code == 400
    assert "Invalid" in response.json['error']

✅ [CRIT-001] CORREGIDA

Output: documentation/payment_api_security/AECF_02_FIX_SECURITY_CRITICAL.md
```

**Phase 3: FIX_HIGH**
```
AI: "Fixing HIGH vulnerabilities..."

[HIGH-001] Missing authentication:
@app.route('/api/payments/stats')
@admin_required # ← ADDED
def get_payment_stats():
    ...

[HIGH-002] Amount validation:
# Validar amount server-side contra DB
expected_amount = Cart.query.get(cart_id).calculate_total()
if provided_amount != expected_amount:
    return error(400, 'Amount mismatch')

✅ [HIGH-001] CORREGIDA
✅ [HIGH-002] CORREGIDA

Output: documentation/payment_api_security/AECF_03_FIX_SECURITY_HIGH.md
```

**Phase 4: RISK DECISION**
```
AI: "How do you want to proceed with MEDIUM/LOW vulnerabilities?"

User: "MED-001 (rate limiting): postpones to next sprint with compensatory monitoring.
LOW-001 (version header): accept risk."
```

**Phase 5: RESIDUAL_RISKS**
```
AI: "Documenting residual risks..."

## Accepted Vulnerabilities

### [MED-001] Falta rate limiting
Severity: MEDIUM (CVSS 5.3)
Justification: Urgent deployment necessary
Compensatory measures:
- Alerts > 10 attempts/user/hour
- Active dashboard monitoring
Plan: Implement in sprint 2026-Q1-S3
Approved by: John Doe, 2026-02-10

### [LOW-001] API version en header
Severity: LOW (CVSS 2.1)
Justification: Minor info disclosure, useful for debugging
No mitigation required
Approved by: Jane Smith, 2026-02-10

Output: documentation/payment_api_security/AECF_04_RESIDUAL_RISKS.md
```

**Phase 6: CLEARANCE**
```
AI: "Final verification..."

✅ CRITICAL Vulnerabilities: 0
✅ HIGH Vulnerabilities: 0 (fixed)
✅ MEDIUM Vulnerabilities: Documented and approved
✅ LOW Vulnerabilities: Documented and approved

🔒 SECURITY CLEARANCE GRANTED
✅ CODE APPROVED FOR DEPLOY TO PRODUCTION
```

**Total time**: 3 hours (with corrections)

---

## � Skill 5: aecf_explain_behavior

### When to Use
✅ Understand why the system acts in a certain way
✅ Analyze unexpected behaviors (before debugging)
✅ Investigate system decisions (403, timeouts, calculations)
✅ Pre-debugging preparation
✅ Onboarding: understand critical flows
❌ Fix bugs (use `00_DEBUG.md` or normal flow)
❌ Audit quality (use `05_AUDIT_CODE.md`)
❌ Document general functionality (use `aecf_document_legacy`)

### Syntax
```
"Explain why [observed behavior]. Use skill: aecf_explain_behavior TOPIC: [name]"
```

### Example 1: Why does endpoint return 403?
```
User: "The POST /api/orders endpoint returns 403 for user ID 12345,
but for user 67890 it works. Same payload, same valid JWT token.
Explain why. Use skill: aecf_explain_behavior TOPIC: orders_403"
```

**What it does**:
1. [00_EXPLAIN_BEHAVIOR] Analyze the behavior
   - Identifica entry points (app/routes/orders.py)
- Trace complete flow step by step
   - Analiza valores: user 12345 role='customer', user 67890 role='premium_customer'
- Identifies critical decision: `if user.role in ['admin', 'premium_customer']`
- Analyze configuration: ALLOWED_ORDER_ROLES, feature flags
- Explains complete causality

**Output**:
```markdown
### 📋 EXECUTIVE SUMMARY
The system returns 403 because user 12345 has role='customer',
and the code in orders.py line 45 only allows 'admin' or 'premium_customer' roles.

### 🔄 EXECUTION FLOW
1. POST /api/orders → create_order() (orders.py:32)
2. JWT validated ✓ (both users)
3. check_permissions() ejecutado (middleware.py:18)
4. Query DB: SELECT role FROM users WHERE id = ?
   - User 12345: role='customer'
   - User 67890: role='premium_customer'
5. Validation line 45: if user.role in ALLOWED_ORDER_ROLES
   - User 12345: False → return 403
   - User 67890: True → continue

### 🎯 CRITICAL DECISION POINTS
Line 45 (orders.py):
Condition: user.role in ['admin', 'premium_customer']
User 12345: 'customer' NOT IN list → 403 ❌
User 67890: 'premium_customer' IN list → ✓

### 💡 CAUSAL EXPLANATION
The system returns 403 because a role restriction exists on line 45.
This restriction is active because FEATURE_FLAG_RESTRICT_ORDERS=true.
Only 'admin' or 'premium_customer' users can create orders.

### 📌 CONCLUSION
INTENTIONAL behavior according to current configuration.
If 'customer' should be allowed, modify ALLOWED_ORDER_ROLES or check feature flag.
```

**Total time**: 20 min

**User decide**:
- "OK, I understand. It's actually a permissions bug." → Continue to `00_DEBUG.md`
- "I understood, I just wanted to know why." → DONATE ✅

### Example 2: Why is query slow?
```
User: "Report query takes 30 seconds, before it took 2 seconds.
There were no code changes. There's just more data now.
Explain why. Use skill: aecf_explain_behavior TOPIC: slow_reports"
```

**Output**:
```markdown
### 📋 EXECUTIVE SUMMARY
The system takes 30 seconds for N+1 query problem: executes 1 initial query
+ 50,000 individual queries. Each sub-query takes ~0.6ms.

### 🔄 EXECUTION FLOW
1. generate_monthly_report() (reports.py:45)
2. Query: SELECT * FROM orders WHERE month = '2026-01'
   Time: 100ms, Rows: 50,000
3. Loop: for order in orders: (line 52)
   4. Query: SELECT * FROM order_items WHERE order_id = ?
Executed 50,000 times
      Total time: 50,000 × 0.6ms = 30 segundos

### 💡 CAUSAL EXPLANATION
The increase from 2s → 30s is due to the growth of orders (5,000 → 50,000).
Architectural problem: N+1 queries without index in order_items.order_id.
Linear growth: O(n) where n = number of orders.

### 📌 CONCLUSION
Functionally correct behavior, but inefficient.
Solution: Use JOIN or caching to remove N+1 pattern.
```

**Total time**: 25 min

**User decides**: "I need to optimize with JOIN." → Continue to `00_PLAN.md`

### Example 3: Why is the order processed twice?
```
User: "Order ID 789 was processed twice. Charged the user twice.
Logs show two entries of 'order_processed' 2 seconds apart.
Explain why. Use skill: aecf_explain_behavior TOPIC: double_process"
```

**Output**:
```markdown
### 📋 EXECUTIVE SUMMARY
Race condition: both requests read status='pending' before
anyone will update it (3 second window). There is no transactional lock
ni idempotency key.

### 🔄 EXECUTION FLOW
Timestamp | Request | Action
10:15:30  | Req 1   | Check: status='pending' ✓
10:15:30  | Req 1   | Process payment... (3 segundos)
10:15:32 | Req 2 | Check: status='pending' ✓ (Req 1 not updated yet)
10:15:32  | Req 2   | Process payment... (segundo cargo)
10:15:33  | Req 1   | UPDATE status='processed'
10:15:35  | Req 2   | UPDATE status='processed'

### 🎯 CRITICAL DECISION POINTS
Line 67 (processor.py): Check-then-act without lock
- No hay SELECT FOR UPDATE
- No hay transaction isolation
- No hay idempotency key validation

### 💡 CAUSAL EXPLANATION
User double-click + 3 second processing time created window
vulnerable for race condition. Both requests passed the status check
before anyone updated it.

### 📌 CONCLUSION
Critical bug: Missing transactional locking mechanism or idempotency key.
```

**Total time**: 35 min

**User decides**: "Critical bug. I need to add idempotency key." → Continue to `00_DEBUG.md`

---

## 📊 Skill 6: aecf_code_standards_audit

### When to Use
✅ Audit legacy or existing code against standards
✅ Pre-refactoring: identify what needs correction
✅ Verify compliance with organizational conventions
✅ Identify technical debt
✅ Onboarding of new code
❌ Newly implemented code in an AECF phase (use `05_AUDIT_CODE`)
❌ Security audit (use `aecf_security_review`)

### Syntax

**Forma simple (recomendada)**:
```
"skill: code_standards_audit. TOPIC: STANDARDS"
```

**Forma con scope**:
```
"skill: code_standards_audit. TOPIC: backend_standards. Scope: sentinel-multichat/backend"
```

**Forma natural**:
```
"Review the code and tell me what things I should change according to the standards"
```

### Example: Standards Audit
```
User: "skill: code_standards_audit. TOPIC: STANDARDS"
```

**What the skill does**:
1. Carga contextos (SYSTEM_CONTEXT, PROJECT_CONTEXT, governance)
2. Scan files in scope
3. Analyze against ALL defined standards
4. Classify findings by severity (CRITICAL/WARNING/INFO)
5. **Create file** with the complete report

**Output generado**:
```
documentation/STANDARDS/
└── AECF_01_CODE_STANDARDS_AUDIT.md
```

**The report includes**:
- Executive Summary con score de compliance
- Finds by category with `path/file.py:line`
- Prioritized violations (CRITICAL → WARNING → INFO)
- Compliance metrics
- Actionable recommendations

**Result**: Complete report serving as input for `06_FIX_CODE`

---

## 🔄 GO/NO-GO Handling

### Automatic Loops

The skills handle GO/NO-GO loops automatically:

```
PLAN → AUDIT (NO-GO) → FIX → AUDIT (NO-GO) → FIX → AUDIT (GO) → Continuar...
```

**You don't need to intervene** in each loop, the AI ​​executes until GO is obtained.

### When to Intervene

You only need to intervene when:

1. **CONDITIONAL GO**: Decide whether to accept risk or mitigate
   ```
   AI: "AUDIT_CODE veredicto: GO CONDICIONAL
WARNING: Rate limiting is missing on critical endpoint.
Do you want to: a) Correct, b) Accept risk, c) Implement compensatory measure?"
   ```

2. **Multiple NO-GOs**: Plan may be poorly defined
   ```
AI: "AUDIT_PLAN has returned NO-GO 3 consecutive times.
It seems that the requirements are unclear.
Suggestion: Clarify with stakeholders before continuing."
   ```

3. **Tests flakey**: Tests non-deterministic
   ```
AI: "AUDIT_TESTS detected flaky tests:
        - test_concurrent_requests (falla intermitente)
Requires manual correction."
   ```

---

## 💡 Tips for Use

### ✅ Best Practices

1. **Be specific in the description**
- ❌ "Implement export"
- ✅ "Implement endpoint /api/export with PDF and CSV formats, filters by date, permissions control"

2. **Choose descriptive TOPICs**
   - ❌ "abc", "test", "new_feature"
   - ✅ "report_export", "mfa_auth", "payment_api_security"

3. **Use the correct skill**
   - Nueva feature → `aecf_new_feature`
- Emergency → `aecf_hotfix`
- Document first → `aecf_document_legacy`
   - Security → `aecf_security_review`
- Understand behavior → `aecf_explain_behavior`
- Code standards → `aecf_code_standards_audit`
   - Evaluar madurez → `aecf_maturity_assessment`
   - Refactorizar → `aecf_refactor`
- Technical Debt → `aecf_tech_debt_assessment`
   - Pre-release → `aecf_release_readiness`
- Dependencies → `aecf_dependency_audit`
   - Replayability → `aecf_system_replayability_adaptive`

4. **Review audit outputs**
- Don't assume GO means perfect
- CONDITIONAL GO requires informed decision

### ❌ Common Errors

1. **Use hotfix for non-critical bugs**
   ```
❌ "Bug in logout button. Use: aecf_hotfix"
✅ "Bug in logout button. Use: aecf_new_feature" (normal flow)
   ```

2. **Do not document legacy code before modifying**
   ```
❌ "Modify old auth module. Use: aecf_new_feature"
✅ "Document auth module. Use: aecf_document_legacy"
[After] "Modify to add MFA. Use: aecf_new_feature"
   ```

3. **Skip testing**
   ```
❌ "Implement feature but without tests for now"
✅ Skills v2.0 include mandatory testing
   ```

---

## 📊 Skill Comparison

| Aspecto | new_feature | hotfix | document_legacy | security_review | code_standards | maturity_assessment | refactor | tech_debt | release_readiness | dependency_audit | data_strategy |
|---------|-------------|--------|-----------------|-----------------|----------------|---------------------|----------|-----------|-------------------|------------------|---------------|
| **Tiempo** | 1.5-4h | 1-3h | 30min-2h | 45min-6h | 30min-4h | 1-3h | 2-6h | 1-4h | 30min-2h | 30min-2h | 20min-3h |
| **Testing** | Mandatory | Critical minimum | N/A | Security tests | N/A (report only) | N/A | Pre+Post | N/A | Validates existing | N/A | N/A (design) |
| **Audit** | Complete | Accelerated | N/A | Specialized | Exhaustive | 10 dimensions | Complete | 6 categories | Cross-phase | Supply chain | Decision matrix |
| **Output** | 8+ docs | 1-2 docs | 2-3 docs | 2-5 docs | 1 doc | 1 assessment | 4+ docs | 1 assessment | 1 verdict | 1 report | 1 strategy + handoff |
| **Urgency** | Normal | CRITICISM | Low | Medium-High | Normal | Low | Normal | Normal | Medium | Medium | Normal |
| **Modify code** | Yes | Yes | No | Yes | No | No | Yes | No | No | No | No | No |

---

## 🆘 Troubleshooting

### Problem: Skill takes a long time
**Cause**: Multiple NO-GOs, unclear requirements
**Solution**: Stop and clarify requirements with stakeholders

### Problem: Tests with low coverage
**Causa**: TEST_STRATEGY incompleta  
**Solution**: In TEST_IMPLEMENTATION, explicitly specify missing cases

### Problem: Security review detects CRITICS
**Cause**: Insecure code
**Solution**: The skill will automatically correct with FIX_CODE

### Issue: Hotfix fails in production
**Cause**: Incorrect RCA
**Solution**: Immediate ROLLBACK, re-evaluate with deeper DEBUG

---

## 📖 Complete Documentation

- **[Skills Guide](skills/README_SKILLS.md)** - Comprehensive guide with examples
- **[AECF v2.0 README](README_AECF_v2.md)** - Main documentation
- **[Individual Prompts](aecf/)** - If you need to execute manually

---

**Ready to get started?** Choose your use case and run the corresponding skill:

```
1. New feature → "Implement [X]. Use skill: aecf_new_feature TOPIC: [Y]"
2. Hotfix → "🚨 P1: [X]. Use skill: aecf_hotfix TOPIC: [Y]"
3. Document → "Documentar [X]. Use skill: aecf_document_legacy TOPIC: [Y]"
4. Security → "Security review [X]. Use skill: aecf_security_review TOPIC: [Y]"
5. Explain → "Explain why [X]. Use skill: aecf_explain_behavior TOPIC: [Y]"
6. Standards → "skill: code_standards_audit. TOPIC: [Y]"
7. Maturity → "Assess AECF maturity. Use skill: aecf_maturity_assessment TOPIC: [Y]"
8. Refactor → "Refactor [X]. Use skill: aecf_refactor TOPIC: [Y]"
9. Technical debt → "Assess technical debt [X]. Use skill: aecf_tech_debt_assessment TOPIC: [Y]"
10. Pre-release → "Validar release [X]. Use skill: aecf_release_readiness TOPIC: [Y]"
11. Dependencies → "Audit dependencies [X]. Use skill: aecf_dependency_audit TOPIC: [Y]"
12. Data strategy → "Design data strategy for [X]. Use skill: aecf_data_strategy TOPIC: [Y]"
13. Replayability → "Add replay capability [X]. Use skill: aecf_system_replayability_adaptive TOPIC: [Y]"
14. Project context → "Generate project context. Use skill: aecf_project_context_generator"
```

> **Remember**: Thanks to the SKILL_DISPATCHER, you can use natural language.
> "Audit backend standards" is enough to activate the correct skill.

And let AECF do the rest! 🚀

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check


