# Lab 6: AI-Native Product Re-Thinking (Optional Capstone)

**Theme:** Design the app around AI  
**Duration:** ~7 hours  
**Prerequisites:** Completed Lab 5 (or very familiar with Labs 1-5)

---

## Context

Labs 1-5 treated PetClinic as fixed: Here's a legacy app; add AI to it. Lab 6 inverts the question: **If we were building PetClinic from scratch today, knowing what we know about AI, what would we build differently?**

This is not implementation. It's architecture re-imagination. It's asking whether CRUD-based interfaces are still the right design when AI can mediate human-computer interaction.

---

## What This Lab Proves

1. **AI is not an enhancement—it reshapes UX.** Once you have agents that can reason and decide, screen-by-screen interaction feels like a legacy pattern.
2. **CRUD is no longer the primary interaction model.** Instead of "open screen → find record → edit fields → save," you have "state intent → AI handles execution → show results."
3. **Event-first, insight-first design changes architecture.** When AI is the primary interface, the underlying data model and event flow must support continuous reasoning, not batch transactions.

---

## Key Activities

### Activity 1: Challenge the Current UX
Start with PetClinic's current experience:
- [ ] Owner logs in → searches for pet → views visits → reads notes → decides on next action
- For each step, ask: **Does an AI-first interface change this?**
  - Could the system proactively surface relevant visits? (not wait for search)
  - Could it recommend next actions without the vet clicking? (not wait for vet decision)
  - Could it learn vet preferences and adapt the interface? (not show one-size-fits-all)

### Activity 2: Reimagine Interaction Flows
- [ ] Design an AI-native workflow: Vet starts visit → AI observes → AI provides real-time suggestions → Vet approves or overrides → System executes
- [ ] Replace "view notes" with "understand pet context" (AI synthesizes across all notes, history, patterns)
- [ ] Replace "create visit record" with "declare outcome → AI generates artifact → Vet approves"
- [ ] Replace "plan follow-up" with "AI recommends timing and type → Vet confirms"

### Activity 3: Rethink Data & Event Architecture
Current architecture: Records → Screens → Forms → Database  
AI-native architecture: **Events → Reasoning → Artifacts → Persistence**
- [ ] What events trigger AI reasoning? (visit created, note entered, problem flagged)
- [ ] What data must be available in real-time for AI to suggest? (not just at query time)
- [ ] How does the data model change if AI is constantly reasoning over it?
- [ ] What does "audit trail" look like when AI decisions are continuous?

### Activity 4: Design for AI Failure & Fallback
- [ ] What happens if AI suggests something and the vet rejects it?
- [ ] Can the system learn from rejections? (or is that too risky)
- [ ] What does the UI look like when AI is unavailable? (system must degrade)
- [ ] How do you onboard new vets who haven't trained the AI on their preferences?

### Activity 5: Create "If We Started Today" Narrative
- [ ] Write a design document: "PetClinic re-imagined for AI"
- [ ] Include wireframes/mockups of key screens (intent-driven, not CRUD)
- [ ] Describe the data model (event-first? real-time? streaming?)
- [ ] Explain architectural changes required to support AI-first interaction

---

## Checkpoint 1: Re-Imagined Design
Before completing this lab, verify:
- [ ] You've critiqued at least 3 existing PetClinic screens and proposed AI-native alternatives
- [ ] You've sketched at least one end-to-end AI-native workflow
- [ ] You've identified data model changes required to support continuous reasoning
- [ ] You've designed graceful degradation for when AI is unavailable or uncertain

---

## Outputs from This Lab

### Output 1: AI-Native UX Concepts
Designs for how veterinarians would interact with PetClinic if it were built from scratch with AI in mind:
- Intent-driven workflows (instead of CRUD screens)
- Real-time suggestions (instead of passive data display)
- Continuous reasoning (instead of point-in-time decisions)

