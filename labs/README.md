# AI Modernization Labs

A structured 7-lab progression teaching AI integration patterns on Spring PetClinic.

## Overview

This lab series guides you from legacy baseline through enterprise-scale AI governance. Each lab builds on the previous, introducing new AI capabilities, architectural patterns, and governance practices. The progression moves from *"where customers actually are"* to *"where AI reshapes the product entirely."*

**Duration:** ~40-50 hours total across all labs  
**Prerequisites:** Basic knowledge of Spring Boot, REST APIs, and relational databases

---

## Lab Progression

### **Lab 0: Legacy Baseline & AI Readiness**
- **Theme:** Start where customers actually are
- **Mindset:** No AI, no cloud assumptions, no refactors yet
- **What you'll prove:** This is a real legacy enterprise app; AI is not "added" yet—only assessed
- **Key outcomes:** AI opportunity map, constraints list, baseline architecture diagram
- **Duration:** ~6 hours

---

### **Lab 1: In-App AI with RAG (Assistive AI)**
- **Theme:** AI answers questions inside the application
- **Mindset:** AI as a feature, not a chatbot
- **What you'll prove:** AI can deliver value without changing workflows; RAG fits naturally into legacy apps
- **Key outcomes:** "Ask about a patient" capability with citations and confidence bounds
- **Duration:** ~7 hours
- **Prerequisites:** Complete Lab 0

---

### **Lab 2: AI-Assisted Actions with Human-in-the-Loop**
- **Theme:** AI proposes, humans decide
- **Mindset:** AI drafts, people approve
- **What you'll prove:** Enterprises don't fear AI—they fear uncontrolled AI; human-in-the-loop is a design feature, not a constraint
- **Key outcomes:** Draft artifacts with approval checkpoints and explainability metadata
- **Duration:** ~8 hours
- **Prerequisites:** Complete Lab 1

---

### **Lab 3: Single-Agent Workflows (Goal-Oriented AI)**
- **Theme:** AI reasons across steps
- **Mindset:** From suggestions → goal pursuit
- **What you'll prove:** Agents are not automation scripts; reasoning loops ≠ uncontrolled behavior
- **Key outcomes:** Clinical Assistant Agent with tool-constrained execution and observable reasoning
- **Duration:** ~8 hours
- **Prerequisites:** Complete Lab 2

---

### **Lab 4: Multi-Agent System (MAS)**
- **Theme:** Separation of cognitive responsibilities
- **Mindset:** Teams scale intelligence by separating thinking
- **What you'll prove:** Complex decisions should never live in one prompt; multi-agent design improves safety and clarity
- **Key outcomes:** Agent role contracts, orchestration flows, conflict resolution strategy
- **Duration:** ~9 hours
- **Prerequisites:** Complete Lab 3

---

### **Lab 5: Platform & Governance (Enterprise AI)**
- **Theme:** Many teams, one AI platform
- **Mindset:** Innovation locally, governance centrally
- **What you'll prove:** AI must be governed like any other enterprise platform; teams should not reinvent prompts, models, or safety rules
- **Key outcomes:** Centralized AI platform architecture with policy enforcement and telemetry
- **Duration:** ~9 hours
- **Prerequisites:** Complete Lab 4

---

### **Lab 6: AI-Native Product Re-Thinking (Optional Capstone)**
- **Theme:** Design the app around AI
- **Mindset:** If we built this today, what would change?
- **What you'll prove:** AI is not an enhancement—it reshapes UX; CRUD is no longer the primary interaction model
- **Key outcomes:** AI-native UX concepts, re-imagined architecture, "if we started today" narrative
- **Duration:** ~7 hours
- **Prerequisites:** Complete Lab 5 (optional capstone; can be skipped)

---

## How to Use These Labs

1. **Start with Lab 0.** Do not skip. It establishes the domain model and grounds all subsequent labs in real customer context.
2. **Follow the sequence 0→6.** Each lab assumes knowledge and code artifacts from the previous lab.
3. **Read each lab fully before starting.** Labs are self-contained; they include setup, activities, checkpoints, and reflection.
4. **Hands-on work.** Each lab involves writing code, running queries, or designing interactions. Avoid copying snippets; understand *why* each pattern exists.
5. **Document your constraints.** As you progress, keep a running log of safety rules, approval gates, and governance decisions. Lab 5 will ask you to formalize them.

---

## Core Principles Across All Labs

- **Start with value, not technology.** Every lab begins by asking "where does this solve a real customer problem?"
- **Humans are the governors, not the governed.** No feature is ever deployed without human visibility, understanding, and approval.
- **Observe and iterate.** Each lab includes reflection checkpoints. Use them to question assumptions.
- **Safety scales with scope.** As AI capabilities expand (Labs 0→5), governance complexity increases by design.

---

## Outcomes by Discipline

### For **Product Managers:**
- Lab 0: Identify where AI adds product differentiation
- Lab 1: Scope MVP features (RAG, Q&A)
- Lab 2: Design approval workflows
- Lab 3-5: Plan rollout and governance strategy
- Lab 6: Reimagine the product experience

### For **Engineers:**
- Lab 0: Map domain entities and constraints
- Lab 1: Integrate RAG and vector search
- Lab 2: Implement approval workflows
- Lab 3: Build single-agent reasoning loops
- Lab 4: Orchestrate multi-agent collaboration
- Lab 5: Deploy centralized AI platform
- Lab 6: Rearchitect for AI-native interactions

### For **Security & Compliance:**
- Lab 0: Identify data usage and sensitivity
- Lab 1: Scope retrieval safety rules
- Lab 2: Design audit trails
- Lab 3-5: Enforce governance policies
- Lab 6: Evaluate new risk surface

---

## File Structure

```
labs/
├── README.md                          # This file
├── lab-00-legacy-baseline.md          # Lab 0
├── lab-01-assistive-ai-rag.md         # Lab 1
├── lab-02-human-in-loop.md            # Lab 2
├── lab-03-single-agent.md             # Lab 3
├── lab-04-multi-agent.md              # Lab 4
├── lab-05-platform-governance.md      # Lab 5
└── lab-06-ai-native-capstone.md       # Lab 6
```

---

## Getting Help

- **Lab concepts unclear?** Reread the theme and mindset at the top of the lab. They explain *why* this pattern exists.
- **Code not running?** Check the prerequisites section. You may have missed a dependency from a previous lab.
- **Architecture question?** Review the Lab 0 baseline diagram. All subsequent labs build on it.
- **Governance question?** Skip to Lab 5 and read the platform architecture section, then return to your current lab.

---

## Feedback & Updates

These labs evolve. If you discover:
- **Unclear instructions:** File an issue with the specific lab number and section.
- **Missing prerequisites:** Check if the activity assumes code from a prior lab.
- **Outdated model names or API signatures:** Verify against the model provider's latest docs.

---

**Last updated:** 2024  
**Maintained by:** Max Bush, Solution Engineer
