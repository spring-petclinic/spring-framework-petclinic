# Lab 1: In-App AI with RAG (Assistive AI)

**Theme:** AI answers questions inside the application  
**Duration:** ~7 hours  
**Prerequisites:** Completed Lab 0

---

## Context

Lab 0 identified opportunities. Lab 1 builds the first AI feature: natural-language Q&A grounded strictly in PetClinic data.

This is **Assistive AI**—AI that augments understanding without replacing human judgment or changing workflows. You ask it questions; it retrieves and synthesizes answers from existing data. No hallucinations. No external knowledge. No automation.

---

## What This Lab Proves

1. **AI can deliver value without changing workflows.** Staff don't need to learn new interaction patterns; Q&A fits naturally into existing apps.
2. **RAG (Retrieval-Augmented Generation) fits naturally into legacy apps.** You don't refactor the backend; you layer AI on top.
3. **Citations ground trust.** Users trust AI more when they can click through to source records.
4. **Bounded confidence is a feature.** "I don't know" from AI is better than a confident hallucination.

---

## Key Activities

### Activity 1: Build a Vector Index
- [ ] Extract and index all PetClinic entities (owners, pets, visits, notes)
- [ ] Embed text (owner names, pet histories, notes) into a vector database
- [ ] Verify retrieval: Can you search by semantic similarity?

### Activity 2: Add Q&A to the UI
- [ ] Create an "Ask about a patient" widget in the PetClinic UI
- [ ] User types a natural-language question
- [ ] System retrieves relevant records (owners, pets, visits)
- [ ] LLM synthesizes a grounded answer with citations

### Activity 3: Enforce Retrieval Bounds
- [ ] Answers cite specific records (no standalone claims)
- [ ] System declines to answer if confidence is low
- [ ] Explain why an answer could not be provided

### Activity 4: Measure Performance
- [ ] Accuracy: Does the answer match the retrieved data?
- [ ] Relevance: Does the answer address the question?
- [ ] User trust: Do staff find the citations helpful?

---

## Checkpoint 1: RAG Foundation
Before moving forward, verify:
- [ ] Vector database is populated and searchable
- [ ] Q&A widget loads and accepts input
- [ ] System returns grounded answers with citations
- [ ] Low-confidence questions result in "I don't know"

---

## Outputs from This Lab

### Output 1: Grounded Q&A Feature
A deployed capability within PetClinic that:
- Accepts natural-language questions from veterinarians
- Retrieves relevant records via semantic search
- Synthesizes answers grounded in source data
- Cites sources for every claim
- Declines to answer when uncertain

### Output 2: Vector Database Schema
Documentation of:
- What entities are indexed (owners, pets, visits, notes)
- Embedding strategy (model, dimension, refresh cadence)
- Retrieval logic (semantic similarity thresholds, ranking)

### Output 3: Confidence Assessment Framework
Define:
- When does the system respond with high confidence?
- When does it respond with low confidence?
- When does it decline to answer?

---

## Teaching Moment

> **"This is not automation—this is augmented understanding."**

RAG is fundamentally different from automation. It doesn't *do* anything; it *answers* questions. The vet remains in control. The data comes from the system, not from AI inference. Citations restore the trust that "generative" systems often break.

This is the safest form of AI in enterprise: constrained, grounded, auditable.

---

## Reflection Questions

Before moving to Lab 2:

1. **What was the hardest part about implementing RAG in an existing system?**
2. **What types of questions does RAG handle well? Poorly?**
3. **If a user gets a wrong answer, how would you debug it?**
4. **Would you deploy this to production today? What's missing?**

---

## Next Steps

Move to **Lab 2: AI-Assisted Actions with Human-in-the-Loop** when ready.

Lab 2 moves beyond Q&A (passive augmentation) to action drafting (active assistance). AI will propose visit summaries, follow-up plans, and owner messages—but humans approve before execution.

---

*Lab 1 content placeholder. Full content will be authored by CJ.*
