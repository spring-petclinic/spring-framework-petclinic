# Technical Patterns: PetClinic AI Modernization Labs

**Domain:** AI and App Modernization  
**Author:** Josh (Domain Expert)  
**Purpose:** Technical foundation for labs 1-5. Reference this for architectural decisions, system design patterns, and implementation guidance.

---

## Lab 1: In-App AI with RAG (Assistive AI)

### Indexing Strategy for PetClinic Data

**Domain Model to Index:**
- **Owners** (name, contact, history)
- **Pets** (name, type, breed, weight, notes)
- **Visits** (date, type, notes, treatments)
- **Clinical Notes** (observations, diagnoses, follow-up actions)

**Indexing Approach:**
1. **Granular Chunking:** Index at the document level (one Pet + full history = one document), not at paragraph level. This preserves context and reduces hallucination from fragmented information.
2. **Metadata Enrichment:** Tag each indexed record with:
   - `entity_type` (owner | pet | visit | note)
   - `entity_id` (PetClinic database ID)
   - `created_date` / `modified_date`
   - `clinical_relevance` (high | medium | low)
3. **Multi-Field Mapping:** Use Azure AI Search field definitions:
   - `text` (searchable, full content)
   - `summary` (filterable, auto-generated 1-2 line summary)
   - `entity_id` (filterable, for citation tracking)
   - `raw_json` (not searchable, for exact data retrieval)

**Azure AI Search Configuration:**
- Use **semantic search** (BM25 + semantic re-ranking) to rank clinically relevant results above keyword matches
- Enable **vector fields** for embedding-based retrieval (prepare for future semantic models)
- Create a **suggester** for autocomplete on pet/owner names

### Retrieval Patterns

**Semantic Search (Primary Pattern):**
```
1. User asks: "What health issues has Bella (the dog) had?"
2. Convert to semantic search: "dog named Bella health problems conditions"
3. Azure AI Search re-ranks BM25 results using semantic understanding
4. Filter results to entity_id = "Bella" to avoid confusion with other pets
5. Return top 3-5 visits/notes with highest semantic relevance
```

**Hybrid Retrieval (Safety-Critical Queries):**
- Use both keyword AND vector search for questions about:
  - Medications, allergies, contraindications
  - Age-critical treatments
  - Breed-specific conditions
- Rank by semantic relevance but always include exact-match keyword results
- Require user confirmation if results vary between methods (signals ambiguity)

**Fallback Patterns:**
- If semantic search < 0.5 confidence: offer clarifying follow-up questions
- If no results found: suggest browsing all visits/pets for this owner
- If results are contradictory: surface both options and explain the difference

### Grounding and Citation Approaches

**Citation Metadata Structure:**
Each retrieved chunk must carry:
```json
{
  "cited_record": {
    "entity_type": "visit",
    "entity_id": "visit-2024-001",
    "pet_name": "Bella",
    "visit_date": "2024-01-15",
    "clinician": "Dr. Smith"
  },
  "excerpt": "Bella showed signs of ear infection...",
  "retrieval_score": 0.87,
  "source_url": "/app/pets/bella/visits/2024-001"
}
```

**Grounding Rules:**
1. **Only ground in indexed data.** Never accept LLM hallucinations as fact.
2. **Acknowledge knowledge cutoffs.** If no visit data exists for >6 months, say so.
3. **Surface contradictions.** If two visits contradict each other, show both with dates and ask the clinician which is authoritative.
4. **Metadata-aware responses:**
   - If retrieved data is >1 year old, mark as "historical" not current
   - If multiple pets have similar conditions, disambiguate by name + ID

**Citation Display in UI:**
- Show inline citations: "Bella had an ear infection [on Jan 15, 2024](link to visit record)"
- Include citation count in answer header: "3 visits cited"
- Provide "View Source" button for each citation linking directly to the clinical record

### Azure AI Search & Semantic Kernel Integration Patterns

