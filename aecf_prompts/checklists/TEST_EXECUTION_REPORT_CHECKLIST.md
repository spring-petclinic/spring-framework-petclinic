# AECF - TEST_EXECUTION_REPORT CHECKLIST

## 1. Scope Validation
- [ ] Scope matches approved TEST_STRATEGY
- [ ] Only approved tests were executed
- [ ] No unauthorized production code change occurred in this phase

## 2. Execution Evidence
- [ ] Exact commands recorded
- [ ] Working directory recorded
- [ ] Environment or runtime assumptions recorded
- [ ] Pass or fail or skip or error counts recorded

## 3. Coverage and Metrics
- [ ] Coverage result documented or blocker explained
- [ ] Execution duration documented
- [ ] Critical uncovered areas documented

## 4. Risk Category Coverage
- [ ] Security or permission evidence documented
- [ ] Error forcing evidence documented
- [ ] SQL injection or input validation evidence documented when applicable
- [ ] Performance or timeout or pagination evidence documented when applicable
- [ ] Logging or resource handling evidence documented when applicable

## 5. Findings Integrity
- [ ] Failing tests listed explicitly
- [ ] Blockers listed explicitly
- [ ] Recommendations traceable to execution evidence

## 6. Decision Integrity
- [ ] Verdict matches observed execution results
- [ ] Residual gaps documented
- [ ] No hidden assumptions remain unstated

## FINAL CHECK
All items above must be TRUE before issuing GO verdict.

## SCORING TABLE

| Category | Weight | Items evaluated | Score |
|----------|--------|----------------|-------|
| Scope Validation | 2 | 3 |  |
| Execution Evidence | 3 | 4 |  |
| Coverage and Metrics | 2 | 3 |  |
| Risk Category Coverage | 3 | 5 |  |
| Findings Integrity | 2 | 3 |  |
| Decision Integrity | 3 | 3 |  |

## FINAL SCORE
- Score bruto:
- Score normalizado:
- Nivel de madurez:
- Veredicto automatico:

**RULE**: If command evidence or failure evidence is missing -> automatic NO-GO

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
