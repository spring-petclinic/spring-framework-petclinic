# Josh — History

## Project Knowledge

### Day 1 Context
- **Project:** petclinic-ai-modernization-labs
- **User:** Max Bush (Solution Engineer)
- **Goal:** Ensure technical accuracy of AI modernization patterns
- **Base App:** Spring PetClinic (Java/Spring Boot)
- **AI Stack:** Azure AI services, likely Semantic Kernel for agent patterns

### Technical Domains to Cover
- **Lab 1:** RAG architecture — indexing, retrieval, grounding, citations
- **Lab 2:** Human-in-the-loop — approval flows, confidence scoring, explainability
- **Lab 3:** Single-agent — tool calling, bounded execution, observable reasoning
- **Lab 4:** Multi-agent — orchestration, role contracts, conflict resolution
- **Lab 5:** Platform governance — centralized model access, prompt versioning, telemetry

## Learnings

### Technical Patterns Documentation (Lab 1-5)
Created `/labs/technical-patterns.md` defining:

**Lab 1 (RAG):** 
- Granular chunking strategy (document-level, not paragraph) to preserve context
- Metadata enrichment (entity_type, entity_id, clinical_relevance) for citation tracking
- Hybrid retrieval (semantic + BM25) for safety-critical queries
- Azure AI Search semantic re-ranking + vector fields for embedding readiness
- Confidence scoring formula: (semantic_score × 0.7) + (bm25_score × 0.3)

**Lab 2 (Human-in-the-Loop):**
- Draft-Approve flow: generate → store with metadata → review → approve/edit/reject
- Per-statement confidence with grounding (which records support each claim)
- Reasoning trace JSON structure capturing how AI arrived at recommendations
- Conditional approval rules: high-confidence (auto), medium (read reasoning), low (explicit edits)
- Explainability metadata distinguishing data vs. inference

**Lab 3 (Single Agent):**
- Role contracts as JSON (declarative role, scope, authority level, tools)
- Tool whitelist enforcement via middleware
- Bounded execution: agents draft/suggest but never create records without approval
- Tool calling pattern with Semantic Kernel using [KernelFunction] attributes
- Agentic loop with explicit reasoning logging at each step
- Observable reasoning UI pattern showing step-by-step agent thinking

**Lab 4 (Multi-Agent):**
- Three-agent pattern: Clinical Reasoning → Compliance & Safety → Communication
- Sequential orchestration with short-circuit on safety failures
- Role contracts defining veto authority (Compliance can block, Clinical cannot override)
- Shared context (read-only) vs. shared authority (none; each agent owns its output)
- Conflict resolution rules: escalate disagreements to human, never auto-resolve
- Audit trail logging all agent decisions with timestamps and reasoning

**Lab 5 (Governance):**
- Model registry (single source of truth for approved models, endpoints, costs)
- Centralized kernel configuration (all teams use same endpoint/credentials)
- Prompt versioning with active/deprecated/sunset states
- Usage telemetry pipeline: cost calculation, performance metrics, quality tracking
- Budget alerts with rate-limiting for teams exceeding thresholds
- Policy enforcement at request time: model approval → use case approval → quota → PII filtering → output filtering
