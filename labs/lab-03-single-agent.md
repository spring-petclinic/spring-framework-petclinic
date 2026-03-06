# Lab 3: Single-Agent Workflows (Goal-Oriented AI)

**Theme:** AI reasons across steps  
**Mindset:** From suggestions → goal pursuit  
**Duration:** ~10–12 hours  
**Prerequisites:** Completed Labs 0–2

---

## Context

Labs 1–2 treated AI as a tool: it answered questions (Lab 1: RAG) or generated drafts for human approval (Lab 2: HITL). Lab 3 introduces something fundamentally different: an **Agent**—an AI system that reasons autonomously across multiple steps to accomplish a bounded goal.

An agent isn't a script. It perceives its environment (clinical records, patient history), deliberates (identifies gaps, weighs options), and acts (calls tools, synthesizes information)—iteratively, until it reaches a conclusion. Then it surfaces that conclusion for human review.

The key insight: **An agent with constraints and visibility is safer and more powerful than an automation script.**

---

## What This Lab Proves

1. **Agents are not automation scripts.** Scripts follow fixed rules; agents reason about novel situations. Reasoning scales to edge cases that scripts miss.
2. **Reasoning loops ≠ uncontrolled behavior.** An agent with explicit tool constraints (can retrieve, cannot execute) and approval gates is safer than a script that makes irreversible decisions implicitly.
3. **Observability enables trust.** You must see every reasoning step, every tool call, every decision—so you can understand why the agent made choices and improve it over time.

---

## Learning Objectives

By the end of Lab 3, you will:

- **Understand agent architecture:** What is an agent? How does it reason? What are its boundaries?
- **Design bounded agents:** Define the decision space (scope), tools, and constraints that make an agent reliable.
- **Implement a reasoning loop:** Build the observe → think → act → pause → repeat cycle.
- **Make reasoning observable:** Surface every step the agent takes so humans can audit, debug, and trust.
- **Evaluate agent reliability:** Measure decision quality, identify failure modes, and know when escalation is needed.

---

## Key Teaching Moments

1. **"An agent is a bounded decision-maker, not a free-roaming process."**  
   Enterprises fear agents because they imagine AI running loose, making unsupervised decisions. The antidote: explicit boundaries (tool constraints), visibility (reasoning logs), and approval gates (human checkpoints). A scoped, observable agent is safer than an ambiguous automation script.

2. **"Scope is safety."**  
   A narrow, well-defined agent (e.g., "analyze clinical history and draft a summary") is more reliable than a powerful, vague one (e.g., "improve patient outcomes"). Tight scope enables you to predict, test, and audit the agent's reasoning.

3. **"Escalation is a feature, not a failure."**  
   An agent that escalates at the right moment (when uncertain, when constraints are hit, when human judgment is needed) is doing exactly what you need. Escalation is how bounded agents handle unbounded problems.

---

## Prerequisites

Before starting Lab 3, you must have completed:

- **Lab 0:** Understand PetClinic's baseline workflows and data model
- **Lab 1:** Understand RAG and how to retrieve relevant clinical context
- **Lab 2:** Understand human-in-the-loop patterns and approval workflows

You should also be familiar with:
- C# and async/await patterns
- Semantic Kernel basics (plugins, function calling)
- Azure AI Search or similar retrieval systems

---

## Activity 1: Define the Clinical Assistant Agent

### Goal
Design an agent that can answer: **"Summarize this patient's visit and recommend next steps."**

### Success Criteria
- Agent can retrieve relevant clinical context (visit notes, medical history, medication records)
- Agent can identify clinical patterns (e.g., recurring infections, allergy indicators)
- Agent can draft a structured summary (findings, assessment, plan) with confidence scores
- Agent surfaces all sources and reasoning steps
- Agent **does not** execute actions (no record creation, no owner contact, no prescriptions)

### Instructions

#### Step 1: Define Agent Scope
Create a document or configuration that defines:

**Agent Name:** Clinical Summary Assistant  
**Agent Goal:** Prepare a complete clinical summary and evidence-based follow-up plan for a patient visit  
**Agent Domain:** Veterinary clinical reasoning (pet health analysis, pattern recognition, care planning)

**Agent Boundaries:**
- ✅ **Can do:** Retrieve records, analyze data, draft summaries, ask clarifying questions, request human approval
- ❌ **Cannot do:** Create or modify medical records, contact owners, prescribe medications alone, execute irreversible actions

**Inputs:**
- New visit information (date, presenting complaint, clinical observations)
- Pet profile (age, breed, weight, medical history)
- Medication history
- Clinical guidelines and policies

**Outputs:**
- Clinical summary (structured: history, findings, assessment)
- Recommended next steps (follow-up timing, tests, specialist referrals)
- Confidence scores for each recommendation
- Complete audit trail (sources, reasoning)

**Success Metrics:**
- Vets approve ≥85% of summaries without significant edits
- Agent identifies clinically relevant patterns ≥90% of the time
- Zero escalations due to out-of-scope behavior (all tool calls are pre-approved)

---

#### Step 2: Design Agent Tools
List every tool the agent can call. Each tool must:
1. Be retrievable or read-only (no mutations)
2. Return structured, grounded data
3. Be safe to call repeatedly without side effects

