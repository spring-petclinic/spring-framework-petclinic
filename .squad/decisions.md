# Squad Decisions

## Active Decisions

### 1. Lab File Structure & Organization

**Decided by:** Bartlet (Lead)  
**Date:** 2024  
**Status:** Approved

#### What Was Decided

- **Location:** All labs in `/labs/` directory
- **File naming:** `lab-NN-kebab-case-title.md` (00-06)
- **README:** Single `labs/README.md` introduces series, lists all 7 labs, defines prerequisites and progression

#### Lab Structure Template
Each lab file includes:
1. **Context** — What problem does this lab solve? How does it build on prior labs?
2. **Theme & Mindset** — The core principle (e.g., "AI proposes, humans decide")
3. **What This Lab Proves** — Strategic value, not just technical capability
4. **Key Activities** — Hands-on work organized with checkboxes
5. **Checkpoint** — Validation gates before proceeding
6. **Outputs** — Concrete deliverables
7. **Teaching Moment** — Singular insight that encapsulates the lab's value
8. **Reflection Questions** — For learner metacognition
9. **Next Steps** — Bridge to the next lab

#### Naming Convention Rationale
- `lab-00` through `lab-06` ensures alphabetic ordering and clarity
- Kebab case in filenames improves readability in URLs and filesystem

#### Progression Logic
The 7 labs follow a clear arc:
- **Labs 0-2 (Foundation):** Assess → Q&A → Approval workflows (understand value, build trust)
- **Labs 3-4 (Reasoning):** Single agent → Multi-agent (extend capability, improve judgment)
- **Lab 5 (Scale):** Platform & governance (scale safely across organization)
- **Lab 6 (Reimagine):** AI-native architecture (reshape product, optional capstone)

---

### 2. Technical Patterns Foundation for Labs 1-5

**Author:** Josh (Domain Expert)  
**Date:** 2024-01-15  
**Status:** Approved

#### Key Decisions

**RAG Indexing Strategy: Document-Level Granularity**
- Index at document level (one pet + full history = one document), not paragraph level
- Preserves clinical context and reduces hallucination
- Cleaner citation tracking (entire document is one source)

**Confidence Scoring: Composite Formula**
- Confidence = (semantic_score × 0.7) + (bm25_score × 0.3)
- Semantic search captures meaning; BM25 provides grounding in exact term matches
- Tunable weights based on lab testing results

**Multi-Agent Authority: Compliance Has Veto**
- Compliance & Safety Agent has veto authority over Clinical Reasoning Agent decisions
- Safety is non-negotiable in veterinary context
- Clear authority prevents circular negotiations; escalates conflicts to human

**Governance: Centralized Kernel Configuration**
- All teams use a single, centrally-configured Semantic Kernel instance for Azure OpenAI
- Eliminates secrets sprawl; enables consistent cost tracking and policy enforcement
- Simplifies model upgrades

**Explainability: Reasoning Trace as First-Class Data**
- Every AI output includes structured reasoning trace (steps, decisions, alternatives considered)
- Enables user audit and contestation of AI decisions
- Supports governance compliance and captures "why" for model improvement

---

### 3. Learning Objectives Framework for Labs 0–6

**Author:** Toby (Curriculum Developer)  
**Date:** 2024  
**Status:** Approved

#### Decision

Created `labs/learning-objectives.md` with per-lab pedagogical framework:

**Per-Lab Structure (Labs 0–6)**
- One clear "aha moment" (emotional insight)
- 3–5 learning objectives
- Mental models and analogies
- Connection to the next lab
- Common misconceptions to address

**Progressive Responsibility Model**
Labs shift agency from learner to system:
- **Labs 0–1:** System as tool (understand, retrieve)
- **Labs 2–3:** Learner as designer (control, autonomy)
- **Labs 4–5:** Learner as architect (orchestration, governance)
- **Lab 6:** Learner as leader (transformation)

**Failure as Pedagogy**
Each lab includes built-in failure points where learners experience why constraints matter through direct experience, not lecture.

**Mental Models Over Technical Details**
Each lab has one strong analogy (captain/co-pilot, medical panel, airline safety) that maps AI concepts to familiar human experience.

**Scaffolding Strategy**
Each lab builds on trust from the previous:
- Lab 1 trusts RAG works; Lab 2 asks: what if it's wrong?
- Lab 2 trusts humans decide; Lab 3 asks: can we automate safely?
- Lab 3 trusts agents work; Lab 4 asks: what if agents disagree?
- Lab 4 trusts scale; Lab 5 asks: how do we govern it?
- Lab 5 establishes governance; Lab 6 asks: what if it's invisible?

#### Key Pedagogical Principles

| Principle | Rationale |
|-----------|-----------|
| **Every lab has one "aha"** | Sticky insights stick. One clear idea per lab beats five scattered concepts. |
| **Failure is the teacher** | Learners retain lessons from problems they solve, not explanations they read. |
| **Analogies > abstractions** | AI is abstract. Captain/co-pilot, panel diagnosis, airline safety—these are concrete and transferable. |
| **Success criteria come first** | Learners should know what "winning" looks like *before* starting, not after. |
| **Labs build on each other** | Not just technically (RAG enables agents) but conceptually (trust enables the next challenge). |

---

## Governance

- All meaningful changes require team consensus
- Document architectural decisions here
- Keep history focused on work, decisions focused on direction
