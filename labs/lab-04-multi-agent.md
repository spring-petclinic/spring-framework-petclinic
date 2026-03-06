# Lab 4: Multi-Agent System (MAS)

**Theme:** Separation of cognitive responsibilities  
**Duration:** ~9 hours  
**Prerequisites:** Completed Lab 3

---

## Context

Lab 3 proved single agents work. But complex decisions—especially in healthcare—need multiple perspectives.

Lab 4 introduces **Multi-Agent Systems (MAS)**—where specialized agents collaborate, critique, and coordinate. No single agent owns the truth; instead, agents with different roles (clinical, compliance, communication) contribute perspectives to a shared decision.

This is how teams scale judgment.

---

## What This Lab Proves

1. **Complex decisions should never live in one prompt.** Spreading reasoning across agents improves clarity, auditability, and safety. When clinical reasoning is mixed with compliance checking is mixed with communication strategy, you can't trace why a decision was made.

2. **Multi-agent design improves safety *and* clarity.** When agents have separate roles, conflicts surface explicitly (not hidden in ambiguous prompts). A compliance concern isn't a whisper in the system prompt; it's a veto from a dedicated agent.

3. **Agents can collaborate without shared authority.** Each agent respects the others' domains and flags concerns transparently. Clinical reasoning doesn't dictate communication. Compliance doesn't override clinical judgment—it escalates.

---

## Key Activities

### Activity 1: Define Agent Roles

You will define three specialized agents, each with a role contract that spells out what it can do, what it cannot do, and how it relates to the others.

#### Agent 1: Clinical Reasoning Agent
- **Goal:** Analyze clinical data and identify patterns in a pet's health history
- **Inputs:** Clinical records, pet profile, visit notes
- **Outputs:** Clinical analysis (patterns, risk assessment, evidence-based observations)
- **Can do:** Retrieve clinical records, analyze historical patterns, identify clinical significance
- **Cannot do:** Override compliance constraints, make final decisions, contact owners
- **Escalation trigger:** "Should we refer to a specialist?" → defer to Compliance Agent for cost/policy constraints

#### Agent 2: Compliance & Safety Agent
- **Goal:** Validate decisions against safety policies, ethics, regulations, and organizational constraints
- **Inputs:** Clinical analysis from Clinical Reasoning Agent
- **Outputs:** Safety verdict (PASS / FLAG / FAIL), compliance notes, risk level assessment
- **Can do:** Review clinical analysis against policies, identify regulatory/safety concerns, flag cost or resource constraints
- **Cannot do:** Override clinical judgment, contact owners, make clinical recommendations
- **Escalation trigger:** Produces veto authority: if Compliance flags a concern, Clinical Reasoning *must* address it before proceeding
- **Teaching moment:** "Compliance doesn't block good care—it prevents harm we haven't considered."

#### Agent 3: Communication Agent
- **Goal:** Draft clear, empathetic communication for owners about clinical findings and next steps
- **Inputs:** Clinical analysis, safety verdict from Compliance Agent
- **Outputs:** Draft message to owner (with tone assessment, readability level, clarity checks)
- **Can do:** Draft messages, assess tone, rewrite for clarity, suggest follow-up language
- **Cannot do:** Send messages directly, modify clinical recommendations, create records
- **Relationship to others:** Takes feedback from Clinical and Compliance; refines *how* we communicate, not *what* we communicate

---

### Activity 2: Implement Orchestration

You will design how these three agents coordinate—who runs first, when they can run in parallel, how context flows between them, and what happens when they disagree.

#### Orchestration Flow (Sequential Pattern—Most Common)

