# Lab 0: Legacy Baseline & AI Readiness

## Overview

Welcome to PetClinic AI Modernization. Before we talk about AI, we need to understand the **legacy system as it exists today**. This lab is about discovery, not transformation.

You'll first establish a supported Java 21 baseline with GitHub Copilot app modernization, then explore a real enterprise application—the Spring PetClinic—and identify where human judgment currently makes decisions. After that, you'll map where AI *could* add value, without building or deploying any AI yet.

**The Core Teaching Moment:** "Before asking how to add AI, first create a stable baseline—then ask where AI creates product value."

---

## Learning Objectives

By the end of this lab, you will:

1. **Establish a modernized baseline** — use GitHub Copilot app modernization to review and apply a Java 17 → Java 21 upgrade plan
2. **Understand the PetClinic domain** — explore Owners, Pets, Visits, and Vets
3. **Identify human judgment** — find decisions made manually today
4. **Discover hidden data** — uncover visit notes, history, and patterns that could inform AI
5. **Map AI opportunities** — create an opportunity list for Q&A, summaries, and recommendations
6. **Document constraints** — identify safety, accuracy, and approval boundaries
7. **Visualize the baseline** — draw the pre-AI architecture

---

## Prerequisites

- Git installed and available in your terminal
- VS Code 1.106+ with GitHub Copilot enabled
- GitHub Copilot app modernization installed in VS Code (restart VS Code after installation if prompted)
- Java 21+ and Maven 3.8+ (the modernization step upgrades the project before you run it)
- ~60 minutes of time
- **No AI knowledge required** — this is modernization plus exploration

---

## Time Estimate

**60 minutes** including runtime modernization, exploration, and documentation

---

## Step-by-Step Instructions

### Step 00: Modernize the Baseline Before Adding AI

Before you analyze AI readiness, put the application on a current LTS runtime. This keeps the rest of the lab focused on product value instead of mixing AI work with avoidable Java runtime drift.

1. Open the repository folder in VS Code.

2. If VS Code shows this prompt, accept it:
   > "This project is using an older Java runtime (17). Would you like to install GitHub Copilot app modernization extension and upgrade it to Java 21 (LTS)?"

   If you do **not** see the prompt, install GitHub Copilot app modernization manually and restart VS Code if asked.

3. Open the GitHub Copilot app modernization pane in the sidebar. App modernization can also be started from the Quickstart panel or Copilot Chat, but for this lab use the sidebar pane so you can watch the workflow step by step.

4. Choose `Upgrade Runtime & Frameworks` and review the proposed plan. The extension can analyze the project, propose an upgrade plan, and prepare plan/progress artifacts before it changes code.

5. Let the modernization workflow run. It may check out a new branch, execute transformations, automatically fix issues during progress, and run build or validation loops while recording commits, logs, output, and a final summary.

6. Review the summary carefully when the run finishes. If the results look good, keep the upgraded branch or working tree and use that as your baseline for the rest of Lab 0.

7. Capture a few comparison notes before moving on:
   - What changed between the Java 17 baseline and the Java 21 baseline?
   - Which fixes happened automatically?
   - What build warnings, errors, or compatibility concerns were removed?

> **Why this happens now:** Later labs are about AI patterns, retrieval, approval, and governance. Upgrading first reduces noise so you can evaluate AI opportunities on a cleaner baseline.

> **Note:** App modernization can also support assessment, planning, transformations, security validation, deployment workflows, and separate unit-test generation. In this lab, stay focused on the runtime/framework upgrade and the summary of what changed.

### Step 1: Clone and Explore the Repository

1. Open your terminal and navigate to a working directory.

2. Clone the petclinic-ai-modernization-labs repository:
   ```bash
   git clone https://github.com/your-org/petclinic-ai-modernization-labs.git
   cd petclinic-ai-modernization-labs
   ```

3. List the main directories:
   ```bash
   ls -la
   ```

   You should see:
   - `src/` — the Spring application code
   - `labs/` — lab documentation
   - `pom.xml` — Maven build file
   - `readme.md` — project README

> **Note:** This is a Spring Framework application with a 3-layer architecture: Web (UI) → Service (business logic) → Repository (data access). No cloud, no AI yet—just a classic enterprise application.

---

### Step 2: Start PetClinic Locally

Use the upgraded branch or working tree from Step 00 so the rest of the lab reflects your Java 21 baseline.

1. Build and start the application:
   ```bash
   ./mvnw jetty:run-war
   ```
   
   On Windows:
   ```bash
   mvnw.cmd jetty:run-war
   ```

2. Wait for the message indicating the server has started (usually takes 10-30 seconds).

3. Open your browser and visit:
   ```
   http://localhost:8080/
   ```

   You should see the PetClinic home page with a navigation menu.

> **Teaching Moment:** This is a real enterprise web application running on Jetty. It uses a database (H2 in-memory by default) and serves dynamic content. This is what "legacy" looks like: simple, stable, proven. No complex infrastructure. Now let's see what's inside.

---

### Step 3: Explore the Domain (Owners, Pets, Visits)

In the PetClinic browser window, explore each major entity:

