# AECF — DATA STRATEGY CHECKLIST

## 1. Data Source Characterization
- [ ] Volume assessed (GB/day, rows/day, growth)
- [ ] Velocity assessed (generation frequency, batch windows)
- [ ] Variety assessed (schema stability, formats)
- [ ] Veracity assessed (quality, duplicates, re-statements)
- [ ] API/Connector behavior documented (limits, pagination, auth)
- [ ] Data lifecycle understood (immutable vs. mutable, corrections)

## 2. Constraints & Requirements
- [ ] Infrastructure constraints identified
- [ ] Budget constraints documented
- [ ] Data freshness SLA defined
- [ ] Query patterns identified (OLTP/OLAP/mixed)
- [ ] Retention requirements documented
- [ ] Compliance/audit requirements checked

## 3. Strategy Enumeration
- [ ] Minimum 3 strategies identified
- [ ] Each strategy has technical description
- [ ] Prerequisites documented per strategy
- [ ] Complexity scored (implementation + operational)
- [ ] No viable strategy omitted without justification

## 4. Trade-off Analysis
- [ ] Pros/contras documented per strategy
- [ ] Best/worst scenarios identified per strategy
- [ ] TCO estimated per strategy (storage, compute, dev, maintenance)
- [ ] Analysis is specific to the data source (not generic)

## 5. Decision Matrix
- [ ] All dimensions scored per strategy
- [ ] Weights justified for this specific scenario
- [ ] Data integrity dimension weighted >= 15%
- [ ] Scoring is evidence-based (not arbitrary)
- [ ] Final ranking computed correctly

## 6. Recommendation Quality
- [ ] Single clear recommendation issued
- [ ] Minimum 3-point justification provided
- [ ] Residual risks identified with mitigations
- [ ] Plan B (alternative strategy) defined
- [ ] Strategy change triggers documented

## 7. Schema & Storage Design
- [ ] Table architecture proposed with rationale
- [ ] Key strategy defined (PK, natural keys, surrogate)
- [ ] Deduplication technique specified and justified
- [ ] Partitioning strategy evaluated
- [ ] Retention/lifecycle policy defined
- [ ] Data flow diagram included

## 8. Downstream Handoff
- [ ] Input for discovery generated (scope, functionality)
- [ ] Input for new_feature generated (description, acceptance criteria)
- [ ] Input for plan generated (decisions, risks, assumptions)
- [ ] NFRs derived from strategy (performance, storage, monitoring)

## FINAL CHECK
All items above must be TRUE before issuing GO verdict.

## SCORING TABLE

| Categoría | Peso | Items evaluados | Score |
|-----------|------|----------------|-------|
| Data Source Characterization | 3 | 6 | |
| Constraints & Requirements | 2 | 6 | |
| Strategy Enumeration | 3 | 5 | |
| Trade-off Analysis | 2 | 4 | |
| Decision Matrix | 3 | 5 | |
| Recommendation Quality | 3 | 5 | |
| Schema & Storage Design | 2 | 6 | |
| Downstream Handoff | 2 | 4 | |

## FINAL SCORE
- Score bruto:
- Score normalizado:
- Nivel de madurez:
- Veredicto automático:

**RULE**: If any CRITICAL finding exists → Score = 0 and automatic NO-GO
**RULE**: If Data Integrity score < 3 → automatic NO-GO
**RULE**: If Recommendation lacks justification → automatic NO-GO

NO explanations.
NO additional commentary.
Only checklist items.

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
