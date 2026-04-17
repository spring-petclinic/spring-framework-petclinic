# MODEL_GOVERNANCE_CONTEXT

## Model Registry
Every model must define:
- Model name
- Version
- Provider
- Cost model
- Intended use

Example:
Model: GPT-4.1
Version: 2026-02
Provider: OpenAI
Cost model: Input/output tokens + per-request overhead
Use: Cost anomaly explanation

## Evaluation Metrics
- Accuracy
- Drift monitoring
- Bias check
- Token consumption

Example:
Monthly evaluation:
    Drift threshold: 5%
    Bias check: manual review sample size 100
    Accuracy floor: 90%
    Token budget variance tolerance: 10%

## Budget Governance
- Max tokens per feature
- Max cost per tenant

Example:
Feature: AI Advisor
    Max tokens per call: 5,000
    Monthly tenant cap: €50

## MANDATORY VALIDATION
- [ ] Every active model has a complete registry entry (name, version, provider, cost model, intended use)
- [ ] Registry entries are versioned and traceable to deployment/release artifacts
- [ ] Monthly evaluation is executed and archived (accuracy, drift, bias, token consumption)
- [ ] Drift threshold breaches trigger documented mitigation actions
- [ ] Bias checks include sample definition, reviewer identity, and resolution notes
- [ ] Feature-level token limits are enforced in runtime controls
- [ ] Tenant-level monthly spend caps are enforced and alerting is configured
- [ ] Governance owner and next review date are recorded