**Tool 1: retrieve_visit_records**
```json
{
  "name": "retrieve_visit_records",
  "description": "Fetch all visit history for a pet, including dates, presenting complaints, notes, and treatments",
  "inputs": {
    "pet_id": "string (required)",
    "time_range_days": "integer (optional, default: 365)"
  },
  "outputs": {
    "visits": [
      {
        "visit_id": "string",
        "date": "ISO8601",
        "presenting_complaint": "string",
        "clinical_notes": "string",
        "treatments": ["string"],
        "clinician": "string"
      }
    ],
    "total_visits": "integer"
  },
  "constraints": "Returns data only; does not create or modify records"
}
```

**Tool 2: retrieve_medication_history**
```json
{
  "name": "retrieve_medication_history",
  "description": "Get all medications prescribed to a pet, including dates, indications, and doses",
  "inputs": {
    "pet_id": "string (required)"
  },
  "outputs": {
    "medications": [
      {
        "medication_id": "string",
        "name": "string",
        "dose": "string",
        "frequency": "string",
        "start_date": "ISO8601",
        "end_date": "ISO8601 (nullable)",
        "indication": "string",
        "prescriber": "string"
      }
    ]
  },
  "constraints": "Returns data only"
}
```

**Tool 3: retrieve_pet_profile**
```json
{
  "name": "retrieve_pet_profile",
  "description": "Get pet demographics, breed-specific risks, and allergy/contraindication information",
  "inputs": {
    "pet_id": "string (required)"
  },
  "outputs": {
    "pet": {
      "pet_id": "string",
      "name": "string",
      "species": "string",
      "breed": "string",
      "age_years": "number",
      "weight_kg": "number",
      "known_allergies": ["string"],
      "chronic_conditions": ["string"],
      "breed_risks": ["string"]
    }
  },
  "constraints": "Returns data only"
}
```

**Tool 4: retrieve_clinical_guidelines**
```json
{
  "name": "retrieve_clinical_guidelines",
  "description": "Get evidence-based guidelines for a condition or treatment",
  "inputs": {
    "query": "string (e.g., 'ear infection in dogs')"
  },
  "outputs": {
    "guidelines": [
      {
        "condition": "string",
        "recommended_workup": ["string"],
        "treatment_options": ["string"],
        "specialist_referral_criteria": ["string"],
        "follow_up_timing": "string"
      }
    ]
  },
  "constraints": "Returns data only; does not provide medical advice"
}
```

**Tool 5: log_reasoning**
```json
{
  "name": "log_reasoning",
  "description": "Record a reasoning step for audit trail and transparency",
  "inputs": {
    "step": "integer (step number)",
    "action": "string (what the agent is doing)",
    "thinking": "string (why the agent is doing it)",
    "confidence": "float (0.0–1.0)"
  },
  "outputs": {
    "logged": true,
    "timestamp": "ISO8601"
  },
  "constraints": "Logging only; no side effects"
}
```

**Tool 6: request_approval**
```json
{
  "name": "request_approval",
  "description": "Surface a draft or recommendation for human review",
  "inputs": {
    "proposal": "string (the recommendation or draft)",
    "reasoning": "string (why the agent recommends this)",
    "confidence": "float (0.0–1.0)"
  },
  "outputs": {
    "awaiting_response": true,
    "approval_request_id": "string"
  },
  "constraints": "Pauses agent execution; does not proceed until human responds"
}
```

**Tool 7: log_failure**
```json
{
  "name": "log_failure",
  "description": "Record when the agent cannot proceed due to missing data or out-of-scope issues",
  "inputs": {
    "failure_reason": "string",
    "missing_data": ["string"],
    "escalation_needed": "boolean"
  },
  "outputs": {
    "logged": true,
    "escalation_request_id": "string (if escalation_needed=true)"
  },
  "constraints": "Logging only"
}
```

---

#### Step 3: Define Decision Points & Guardrails
Document where the agent pauses and requires human input:

**Decision Point 1: Scope Check**
- **When:** Agent receives a request
- **Logic:** Is this within my domain (clinical summary + follow-up plan)?
- **If No:** Escalate to human; log failure
- **If Yes:** Proceed to data gathering

**Decision Point 2: Data Completeness**
- **When:** Agent has retrieved initial records
- **Logic:** Do I have enough information to make a credible analysis?
- **If No:** Request clarification; ask human for missing data
- **If Yes:** Proceed to analysis

**Decision Point 3: Confidence Threshold**
- **When:** Agent finishes drafting recommendations
- **Logic:** Is my confidence ≥70% for each recommendation?
- **If No:** Flag as "lower confidence" and recommend human review before approval
- **If Yes:** Proceed to approval request

**Decision Point 4: Tool Call Whitelist**
- **Constraint:** Agent can only call tools from the approved list (retrieve_*, log_*, request_approval)
- **Enforcement:** Middleware intercepts and blocks any other tool calls
- **Action on Violation:** Log and escalate

**Decision Point 5: Token/Cost Limit**
- **Constraint:** Maximum 10 reasoning loops per request (prevents infinite loops)
- **Action on Breach:** Halt agent, return best-effort output, escalate

