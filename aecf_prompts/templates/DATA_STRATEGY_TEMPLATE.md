# AECF — DATA STRATEGY

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Data Strategy |
> | Phase | DATA_STRATEGY |

---

## 1. Data Source Characterization
### 1.1 Source Identification
- Source name:
- Source type (API / Connector / File Export / Database / Stream):
- Provider/vendor:
- Documentation reference:

### 1.2 Volume Assessment
- Estimated data size per load:
- Estimated rows per load:
- Historical data volume:
- Growth rate (linear / exponential / seasonal):
- Total projected volume (12 months):

### 1.3 Velocity Assessment
- Generation frequency (real-time / hourly / daily / weekly):
- Export/API update frequency:
- Batch window available:
- Rate limiting / throttling:

### 1.4 Variety Assessment
- Data format (JSON / CSV / Parquet / XML / other):
- Schema stability (fixed / evolving / semi-structured):
- Nested structures (yes / no):
- Number of distinct entity types:

### 1.5 Veracity Assessment
- Data quality at source (high / medium / low):
- Known duplicate patterns:
- Re-statements / retroactive corrections (yes / no):
- Correction window (if applicable):
- Consistency guarantees from source:

### 1.6 Operational Characteristics
- API/Connector behavior:
- Pagination support:
- Idempotency guarantees:
- Error handling / retry behavior:
- Authentication / authorization model:

---

## 2. Constraints & Requirements
### 2.1 Infrastructure
- Current database engine:
- Cloud provider / services available:
- Existing ETL/ELT tools:

### 2.2 Business Requirements
- Data freshness SLA:
- Query latency requirements:
- Access patterns (OLTP / OLAP / mixed):
- Concurrent users / queries:

### 2.3 Compliance & Governance
- Data retention requirements:
- Audit trail requirements:
- Data sovereignty / residency:
- PII / sensitive data handling:

### 2.4 Budget & Resources
- Storage budget constraints:
- Compute budget constraints:
- Development capacity (hours/sprint):
- Operational capacity:

---

## 3. Strategies Evaluated

### Strategy A: [Name]
- **Description**:
- **Technical approach**:
- **Prerequisites**:
- **Implementation complexity** (1-5):
- **Operational complexity** (1-5):
- **Estimated relative cost**:

### Strategy B: [Name]
- **Description**:
- **Technical approach**:
- **Prerequisites**:
- **Implementation complexity** (1-5):
- **Operational complexity** (1-5):
- **Estimated relative cost**:

### Strategy C: [Name]
- **Description**:
- **Technical approach**:
- **Prerequisites**:
- **Implementation complexity** (1-5):
- **Operational complexity** (1-5):
- **Estimated relative cost**:

*(Add more strategies as needed)*

---

## 4. Trade-off Analysis

### Strategy A: [Name]
**Pros**:
-

**Contras**:
-

**Best scenario**:

**Worst scenario**:

**Estimated TCO**:
| Component | Cost Level |
|-----------|-----------|
| Storage | |
| Compute | |
| Development | |
| Maintenance | |

### Strategy B: [Name]
*(Same structure)*

### Strategy C: [Name]
*(Same structure)*

---

## 5. Decision Matrix

| Dimension | Weight | Strategy A | Strategy B | Strategy C |
|-----------|--------|-----------|-----------|-----------|
| Implementation Simplicity | 15% | | | |
| Operational Cost | 20% | | | |
| Data Integrity | 20% | | | |
| Scalability | 15% | | | |
| Resilience / Recovery | 10% | | | |
| Data Latency | 10% | | | |
| Maintainability | 10% | | | |
| **Weighted Total** | **100%** | **X.XX** | **X.XX** | **X.XX** |

### Weight Justification
- [Why these weights for this specific scenario]

---

## 6. Recommendation

### 6.1 Recommended Strategy
- **Strategy**: [ID + Name]
- **Final Score**: X.XX / 5.00

### 6.2 Justification (3+ points)
1. [Reason 1 with evidence]
2. [Reason 2 with evidence]
3. [Reason 3 with evidence]

### 6.3 Residual Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| | | | |

### 6.4 Alternative (Plan B)
- **Strategy**: [ID + Name]
- **When to switch**: [Trigger conditions]

### 6.5 Strategy Change Triggers
- Trigger 1: [Condition that invalidates the recommendation]
- Trigger 2:

---

## 7. Schema & Storage Design

### 7.1 Table Architecture
- Tables proposed:
- Rationale (single vs. multiple):
- Normalization level + justification:

### 7.2 Key Strategy
- Primary keys:
- Natural keys:
- Surrogate keys (if applicable):

### 7.3 Partitioning
- Partition strategy:
- Partition key:
- Partition granularity:

### 7.4 Indexing
| Table | Index | Columns | Type | Justification |
|-------|-------|---------|------|--------------|
| | | | | |

### 7.5 Deduplication Strategy
- **Technique**: (UPSERT / MERGE / Window Functions / Hash-Based / other)
- **Dedup key**: [columns]
- **Timing**: Pre-insert / Post-insert / On-merge
- **Justification**:

### 7.6 Retention & Lifecycle
| Tier | Age | Storage | Access Pattern |
|------|-----|---------|---------------|
| Hot | | | |
| Warm | | | |
| Cold/Archive | | | |

### 7.7 Data Flow Diagram
```
[Source] → [Ingestion] → [Staging] → [Transform] → [Target] → [Consumers]
```

---

## 8. Downstream Handoff

### 8.1 For aecf_discovery
- **Scope to investigate**:
- **Functionality to search for**:
- **Key files/modules expected**:

### 8.2 For aecf_new_feature
- **Feature description** (pre-built):
- **Acceptance criteria**:
- **Non-functional requirements**:

### 8.3 For aecf_plan
- **Design decisions already taken**:
- **Risks already evaluated**:
- **Validated assumptions**:

### 8.4 For aecf_refactor
- **Components to refactor** (if existing pipeline):
- **Behavior to preserve**:
- **Expected improvements**:

---

## 9. Implementation Roadmap (High-Level)
| Phase | Description | Estimated Effort | Dependencies |
|-------|-------------|-----------------|-------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

## AECF_COMPLIANCE_REPORT

### Checklist Validation
- [ ] Data source fully characterized
- [ ] Minimum 3 strategies evaluated
- [ ] Decision matrix scored
- [ ] Recommendation issued with justification
- [ ] Schema design proposed
- [ ] Deduplication strategy defined
- [ ] Retention policy defined
- [ ] Downstream handoff generated
- [ ] Residual risks documented

### Verdict
GO / NO-GO
