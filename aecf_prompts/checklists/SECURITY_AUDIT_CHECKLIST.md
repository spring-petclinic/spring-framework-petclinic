# AECF — SECURITY_AUDIT CHECKLIST

## 1. Scope Validation
- [ ] Scope matches PLAN
- [ ] No scope expansion
- [ ] No implicit redesign

## 2. Security Controls
- [ ] No sensitive data exposure
- [ ] Access control validated
- [ ] Enumeration mitigated
- [ ] Logging covers security events

## 3. Resource Management
- [ ] No open resources
- [ ] Proper context managers used

## 4. Logging & Observability
- [ ] No print() usage
- [ ] Structured logging used
- [ ] Errors logged properly

## 5. Compliance with Previous Phase
- [ ] PLAN approved (if applicable)
- [ ] AUDIT verdict respected
- [ ] No phase violation

## 6. Production Readiness
- [ ] Edge cases considered
- [ ] Error handling complete
- [ ] No silent failures
- [ ] No hidden side effects

## 7. Decision Integrity
- [ ] No unauthorized decisions
- [ ] All decisions traceable to PLAN

## 8. OWASP Coverage
- [ ] Injection tested
- [ ] Access control tested
- [ ] Cryptographic issues reviewed
- [ ] Configuration reviewed

## FINAL CHECK
All items above must be TRUE before issuing GO verdict.

## SCORING TABLE

| Categoría | Peso | Items evaluados | Score |
|-----------|------|----------------|-------|
| Scope Validation | 2 | 3 |  |
| Security Controls | 3 | 4 |  |
| Resource Management | 2 | 2 |  |
| Logging & Observability | 2 | 3 |  |
| Compliance with Previous Phase | 3 | 3 |  |
| Production Readiness | 2 | 4 |  |
| Decision Integrity | 3 | 2 |  |
| OWASP Coverage | 2 | 4 |  |

## FINAL SCORE
- Score bruto:
- Score normalizado:
- Nivel de madurez:
- Veredicto automático:

**RULE**: If any CRITICAL finding exists → Score = 0 and automatic NO-GO

NO explanations.
NO additional commentary.
Only checklist items.

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