---

### Deliverable: Agent Design Document

Create a document at `labs/agents/clinical-summary-agent.md` with:
1. Agent scope, goal, and boundaries (as defined above)
2. Tool specifications (all 7 tools)
3. Decision points and guardrails
4. Success metrics

---

## Activity 2: Implement the Reasoning Loop

### Goal
Build the agent's core loop: **Observe → Think → Act → Pause → Repeat**.

### Instructions

#### Step 1: Implement Agent Class
Create a C# class that encapsulates the reasoning loop:

```csharp
public class ClinicalSummaryAgent
{
    private readonly IKernel _kernel;
    private readonly ISearchClient _searchClient;
    private readonly IApprovalService _approvalService;
    private readonly ILogger<ClinicalSummaryAgent> _logger;

    public ClinicalSummaryAgent(
        IKernel kernel,
        ISearchClient searchClient,
        IApprovalService approvalService,
        ILogger<ClinicalSummaryAgent> logger)
    {
        _kernel = kernel;
        _searchClient = searchClient;
        _approvalService = approvalService;
        _logger = logger;
    }

    public async Task<AgentResult> AnalyzePetVisitAsync(string petId, string visitNotes)
    {
        var result = new AgentResult { PetId = petId, ReasoningSteps = new List<ReasoningStep>() };
        
        // Step 0: Validate scope
        if (!IsWithinScope(visitNotes))
        {
            result.Status = AgentStatus.OutOfScope;
            _logger.LogWarning("Request out of scope: {VisitNotes}", visitNotes);
            return result;
        }

        // Step 1: Gather context
        var step1 = new ReasoningStep 
        { 
            StepNumber = 1, 
            Action = "retrieve_context",
            Thinking = "Need pet profile, medical history, and clinical guidelines to analyze this visit"
        };
        
        var petProfile = await RetrievePetProfileAsync(petId);
        var visitHistory = await RetrieveVisitRecordsAsync(petId);
        var medications = await RetrieveMedicationHistoryAsync(petId);
        
        step1.Result = $"Retrieved {visitHistory.Count} prior visits, {medications.Count} medications, pet profile for {petProfile.Name}";
        step1.Confidence = 0.95;
        result.ReasoningSteps.Add(step1);

        // Step 2: Analyze patterns
        var step2 = new ReasoningStep
        {
            StepNumber = 2,
            Action = "analyze_patterns",
            Thinking = "Look for recurring conditions, medication interactions, breed-specific risks"
        };
        
        var patterns = IdentifyPatterns(visitHistory, medications, petProfile);
        step2.Result = $"Identified {patterns.Count} clinically relevant patterns";
        step2.Confidence = patterns.Average(p => p.Confidence);
        result.ReasoningSteps.Add(step2);

        // Step 3: Retrieve relevant guidelines
        var step3 = new ReasoningStep
        {
            StepNumber = 3,
            Action = "retrieve_guidelines",
            Thinking = $"Get evidence-based guidelines for the identified conditions: {string.Join(", ", patterns.Select(p => p.Condition))}"
        };
        
        var guidelines = new List<ClinicalGuideline>();
        foreach (var pattern in patterns)
        {
            var guideline = await RetrieveClinicalGuidelinesAsync(pattern.Condition);
            guidelines.AddRange(guideline);
        }
        
        step3.Result = $"Retrieved {guidelines.Count} guideline recommendations";
        step3.Confidence = 0.90;
        result.ReasoningSteps.Add(step3);

        // Step 4: Draft summary and plan
        var step4 = new ReasoningStep
        {
            StepNumber = 4,
            Action = "draft_summary",
            Thinking = "Synthesize all findings into a structured clinical summary and follow-up plan"
        };
        
        var draftSummary = DraftClinicalSummary(petProfile, visitHistory, patterns, guidelines, visitNotes);
        step4.Result = $"Drafted summary with {draftSummary.RecommendedActions.Count} action items";
        step4.Confidence = draftSummary.OverallConfidence;
        result.ReasoningSteps.Add(step4);

        // Step 5: Check confidence threshold
        if (step4.Confidence < 0.70m)
        {
            result.ConfidenceNote = $"Lower confidence ({step4.Confidence:P}) - recommend veterinarian review before approval";
        }

        // Step 6: Request approval
        var step5 = new ReasoningStep
        {
            StepNumber = 5,
            Action = "request_approval",
            Thinking = "Surface draft for veterinarian review and approval"
        };
        
        var approvalRequest = await _approvalService.CreateApprovalRequestAsync(
            new ApprovalRequest
            {
                PetId = petId,
                Content = draftSummary,
                ReasoningTrace = result.ReasoningSteps,
                RequestedBy = "ClinicalSummaryAgent",
                RequiredRole = "Veterinarian"
            });
        
        step5.Result = $"Approval request created: {approvalRequest.Id}";
        step5.AwaitingHumanResponse = true;
        result.ReasoningSteps.Add(step5);

        result.Status = AgentStatus.AwaitingApproval;
        result.DraftSummary = draftSummary;
        result.ApprovalRequestId = approvalRequest.Id;

        return result;
    }

    private bool IsWithinScope(string visitNotes)
    {
        // Check if request is asking for something outside the agent's scope
        // (e.g., "perform surgery", "contact the owner", "fill a prescription")
        var outOfScopeKeywords = new[] { "surgery", "contact owner", "prescribe", "execute", "send message" };
        return !outOfScopeKeywords.Any(k => visitNotes.Contains(k, StringComparison.OrdinalIgnoreCase));
    }

    private List<ClinicalPattern> IdentifyPatterns(
        List<Visit> visits,
        List<Medication> medications,
        PetProfile profile)
    {
        var patterns = new List<ClinicalPattern>();

        // Look for recurring conditions
        var conditionFrequency = visits
            .SelectMany(v => ExtractConditions(v.Notes))
            .GroupBy(c => c)
            .Where(g => g.Count() >= 2);

        foreach (var condition in conditionFrequency)
        {
            patterns.Add(new ClinicalPattern
            {
                Condition = condition.Key,
                Frequency = condition.Count(),
                Confidence = Math.Min(0.95m, 0.6m + (condition.Count() * 0.1m)),
                ClinicalSignificance = "Recurring condition may indicate chronic issue or allergy"
            });
        }

        // Check for medication interactions
        foreach (var medication in medications.Where(m => m.EndDate == null))
        {
            foreach (var other in medications.Where(m => m.EndDate == null && m.MedicationId != medication.MedicationId))
            {
                if (CheckInteraction(medication, other))
                {
                    patterns.Add(new ClinicalPattern
                    {
                        Condition = $"Medication interaction: {medication.Name} + {other.Name}",
                        Confidence = 0.85m,
                        ClinicalSignificance = "Potential drug interaction; recommend pharmacology review"
                    });
                }
            }
        }

        // Check breed-specific risks
        foreach (var risk in profile.BreedRisks)
        {
            var relatedVisits = visits.Where(v => v.Notes.Contains(risk)).ToList();
            if (relatedVisits.Any())
            {
                patterns.Add(new ClinicalPattern
                {
                    Condition = $"Breed-specific risk: {risk}",
                    Frequency = relatedVisits.Count(),
                    Confidence = 0.80m,
                    ClinicalSignificance = $"Monitoring recommended for {profile.Breed}-specific condition"
                });
            }
        }

        return patterns;
    }

    private List<Visit> RetrieveVisitRecordsAsync(string petId) => throw new NotImplementedException("Call Azure AI Search");
    private PetProfile RetrievePetProfileAsync(string petId) => throw new NotImplementedException("Call database");
    private List<Medication> RetrieveMedicationHistoryAsync(string petId) => throw new NotImplementedException("Call database");
    private Task<List<ClinicalGuideline>> RetrieveClinicalGuidelinesAsync(string condition) => throw new NotImplementedException("Call knowledge base");
    private ClinicalSummary DraftClinicalSummary(PetProfile profile, List<Visit> history, List<ClinicalPattern> patterns, List<ClinicalGuideline> guidelines, string visitNotes) => throw new NotImplementedException();
    private List<string> ExtractConditions(string notes) => throw new NotImplementedException();
    private bool CheckInteraction(Medication med1, Medication med2) => throw new NotImplementedException();
}
```