### Output 2: Re-Imagined Architecture Diagram
A high-level architecture showing:
- Event streams (what triggers reasoning)
- AI reasoning layer (continuous, not on-demand)
- Artifact generation (summaries, plans, messages generated continuously)
- Approval & execution (vet confirms before persistence or communication)
- Fallback modes (what happens if AI is unavailable)

### Output 3: "If We Started Today" Narrative
A document describing:
- What would change from the current PetClinic architecture
- What problems does AI-native design solve that CRUD cannot?
- What new problems emerge? (complexity, latency, model behavior)
- What would be the hardest migration path from current to AI-native?

---

## Teaching Moment

> **"AI maturity ends when AI becomes invisible—but indispensable."**

The early stage of AI is visible agents: You see the reasoning, approve the decisions, control the behavior. That's good for safety and trust.

But mature AI-native products hide the agent layer entirely. The user perceives intent-driven interaction, not agent choreography. "I want a follow-up in two weeks" becomes a simple statement; the AI handles the rest (scheduling, messaging, reminders, escalation if needed).

This lab asks: What would that look like?

---

## Reflection Questions

Complete these before finalizing Lab 6:

1. **What's one feature of current PetClinic that would be fundamentally different in an AI-native version?**
2. **What data would AI need access to that it doesn't have today?**
3. **What decisions should vets always approve, even in an AI-native system? Why?**
4. **If you had infinite resources, what would you build first to move toward AI-native?**
5. **What legacy constraints from the current system would you drop?**

---

## Next Steps

Lab 6 is the capstone. **You are finished.**

If you completed Labs 0-6:
- You understand the full spectrum of AI integration: from assessment (Lab 0) to re-architecture (Lab 6)
- You can explain why governance matters (Lab 5) and how to build it
- You can design safe AI interactions (Labs 1-4) without reinventing wheels
- You can speak to executives about the strategic implications of AI (Labs 3, 4, 6) and to engineers about implementation (Labs 1-2, 5)

---

## Reflection: What You've Built

Over 40-50 hours across 7 labs, you've done the following:

| Lab | What You Built | Why It Matters |
|---|---|---|
| 0 | AI Opportunity Map | You identified where AI creates value, not just hype |
| 1 | Grounded Q&A (RAG) | You proved AI can augment without replacing |
| 2 | Human-in-the-Loop Drafting | You proved AI can be safe with oversight |
| 3 | Single Agent | You proved reasoning scales without runaway automation |
| 4 | Multi-Agent System | You proved complex decisions need multiple perspectives |
| 5 | Enterprise Platform | You proved AI can be governed and scaled |
| 6 | AI-Native Re-Architecture | You proved AI reshapes products, not just processes |

Each step builds confidence: from "can we trust AI?" (Labs 1-2) to "how do we scale it?" (Labs 4-5) to "how do we rethink around it?" (Lab 6).

---

## Deep Dive: Design Exercises

### Exercise 1: Deconstruct Current PetClinic

Start by analyzing how PetClinic works today. Pick one common vet workflow:

**Scenario: A returning pet owner calls in with a concern about their dog's recurring ear infection.**

*Current workflow:*
1. Receptionist answers phone → logs call → schedules visit
2. Visit day: Vet reviews owner's note → pulls history → examines pet
3. Vet documents findings → selects diagnosis → prescribes treatment
4. Staff schedules follow-up → sends owner instructions via text/email
5. Follow-up: Vet reviews outcome notes → determines next treatment

*What's wrong with this:*
- Information is siloed: Receptionist doesn't know vet will need detailed ear history
- Vet manually searches for relevant visits (2023 ear exam? 2021 treatment?)
- No pattern recognition: Is this actually a chronic issue? Was the prior treatment incomplete?
- Decisions are point-in-time: Vet decides treatment *during* visit, not informed by patterns
- Follow-up is manual: Vet has no reminder that outcomes matter; infection is "resolved" until owner calls again

**Your task:** For this scenario, write out what an **AI-native version** looks like.

