# CJ — History

## Project Knowledge

### Day 1 Context
- **Project:** petclinic-ai-modernization-labs
- **User:** Max Bush (Solution Engineer)
- **Goal:** Write detailed, step-by-step lab documentation
- **Format:** Markdown files in /labs folder
- **Style:** Clear instructions + teaching moments + notes explaining "why"

### Lab Series Overview
- Lab 0: Legacy Baseline & AI Readiness
- Lab 1: In-App AI with RAG (Assistive AI)
- Lab 2: AI-Assisted Actions with Human-in-the-Loop
- Lab 3: Single-Agent Workflows (Goal-Oriented AI)
- Lab 4: Multi-Agent System (MAS)
- Lab 5: Platform & Governance (Enterprise AI)
- Lab 6: AI-Native Product Re-Thinking (Capstone)

## Learnings

### Lab 0 Authoring (Completed)

**Key discoveries while writing Lab 0:**
- PetClinic domain is rich with exploration opportunities: Owners → Pets → Visits with free-form clinical descriptions
- Visit descriptions are the critical data asset—capturing vet judgment in natural language that can be analyzed by AI
- The app has a clean 3-layer architecture (Web → Service → Repository) that makes AI integration points clear
- Safety/approval constraints are essential: AI must suggest, never decide alone on medical matters
- Staff experience matters—a scheduling AI is only useful if it saves time (must be fast)

**Writing style observations:**
- Users need hands-on exploration (clicking around UI, seeing data) before abstract concepts land
- Teaching moments work best when tied to specific domain elements (e.g., "visit descriptions capture judgment")
- Checkpoints and reflection questions help users retain and apply learning
- Showing a concrete opportunity table (Decision Point → AI Potential → Constraint) clarifies the "why"

**For future labs:**
- Lab 1 should leverage the visit descriptions discovered in Lab 0 for RAG queries
- Staff trust in AI depends heavily on explainability ("why did you recommend this vet?")
- Use Lab 0's opportunity map as a roadmap for what features to build in Labs 1-6
- Always explain why a feature matters operationally (saves time, improves care, reduces errors)