#### Step 2: Define Data Structures
Create classes to hold reasoning steps and agent results:

```csharp
public class ReasoningStep
{
    public int StepNumber { get; set; }
    public string Action { get; set; }
    public string Thinking { get; set; }
    public string Result { get; set; }
    public decimal Confidence { get; set; }
    public bool AwaitingHumanResponse { get; set; }
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
}

public class AgentResult
{
    public string PetId { get; set; }
    public AgentStatus Status { get; set; }
    public List<ReasoningStep> ReasoningSteps { get; set; }
    public ClinicalSummary DraftSummary { get; set; }
    public string ApprovalRequestId { get; set; }
    public string ConfidenceNote { get; set; }
}

public class ClinicalSummary
{
    public string History { get; set; }
    public string Assessment { get; set; }
    public List<RecommendedAction> RecommendedActions { get; set; }
    public List<string> Sources { get; set; }
    public decimal OverallConfidence { get; set; }
}

public class RecommendedAction
{
    public string Action { get; set; }
    public string Rationale { get; set; }
    public DateTime RecommendedDate { get; set; }
    public decimal Confidence { get; set; }
    public List<string> SupportingEvidence { get; set; }
}

public enum AgentStatus
{
    Analyzing,
    AwaitingApproval,
    Approved,
    Rejected,
    OutOfScope,
    Failed
}
```

#### Step 3: Integrate with Semantic Kernel
Register the agent's tools with Semantic Kernel:

```csharp
public static void RegisterClinicalAgentTools(IKernelBuilder builder)
{
    var clinicalTools = new ClinicalTools(_searchClient, _database, _approvalService);
    
    builder.Plugins.AddFromObject(clinicalTools, "clinical");
}

public class ClinicalTools
{
    [KernelFunction("retrieve_visit_records")]
    public async Task<string> RetrieveVisitRecordsAsync(string petId, int timeDays = 365)
    {
        var visits = await _database.GetVisitsAsync(petId, timeDays);
        return JsonConvert.SerializeObject(new { visits = visits });
    }

    [KernelFunction("retrieve_pet_profile")]
    public async Task<string> RetrievePetProfileAsync(string petId)
    {
        var profile = await _database.GetPetProfileAsync(petId);
        return JsonConvert.SerializeObject(profile);
    }

    [KernelFunction("log_reasoning")]
    public Task<string> LogReasoningAsync(int step, string action, string thinking, decimal confidence)
    {
        _logger.LogInformation("Agent step {Step}: {Action} | Confidence: {Confidence:P}", step, action, confidence);
        return Task.FromResult("Logged");
    }

    [KernelFunction("request_approval")]
    public async Task<string> RequestApprovalAsync(string proposal, string reasoning, decimal confidence)
    {
        var request = await _approvalService.CreateApprovalRequestAsync(new ApprovalRequest
        {
            Content = proposal,
            Reasoning = reasoning,
            Confidence = confidence
        });
        return JsonConvert.SerializeObject(new { approval_request_id = request.Id, awaiting_response = true });
    }
}
```

---

### Deliverable: Reasoning Loop Implementation

Your code should:
1. ✅ Retrieve all relevant data (visit history, pet profile, medications, guidelines)
2. ✅ Analyze patterns iteratively
3. ✅ Draft a structured summary with confidence scores
4. ✅ Log every step with reasoning
5. ✅ Request approval before returning final output
6. ✅ Handle failures gracefully (log and escalate)

---

## Activity 3: Expose Tool Calls & Reasoning

### Goal
Make the agent's thinking visible so humans can understand, audit, and improve it.

### Instructions

#### Step 1: Build Reasoning Visualization
Create a UI component that displays:

**Raw Reasoning Trace (JSON):**
```json
{
  "pet_id": "bella-001",
  "request_timestamp": "2024-01-15T09:30:00Z",
  "reasoning_steps": [
    {
      "step": 1,
      "action": "retrieve_context",
      "thinking": "User asked for summary of today's visit. I need pet profile, medical history, and treatment guidelines.",
      "result": "Retrieved 5 prior visits, 3 active medications, pet profile",
      "confidence": 0.95,
      "timestamp": "2024-01-15T09:30:02Z"
    },
    {
      "step": 2,
      "action": "analyze_patterns",
      "thinking": "I notice Bella has had 3 ear infections in the past 12 months. This is clinically significant and suggests chronic condition.",
      "result": "Identified recurring ear infections as primary concern",
      "confidence": 0.88,
      "patterns_found": [
        {
          "condition": "Ear infection (recurring)",
          "frequency": 3,
          "evidence": ["2024-01-10 visit notes", "2023-11-22 visit notes", "2023-08-15 visit notes"]
        }
      ],
      "timestamp": "2024-01-15T09:30:05Z"
    },
    {
      "step": 3,
      "action": "retrieve_guidelines",
      "thinking": "For recurring ear infections, best practice is to rule out allergies. Need dermatology guidelines.",
      "result": "Retrieved standard treatment protocols for chronic otitis",
      "confidence": 0.92,
      "guidelines": ["Rule out allergies", "Consider allergy testing", "Dermatology referral if recurrent"],
      "timestamp": "2024-01-15T09:30:08Z"
    },
    {
      "step": 4,
      "action": "draft_summary",
      "thinking": "Synthesizing all findings: recurring infections + breed predisposition = recommend dermatology referral for allergy testing.",
      "result": "Draft summary created with 2 recommended actions",
      "confidence": 0.72,
      "timestamp": "2024-01-15T09:30:12Z"
    },
    {
      "step": 5,
      "action": "request_approval",
      "thinking": "My confidence is 72%, which is below ideal but reasonable for a recommendation. Surfacing for vet approval.",
      "result": "Approval request created; awaiting veterinarian review",
      "confidence": 1.0,
      "awaiting_response": true,
      "approval_request_id": "appr-2024-001",
      "timestamp": "2024-01-15T09:30:15Z"
    }
  ]
}
```

**Human-Readable Reasoning Display (UI):**
```
Clinical Summary Assistant is analyzing Bella's visit...

STEP 1: Gathering Context ✓
  → Retrieved 5 prior visits (2024, 2023, 2022)
  → Retrieved 3 active medications
  → Retrieved pet profile (Golden Retriever, 5 years old)
  Confidence: 95%

STEP 2: Identifying Patterns ✓
  → Bella has had 3 ear infections in the past year
  → Pattern frequency: HIGH (likely chronic condition)
  → Breed risk: Golden Retrievers prone to allergies
  Confidence: 88%

STEP 3: Checking Clinical Guidelines ✓
  → Guideline: Recurring infections suggest allergy testing
  → Recommended action: Dermatology referral for allergy workup
  → Standard follow-up: Re-evaluate after 4 weeks
  Confidence: 92%

STEP 4: Drafting Summary ✓
  → Assessment: Chronic otitis, likely allergy-related
  → Recommendation #1: Refer to dermatology for allergy testing
    Confidence: 72% (inference-based, not explicit in records)
  → Recommendation #2: Recheck ears in 2 weeks
    Confidence: 88% (standard protocol for recurring infection)

⏳ STEP 5: Awaiting Approval
  → Proposal ready for veterinarian review
  → [View Full Reasoning] [Approve] [Edit] [Reject]
```