*Example AI-native flow (not implementation, just interaction):*
1. Owner calls with concern → Receptionist states intent: "Recurring ear concern"
2. System (AI) immediately:
   - Surfaces entire ear treatment history (2021 initial, 2022 follow-up, 2023 recurrence)
   - Flags pattern: "Infection recurred 8 months after prior treatment"
   - Suggests: "Prior treatment was antibiotic-only; consider addressing underlying cause"
   - Recommends: "Schedule extended visit; pre-flag for allergy testing"
3. Vet arrives; AI presents:
   - Visual timeline of ear issues and treatments
   - Flagged contraindications ("Dog is sensitive to Bactrim; check before prescribing")
   - Suggested examinations ("Check for allergies, consider ear cytology")
4. Vet examines pet → enters findings
5. AI (in real-time):
   - Analyzes findings against history
   - Suggests diagnosis with confidence level
   - Recommends treatment options with success rates for *this specific pet*
   - Flags: "Treatment X failed in 2022; recommend Y instead"
6. Vet approves treatment
7. System:
   - Generates owner message explaining issue and plan
   - Schedules automatic follow-up: "Check in after 5 days"
   - Sets reminders for vet: "Review outcome on Day 7; if infection persists, escalate to specialist"
8. Day 5: Owner reports improvement; AI notes this
9. Day 10: AI alerts vet: "Still not fully healed; recommend specialist consult" (proactive, not reactive)

**Now do this for:**
- Scheduling a new patient visit
- Diagnosing a complex case with multiple symptoms
- Sending owner aftercare instructions
- Deciding whether a pet needs hospitalization

For each, identify:
- **What information is currently scattered?** (Where would AI need to synthesize?)
- **What decisions are made in the dark?** (Where would pattern recognition help?)
- **What follow-ups are forgotten?** (Where would continuous reasoning help?)
- **What could be proactive instead of reactive?** (Where could AI suggest before the user asks?)

---

### Exercise 2: Design Intent-Driven Interfaces

In current PetClinic, users navigate screens: login → search → view → edit → save.

In AI-native PetClinic, users **declare intent** and AI handles execution.

**Redesign these interactions:**

#### Original: Create Visit Record
Current flow:
- Vet clicks "New Visit"
- Fills form: date, pet, owner, reason, findings, diagnosis, treatment
- Clicks Save

AI-native alternative:
- Vet (in the exam room) says: "Golden retriever, ear infection, looks like recurring issue from 2022, starting antibiotics and prednisone, follow-up in 10 days"
- System:
  - Extracts intent (diagnosis, treatment, follow-up)
  - Cross-checks: Is the treatment appropriate? Any contraindications?
  - Generates visit record
  - Drafts owner message
  - Schedules follow-up task
  - Vet reviews and approves (or edits)

Your turn: Redesign these:
1. **Search pet's history** → Instead of vet typing a name, how does AI surface relevant history proactively?
2. **Schedule follow-up visit** → Instead of clicking "Schedule," how does AI recommend timing and type?
3. **Send owner instructions** → Instead of copy-pasting templates, how does AI generate personalized instructions?
4. **Flag drug interaction** → Instead of vet manually checking, how does AI catch this automatically?

For each, sketch:
- **User input:** What does the vet *actually say or do*?
- **AI processing:** What does the system do behind the scenes?
- **Presentation:** How does the result show up for vet approval?
- **Fallback:** What if AI is unavailable?

---

### Exercise 3: Reimagine the Data Model

Current PetClinic data model is **record-centric**:
```
Pet → Visit → VetNote
    → Diagnosis
    → Prescription
```

Each record is created, then static. Data flows: human → form → database.

**AI-native data model is event-centric**:
```
Event Stream:
  - visit_started
  - observation_recorded (real-time from vet)
  - ai_suggestion_generated
  - vet_decision_made
  - outcome_recorded
  
Real-Time State:
  - current_pet_profile (continuously updated, AI-synthesized)
  - active_issues (patterns AI detected)
  - pending_decisions (what needs vet approval)
  - follow_up_obligations (when should system remind vet)
```