**Index Creation (C# with Semantic Kernel):**
```csharp
// Create Azure AI Search index aligned to PetClinic data model
var indexClient = new SearchIndexClient(endpoint, new AzureKeyCredential(key));

var index = new SearchIndex("petclinic-index")
{
    Fields = new FieldCollection
    {
        new SearchField("id", SearchFieldDataType.String) { IsKey = true },
        new SearchField("entity_type", SearchFieldDataType.String) { IsFilterable = true },
        new SearchField("entity_id", SearchFieldDataType.String) { IsFilterable = true, IsFacetable = true },
        new SearchField("text", SearchFieldDataType.String) { IsSearchable = true, IsRetrievable = true },
        new SearchField("summary", SearchFieldDataType.String) { IsSearchable = true },
        new SearchField("embedding", SearchFieldDataType.Collection(SearchFieldDataType.Single)) { IsSearchable = true },
        new SearchField("created_date", SearchFieldDataType.DateTimeOffset) { IsFilterable = true, IsSortable = true }
    },
    SemanticConfiguration = new SemanticConfiguration("default", ...)
};

await indexClient.CreateIndexAsync(index);
```

**RAG Kernel Implementation (Semantic Kernel):**
```csharp
// Build a RAG chain: user query → search → prompt → LLM
var kernel = new KernelBuilder()
    .WithAzureOpenAIChatCompletion(...)
    .Build();

// Register Azure AI Search as a plugin
var searchPlugin = kernel.ImportPluginFromObject(
    new AzureAISearchPlugin(searchClient),
    "search"
);

// Define RAG prompt
var ragPrompt = @"
You are a veterinary assistant. Answer the user's question using ONLY the provided 
clinical records. If information is not in the records, say 'I don't have data on that.'

Records:
{{$retrieved_records}}

Question: {{$question}}

Answer (with inline citations):";

// Execute RAG chain
var result = await kernel.InvokeAsync<string>(
    ragPrompt,
    new KernelArguments
    {
        { "question", userQuestion },
        { "retrieved_records", await searchPlugin.SearchAsync(userQuestion) }
    }
);
```

**Confidence Scoring:**
- Combine Azure AI Search `@search.score` (BM25 relevance) with semantic re-ranking score
- Formula: `confidence = (semantic_score * 0.7) + (bm25_score * 0.3)`
- Display confidence only if > 0.6; if < 0.6, surface uncertainty ("I'm not confident about this answer")

---

## Lab 2: AI-Assisted Actions with Human-in-the-Loop

### Approval Workflow Patterns

**Draft-Approve Flow (Primary Pattern):**
```
1. User triggers action: "Summarize Bella's visit history"
2. AI generates DRAFT artifact (summary, follow-up plan, message to owner)
3. System stores draft with:
   - generated_content (what AI produced)
   - reasoning_trace (how AI arrived at this)
   - source_citations (which records informed it)
   - confidence_scores (per statement)
4. UI shows draft with "Edit" and "Approve" buttons
5. User can:
   a) Approve as-is → artifact becomes final, persisted to database
   b) Edit → manual changes override AI suggestions
   c) Reject → discarded, user can regenerate
6. If approved, audit log records: who approved, when, any edits made
```

**Conditional Approval (Advanced Pattern):**
- High-confidence recommendations (>0.85): Single-click approval
- Medium-confidence (0.6-0.85): Require user to read reasoning before approval
- Low-confidence (<0.6): Require explicit edits OR re-generation request

**Chainable Approvals:**
- Lab 3+ pattern: Approval for *intermediate* steps (e.g., agent drafts analysis → human approves → agent proceeds to next step)

### Confidence Scoring Approaches

**Per-Statement Confidence:**
When AI generates a draft, attach confidence metadata to each semantic unit:
```json
{
  "draft": {
    "content": "Bella has had 3 ear infections in the past year.",
    "statements": [
      {
        "text": "Bella has had 3 ear infections",
        "confidence": 0.92,
        "supported_by": ["visit-2024-001", "visit-2023-009", "visit-2023-006"],
        "reasoning": "All 3 visits explicitly mention ear infection diagnosis"
      },
      {
        "text": "in the past year",
        "confidence": 0.88,
        "supported_by": ["visit-2024-001 (Jan 2024)", "visit-2023-009 (Oct 2023)", "visit-2023-006 (Sep 2023)"],
        "reasoning": "Dates confirm all within 12-month window"
      }
    ]
  }
}
```

**Confidence Factors:**
1. **Data freshness:** Recent data (< 6 months) = +0.1; older data = -0.1
2. **Source agreement:** Multiple sources say same thing = +0.15; single source = 0
3. **LLM reasoning:** Chain-of-thought shows clear logic = +0.1; vague reasoning = -0.1
4. **Domain specificity:** Clinical terms in original records = +0.1; inference = -0.05

**Composite Confidence (for whole artifact):**
```
artifact_confidence = AVERAGE(statement_confidences) adjusted by:
  + 0.05 if all statements grounded in retrieved data
  - 0.1 if any statement is inference or extrapolation
  - 0.15 if recommendations exist without explicit clinical basis
```

### Explainability Metadata Structure

**Reasoning Trace (capture what the LLM "thought"):**
```json
{
  "reasoning_trace": {
    "step_1_retrieval": {
      "query": "Bella ear infection history",
      "records_found": 3,
      "summary": "Found 3 visits mentioning ear infection"
    },
    "step_2_analysis": {
      "pattern_identified": "Recurring ear infections (3 in 12 months)",
      "clinical_significance": "Suggests chronic condition, not one-off",
      "confidence": 0.88
    },
    "step_3_recommendation": {
      "generated": "Consider referral to dermatologist for allergy testing",
      "basis": "Recurring infections often indicate underlying allergy",
      "confidence": 0.72,
      "reasoning": "This is inference; no allergy mentioned in records"
    }
  }
}
```

**Why This Matters:**
- User can see *exactly* where the AI's logic came from
- Identifies inferences vs. facts: "This is my conclusion, not in the records"
- Allows user to contest specific reasoning steps, not the whole artifact

**Surface in UI:**
```
[DRAFT] Bella Follow-up Recommendation
════════════════════════════════════════
Suggested: "Refer to dermatologist for allergy testing"

Why: Bella has had 3 ear infections in the past 12 months, 
     suggesting a chronic condition (likely allergy-related).

Confidence: 72% 
⚠️ Note: This is a clinical inference, not explicitly stated in her records.

Sources:
  - Visit 2024-01-15: Ear infection
  - Visit 2023-10-22: Ear infection  
  - Visit 2023-09-10: Ear infection

[Edit] [Approve] [Reject] [Regenerate]
```

### UI Patterns for Draft/Approve Flows

**Draft Editing Strategy:**
- Support in-line editing with smart suggestions
- If user edits a statement, system re-scores confidence (user override = 1.0 confidence)
- Track which parts are AI-generated vs. user-edited in approval audit log

**Visual Distinction:**
```
[AI-GENERATED] Bella has had 3 ear infections    [confidence: 92%]
┌─────────────────────────────────────────────────────────────┐
│ [USER-EDITED] in the past year, suggesting chronic issues   │
│               (Originally: "in the past year")               │
└─────────────────────────────────────────────────────────────┘
[AI-GENERATED] Consider allergy testing           [confidence: 72%]
```

**Approval Checkpoint UI:**
- Show side-by-side: AI draft + reasoning trace
- One-click approve for high confidence (>0.85)
- Require deliberate action (checkbox "I've reviewed the reasoning") for medium confidence
- Require explicit changes + comment for low confidence

**Batch Approval Pattern (for multi-item recommendations):**
- Show all draft items with visual grouping by confidence level
- Allow user to approve all high-confidence items at once
- Require individual review for medium/low confidence items

---

## Lab 3: Single-Agent Workflows (Goal-Oriented AI)

### Agent Role Definition Patterns

**Role Contract (Declarative Definition):**
```json
{
  "agent_name": "Clinical Assistant",
  "goal": "Improve clinical documentation and follow-up planning by drafting summaries and next steps",
  
  "scope": {
    "can_do": [
      "Read clinical records (visits, notes, medications)",
      "Analyze patterns in historical data",
      "Draft visit summaries and follow-up recommendations",
      "Request human approval before any action persists"
    ],
    "cannot_do": [
      "Create new medical records without approval",
      "Schedule appointments",
      "Dispense medications",
      "Contact owners directly",
      "Make autonomous medical decisions"
    ]
  },

  "authority_level": "suggest_and_draft_only",
  
  "reasoning_mode": "chain_of_thought_with_human_checkpoints",
  
  "tools_available": [
    "retrieve_clinical_records",
    "request_human_approval",
    "log_reasoning_step"
  ]
}
```

**Why This Matters:**
- Defines the line between AI reasoning and human judgment
- Makes constraints explicit in code, not vague in natural language
- Enables multi-agent systems (Lab 4) to reference role contracts

### Tool Calling with Semantic Kernel

**Tool Definition (Register capabilities, not actions):**
```csharp
[KernelFunction("retrieve_records")]
[Description("Retrieve clinical records for a specific pet")]
public async Task<string> RetrieveRecords(
    [Description("Pet name or ID")] string petIdentifier,
    [Description("Filter by record type: visit | note | medication")] string? recordType = null
)
{
    // Implementation: call RAG search, return grounded results
    var results = await _searchClient.SearchAsync(
        $"pet: {petIdentifier} {recordType}",
        new SearchOptions { Size = 10 }
    );
    return JsonConvert.SerializeObject(results);
}

[KernelFunction("request_approval")]
[Description("Request human approval before executing an action")]
public async Task<ApprovalResult> RequestApproval(
    [Description("What approval is being requested")] string action,
    [Description("Why this action is needed")] string reasoning,
    [Description("Confidence in this recommendation (0.0-1.0)")] double confidence
)
{
    var approval = await _approvalService.CreateApprovalRequest(new ApprovalRequest
    {
        Action = action,
        Reasoning = reasoning,
        Confidence = confidence,
        Timestamp = DateTime.UtcNow
    });
    
    // Block agent until human responds
    return await _approvalService.WaitForApprovalAsync(approval.Id);
}

[KernelFunction("log_reasoning")]
[Description("Log a reasoning step for audit and explainability")]
public void LogReasoning(
    [Description("The reasoning step")] string step,
    [Description("Why this step was taken")] string justification
)
{
    _logger.LogInformation("Agent reasoning: {Step} | Justification: {Justification}", step, justification);
}
```

**Kernel Invocation (Agent Loop):**
```csharp
var kernel = new KernelBuilder()
    .WithAzureOpenAIChatCompletion(...)
    .Build();

// Register tools
kernel.ImportPluginFromObject(new ClinicalTools(_searchClient, _approvalService), "clinical");

var systemPrompt = @"
You are the Clinical Assistant. Your role is to:
1. Analyze clinical records
2. Draft summaries and recommendations
3. Request human approval before actions persist

You CANNOT create records or take autonomous action.
Always explain your reasoning.
Always request approval before suggesting changes to the system.
";

var messages = new List<ChatMessage>
{
    new SystemChatMessage(systemPrompt),
    new UserChatMessage("Summarize Bella's visit history and suggest next steps")
};

// Agentic loop (multiple turns)
var chatHistory = new ChatHistory(systemPrompt);
while (true)
{
    var response = await kernel.GetRequiredService<IChatCompletion>()
        .GetChatMessageContentsAsync(messages);
    
    if (response[0].Content.Contains("</tool_call>"))
    {
        // Agent called a tool; process it
        var toolResult = await ExecuteToolCall(response[0].Content);
        messages.Add(new AssistantChatMessage(response[0].Content));
        messages.Add(new ToolResultMessage(toolResult));
    }
    else
    {
        // Agent produced final answer
        return response[0].Content;
    }
}
```

### Bounded Execution (What Can/Can't an Agent Do)

**Execution Boundaries (Hard Constraints):**
1. **No persistence without approval:** Agent can *draft* but not *create* records
2. **No external communication:** Agent cannot send emails or SMS to owners
3. **No medication decisions:** Agent can *suggest* follow-up; clinician decides
4. **Tool call whitelist:** Agent can only call pre-registered, vetted tools
5. **Token/cost limits:** Set max tokens per reasoning loop (e.g., 5 tool calls max)

**Implementation Pattern:**
```csharp
// Middleware: intercept tool calls and enforce boundaries
public class ToolCallBoundaryEnforcer : KernelPlugin
{
    private static readonly HashSet<string> AllowedTools = new()
    {
        "retrieve_records",
        "request_approval",
        "log_reasoning"
    };
    
    private static readonly HashSet<string> ForbiddenToolPatterns = new()
    {
        "create_", "delete_", "update_", "send_", "notify_"
    };

    public override async Task<KernelContent> InvokeAsync(
        KernelFunctionInvocation invocation, 
        KernelContext context)
    {
        var toolName = invocation.Function.Name;
        
        // Check whitelist
        if (!AllowedTools.Contains(toolName))
            throw new UnauthorizedToolCallException($"Tool '{toolName}' not allowed");
        
        // Check forbidden patterns
        if (ForbiddenToolPatterns.Any(p => toolName.StartsWith(p)))
            throw new UnauthorizedToolCallException($"Tool pattern '{toolName}' violates boundaries");
        
        return await base.InvokeAsync(invocation, context);
    }
}
```

### Observable Reasoning (Surface Agent Thinking)

**Reasoning Trace (what the agent "thought"):**
```json
{
  "agent_reasoning_trace": [
    {
      "step": 1,
      "action": "retrieve_records",
      "input": "pet: Bella, recordType: visit",
      "reasoning": "User asked for visit history, so I need to fetch visits",
      "result": "Found 5 visits (2024, 2023, 2022)"
    },
    {
      "step": 2,
      "action": "log_reasoning",
      "thinking": "I notice a pattern: Bella had 3 ear infections in the past year. This is clinically significant.",
      "confidence": 0.88
    },
    {
      "step": 3,
      "action": "request_approval",
      "proposal": "Draft a recommendation to refer Bella to dermatology for allergy testing",
      "reasoning": "Recurring infections suggest underlying allergy; dermatology referral is standard practice",
      "confidence": 0.72,
      "awaiting_human_response": true
    }
  ]
}
```

**UI Display Pattern (Show Agent's Work):**
```
Clinical Assistant is analyzing Bella's records...

STEP 1: Retrieving clinical records
  ✓ Found 5 visits (2024, 2023, 2022)
  
STEP 2: Analyzing patterns
  → Identified: 3 ear infections in 12 months (recurring)
  → Clinical significance: Likely chronic condition
  
STEP 3: Generating recommendation
  → Proposal: "Refer to dermatology for allergy testing"
  → Reasoning: Recurring infections → allergy hypothesis
  → Confidence: 72% (this is inference, not explicit in records)
  
⏳ AWAITING APPROVAL: Do you approve this recommendation?
   [View Full Reasoning] [Approve] [Edit] [Reject]
```

**Explainability Through Reasoning Tokens:**
- Use OpenAI extended thinking (if available) to capture step-by-step logic
- If not available, explicitly log reasoning at each tool call
- In UI, allow users to "expand" any step to see detailed reasoning

---

## Lab 4: Multi-Agent System (MAS)

### Agent Role Contracts

**Define each agent as a separate role with clear boundaries:**

#### Agent 1: Clinical Reasoning Agent
```json
{
  "name": "Clinical Reasoning",
  "role": "Analyze clinical data and identify patterns",
  "inputs": ["clinical_records", "pet_profile"],
  "outputs": ["clinical_analysis", "risk_assessment", "evidence"],
  "can_invoke": ["retrieve_records", "log_reasoning"],
  "cannot_invoke": ["request_approval", "create_record"],
  "conflict_resolution": "Defers to Compliance Agent on safety/ethics questions"
}
```

#### Agent 2: Compliance & Safety Agent
```json
{
  "name": "Compliance & Safety",
  "role": "Validate decisions against safety policies, ethics, and regulations",
  "inputs": ["proposed_action", "clinical_analysis"],
  "outputs": ["safety_verdict", "compliance_notes", "risk_level"],
  "can_invoke": ["retrieve_records", "log_reasoning"],
  "cannot_invoke": ["request_approval", "contact_owner"],
  "conflict_resolution": "Has veto authority; Clinical Reasoning must address concerns"
}
```

#### Agent 3: Communication Agent
```json
{
  "name": "Communication",
  "role": "Draft clear, empathetic communication for owners",
  "inputs": ["clinical_analysis", "safety_verdict"],
  "outputs": ["draft_message", "tone_assessment"],
  "can_invoke": ["retrieve_records", "log_reasoning"],
  "cannot_invoke": ["send_message", "create_record"],
  "conflict_resolution": "Takes feedback from Clinical and Compliance; can only revise drafts"
}
```

**Why Role Contracts Matter:**
- Separates concerns: clinical thinking ≠ safety checking ≠ communication
- Prevents shared authority: Compliance can veto, Clinical cannot override
- Enables auditing: each agent's decisions are traceable
- Scales with consistency: add new agents without breaking existing ones

### Orchestration Patterns

**Sequential Orchestration (Most Common):**
```
User Request
    ↓
1. Clinical Reasoning Agent
   - Analyze pet's clinical history
   - Identify patterns & risks
   - Output: clinical_analysis + evidence
    ↓
2. Compliance & Safety Agent
   - Review clinical_analysis against policies
   - Validate safety, ethics, regulations
   - Output: safety_verdict (PASS/FAIL/FLAG)
    ↓
3. Communication Agent (if PASS)
   - Draft owner message
   - Ensure clarity & empathy
   - Output: draft_message
    ↓
4. Human Approval Gateway
   - Clinician reviews all 3 agent outputs
   - Can approve, edit, or reject entire flow
    ↓
Final Output (Draft with audit trail)
```

**Implementation Pattern (C# with Semantic Kernel):**
```csharp
public async Task<MASResult> OrchestrateMultiAgent(string petId, string userQuery)
{
    var result = new MASResult();
    
    // Stage 1: Clinical Reasoning
    var clinicalAgent = new ClinicalReasoningAgent(_kernel);
    var clinicalOutput = await clinicalAgent.AnalyzeAsync(petId, userQuery);
    result.ClinicalAnalysis = clinicalOutput;
    
    if (!clinicalOutput.Success)
        return result; // Short-circuit if analysis fails
    
    // Stage 2: Compliance & Safety Review
    var complianceAgent = new ComplianceAgent(_kernel);
    var safetyVerdictOutput = await complianceAgent.ReviewAsync(clinicalOutput);
    result.SafetyVerdictOutput = safetyVerdictOutput;
    
    if (safetyVerdictOutput.Verdict == SafetyVerdictType.FAIL)
    {
        result.Status = "BLOCKED_BY_SAFETY_POLICY";
        return result; // Do not proceed
    }
    
    // Stage 3: Communication Drafting
    var commAgent = new CommunicationAgent(_kernel);
    var draftOutput = await commAgent.DraftAsync(clinicalOutput, safetyVerdictOutput);
    result.DraftCommunication = draftOutput;
    
    // Stage 4: Audit trail & human approval
    result.AuditTrail = new AuditTrail
    {
        Stage1_Clinical = clinicalOutput,
        Stage2_Safety = safetyVerdictOutput,
        Stage3_Communication = draftOutput,
        OverallStatus = "READY_FOR_APPROVAL"
    };
    
    return result;
}
```

**Parallel Orchestration (Specialized Pattern):**
When agents are *independent* (e.g., gathering info), run in parallel:
```
User Request
    ↓
┌─────────────────────────────────────────┐
├─> Agent A: Fetch visit history          │
├─> Agent B: Fetch medication history     │
├─> Agent C: Fetch breed-specific risks   │
└─────────────────────────────────────────┘
         (await all tasks)
    ↓
Merge results → Sequential orchestration begins
```

**Trigger-Based Orchestration (Advanced Pattern):**
Agents trigger the next stage based on findings:
```
Clinical Reasoning: "Found potential medication interaction"
    ↓ [triggers conditional path]
Compliance Agent: "Interaction flagged in policy"
    ↓ [triggers escalation]
Communication Agent: "Draft message recommends vet consultation"
    ↓ [triggers human approval]
```

### Conflict Resolution Strategies

**Authority Hierarchy (Recommended):**
```
Human Clinician (final authority)
    ↓
Compliance Agent (veto authority on safety)
    ↓
Clinical Reasoning Agent (primary analysis)
    ↓
Communication Agent (output only, no veto)
```

**Conflict Resolution Rules:**

1. **Clinical vs. Compliance Conflict:**
   - Clinical says: "This allergy testing is recommended"
   - Compliance says: "Owner has 3 denied claims in past 6 months; cost-prohibitive"
   - **Resolution:** Compliance flag is recorded, Communication drafts message explaining constraints

2. **Clinical vs. Communication Conflict:**
   - Clinical produces: "Bella needs aggressive antibiotic therapy"
   - Communication says: "This language is alarming and may provoke owner anxiety"
   - **Resolution:** Clinical reasoning stands; Communication rewrites tone without changing substance

3. **Multi-Agent Disagreement (Rare but Critical):**
   - **Pattern:** Log all disagreements as audit entries
   - **Action:** Flag for human review immediately
   - **Never auto-resolve:** Disagreement signals uncertainty; escalate to human

**Explicit Conflict Logging:**
```json
{
  "stage": "compliance_review",
  "conflict_type": "cost_vs_recommendation",
  "clinical_reasoning": "Allergy testing is standard for recurring infections",
  "compliance_concern": "Owner cannot afford diagnostic; policy recommends alternative",
  "resolution": "ESCALATE_TO_HUMAN",
  "timestamp": "2024-01-15T10:30:00Z",
  "human_review_required": true
}
```

### Shared Context Without Shared Authority

**Shared Context (Read-Only Inputs):**
All agents can read:
- Clinical records (visits, notes, medications)
- Pet profile (demographics, breed, age)
- Owner profile (communication preferences, past interactions)
- Policies & guidelines (shared reference)

```csharp
public class SharedContext
{
    public PetRecord PetData { get; set; }          // read-only
    public List<Visit> ClinicalHistory { get; set; } // read-only
    public OwnerProfile OwnerData { get; set; }      // read-only
    public PolicySet CompliancePolicies { get; set; } // read-only
}

// Agents receive this context but cannot modify it
public async Task<Output> AnalyzeAsync(SharedContext context, string query)
{
    // Use context, but don't mutate it
    var analysis = AnalyzeClinicalHistory(context.ClinicalHistory);
    return new Output { Analysis = analysis };
}
```

**No Shared Authority (Each Agent Owns Its Decision):**
- Clinical Reasoning Agent owns clinical analysis; no other agent changes it
- Compliance Agent owns safety verdict; Clinical cannot override
- Communication Agent owns message tone; Clinical cannot mandate phrasing

**Shared State Machine (Track Progress Without Central Control):**
```csharp
public enum MASStage { Clinical = 1, Compliance = 2, Communication = 3, Approval = 4 }

public class MASExecutionState
{
    public MASStage CurrentStage { get; set; } = MASStage.Clinical;
    
    // Each agent records its own output
    public ClinicalOutput ClinicalResult { get; set; }
    public SafetyVerdictOutput SafetyResult { get; set; }
    public CommunicationOutput CommResult { get; set; }
    
    // Progression rules
    public bool CanAdvanceToCompliance => ClinicalResult?.Success ?? false;
    public bool CanAdvanceToCommunication => SafetyResult?.Verdict != SafetyVerdictType.FAIL;
    public bool ReadyForApproval => CommResult != null;
}
```

**Audit Trail (Complete Transparency):**
Every agent decision is logged with:
- What was input
- What was output
- Reasoning (chain-of-thought)
- Confidence/uncertainty
- Timestamp & agent identity

---

## Lab 5: Platform & Governance (Enterprise AI)

### Centralized Model Access Patterns

**Model Registry (Single Source of Truth):**
```json
{
  "models": [
    {
      "id": "gpt-4-turbo",
      "provider": "Azure OpenAI",
      "endpoint": "https://petclinic-ai.openai.azure.com/",
      "deployment_id": "gpt4-prod-v1",
      "version": "2024-04-09",
      "cost_per_1k_tokens": { "input": 0.03, "output": 0.06 },
      "approved_for": ["general_qa", "clinical_summarization", "owner_communication"],
      "blocked_for": ["autonomous_decisions", "medical_diagnosis"],
      "rate_limits": { "rpm": 100, "tpm": 100000 },
      "slo": "99.9% uptime"
    }
  ]
}
```

**Centralized Kernel Configuration (All Teams Use Same):**
```csharp
public class CentralizedAIConfiguration
{
    public static IKernelBuilder ConfigureSharedKernel(this IKernelBuilder builder)
    {
        var config = new ConfigurationBuilder()
            .AddAzureKeyVault(new Uri(keyVaultUri), new DefaultAzureCredential())
            .Build();
        
        // All teams use same endpoint, credentials, model
        builder.WithAzureOpenAIChatCompletion(
            modelId: config["AzureOpenAI:ModelId"],
            endpoint: config["AzureOpenAI:Endpoint"],
            apiKey: config["AzureOpenAI:ApiKey"]
        );
        
        return builder;
    }
}

// Teams use this instead of their own config
var kernel = new KernelBuilder()
    .ConfigureSharedKernel()
    .Build();
```

**Access Control (Role-Based):**
```csharp
public class ModelAccessPolicy
{
    public bool CanUseModel(string userId, string modelId, string useCase)
    {
        var userRole = _authService.GetUserRole(userId);
        var policyRule = _policyStore.GetRule(modelId, useCase);
        
        if (!policyRule.AllowedRoles.Contains(userRole))
            throw new UnauthorizedAccessException($"Role {userRole} cannot use {modelId} for {useCase}");
        
        // Additional checks: cost limits, audit flags
        if (policyRule.RequiresAudit && !_auditService.IsEnabled(userId))
            throw new PolicyViolationException("Audit must be enabled for this use case");
        
        return true;
    }
}
```

### Prompt Versioning Strategies

**Semantic Prompt Registry:**
```json
{
  "prompts": [
    {
      "id": "clinical_summary",
      "version": "2.1",
      "description": "Summarize a pet's clinical history",
      "content": "You are a veterinary summarizer...",
      "parameters": {
        "temperature": 0.3,
        "max_tokens": 500,
        "top_p": 0.9
      },
      "approved_by": "Dr. Smith",
      "approval_date": "2024-01-10",
      "status": "ACTIVE",
      "notes": "v2.1: Improved citation accuracy; reduced hallucinations by 12%"
    },
    {
      "id": "clinical_summary",
      "version": "2.0",
      "status": "DEPRECATED",
      "sunset_date": "2024-02-10"
    }
  ]
}
```

**Prompt Evolution Without Disruption:**
```csharp
public async Task<string> SummarizeClinicalHistory(string petId)
{
    // Always fetch ACTIVE prompt version
    var prompt = await _promptRegistry.GetActiveAsync("clinical_summary");
    
    var kernel = _kernelFactory.Create();
    var result = await kernel.InvokeAsync<string>(
        prompt.Content,
        new KernelArguments { { "petId", petId } }
    );
    
    return result;
}
```

**A/B Testing Prompts:**
```csharp
// Route based on experiment cohort
var prompt = _experimentFramework.ShouldUse("prompt_variant_b", userId)
    ? await _promptRegistry.GetAsync("clinical_summary", version: "2.1")
    : await _promptRegistry.GetAsync("clinical_summary", version: "2.0");

// Track metrics separately per version
_metrics.RecordUsage("clinical_summary", version: prompt.Version, userId: userId);
```

**Rollback Strategy:**
- Keep previous 3 versions in registry
- If new version shows performance degradation (error rate > 5%, latency > 2x), auto-rollback
- Notify team of rollback + analysis

### Telemetry and Cost Tracking

**Comprehensive Usage Tracking:**
```csharp
public class AIPlatformTelemetry
{
    public async Task LogUsageAsync(UsageRecord record)
    {
        // Record in Application Insights / Azure Monitor
        _telemetryClient.TrackEvent("AIModelUsage", new Dictionary<string, string>
        {
            { "model_id", record.ModelId },
            { "prompt_version", record.PromptVersion },
            { "use_case", record.UseCase },
            { "user_id", record.UserId },
            { "team", record.Team }
        }, new Dictionary<string, double>
        {
            { "input_tokens", record.InputTokens },
            { "output_tokens", record.OutputTokens },
            { "latency_ms", record.LatencyMs },
            { "cost_usd", record.CostUsd }
        });
        
        // Store in database for historical analysis
        await _cosmosDb.InsertAsync(record);
    }
}
```

**Cost Calculation:**
```csharp
public class CostCalculator
{
    public decimal CalculateCost(string modelId, int inputTokens, int outputTokens)
    {
        var pricing = _modelRegistry.GetPricing(modelId);
        
        var inputCost = (inputTokens / 1000.0m) * pricing.InputCostPer1k;
        var outputCost = (outputTokens / 1000.0m) * pricing.OutputCostPer1k;
        
        return inputCost + outputCost;
    }
}
```

**Dashboards & Reporting:**
```
AI Platform Usage Dashboard
═══════════════════════════════════════════════════════════════

COSTS (Today)
├─ Total: $2,341.50
├─ By Model:
│  ├─ gpt-4-turbo: $1,890 (80.7%)
│  ├─ gpt-35-turbo: $451.50 (19.3%)
├─ By Team:
│  ├─ Clinical: $1,500 (64%)
│  ├─ Communication: $620 (26%)
│  ├─ Admin: $221.50 (10%)
└─ By Use Case:
   ├─ summarization: $1,200
   ├─ draft_generation: $890
   └─ qa: $251.50

USAGE METRICS
├─ API Calls: 4,521
├─ Avg Latency: 1.2s
├─ Error Rate: 0.3%
├─ Cache Hit Rate: 42%

QUALITY METRICS
├─ User Satisfaction: 4.2/5
├─ Citation Accuracy: 94%
├─ Approval Rate: 88%
```

**Budget Alerts:**
```csharp
public class BudgetMonitor
{
    public async Task CheckBudgetsAsync()
    {
        var dailyUsage = await _telemetryClient.GetDailyCostAsync();
        
        foreach (var team in _organization.Teams)
        {
            var teamCost = dailyUsage.Where(u => u.Team == team.Id).Sum(u => u.Cost);
            var budget = team.MonthlyAIBudget / 30; // Daily threshold
            
            if (teamCost > budget * 0.8) // 80% threshold
                await _alertService.NotifyAsync($"{team.Name} at 80% of daily budget");
            
            if (teamCost > budget)
                await _throttleService.LimitTeamAsync(team.Id); // Rate-limit this team
        }
    }
}
```

### Policy Enforcement Points

**Request-Time Validation:**
```csharp
public class AIRequestValidator : IKernelPlugin
{
    public async Task<bool> ValidateRequestAsync(KernelFunctionInvocation invocation)
    {
        var policies = await _policyStore.GetPoliciesAsync();
        
        // Check 1: Model approved for this use case?
        var modelPolicy = policies.FirstOrDefault(p => p.ModelId == invocation.ModelId);
        if (!modelPolicy.ApprovedUseCases.Contains(invocation.UseCase))
            throw new PolicyViolationException($"Model {invocation.ModelId} not approved for {invocation.UseCase}");
        
        // Check 2: User has quota remaining?
        var userQuota = await _quotaService.GetRemainingAsync(invocation.UserId);
        if (userQuota.MonthlyTokens < 1000)
            throw new QuotaExceededException("Monthly token quota exceeded");
        
        // Check 3: Sensitive data filter?
        if (invocation.Input.Contains("SSN") || invocation.Input.Contains("password"))
            throw new DataLeakageException("Prompt contains sensitive data");
        
        // Check 4: Output filtering (for PII, medical privacy)?
        var result = await invocation.InvokeAsync();
        var filtered = await _outputFilter.FilterAsync(result, DataClassification.PII);
        
        return true;
    }
}
```

**Policy Decision Tree:**
```
User invokes AI function
    ↓
Is model in approved registry? ──NO──> REJECT
    ↓ YES
Is use case in model's approved list? ──NO──> REJECT
    ↓ YES
Does user have required role? ──NO──> REJECT
    ↓ YES
Does user have quota remaining? ──NO──> REJECT (or throttle)
    ↓ YES
Does prompt contain sensitive data? ──YES──> REJECT
    ↓ NO
Execute function
    ↓
Filter output for PII/PHI
    ↓
Log usage + cost
    ↓
Return to user
```

**Audit & Compliance Logging:**
```csharp
public class ComplianceLogger
{
    public async Task LogAIActionAsync(AIAction action)
    {
        var log = new ComplianceLog
        {
            Timestamp = DateTime.UtcNow,
            UserId = action.UserId,
            ModelId = action.ModelId,
            UseCase = action.UseCase,
            InputTokens = action.InputTokens,
            OutputTokens = action.OutputTokens,
            InputHash = Hash(action.Input), // Don't store raw input
            OutputHash = Hash(action.Output),
            PolicyChecksPassed = action.PolicyChecksPassed,
            Cost = action.Cost,
            Latency = action.Latency
        };
        
        await _complianceDb.InsertAsync(log);
        
        // For audit investigation (longer retention)
        if (action.UseCase == "clinical_recommendation")
            await _longTermArchive.InsertAsync(log);
    }
}
```

---

## Cross-Lab Principles

**These principles apply across all labs:**

1. **Explainability > Optimization:** Show reasoning before raw accuracy. A 85% confident answer with clear explanation beats 95% without.

2. **Grounding Over Hallucination:** Every claim must trace back to indexed data or explicit human input. If the LLM goes off-script, the system fails.

3. **Human Authority, Not Automation:** Approval workflows are *features*, not obstacles. They build trust and enable governance.

4. **Bounded Autonomy:** Agents suggest, decide, or draft—but never take irreversible action without human consent.

5. **Observable Reasoning:** Surface agent thinking. Users should be able to audit and contest any AI decision.

6. **Composable Patterns:** Labs build on each other: Lab 1 (RAG) informs Lab 2 (approval), Lab 3 (single agent) informs Lab 4 (multi-agent), Lab 5 (governance) sits across all.

---

## Implementation Checklist by Lab

### Lab 1: RAG
- [ ] Index PetClinic entities with metadata
- [ ] Implement semantic search + hybrid retrieval fallback
- [ ] Build citation tracking & grounding logic
- [ ] Create Azure AI Search index configuration
- [ ] Integrate with Semantic Kernel RAG chain
- [ ] Test confidence scoring on sample queries

### Lab 2: Human-in-the-Loop
- [ ] Design approval request data structure
- [ ] Build per-statement confidence metadata
- [ ] Implement reasoning trace capture
- [ ] Create UI draft/edit/approve flow
- [ ] Build confidence-based auto-approval logic
- [ ] Test approval audit trail

### Lab 3: Single Agent
- [ ] Define agent role contract (JSON)
- [ ] Register tools with Semantic Kernel
- [ ] Implement bounded execution middleware
- [ ] Build agentic loop with tool calling
- [ ] Capture and surface reasoning steps
- [ ] Test tool whitelist enforcement

### Lab 4: Multi-Agent
- [ ] Define 3 agent role contracts
- [ ] Implement sequential orchestration
- [ ] Build conflict resolution rules
- [ ] Create shared context (read-only)
- [ ] Implement audit trail for all decisions
- [ ] Test parallel execution for independent stages

### Lab 5: Governance
- [ ] Build model registry
- [ ] Create centralized kernel configuration
- [ ] Implement prompt versioning system
- [ ] Build usage telemetry pipeline
- [ ] Create cost tracking dashboard
- [ ] Implement policy validation middleware

---

## References

- **Azure AI Search:** https://learn.microsoft.com/en-us/azure/search/
- **Semantic Kernel:** https://github.com/microsoft/semantic-kernel
- **Azure OpenAI:** https://learn.microsoft.com/en-us/azure/ai-services/openai/
- **Responsible AI Principles:** https://www.microsoft.com/en-us/ai/responsible-ai

---

**Version:** 1.0  
**Last Updated:** 2024-01-15  
**Maintained By:** Josh (Domain Expert)