```
┌─────────────────────────────────────────────────────────────────┐
│ User: "Analyze Bella's recurring ear infections and plan care"  │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
              ┌──────────────────────┐
              │ STAGE 1: CLINICAL    │
              │ Reasoning Agent      │
              └────────┬─────────────┘
                       ↓ (output: clinical_analysis + evidence)
              ┌──────────────────────┐
              │ STAGE 2: COMPLIANCE  │
              │ & Safety Agent       │
              │ Reviews analysis     │
              │ verdict: PASS/FLAG   │
              └────────┬─────────────┘
                       ↓ (if PASS)
              ┌──────────────────────┐
              │ STAGE 3: COMMUNICATION
              │ Agent drafts message │
              │ for owner            │
              └────────┬─────────────┘
                       ↓
              ┌──────────────────────┐
              │ STAGE 4: HUMAN APPROVAL
              │ Vet reviews all      │
              │ 3 outputs + audit    │
              └────────┬─────────────┘
                       ↓
        ┌──────────────────────────┐
        │ Final output + audit log │
        └──────────────────────────┘
```

**Why sequential?** Clinical analysis must happen first (it's the foundation). Compliance must review clinical output before Communication drafts, so Communication knows what constraints or concerns exist. Human approval comes last, informed by all three perspectives.

**Implementation Pattern:**

```csharp
public async Task<MASResult> OrchestrateMultiAgent(
    string petId,
    string userQuery)
{
    var auditTrail = new List<AuditEntry>();
    var result = new MASResult();

    try
    {
        // Stage 1: Clinical Reasoning
        var clinicalAgent = new ClinicalReasoningAgent(_kernel);
        var clinicalOutput = await clinicalAgent.AnalyzeAsync(petId, userQuery);
        
        auditTrail.Add(new AuditEntry
        {
            Stage = "Clinical",
            Output = clinicalOutput,
            Timestamp = DateTime.UtcNow
        });

        if (!clinicalOutput.Success)
        {
            result.Status = "CLINICAL_ANALYSIS_FAILED";
            result.AuditTrail = auditTrail;
            return result;
        }

        // Stage 2: Compliance & Safety Review
        var complianceAgent = new ComplianceAgent(_kernel);
        var safetyVerdictOutput = await complianceAgent.ReviewAsync(
            clinicalOutput,
            petId);
        
        auditTrail.Add(new AuditEntry
        {
            Stage = "Compliance",
            Output = safetyVerdictOutput,
            Timestamp = DateTime.UtcNow
        });

        // Check verdict before proceeding
        if (safetyVerdictOutput.Verdict == SafetyVerdictType.FAIL)
        {
            result.Status = "BLOCKED_BY_SAFETY_POLICY";
            result.SafetyReason = safetyVerdictOutput.FlaggedConcern;
            result.AuditTrail = auditTrail;
            return result;
        }

        // Stage 3: Communication Drafting
        var commAgent = new CommunicationAgent(_kernel);
        var draftOutput = await commAgent.DraftAsync(
            clinicalOutput,
            safetyVerdictOutput);
        
        auditTrail.Add(new AuditEntry
        {
            Stage = "Communication",
            Output = draftOutput,
            Timestamp = DateTime.UtcNow
        });

        // Assemble result
        result.Status = "READY_FOR_APPROVAL";
        result.ClinicalAnalysis = clinicalOutput;
        result.SafetyVerdictOutput = safetyVerdictOutput;
        result.DraftCommunication = draftOutput;
        result.AuditTrail = auditTrail;

        return result;
    }
    catch (Exception ex)
    {
        result.Status = "ERROR";
        result.Error = ex.Message;
        result.AuditTrail = auditTrail;
        return result;
    }
}
```

#### Parallel Retrieval (Optimization Pattern)

In some cases, agents can work in parallel—for example, when gathering independent context:

```
User Request
    ↓
┌──────────────────────────────────────────────┐
├─ Fetch visit history (Clinical prepares)     │
├─ Fetch medication history (Compliance needs) │
├─ Fetch breed-specific risks (Clinical needs) │
└──────────────────────────────────────────────┘
         (await all tasks)
    ↓
Merge context → Sequential orchestration continues
```

**When to use parallel:** Only when agents are *independent*. Clinical and Compliance must sequence because Compliance reads Clinical's output.

---

### Activity 3: Prevent Shared Authority, Allow Shared Context

This is the tension of multi-agent systems: agents must share information *without sharing veto power*.

#### Shared Context (Read-Only)

All three agents can *read*:
- Pet clinical records (visits, notes, diagnoses)
- Pet profile (name, breed, age, weight)
- Owner profile (communication preferences, past interactions)
- Organizational policies (treatment guidelines, safety constraints)

```csharp
public class SharedContext
{
    // All agents can read these; none can modify
    public PetRecord PetData { get; set; }
    public List<Visit> ClinicalHistory { get; set; }
    public OwnerProfile OwnerData { get; set; }
    public PolicySet CompliancePolicies { get; set; }
    public TreatmentGuidelines ClinicalGuidelines { get; set; }
}
```

#### No Shared Authority (Each Agent Owns Its Decision)

- **Clinical Reasoning Agent** owns the clinical analysis. No other agent can change the diagnosis or risk assessment.
- **Compliance Agent** owns the safety verdict. Clinical Agent cannot override "Compliance says FAIL."
- **Communication Agent** owns the message. Clinical Agent cannot mandate the exact phrasing.

**This is important:** If Clinical thinks a recommendation is safe but Compliance flags a regulatory concern, the resolution is *escalation to human*, not one agent overriding the other.

#### Conflict Resolution Hierarchy

```
Human Clinician (final authority)
         ↑
         │
Compliance Agent (veto authority on safety/policy)
         ↑
         │
Clinical Reasoning Agent (primary analysis)
         ↑
         │
Communication Agent (output only, no veto power)
```

**Rule:** In case of disagreement, escalate upward. Never auto-resolve.

---

### Activity 4: Handle Disagreement Explicitly

When agents conflict, make the conflict visible as data, not a hidden trade-off.

#### Example Conflict 1: Clinical vs. Compliance

```
STAGE 1 (Clinical): "Bella needs dermatology referral for allergy testing.
                     Recurring ear infections suggest underlying allergy."

STAGE 2 (Compliance): "Owner has 3 denied insurance claims in past 6 months.
                      Specialty referral flagged as cost-prohibitive.
                      Recommend: Try dietary adjustment first."
```

**Resolution:** Don't hide this. Log it as a conflict entry:

```json
{
  "conflict_id": "bella-001-clinical-vs-cost",
  "stage": "compliance_review",
  "clinical_recommendation": "Dermatology referral for allergy testing",
  "compliance_concern": "Cost-prohibitive for this owner",
  "resolution_required": "HUMAN",
  "timestamp": "2024-01-15T10:30:00Z",
  "audit_entry": "Compliance and Clinical perspectives conflict. Human must decide: pursue ideal care or honor cost constraints."
}
```

The Communication Agent then drafts a message that *acknowledges* the constraint:

```
"We recommend allergy testing with a dermatologist to find the root cause.
This will help us treat her more effectively long-term.

I know specialty care can be expensive. Let's talk about options—we can
start with a dietary trial while we explore referral timing."
```

Notice: We don't hide the recommendation. We communicate both the clinical ideal *and* the practical constraint.

#### Example Conflict 2: Clinical vs. Communication

```
STAGE 1 (Clinical): "Bella requires immediate antibiotic therapy.
                     Risk of otitis media if untreated."

STAGE 3 (Communication): "Recommending immediate aggressive antibiotics
                         may alarm the owner. Suggest gentler language."
```

**Resolution:** Clinical judgment stands. Communication *rewrites tone*, not substance:

**BEFORE:** "Bella requires immediate aggressive antibiotic therapy to prevent middle ear infection."

**AFTER:** "To prevent the infection from spreading to her middle ear, we recommend starting antibiotics this week."

(Same recommendation, different tone.)

---

### Activity 5: Test Collaboration and Safety

Now test the system with realistic scenarios. The goal is to verify that:
1. Agents collaborate effectively
2. Safety concerns surface explicitly
3. Humans can understand *why* a decision was blocked or approved

#### Scenario 1: Routine Follow-Up (Should PASS Smoothly)

```
Input: "12-month follow-up for Max, a 5-year-old golden retriever. Last visit routine; no concerns."

Clinical Agent: "Routine follow-up. No clinical issues identified. Recommend annual vaccines and dental check."

Compliance Agent: "All recommendations within standard care guidelines. No safety flags."

Communication Agent: "Owner is experienced and pragmatic. Draft message: 'Max looks great! Time for annual vaccines and dental exam. Let's schedule.'"

Outcome: APPROVED. Flow through all three agents without conflict.
```

#### Scenario 2: Cost-Constrained Decision (Surfaces Conflict)

```
Input: "Bella, 7 years old, recurrent ear infections (3 in 12 months). Consider allergy testing."

Clinical Agent: "Recommend dermatology referral for allergy testing. Recurring infections suggest underlying allergy. This is standard for chronic cases."

Compliance Agent: "Owner has history of high-cost procedures. Policy recommends trialing dietary/environmental management first before specialty referral. FLAG: Cost-prohibitive for this owner."

Communication Agent: "Owner is anxious. Recommend acknowledging concern while offering path forward."

Outcome: FLAG (not FAIL). System escalates to vet with all three perspectives visible.
```

#### Scenario 3: Safety Concern (Blocks Decision)

```
Input: "Rocky, senior dog, possible medication interaction. Owner taking new arthritis medication. Recommend pain management."

Clinical Agent: "Senior dog with arthritis. Pain management recommended."

Compliance Agent: "SAFETY CHECK: New medication is NSAIDs. Owner already on warfarin (blood thinner). NSAIDs + warfarin = bleeding risk. This is contraindicated. VERDICT: FAIL."

Outcome: BLOCKED. System prevents recommendation before it reaches Communication or Human.
```

---

## Checkpoint 1: Multi-Agent Coordination

Before moving forward, verify all of the following:

- [ ] **Three agents are defined** with explicit role contracts
- [ ] **Each agent focuses on its domain:**
  - Clinical Agent analyzes medical patterns
  - Compliance Agent checks safety/policy
  - Communication Agent handles owner messaging
- [ ] **Orchestration flow is implemented** and tested end-to-end
- [ ] **Data flows correctly** from Clinical → Compliance → Communication
- [ ] **Conflicts surface visibly** (conflicts are logged, not hidden)
- [ ] **No agent has unilateral authority** (Clinical cannot override Compliance; Compliance cannot override Clinical)
- [ ] **Audit trail captures everything:**
  - All three agent outputs
  - Any conflicts detected
  - Final human approval/edit
- [ ] **At least 3 test scenarios pass** (routine, flag, and fail cases)

---

## Outputs from This Lab

### Output 1: Multi-Agent System Architecture

A working system with three specialized agents deployed:

- **Clinical Reasoning Agent** — recommends treatments, identifies patterns, surfaces clinical evidence
- **Compliance & Safety Agent** — flags safety concerns, validates against policies, owns veto authority
- **Communication Agent** — drafts owner messaging, assesses tone, ensures clarity

Each agent has:
- Role contract (what it does, what it doesn't)
- Tool set (what APIs/functions it can call)
- Output schema (what it produces)
- Integration points (how it reads/writes shared context)

### Output 2: Orchestration Flow Documentation

Document that covers:
- Agent roles and decision boundaries
- Workflow sequence (serial, parallel, conditional)
- Data handoff between agents (how does Clinical's output become Compliance's input?)
- Conflict detection and resolution strategy (what happens when agents disagree?)
- Approval gates (where humans review and decide)
- Audit trail structure (what gets logged at each stage)

**Example:** A diagram showing the three agents, sequential flow, conflict resolution hierarchy, and audit checkpoint.

### Output 3: Collaboration Examples

Concrete, working scenarios that demonstrate:
- Where agents improved decision quality by collaborating
  - Example: Compliance caught a medication interaction Clinical missed
- Where agents caught potential errors from each other
  - Example: Communication flagged that the clinical message was too technical for the owner
- Cases where human judgment was required to resolve agent disagreement
  - Example: Cost vs. clinical ideal—agent system surfaces the trade-off, human decides

For each example, include:
- Initial input (user query)
- All three agent outputs
- Audit trail showing reasoning
- How conflict was resolved
- What the human decided and why

---

## Teaching Moment

> **"Multi-agent systems scale judgment, not just throughput."**

Single-agent systems scale by making one agent faster or smarter. Multi-agent systems scale by adding *judgment diversity*.

When you separate clinical reasoning from compliance reasoning from communication strategy, each agent becomes simpler, more focused, and easier to audit. And when they collaborate, disagreement surfaces explicitly—not buried in ambiguous prompts.

A single prompt saying "Recommend care, but be safe, and write it clearly" is ambiguous. It forces one agent to balance clinical judgment, safety constraints, and communication strategy simultaneously—and when it gets something wrong, it's unclear *which* judgment failed.

Three agents with separate roles make the failure explicit: "Clinical said X. Compliance said no because of Y. Communication phrased it as Z. Human decided W."

That transparency is what makes multi-agent systems safer than single agents. And it's what makes them more valuable in healthcare, where you can't afford ambiguity.

---

## Reflection Questions

Before moving to Lab 5, think through these:

1. **What decision quality improved by adding a Compliance Agent?**
   - What mistakes did the Compliance Agent catch that Clinical might have missed?
   - Would a single agent catch the same things?

2. **What kinds of conflicts should humans always resolve? What can agents resolve?**
   - Example of agent-resolvable conflict: Clinical recommends different timing; Compliance clarifies when based on policy.
   - Example of human-required conflict: Clinical ideal (specialty referral) vs. owner's cost constraints.

3. **If you added a fourth agent (e.g., Cost-Awareness or Logistics), where would it fit in the workflow?**
   - Would it be sequential (insert after Compliance)? Parallel (gather cost info in parallel with clinical)?
   - What would "veto authority" look like for a Cost-Awareness agent?

4. **How would you explain to a vet why a decision was blocked by the Compliance Agent?**
   - Can you show the reasoning? Can you point to the policy?
   - Can the vet override the agent, and how is that documented?

5. **What's the cost of this orchestration in time and complexity?**
   - Does running three agents take 3x longer than one?
   - Is it worth it?

---

## Potential Implementation Challenges & How to Handle Them

### Challenge 1: "Orchestration Overhead"

**Problem:** Three sequential agents take longer than one agent.

**Reality:** Yes, usually. But the trade-off is worth it because:
- Safety catches (Compliance prevents bad recommendations)
- Auditability (you can trace why a decision was made)
- Maintainability (changing one agent doesn't break the others)

**Mitigation:** Use parallel retrieval where possible. Cache common queries. Profile the system to find bottlenecks.

### Challenge 2: "Agents Get Into Loops"

**Problem:** Clinical revises its output based on Compliance feedback; Compliance revises again; endless cycle.

**Reality:** This shouldn't happen if role boundaries are clear.

**Prevention:** Make orchestration one-way:
- Clinical runs once, produces output
- Compliance reviews (doesn't ask Clinical to re-run)
- If Compliance says FAIL, escalate to human (don't loop back)

### Challenge 3: "Agents Produce Conflicting Outputs"

**Problem:** Clinical says "safe," Compliance says "unsafe"—system is broken.

**Reality:** This isn't broken. It's *exactly what you want*. Conflict = system is working.

**Action:** Log the conflict, escalate to human, let human decide. Never auto-resolve agent conflicts in safety-critical domains.

### Challenge 4: "What If Compliance Agent Halluccinates Policy?"

**Problem:** Compliance Agent says "Policy forbids this" but policy doesn't actually forbid it.

**Reality:** This is why you have a human in the loop.

**Mitigation:** Structure Compliance as a retrieval + reasoning system:
1. Agent retrieves the actual policy document
2. Agent reasons about whether recommendation complies
3. Agent cites the policy section in its verdict

This way, humans can verify the policy citation.

---

## Extended Reading: Agent Prompts (Role Contracts in Prose)

### Clinical Reasoning Agent Prompt

```
You are the Clinical Reasoning Agent for PetClinic.

Your role: Analyze a pet's clinical history and recommend medical care.

You must:
1. Read the pet's clinical records (visits, notes, medications, diagnoses)
2. Identify patterns, recurring issues, or concerning trends
3. Apply clinical guidelines to recommend next steps
4. Cite evidence from the records
5. Flag any uncertainties or gaps in data

You must NOT:
1. Override safety or compliance concerns (the Compliance Agent owns that)
2. Make final decisions (a human clinician will approve)
3. Contact the owner directly
4. Assume facts not in the records

Your output must include:
- Clinical analysis (patterns, risks, recommendations)
- Evidence (which records support your analysis?)
- Confidence level (0.0-1.0) for each recommendation
- Gaps or uncertainties

If you're uncertain about a recommendation, say so. Uncertainty is useful information.
```

### Compliance & Safety Agent Prompt

```
You are the Compliance & Safety Agent for PetClinic.

Your role: Validate clinical recommendations against safety policies, ethics, regulations, and organizational constraints.

You must:
1. Read the Clinical Agent's analysis
2. Check each recommendation against:
   - Patient safety guidelines (contraindications, drug interactions)
   - Organizational policies (cost constraints, resource limits)
   - Regulatory requirements (if applicable)
   - Owner context (can they afford this? do they have access?)
3. Produce a verdict: PASS, FLAG, or FAIL
4. Cite the policy or concern

You must NOT:
1. Override the Clinical Agent's analysis (your job is to flag concerns, not to redo diagnosis)
2. Make final decisions (a human will review your verdict)
3. Contact the owner

Your output must include:
- Verdict (PASS / FLAG / FAIL)
- Reason (which policy, which concern?)
- Recommended action (if FLAG: suggest alternative; if FAIL: explain why it's blocked)
- Confidence (is this definitely a problem, or should a human verify?)

If you find a safety concern, surface it immediately. Do not pass it silently.
```

### Communication Agent Prompt

```
You are the Communication Agent for PetClinic.

Your role: Draft clear, empathetic messages to owners about their pet's care.

You must:
1. Read the Clinical Agent's analysis and Compliance Agent's verdict
2. Understand what the vet is recommending (treatment, follow-up, etc.)
3. Write a message for the owner that is:
   - Medically accurate (don't change clinical content)
   - Empathetic and reassuring
   - Clear (appropriate reading level for the owner)
   - Action-oriented (what does the owner need to do next?)
4. If there are constraints (cost, resource), acknowledge them compassionately

You must NOT:
1. Change the clinical recommendation (if Clinical says "antibiotics," you don't suggest "try herbs instead")
2. Ignore the Compliance verdict (if Compliance flagged a concern, your message should acknowledge it)
3. Send the message directly (a human will review and send)

Your output must include:
- Draft message (for the owner)
- Tone assessment (is this appropriate for this owner's communication style?)
- Readability level (is this clear to a non-veterinarian?)
- Clarity checks (are the next steps obvious?)

If the clinical recommendation is complex or jarring, draft a message that explains *why* it's necessary.
```

---

## Success Criteria

You've successfully completed Lab 4 when:

1. **System architecture is clear:** Three agents, clear role contracts, visible orchestration flow
2. **Agents collaborate:** Data flows correctly through the pipeline; no deadlocks or confusion
3. **Conflicts surface as data:** When agents disagree, you can see the disagreement in logs (not hidden)
4. **Humans control final decisions:** All three agent outputs are visible in the approval interface; human can override any agent
5. **Audit trail is complete:** Every decision (agent and human) is logged with reasoning and source citations
6. **Test scenarios pass:** Routine cases flow smoothly; edge cases surface conflicts appropriately; safety concerns block decisions
7. **Team understands the model:** Vets can explain why a recommendation was approved/blocked; they trust the system

---

## Next Steps

Move to **Lab 5: Governance & Compliance (Enterprise AI)** when ready.

Lab 4 proved multi-agent systems work at the team level. But what happens when 50 teams build 50 different agents? Lab 5 shifts from *building AI* to *governing AI*—centralizing platform, policy, and oversight across an organization.

Lab 4 asks: "How do we make complex decisions as a team?"  
Lab 5 asks: "How do we scale teams of teams safely?"

---

*Lab 4 content authored by CJ (Technical Writer), based on pedagogical framework by Toby and technical patterns by Josh.*