This changes everything:
- **Writes:** AI records events, not final states. "Vet suspected ear infection" is different from "Vet diagnosed ear infection."
- **Reads:** AI queries not just historical records, but *live events*. This enables real-time suggestions.
- **Reasoning:** AI can reason *as the visit happens*, not after.

**Your task:**
1. List the key events in a typical vet visit (before, during, after)
2. For each event, ask: **What should AI do immediately when this event fires?**
   - When visit_started → AI surfaces pet history
   - When observation_recorded → AI suggests next examination
   - When vet_decision_made → AI checks for contraindications
   - etc.
3. Design the audit trail: If AI suggested something and vet accepted it, what gets logged?
   - Just the final state? (audit nightmare)
   - Every event? (too much noise)
   - Decisions + reasoning? (right balance)

---

### Exercise 4: Handle Failure Gracefully

AI-native systems are more capable but also more complex. What goes wrong, and how do you design graceful degradation?

**Scenario: AI suggests a diagnosis, but the vet strongly disagrees.**

Current system: Vet ignores AI and makes own decision (AI learns nothing, fails silently).

AI-native system: 
- Vet's rejection is itself an event: "ai_suggestion_rejected"
- Vet documents reasoning: "I think it's allergies, not infection" (or just overrides)
- System captures: This case was edge case for AI model; vet had a better intuition
- Over time: Does AI improve by learning from vet overrides? Can it?

**Design for these failure modes:**

1. **AI unavailable:** System loses internet; AI suggestions vanish. Vet still has to work.
   - What UI/UX changes?
   - What information is cached locally?
   - How does vet proceed without suggestions?

2. **AI uncertain:** System rates confidence at 40% for diagnosis. Should it still suggest?
   - Show uncertainty explicitly? ("Possibly ear infection (40% confident)")
   - Stay silent? (Vet notices nothing)
   - Escalate to human? (Too many false escalations)

3. **Distribution shift:** Model trained on young dogs; senior dog presents with unusual symptoms.
   - How does AI signal: "This is outside my training"?
   - Does it escalate or still suggest?
   - How does vet know whether to trust the suggestion?

4. **Adversarial input:** Owner lies about pet's history or vet intentionally gives bad data.
   - Can AI detect inconsistencies? ("You said no prior ear issues, but medical record shows 3 prior visits for ears")
   - What's the vet's obligation to verify?

For each scenario, design:
- **Detection:** How does the system know something is wrong?
- **Escalation:** Does it go to vet? Compliance team? Logged for review?
- **Recovery:** How does the system get back to normal?

---

### Exercise 5: Write the "If We Started Today" Narrative

This is your capstone artifact. Write a design document: **PetClinic re-imagined for an AI-native world.**

**Structure:**

#### 1. Executive Summary (1 page)
- What would change from current PetClinic?
- What problems does AI-native design solve?
- What's the business case? (reduced time per visit? improved outcomes? better owner experience?)

#### 2. The Vet's Day (Before & After)
Compare a day in the life of a vet in current vs. AI-native PetClinic.

*Current:*
- 8:00am: Review day's schedule (15 visits)
- 8:15am: Pull first patient's file (search by name, open record, read notes)
- 8:25am: Patient arrives; vet examines (15 min)
- 8:40am: Type visit notes (10 min)
- etc.

*AI-native:*
- 8:00am: System presents prioritized day (6 routine, 2 complex, 7 follow-ups; estimated 6 hours work)
- 8:15am: AI has already surfaced first patient's context (genetic predispositions, prior treatments, owner notes from intake form)
- 8:25am: Patient arrives; vet examines while AI suggests observations
- 8:40am: Vet says "Ear infection, recurrent, starting treatment X"; AI generates all artifacts
- etc.

What changed? Time? Cognitive load? Decision quality? Owner experience?

#### 3. Architecture Diagram
Not code, just conceptual flow:

```
┌─────────────────┐
│ Vet Interaction │ (voice, form, touch)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Event Capture   │ (convert interaction → events)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AI Reasoning    │ (real-time, async)
│ - Synthesis     │
│ - Suggestions   │
│ - Checks        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vet Approval    │ (review, edit, approve)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Artifact Gen    │ (records, messages, reminders)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Persistence     │ (event store + read models)
└─────────────────┘
```

For each box, explain:
- What goes in?
- What comes out?
- How is it different from current PetClinic?

#### 4. Data Model Changes
Show the shift from current (record-centric) to AI-native (event-centric).

Current:
```sql
visits table: id, pet_id, date, vet_id, notes, diagnosis_id, treatment_id
diagnoses table: id, name, confidence
treatments table: id, name, dosage
```

AI-native:
```sql
events table: id, timestamp, type, actor, entity, data, ai_processed
pet_profiles table: id, computed_state (JSON), last_updated
active_issues table: id, issue_type, confidence, suggested_by, vet_response
audit_log table: id, timestamp, action, actor, reasoning
```

Explain:
- Why events instead of records?
- What's in `computed_state`?
- How often is it updated?
- How do you query this for vet suggestions?

#### 5. Interaction Examples
Show 2-3 detailed scenarios using the AI-native design.

Example:
**Scenario: Recurring ear infection (same as Exercise 1, but now designed for AI-native PetClinic)**
1. Owner calls in: Vet says "Fluffy has ear infection again"
2. System captures event: `observation_reported("Fluffy", "ear infection concern")`
3. AI fires:
   - Queries pet profile: Past ear issues? Treatments? Outcomes?
   - Generates summary: "Fluffy has had 4 ear infections since 2021. Last treatment (2023) was X; recurred after 8 months."
   - Suggests: "Pattern suggests allergic component; recommend skin testing in addition to antibiotics."
4. Vet sees suggestion before patient arrives
5. During exam: Vet finds swollen ear, records: `observation_recorded("Fluffy", "ear swollen", "pink discharge")`
6. AI fires:
   - Matches pattern to prior issues
   - Checks: "Bactrim contraindicated (used in 2022, triggered vomiting)"
   - Suggests diagnosis: "Chronic otitis externa, bacterial, likely allergy-driven"
   - Suggests treatment: "Antibiotic (fluoroquinolone preferred) + topical steroid + allergy workup"
7. Vet approves (or edits) → `decision_made("Fluffy", "prescribe_X")`
8. AI fires:
   - Generates owner message: "Fluffy has chronic ear issue; we're treating infection and investigating allergies"
   - Schedules check-in: "Day 7 (verify improvement)"
   - Flags vet: "If not improving by day 10, refer to dermatologist"
9. Day 7: Owner reports "much better"
10. AI updates pet profile: "Current treatment working; continue monitoring"
11. Day 14: AI alerts vet: "Verify ear infection resolved; consider starting allergy testing"

This shows:
- Proactive AI (surfaces info before visit)
- Real-time AI (suggests during visit)
- Continuous AI (reminds after visit)
- Pattern recognition (identifies chronic issue, not just acute infection)
- Learning (captures outcomes; improves future suggestions)

#### 6. Migration Path
If you had infinite resources, how would you migrate from current to AI-native?

Options:
- **Big Bang:** Rebuild everything; switch over in one day (risky)
- **Strangler:** Gradually introduce AI-native workflows alongside current (safe but complex)
- **Parallel:** Run both systems side-by-side; measure AI-native quality before trusting it (slow)

For your approach, map:
- What gets built first? (Probably AI reasoning layer + event capture)
- What gets replaced? (Probably forms/screens → intent-driven interaction)
- What's kept? (Probably database persistence; gradually migrate to event store)
- Success criteria? (Time saved? Decisions improved? Owner satisfaction up?)

#### 7. Risks & Mitigations
What could go wrong with AI-native PetClinic?