#### **3.1 Owners**
1. Click **"Find Owners"** in the menu.
2. Search for a last name (e.g., "Davis") or leave blank to see all.
3. Click on an owner to view their profile.
4. **Observe:** What data is captured?
   - Name, address, city, telephone
   - List of pets
   - Each pet's name, birth date, type (Dog, Cat, Bird, etc.)

5. **Question to ask yourself:** *If AI were to assist with owner communications or pet care recommendations, what information would it need?*

#### **3.2 Visits (The Hidden Goldmine)**
1. From an owner's profile, click on a pet name.
2. Scroll down to see the **"Visit(s)"** section.
3. Examine a visit record. Each visit has:
   - **Date** (when the visit happened)
   - **Description** (what the vet noted during the visit)
   - **Pet** (which pet was seen)

4. **This is critical:** The Description field is **free-form text**—human judgment encoded in natural language. Examples might be:
   - "Annual checkup. No issues noted. Continue current diet."
   - "Mild ear infection. Prescribed antibiotics. Recheck in 2 weeks."
   - "Weight concern. Discussed diet changes with owner."

5. **Key insight:** Visit descriptions are a rich data source that an AI system could analyze.

#### **3.3 Vets (Expertise)**
1. Click **"Veterinarians"** in the menu.
2. See a list of vets and their specialties (Surgery, Dentistry, Radiology, etc.).

3. **Observe:** Vets are matched to pets based on specialty and availability. This is a resource allocation problem that could benefit from intelligent scheduling or recommendations.

> **Teaching Moment:** The human judgment here is **implicit**: a staff member mentally matches a pet's needs to a vet's skills. An AI system could formalize and accelerate this matching.

---

### Step 4: Identify Where Human Judgment Exists Today

Now that you've explored the UI, think about the **decisions** being made manually:

| **Decision Point** | **Today (Manual)** | **Data Available** | **Why This Matters** |
|---|---|---|---|
| **Pet Care Recommendations** | Staff or vet recalls past visits, suggests care | Visit history in description field | AI could surface patterns across multiple visits |
| **Vet Assignment** | Staff manually checks specialty, availability | Pet type, vet specialty, visit history | AI could rank best vet matches |
| **Owner Communication** | Staff writes follow-up messages from memory | Visit outcomes, pet history, notes | AI could draft summaries or reminders |
| **Health Insights** | Vet reviews notes to spot trends | Multiple visits per pet over years | AI could detect patterns (recurring issues, weight trends) |
| **Appointment Scheduling** | Staff coordinates vet availability | Vet specialties, pet needs, owner availability | AI could suggest optimal time slots |

> **Note:** We are **not** building AI to automate these yet. We're just identifying where it *could* help.

---

### Step 5: Map AI Opportunities

Create a file called `ai-opportunities.md` in your working directory. Document the following:

#### **5.1 AI Use Cases**

For each decision point above, list **what AI could do**:

```markdown
# AI Opportunities in PetClinic

## 1. Visit Summary & Insights
- **What:** Generate a summary of a pet's visit history to highlight trends
- **Input:** Visit descriptions (raw text)
- **Output:** "Max has had 3 ear infections in the past year. Consider preventative care."
- **Value:** Helps vets and staff spot patterns quickly
- **Constraint:** Summaries must be reviewed by a vet before sharing with owners

## 2. Vet Recommendation Engine
- **What:** Suggest the best vet for a new visit based on pet history and specialty
- **Input:** Pet type, visit history, vet specialties
- **Output:** "Recommend Dr. Helen Leary (Surgery specialist). Max had ear surgery in 2022."
- **Value:** Faster scheduling, better matching
- **Constraint:** Staff must confirm the recommendation before booking

## 3. Owner Communication Draft
- **What:** Auto-generate a follow-up message after a visit
- **Input:** Visit description, pet name, owner name
- **Output:** "Dear George, Max's checkup went well. Please follow the diet recommendations..."
- **Value:** Reduces staff time writing routine messages
- **Constraint:** A person must review and approve before sending

## 4. Preventative Care Alerts
- **What:** Flag pets due for routine care (vaccines, checkups) based on history
- **Input:** Visit history, pet type, age
- **Output:** "Max is overdue for annual checkup (last: 2023-06-15)"
- **Value:** Improves preventative care, increases revenue
- **Constraint:** Must respect owner preferences (don't spam)
```

> **Teaching Moment:** Notice the pattern: **AI suggests, humans decide.** This is the foundation of responsible AI in enterprise systems.

---

### Step 6: Document Constraints & Safety Boundaries

List the **constraints** that will govern any AI system we build:

```markdown
## Safety & Accuracy Constraints

### Medical Safety
- AI-generated recommendations must never replace veterinary judgment
- Summaries of visits must be clearly marked as AI-generated
- Any medical advice must be reviewed by a licensed vet

### Data Privacy
- Owner and pet data is sensitive; AI must not leak PII
- Visit descriptions contain medical information; secure handling required

### Approval Workflows
- AI suggestions for owner communication must be human-approved before sending
- Health trend summaries should be reviewed before sharing with owners
- Vet assignments are recommendations, not automatic

### Accuracy Requirements
- Visit summaries must be factually accurate (no hallucinations)
- Trend detection must cite actual visit records
- Recommendations must have confidence scores

### Operational
- AI should not replace human vet expertise
- Staff must understand why AI made a suggestion (explainability)
- Easy rollback if AI quality drops
```