#### Step 2: Log Tool Calls
Every time the agent calls a tool, log:
1. **Tool name & inputs**
2. **Why the agent called it** (reasoning)
3. **Outputs returned**
4. **Confidence in the result**

```csharp
public async Task<T> LoggedToolCallAsync<T>(string toolName, string reasoning, Func<Task<T>> toolCall)
{
    _logger.LogInformation("Tool call: {ToolName} | Reasoning: {Reasoning}", toolName, reasoning);
    
    var stopwatch = Stopwatch.StartNew();
    var result = await toolCall();
    stopwatch.Stop();
    
    _logger.LogInformation("Tool result: {ToolName} completed in {ElapsedMs}ms", toolName, stopwatch.ElapsedMilliseconds);
    
    return result;
}
```

#### Step 3: Build Sources Citation
Every recommendation must include sources. Create a citation system:

```csharp
public class Citation
{
    public string SourceType { get; set; } // "visit", "guideline", "medication", "pet_profile"
    public string SourceId { get; set; }   // visit-2024-001, guideline-dermatology, etc.
    public string SourceTitle { get; set; } // "Visit on Jan 10, 2024", "Dermatology Guidelines"
    public string ExcerptText { get; set; } // The relevant quote
    public decimal RelevanceScore { get; set; } // 0.0–1.0
    public string SourceUrl { get; set; } // Link to full source
}

public class RecommendedAction
{
    public string Action { get; set; }
    public string Rationale { get; set; }
    public List<Citation> SupportingCitations { get; set; }
    public decimal Confidence { get; set; }
}
```

**UI Display:**
```
RECOMMENDATION: "Refer to dermatology for allergy testing"

Rationale: Recurring ear infections in a breed prone to allergies suggests underlying 
allergen sensitivity. Standard protocol recommends allergy testing to guide treatment.

Supporting Evidence:
  [1] Visit on Jan 10, 2024 — "Bilateral ear infection, mild erythema"
  [2] Visit on Nov 22, 2023 — "Recurrent ear infection, same ear"
  [3] Visit on Aug 15, 2023 — "First reported ear infection"
  [4] Pet Profile — "Golden Retriever, breed-specific risk: allergies"
  [5] Dermatology Guidelines — "Allergy testing recommended for recurrent otitis"

Confidence: 72% (based on pattern inference, not explicit diagnosis)

[View All Sources] [Approve] [Request Clarification]
```

---

### Deliverable: Reasoning Transparency

You should have:
1. ✅ JSON-serializable reasoning trace for every agent run
2. ✅ Human-readable display of reasoning steps (in UI)
3. ✅ Citation system linking recommendations to sources
4. ✅ Tool call logs for debugging and auditing

---

## Activity 4: Test Agent Performance

### Goal
Validate that the agent reasons reliably and handles edge cases gracefully.

### Test Cases

#### Test 1: Happy Path (Common Case)
**Scenario:** Pet with clear clinical pattern (recurring ear infections)  
**Input:** Visit notes + pet history

**Expected Behavior:**
- ✅ Agent retrieves all relevant context
- ✅ Agent identifies recurring infection pattern
- ✅ Agent retrieves dermatology guidelines
- ✅ Agent drafts recommendation for allergy testing
- ✅ Confidence ≥70%
- ✅ Surfaces for approval

**Acceptance Criteria:**
- All reasoning steps visible
- Recommendations grounded in sources
- No hallucinated information
- Execution time <10 seconds

---

#### Test 2: Ambiguous Case (Lower Confidence)
**Scenario:** Pet with non-specific symptoms (lethargy, loss of appetite)  
**Input:** Vague visit notes + limited history

**Expected Behavior:**
- ✅ Agent retrieves available context
- ✅ Agent notes missing data (no prior visits, no clear pattern)
- ✅ Agent asks for clarification (request tool)
- ✅ Agent drafts summary with **low confidence** (<60%)
- ✅ Flags for mandatory veterinarian review
- ✅ Surfaces for approval with confidence warning

**Acceptance Criteria:**
- Agent explicitly states "insufficient data"
- Recommendations are tentative ("Consider checking…")
- Confidence score accurately reflects uncertainty
- Does NOT recommend definitive actions without more data

---

#### Test 3: Out-of-Scope Request
**Scenario:** Request asks agent to "perform surgery" or "prescribe medication"  
**Input:** "Create a surgery plan for Bella"

**Expected Behavior:**
- ✅ Agent detects out-of-scope keyword
- ✅ Agent logs failure with reason
- ✅ Agent escalates to human
- ✅ Returns error message: "This request is outside my scope. Please contact a veterinarian."

**Acceptance Criteria:**
- Agent does NOT attempt to proceed
- Request is logged for audit
- Clear error message to user

---

#### Test 4: Tool Failure Handling
**Scenario:** Database is unavailable when agent tries to retrieve visit records  
**Input:** Normal summary request, but retrieval fails

