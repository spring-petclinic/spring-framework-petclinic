# Bartlet — History

## Project Knowledge

### Day 1 Context
- **Project:** petclinic-ai-modernization-labs
- **User:** Max Bush (Solution Engineer)
- **Goal:** Create 7 detailed markdown labs (Labs 0-6) teaching AI modernization
- **Base App:** Spring PetClinic
- **Output:** Documentation only — no code generation

### Lab Series Overview
- Lab 0: Legacy Baseline & AI Readiness
- Lab 1: In-App AI with RAG (Assistive AI)
- Lab 2: AI-Assisted Actions with Human-in-the-Loop
- Lab 3: Single-Agent Workflows (Goal-Oriented AI)
- Lab 4: Multi-Agent System (MAS)
- Lab 5: Platform & Governance (Enterprise AI)
- Lab 6: AI-Native Product Re-Thinking (Capstone)

## Learnings

### Lab File Organization (Session 1)

**File Naming Convention:** `lab-NN-kebab-case-title.md`
- Format ensures consistent alphabetic ordering (00-06)
- Kebab case titles are readable in filesystem and URLs
- Examples: `lab-00-legacy-baseline.md`, `lab-05-platform-governance.md`

**Structure Decisions:**
1. **Single README.md at labs/ root:** Introduces the series, lists all labs with themes, defines prerequisites, explains progression
2. **Modular lab files:** Each lab is self-contained with context, activities, checkpoints, outputs, teaching moments, and reflection
3. **Progressive capability expansion:** Labs 0→6 follow a clear path from assessment to reengineering
   - Labs 0-2: Foundation (assess, Q&A, approval workflows)
   - Labs 3-4: Reasoning (single agent, multi-agent)
   - Lab 5: Scale (platform, governance)
   - Lab 6: Reimagine (product architecture)
4. **Placeholder content structure:** Each lab file includes:
   - Context + theme
   - "What this lab proves" (strategic value)
   - Key activities with checkboxes
   - Checkpoint validation
   - Outputs definition
   - Teaching moment (key insight)
   - Reflection questions
   - Next steps bridge

**Design Rationale:**
The structure respects the Labs 0→6 progression from the descriptions while making prerequisites explicit. Each lab builds observable capability (RAG, agents, governance) rather than teaching concepts in isolation. The README introduces the series for all audiences (PM, engineer, security) by showing what each role gets from the progression.

**Governance Alignment:**
This structure supports CJ's content authoring: Each lab file provides the narrative skeleton and activity framework. CJ can fill in the "Teaching Moment" and detailed procedures without restructuring. Josh can verify technical patterns in "What this lab proves" sections. Toby can review teaching moments for conceptual coherence.