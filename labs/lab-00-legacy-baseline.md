# Lab 0: Legacy Baseline & AI Readiness

## Overview

Welcome to PetClinic AI Modernization. Before we talk about AI, we need to understand the **legacy system as it exists today**. This lab is about discovery, not transformation.

You'll explore a real enterprise application—the Spring PetClinic—and identify where human judgment currently makes decisions. Then, you'll map where AI *could* add value, without building or deploying any AI yet.

**The Core Teaching Moment:** "Before asking how to add AI, you must ask where AI creates product value."

---

## Learning Objectives

By the end of this lab, you will:

1. **Understand the PetClinic domain** — explore Owners, Pets, Visits, and Vets
2. **Identify human judgment** — find decisions made manually today
3. **Discover hidden data** — uncover visit notes, history, and patterns that could inform AI
4. **Map AI opportunities** — create an opportunity list for Q&A, summaries, and recommendations
5. **Document constraints** — identify safety, accuracy, and approval boundaries
6. **Visualize the baseline** — draw the pre-AI architecture

---

## Prerequisites

- Git installed and available in your terminal
- Java 17+ and Maven 3.8+ (for running the app)
- A text editor or IDE (VS Code, IntelliJ, etc.)
- ~45 minutes of time
- **No AI knowledge required** — this is pure exploration

---

## Time Estimate

**45 minutes** including setup, exploration, and documentation

---

## Step-by-Step Instructions

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
✅ PetClinic is a real 3-layer enterprise application with Owner → Pet → Visit relationships  
✅ The application captures rich **visit descriptions** that are currently only reviewed manually  
✅ Human staff make several routine decisions (vet matching, follow-ups, trend detection)  
✅ These decisions are **opportunities for AI assistance**, not replacement  
✅ Safety, accuracy, and approval workflows will be critical constraints  

### Key Insight
The data is already there. Visit descriptions, visit history, vet specialties—these form a rich foundation for AI. But the value isn't in automating decisions; it's in **augmenting human judgment with insights they don't have time to extract today**.

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