**Expected Behavior:**
- ✅ Agent catches exception
- ✅ Agent logs failure reason
- ✅ Agent attempts fallback (use cached data, if available)
- ✅ If no fallback, agent escalates
- ✅ Clear error message: "Unable to retrieve complete history. Please try again or contact support."

**Acceptance Criteria:**
- No agent crashes
- Error is logged for debugging
- User gets clear message

---

#### Test 5: Token/Cost Limit
**Scenario:** Agent enters a reasoning loop that repeats indefinitely  
**Input:** Malformed request that confuses the agent

**Expected Behavior:**
- ✅ Agent hits max loop count (e.g., 10 iterations)
- ✅ Agent stops and returns best-effort output
- ✅ Logs warning: "Max reasoning iterations reached"
- ✅ Escalates for human review

**Acceptance Criteria:**
- Loop never exceeds max limit
- Agent returns partial output rather than crashing

---

### Implementation: Test Suite

Create an XUnit test file:

```csharp
public class ClinicalSummaryAgentTests
{
    private readonly ClinicalSummaryAgent _agent;

    public ClinicalSummaryAgentTests()
    {
        _agent = new ClinicalSummaryAgent(/* dependencies */);
    }

    [Fact]
    public async Task AnalyzePetVisit_HappyPath_ReturnsStructuredSummary()
    {
        // Arrange
        var petId = "bella-001";
        var visitNotes = "Presenting complaint: ear infection. Bilateral erythema noted.";
        
        // Act
        var result = await _agent.AnalyzePetVisitAsync(petId, visitNotes);
        
        // Assert
        Assert.Equal(AgentStatus.AwaitingApproval, result.Status);
        Assert.NotEmpty(result.ReasoningSteps);
        Assert.NotNull(result.DraftSummary);
        Assert.True(result.DraftSummary.OverallConfidence >= 0.70m, "Summary confidence should be ≥70%");
    }

    [Fact]
    public async Task AnalyzePetVisit_AmbiguousCase_FlagsLowConfidence()
    {
        // Arrange
        var petId = "unknown-pet";
        var visitNotes = "Pet seems unwell. Needs investigation.";
        
        // Act
        var result = await _agent.AnalyzePetVisitAsync(petId, visitNotes);
        
        // Assert
        Assert.NotNull(result.ConfidenceNote);
        Assert.Contains("Lower confidence", result.ConfidenceNote);
    }

    [Fact]
    public async Task AnalyzePetVisit_OutOfScope_Escalates()
    {
        // Arrange
        var petId = "bella-001";
        var visitNotes = "Can you perform surgery on Bella?";
        
        // Act
        var result = await _agent.AnalyzePetVisitAsync(petId, visitNotes);
        
        // Assert
        Assert.Equal(AgentStatus.OutOfScope, result.Status);
    }

    [Fact]
    public async Task AnalyzePetVisit_ReasoningVisible_AllStepsLogged()
    {
        // Arrange
        var petId = "bella-001";
        var visitNotes = "Follow-up visit for ear infection";
        
        // Act
        var result = await _agent.AnalyzePetVisitAsync(petId, visitNotes);
        
        // Assert
        Assert.True(result.ReasoningSteps.Count >= 4, "Should have at least 4 reasoning steps");
        Assert.All(result.ReasoningSteps, step => 
        {
            Assert.NotEmpty(step.Action);
            Assert.NotEmpty(step.Thinking);
            Assert.True(step.Confidence >= 0 && step.Confidence <= 1, "Confidence must be 0.0–1.0");
        });
    }
}
```

---

### Checkpoint 2: Agent Evaluation

Before proceeding, verify:
- [ ] Agent completes end-to-end reasoning for a patient visit
- [ ] All reasoning steps are visible and logged
- [ ] Agent respects tool constraints (no unsupervised execution)
- [ ] Vets can review and approve the final output
- [ ] You can explain what the agent was "thinking" at each step
- [ ] Agent handles failures gracefully (no crashes)
- [ ] Confidence scores accurately reflect uncertainty

---

## Activity 5: Deploy & Monitor

### Goal
Put the agent into use and monitor its performance.

### Instructions

#### Step 1: Create a Web UI
Build a simple interface for vets to:
1. **Paste or select a visit** (new appointment with notes)
2. **See agent analysis** (reasoning steps, patterns, recommendations)
3. **Approve/edit/reject** the draft summary
4. **View sources** (links to supporting visit records)
5. **Log feedback** (was the agent correct? helpful? misleading?)

#### Step 2: Define Success Metrics
Measure agent performance over 50–100 real visits:

| Metric | Target | How to Measure |
|--------|--------|-----------------|
| Approval Rate | ≥85% | % of drafts vets approve without major edits |
| Confidence Accuracy | ≥80% | % of time actual vet approval matches agent confidence |
| Pattern Detection | ≥90% | % of clinically relevant patterns identified |
| Escalation Rate | ≤10% | % of requests marked out-of-scope or requiring human review |
| Execution Time | <10s | Average seconds per analysis |
| User Satisfaction | ≥4/5 | Vet feedback on helpfulness and clarity |

