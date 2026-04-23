# AI_EXPLAINABILITY_CONTEXT

## Purpose
Ensure that every AI-driven feature provides transparent and interpretable outputs.

## Explainability Levels

Level 0 – Black box (NOT allowed in production)
Level 1 – Output justification
Level 2 – Feature importance explanation
Level 3 – Decision traceability
Level 4 – Full reasoning chain (where legally allowed)

Example:

Feature: Cost anomaly detection

Output:
    "Cost increased due to VM scale set expansion"

Explainability:
    - Data sources used: Azure consumption API
    - Variables considered: usage hours, SKU price
    - Threshold logic: >15% deviation month-over-month
    - Model type: statistical baseline + LLM summarization

## Mandatory Explainability Block (for every skill using AI)

AI_EXPLAINABILITY:
    - Model used:
    - Data inputs:
    - Decision logic summary:
    - Deterministic components:
    - Probabilistic components:
    - User-facing explanation included? (YES/NO)

## Logging Requirements

- Store model version
- Store prompt template version
- Store input snapshot hash
- Store output

## Compliance Check

If feature affects:
    - Financial decisions
    - Regulatory data
    - PII
Then minimum explainability level = 2

## Validation Checklist

- [ ] Explainability level assigned (0-4)
- [ ] Level 0 is not used in production
- [ ] Mandatory `AI_EXPLAINABILITY` block is completed
- [ ] Logging includes model version
- [ ] Logging includes prompt template version
- [ ] Logging includes input snapshot hash
- [ ] Logging includes output
- [ ] Compliance check applied (financial/regulatory/PII)
- [ ] Minimum level 2 enforced when required