| Risk | Impact | Mitigation |
|------|--------|-----------|
| AI suggests wrong diagnosis | Patient harmed | Vet always approves before execution; continuous model monitoring |
| System complexity high | Vet workflow degrades | Graceful fallback to manual mode; extensive training |
| Data privacy (sensitive info in events) | HIPAA violation | Encrypt at rest; redact in logs; audit access |
| Model drift (trained on past data; world changes) | AI suggestions stale | Continuous feedback loop; quarterly model retraining |
| Over-automation (vet becomes passive) | Decision quality drops | Keep high-stakes decisions human-explicit; escalate proactively |

#### 8. Success Metrics
How would you measure that AI-native redesign is working?

- **Vet productivity:** Time per visit down 20%? (Make sure it's freed up for better decisions, not burnout)
- **Decision quality:** Diagnoses more accurate? Treatments more effective?
- **Owner satisfaction:** Happier with explanations? More engaged?
- **System reliability:** Uptime? Suggestion quality? Vet override rate?
- **Safety:** Any adverse events? How caught?

---

## Reflection Questions

Before you finish Lab 6, reflect deeply on these:

1. **What's one feature of current PetClinic that would be unrecognizable in an AI-native version?**
   - E.g., "Search" becomes "proactive context surfacing"
   - Think about what this reveals about how AI changes interaction design

2. **What data would AI need access to that it doesn't have today?**
   - Current: pet history, vet notes, diagnosis codes
   - AI-native: real-time observations, previous outcomes, owner feedback, vet feedback on suggestions
   - What does this say about data governance? Privacy?

3. **What decisions should vets *always* approve, even in a mature AI-native system? Why?**
   - Diagnosis? Treatment? Escalation?
   - What's the principle: risk? accountability? professional judgment?

4. **If you had infinite resources, what would you build first to move toward AI-native?**
   - Not: "rebuild the whole system"
   - Instead: What's the smallest thing that proves AI-native is possible?
   - E.g., "AI-driven pet profile synthesis" or "Real-time suggestion engine" or "Event capture layer"
   - What would the vet learn from that MVP?

5. **What legacy constraints from the current system would you drop?**
   - Current PetClinic assumes: humans search, humans initiate, humans complete forms
   - AI-native assumes: AI suggests, humans decide, AI executes
   - What breaks if you make that assumption?

6. **What would you *not* automate, and why?**
   - Diagnosis? Too risky.
   - Treatment? Maybe if confidence is high.
   - Owner communication? Never; too personal.
   - Follow-up scheduling? Could be mostly AI with vet review.
   - What principle divides "automatable" from "not"?

7. **How would you measure maturity in the organization?**
   - Current: "We have an AI system"
   - Mature: "We think in AI by default"
   - What does that look like? How do you know you're there?

---

## Lab 6 Synthesis: What You've Learned Across Labs 0-6

By now, you've traveled from baseline to re-architecture. Here's the arc:

| Lab | Question | Answer | Artifact |
|-----|----------|--------|----------|
| 0 | Where does AI add value? | In decisions, not transactions | Opportunity map |
| 1 | How can AI augment humans? | Retrieve + synthesize context | RAG system |
| 2 | How can we trust AI? | Capture human review + learning | HITL workflow |
| 3 | How can we automate safely? | Scope decisions narrowly; escalate edges | Single agent |
| 4 | How do we scale judgment? | Multiple agents with separation of concerns | Multi-agent system |
| 5 | How do we govern AI? | Centralize platform + policy + monitoring | Enterprise platform |
| 6 | How would we design from scratch? | Invert: make AI primary, UI secondary | Re-imagined architecture |

Each lab answered a question that emerged from the previous one:
- Lab 0 asks "Why AI?" Lab 1 answers "Here's how."
- Lab 1 proves augmentation works. Lab 2 asks "But what if something goes wrong?" 
- Lab 2 keeps one human in the loop. Lab 3 asks "Can multiple decisions be automated?"
- Lab 3 works for one agent. Lab 4 asks "What if we need multiple perspectives?"
- Lab 4 scales decisions. Lab 5 asks "But who governs this?"
- Lab 5 builds infrastructure. Lab 6 asks "If we'd had this infrastructure from the start, what would we build?"

Lab 6 is where the insights converge. It's not about implementation; it's about rethinking.

---

## The Teaching Moment Revisited

> **"AI maturity ends when AI becomes invisible—but indispensable."**

What does this mean?

**Invisible:** The user doesn't see agents, workflows, or AI mechanics. They state intent ("I'm worried about Fluffy's ear") and the system handles execution.

**Indispensable:** But the system couldn't work without AI. Remove the reasoning layer and you're back to manual search, manual forms, manual follow-ups.

The irony is that invisible AI systems are *harder* to build and *more carefully governed* than visible ones. When users see agents, they're cautious. When AI is invisible—baked into the interaction model—users trust it implicitly. That trust must be earned through rigorous monitoring, continuous learning, and clear escalation.

This is the maturity curve:
- **Novice:** "We have AI!" (visible, maybe not trustworthy)
- **Intermediate:** "AI helps humans decide" (visible, trustworthy for specific domains)
- **Mature:** "Interaction design is built around AI" (invisible, trustworthy because it's well-governed)

Lab 6 is asking: What does maturity look like?

---

## If You Have More Time

Lab 6 is designed as a **capstone**, but if you want to go deeper:

1. **Prototype an interaction:** Build one screen/workflow from the AI-native design using HTML/mockup tools. What did you learn?
2. **Data model deep dive:** Actually design the event schema. What queries does AI need to run fast? What data needs to be pre-computed?
3. **Interview vets:** Show them the AI-native design. What excites them? What worries them? Iterate.
4. **Cost analysis:** Current PetClinic costs X to maintain. AI-native would cost Y (more infrastructure, more data storage, more AI compute). Is it worth it?
5. **Regulatory review:** What compliance changes? HIPAA? State vet board requirements? Insurance liability?

These are beyond the scope of Lab 6, but they're the real work of building AI-native products. Lab 6 gives you the vision; these deeper dives would test its feasibility.

---

## Next Steps

Lab 6 is the capstone. **You are finished.**

But finishing a lab series is not finishing AI modernization. In fact:

- **If you work at PetClinic:** This is just the start. You now have the language, mental models, and frameworks to lead the real transformation. Go talk to your team. Start small (maybe one Lab 3 agent), but think big (where does Lab 6 lead?).

- **If you work elsewhere:** These patterns apply everywhere. Wherever you have humans making decisions informed by data, AI can reshape the interaction model. Start with the question from Lab 0: **Where does AI create value?** Then follow the arc: augment (Lab 1), keep humans accountable (Lab 2), automate narrow decisions (Lab 3), scale with multiple perspectives (Lab 4), govern (Lab 5), and eventually reimagine (Lab 6).

- **If you're learning about AI:** You've done the real work. Not just technical tutorials, but thinking about *why* AI matters, *how* to keep it safe, *what* makes it scale, and *when* to reinvent around it. That's the curriculum no course teaches, but every organization needs.

---

## Final Reflection

Before you close this lab, ask yourself:

1. **What was the biggest shift in my thinking from Lab 0 to Lab 6?**
   - Maybe: "I thought AI was about automation; I learned it's about augmentation and then thoughtful re-architecture."
   - Or: "I thought governance was overhead; I learned it's the foundation for trust."

2. **If I could change one thing about how my organization approaches AI, what would it be?**
   - This is the real question. Lab 6 is not about PetClinic; it's about you.

3. **What would I tell someone just starting with AI, based on this series?**
   - Start with value (Lab 0), not hype.
   - Augment before automating (Lab 1-2).
   - Think about governance from day one (Lab 5), not after you've shipped something unsafe.
   - And ultimately, be willing to rethink your product around AI (Lab 6), not just bolt it on.

You've completed a rigorous arc: from assessment to strategy. Now comes the harder part: making it real in your organization. But you have the frameworks. Use them.

---

*Lab 6: AI-Native Product Re-Thinking — written by CJ, technical writer*