> **Note:** These constraints will guide how we build and deploy AI in later labs.

---

### Step 7: Visualize the Baseline Architecture

Create a text-based or simple diagram showing the current PetClinic architecture.

Save this as `baseline-architecture.md`:

```markdown
# PetClinic Baseline Architecture (Pre-AI)

```
┌──────────────────────────────────────────────────────────────┐
│                     Web Layer (UI)                            │
│  - Owner Search, Pet Details, Visit Records, Vet List        │
│  - JSP/Thymeleaf Templates, Spring MVC Controllers           │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │ HTTP Requests
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                   Service Layer (Business Logic)             │
│  - ClinicService: Facade for all operations                  │
│  - Transactions, Caching, Business Rules                     │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │ Method Calls
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                  Repository Layer (Data Access)              │
│  - OwnerRepository, PetRepository, VisitRepository           │
│  - JPA Entities mapped to database                           │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │ SQL
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    H2 In-Memory Database                      │
│  - owners, pets, visits, vets tables                         │
│  - Sample data pre-loaded at startup                         │
└──────────────────────────────────────────────────────────────┘
```

## What's Missing (Today)
- No AI/ML components
- No async tasks or event streaming
- No external integrations (no SMS, email, analytics)
- No audit logging (who changed what, when)
- No role-based access control (everyone sees everything)

## Future: Where AI Will Integrate
- **New AI Service Layer** (future labs): Handles LLM calls, embeddings, RAG
- **Event Bus** (future labs): Triggers AI workflows on data changes
- **Approval Workflow** (future labs): Human-in-the-loop decision gates
- **Vector Store** (future labs): Embedding-based search for visit history
```

---

### Step 8: Verification Checkpoint

Stop the PetClinic server (Ctrl+C in your terminal) and verify your work:

**Checklist:**
- [ ] You reviewed the GitHub Copilot app modernization plan and final summary
- [ ] You compared the Java 17 baseline with the Java 21 upgraded baseline before moving on
- [ ] PetClinic ran successfully at http://localhost:8080
- [ ] You explored at least 2 Owner profiles and their Pets
- [ ] You viewed at least 1 Visit record with description text
- [ ] You saw the Veterinarians list and noted their specialties
- [ ] You created `ai-opportunities.md` with at least 3 use cases
- [ ] You created a constraints list documenting safety boundaries
- [ ] You documented the baseline architecture

**Example file structure:**
```
your-working-directory/
├── ai-opportunities.md
├── constraints.md
├── baseline-architecture.md
└── notes.txt (optional: your observations)
```

---

## Summary & What's Next

### What You Learned
✅ You established a Java 21-ready baseline before discussing AI changes  
✅ PetClinic is a real 3-layer enterprise application with Owner → Pet → Visit relationships  
✅ The application captures rich **visit descriptions** that are currently only reviewed manually  
✅ Human staff make several routine decisions (vet matching, follow-ups, trend detection)  
✅ These decisions are **opportunities for AI assistance**, not replacement  
✅ Safety, accuracy, and approval workflows will be critical constraints  

### Key Insight
The data is already there. Visit descriptions, visit history, vet specialties—these form a rich foundation for AI. But the value isn't in automating decisions; it's in **augmenting human judgment with insights they don't have time to extract today**. That becomes easier to evaluate once the application is running on a current, supportable baseline.

### What's Coming
- **Lab 1:** Build an in-app AI assistant using RAG (Retrieval-Augmented Generation) to answer questions about a pet's history
- **Lab 2:** Add AI-suggested actions with human approval workflows
- **Lab 3:** Build goal-oriented AI agents that can coordinate multi-step tasks
- **Lab 4+:** Advanced orchestration, governance, and product thinking

---

## Resources

- **PetClinic Source Code:** `src/main/java/org/springframework/samples/petclinic/`
- **Domain Models:** `src/main/java/org/springframework/samples/petclinic/model/` (Owner, Pet, Visit, Vet classes)
- **Service Layer:** `src/main/java/org/springframework/samples/petclinic/service/ClinicServiceImpl.java`
- **Spring PetClinic Docs:** http://fr.slideshare.net/AntoineRey/spring-framework-petclinic-sample-application

---

## Questions for Reflection

As you move forward, keep these in mind:

1. **Where is data being created but not fully used?**
   - Visit descriptions capture vet judgment. How could an AI surface patterns in those notes?

2. **What routine decisions could be accelerated?**
   - Today, scheduling a visit requires finding a matching vet manually. Could AI speed this up?

3. **What decisions should remain human-controlled?**
   - Medical recommendations must always go through a vet. How do we enforce this in code?

4. **How will we know if AI is helping?**
   - Fewer staff scheduling errors? Faster response times? More preventative care?

---

**Ready to move on?** In Lab 1, you'll build your first AI feature: an in-app assistant that uses the visit history you explored today to answer owner questions intelligently.