#### Step 3: Monitor in Production
Log every agent run:
- Inputs (pet ID, visit notes)
- Reasoning steps (all 5+)
- Final output (summary, recommendations)
- Human feedback (approved? edited? rejected?)
- Performance (execution time, token usage, cost)

---

### Reflection: Evaluating Your Agent

#### Question 1: What reasoning does the agent do that a static template couldn't?
**Example answer:** A template would always recommend "follow-up in 2 weeks." The agent analyzes the specific pet's history (e.g., "Bella had 3 ear infections in the past year") and recommends "dermatology referral" based on that pattern. The agent reasons about clinical significance; a template just fills blanks.

#### Question 2: What decisions does the agent still get wrong? Why?
**Example answer:** The agent sometimes confuses correlation with causation. It sees Bella on antibiotics for 2 months and recommends stopping them, when actually they're necessary for the underlying condition. The agent lacks domain knowledge about medication duration. We'd improve this by adding a tool to retrieve "standard medication durations" by condition.

#### Question 3: If you added one more tool to the agent, what would it be? Why?
**Example answer:** A tool to "retrieve breed-specific risk guidelines." Bella is a Golden Retriever; the agent should automatically know which conditions are breed-predisposed. Right now it infers breed risk from visit history, which is slower and less reliable.

#### Question 4: Could you deploy this agent today without vet approval for each output? Why or why not?
**Example answer:** No. The agent's confidence is 70–90%, which is good but not 99%+. Clinical decisions have high stakes—a wrong recommendation could harm a pet. Vets must review before the summary is saved or sent to owners. In future labs, if confidence approaches 98%+, we might auto-approve routine cases (e.g., healthy pet, routine check-up).

---

## Summary & What's Next

### What You've Built

**Lab 3 Outputs:**

1. **Clinical Summary Agent**  
   An AI system that reasons through clinical data, identifies patterns, and drafts evidence-based summaries—all with visible reasoning and human approval gates.

2. **Bounded Execution Model**  
   Proof that agents can be reliable when scoped, constrained, and observable. The agent can retrieve and analyze; it cannot execute or decide alone.

3. **Reasoning Transparency**  
   Every step the agent takes is visible: what it observed, what it thought, what tools it called, what it concluded. This enables human oversight and continuous improvement.

### Key Insights

| Insight | What It Means |
|---------|---------------|
| **Agents are reasoning engines, not automation scripts** | They handle novel cases that rigid rules cannot. |
| **Scope is safety** | Tight scope = reliable behavior. Vague scope = unpredictable behavior. |
| **Escalation is a feature** | An agent that asks for help is working correctly. |
| **Observability enables trust** | Humans trust what they can see and explain. |

### The Agent Pattern So Far

| Lab | AI Capability | Human Role | Safety Mechanism |
|-----|---------------|-----------|-------------------|
| Lab 1: RAG | Retrieve context | Decide | User judgment |
| Lab 2: HITL | Draft artifacts | Review & approve | Approval gates |
| Lab 3: Single Agent | Reason across steps | Review & approve | Tool constraints + approval gates |
| **Lab 4: Multi-Agent** | **Multiple perspectives** | **Review & approve** | **Agent coordination + approval gates** |

### Connection to Lab 4: Multi-Agent Systems

Lab 3 proved that a single agent can reason reliably within a bounded domain. Lab 4 asks: **What happens when no single perspective is enough?**

Imagine Bella needs a complex diagnosis. The Clinical Reasoning Agent analyzes the symptoms. But a separate Compliance Agent must check: "Can the owner afford this test?" And a Communication Agent must draft the message in a way that doesn't alarm the owner.

Lab 4 introduces **multi-agent orchestration**—how to compose multiple agents safely, with clear authority and conflict resolution.

---

## Glossary

- **Agent:** An AI system that perceives (observes data), deliberates (reasons about it), and acts (calls tools) iteratively.
- **Bounded Decision-Making:** An agent with explicit scope, tools, and constraints. The opposite of "free-roaming" AI.
- **Reasoning Loop:** The cycle: Observe → Think → Act → Pause → Repeat.
- **Tool Constraint:** Explicit whitelist of what an agent can call. Everything else is forbidden.
- **Approval Gate:** A point where the agent pauses and surfaces its output for human review before proceeding.
- **Escalation:** When an agent detects it cannot proceed (out of scope, insufficient data, low confidence) and asks a human for help.
- **Observable Reasoning:** Logging every step the agent takes so humans can audit, debug, and improve it.

---

## References

- **Learning Objectives:** See `labs/learning-objectives.md` for Lab 3's pedagogical context
- **Technical Patterns:** See `labs/technical-patterns.md`, section "Lab 3: Single-Agent Workflows," for implementation details
- **Semantic Kernel:** https://learn.microsoft.com/en-us/semantic-kernel/ (for function calling and plugins)
- **Azure AI Search:** https://learn.microsoft.com/en-us/azure/search/ (for retrieving clinical context)

---

## Acknowledgments

- **Toby:** Learning objectives and pedagogical framework
- **Josh:** Technical patterns and implementation guidance
- **Max Bush:** Project leadership and domain context

**Lab 3 authored by CJ, Technical Writer**  
**Last updated:** January 2024
