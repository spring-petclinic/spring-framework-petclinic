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

**Index Creation (preferred Python bootstrap; Java app-native alternative):**
```python
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchFieldDataType,
    SearchIndex,
    SearchableField,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    SimpleField,
)

credential = DefaultAzureCredential()
index_client = SearchIndexClient(
    endpoint=endpoint,
    credential=credential,
    audience="https://search.azure.com",
)
search_client = SearchClient(
    endpoint=endpoint,
    index_name="petclinic-index",
    credential=credential,
    audience="https://search.azure.com",
)

index = SearchIndex(
    name="petclinic-index",
    fields=[
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="entity_type", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="entity_id", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SearchableField(name="text", type=SearchFieldDataType.String),
        SearchableField(name="summary", type=SearchFieldDataType.String),
        SimpleField(name="created_date", type=SearchFieldDataType.DateTimeOffset, filterable=True, sortable=True),
    ],
    semantic_search=SemanticSearch(
        configurations=[
            SemanticConfiguration(
                name="default",
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=SemanticField(field_name="summary"),
                    content_fields=[SemanticField(field_name="text")],
                ),
            )
        ]
    ),
)

index_client.create_or_update_index(index)
```

App-native Java services should use `DefaultAzureCredentialBuilder`, `SearchIndexClientBuilder`, and `SearchClientBuilder` with the same RBAC-enabled search service instead of key-based auth.

```java
TokenCredential credential = new DefaultAzureCredentialBuilder().build();

SearchIndexClient indexClient = new SearchIndexClientBuilder()
    .endpoint(endpoint)
    .credential(credential)
    .buildClient();

SearchClient searchClient = new SearchClientBuilder()
    .endpoint(endpoint)
    .indexName("petclinic-index")
    .credential(credential)
    .buildClient();
```

**RAG Kernel Implementation (Semantic Kernel):**
```java
OpenAIAsyncClient openAiClient = new OpenAIClientBuilder()
    .endpoint(endpoint)
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();

ChatCompletionService chatCompletion = OpenAIChatCompletion.builder()
    .withModelId("petclinic-chat")
    .withOpenAIAsyncClient(openAiClient)
    .build();

AzureAiSearchPlugin searchPlugin = new AzureAiSearchPlugin(searchClient);

Kernel kernel = Kernel.builder()
    .withAIService(ChatCompletionService.class, chatCompletion)
    .withPlugin(KernelPluginFactory.createFromObject(searchPlugin, "search"))
    .build();

String result = kernel.invokePromptAsync(
    """
    You are a veterinary assistant. Answer the user's question using ONLY the provided
    clinical records. If information is not in the records, say 'I don't have data on that.'

    Records:
    {{$retrieved_records}}

    Question: {{$question}}

    Answer (with inline citations):
    """,
    KernelArguments.builder()
        .withVariable("question", userQuestion)
        .withVariable("retrieved_records", searchPlugin.search(userQuestion))
        .build())
    .block()
    .getResult();
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
```java
public class ClinicalTools {

    public String retrieveRecords(String petIdentifier, String recordType) throws JsonProcessingException {
        SearchOptions options = new SearchOptions().setTop(10);
        String query = "pet: " + petIdentifier + " " + (recordType == null ? "" : recordType);

        var results = searchClient.search(query, options, Context.NONE);
        return objectMapper.writeValueAsString(results.stream().map(SearchResult::getDocument).toList());
    }

    public ApprovalResult requestApproval(String action, String reasoning, double confidence) {
        ApprovalRequest approval = approvalService.createApprovalRequest(
            new ApprovalRequest(action, reasoning, confidence, Instant.now())
        );

        return approvalService.waitForApproval(approval.id());
    }

    public void logReasoning(String step, String justification) {
        logger.info("Agent reasoning: {} | Justification: {}", step, justification);
    }
}
```

**Kernel Invocation (Agent Loop):**
```java
Kernel kernel = Kernel.builder()
    .withAIService(ChatCompletionService.class, chatCompletionService)
    .withPlugin(KernelPluginFactory.createFromObject(new ClinicalTools(searchClient, approvalService), "clinical"))
    .build();

String systemPrompt = """
    You are the Clinical Assistant. Your role is to:
    1. Analyze clinical records
    2. Draft summaries and recommendations
    3. Request human approval before actions persist

    You CANNOT create records or take autonomous action.
    Always explain your reasoning.
    Always request approval before suggesting changes to the system.
    """;

ChatHistory history = new ChatHistory();
history.addSystemMessage(systemPrompt);
history.addUserMessage("Summarize Bella's visit history and suggest next steps");

InvocationContext invocationContext = InvocationContext.builder()
    .withFunctionChoiceBehavior(FunctionChoiceBehavior.auto(true))
    .build();

while (true) {
    List<ChatMessageContent<?>> response = chatCompletionService
        .getChatMessageContentsAsync(history, kernel, invocationContext)
        .block();

    ChatMessageContent<?> assistantMessage = response.getFirst();
    history.addMessage(assistantMessage);

    if (assistantMessage.getContent() != null && assistantMessage.getContent().contains("function")) {
        history.addToolMessage(executeToolCall(assistantMessage.getContent()));
        continue;
    }

    return assistantMessage.getContent();
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
```java
public final class ToolCallBoundaryEnforcer {

    private static final Set<String> ALLOWED_TOOLS = Set.of(
        "retrieve_records",
        "request_approval",
        "log_reasoning"
    );

    private static final List<String> FORBIDDEN_PREFIXES = List.of("create_", "delete_", "update_", "send_", "notify_");

    public void validate(String toolName) {
        if (!ALLOWED_TOOLS.contains(toolName)) {
            throw new UnauthorizedToolCallException("Tool '%s' is not allowed".formatted(toolName));
        }

        if (FORBIDDEN_PREFIXES.stream().anyMatch(toolName::startsWith)) {
            throw new UnauthorizedToolCallException("Tool pattern '%s' violates execution boundaries".formatted(toolName));
        }
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

**Implementation Pattern (Java with Semantic Kernel):**
```java
public MASResult orchestrateMultiAgent(String petId, String userQuery) {
    MASResult result = new MASResult();

    ClinicalReasoningAgent clinicalAgent = new ClinicalReasoningAgent(kernel);
    ClinicalOutput clinicalOutput = clinicalAgent.analyze(petId, userQuery);
    result.setClinicalAnalysis(clinicalOutput);

    if (!clinicalOutput.success()) {
        return result;
    }

    ComplianceAgent complianceAgent = new ComplianceAgent(kernel);
    SafetyVerdictOutput safetyVerdict = complianceAgent.review(clinicalOutput);
    result.setSafetyVerdictOutput(safetyVerdict);

    if (safetyVerdict.verdict() == SafetyVerdictType.FAIL) {
        result.setStatus("BLOCKED_BY_SAFETY_POLICY");
        return result;
    }

    CommunicationAgent communicationAgent = new CommunicationAgent(kernel);
    CommunicationDraft draft = communicationAgent.draft(clinicalOutput, safetyVerdict);
    result.setDraftCommunication(draft);

    result.setAuditTrail(new AuditTrail(clinicalOutput, safetyVerdict, draft, "READY_FOR_APPROVAL"));
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

```java
public record SharedContext(
    PetRecord petData,
    List<Visit> clinicalHistory,
    OwnerProfile ownerData,
    PolicySet compliancePolicies
) {}

public Output analyze(SharedContext context, String query) {
    String analysis = analyzeClinicalHistory(context.clinicalHistory());
    return new Output(analysis);
}
```

**No Shared Authority (Each Agent Owns Its Decision):**
- Clinical Reasoning Agent owns clinical analysis; no other agent changes it
- Compliance Agent owns safety verdict; Clinical cannot override
- Communication Agent owns message tone; Clinical cannot mandate phrasing

**Shared State Machine (Track Progress Without Central Control):**
```java
public enum MASStage { CLINICAL, COMPLIANCE, COMMUNICATION, APPROVAL }

public class MASExecutionState {
    private MASStage currentStage = MASStage.CLINICAL;
    private ClinicalOutput clinicalResult;
    private SafetyVerdictOutput safetyResult;
    private CommunicationOutput communicationResult;

    public boolean canAdvanceToCompliance() {
        return clinicalResult != null && clinicalResult.success();
    }

    public boolean canAdvanceToCommunication() {
        return safetyResult != null && safetyResult.verdict() != SafetyVerdictType.FAIL;
    }

    public boolean readyForApproval() {
        return communicationResult != null;
    }
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
            "id": "gpt-5.2",
            "provider": "Microsoft Foundry Models",
            "endpoint": "https://petclinic-foundry.services.ai.azure.com/api/projects/petclinic-platform",
            "deployment_id": "gpt-5.2-prod",
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
```java
@Configuration
public class CentralizedAiConfiguration {

    @Bean
    DefaultAzureCredential azureCredential(@Value("${azure.identity.client-id:}") String managedIdentityClientId) {
        DefaultAzureCredentialBuilder builder = new DefaultAzureCredentialBuilder();
        if (StringUtils.hasText(managedIdentityClientId)) {
            builder.managedIdentityClientId(managedIdentityClientId);
        }
        return builder.build();
    }

    @Bean
    Kernel sharedKernel(DefaultAzureCredential credential,
                        @Value("${azure.openai.endpoint}") String endpoint,
                        @Value("${azure.openai.model-id}") String modelId) {
        OpenAIAsyncClient client = new OpenAIClientBuilder()
            .endpoint(endpoint)
            .credential(credential)
            .buildAsyncClient();

        ChatCompletionService chatCompletion = OpenAIChatCompletion.builder()
            .withModelId(modelId)
            .withOpenAIAsyncClient(client)
            .build();

        return Kernel.builder()
            .withAIService(ChatCompletionService.class, chatCompletion)
            .build();
    }
}
```

**Access Control (Role-Based):**
```java
public class ModelAccessPolicy {

    public boolean canUseModel(String userId, String modelId, String useCase) {
        String userRole = authService.getUserRole(userId);
        PolicyRule policyRule = policyStore.getRule(modelId, useCase);

        if (!policyRule.allowedRoles().contains(userRole)) {
            throw new UnauthorizedAccessException("Role %s cannot use %s for %s".formatted(userRole, modelId, useCase));
        }

        if (policyRule.requiresAudit() && !auditService.isEnabled(userId)) {
            throw new PolicyViolationException("Audit must be enabled for this use case");
        }

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
```java
public String summarizeClinicalHistory(String petId) {
    PromptDefinition prompt = promptRegistry.getActive("clinical_summary");

    return kernelFactory.create()
        .invokePromptAsync(
            prompt.content(),
            KernelArguments.builder().withVariable("petId", petId).build())
        .block()
        .getResult();
}
```

**A/B Testing Prompts:**
```java
PromptDefinition prompt = experimentFramework.shouldUse("prompt_variant_b", userId)
    ? promptRegistry.get("clinical_summary", "2.1")
    : promptRegistry.get("clinical_summary", "2.0");

metrics.recordUsage("clinical_summary", prompt.version(), userId);
```

**Rollback Strategy:**
- Keep previous 3 versions in registry
- If new version shows performance degradation (error rate > 5%, latency > 2x), auto-rollback
- Notify team of rollback + analysis

### Telemetry and Cost Tracking

**Comprehensive Usage Tracking:**
```java
public class AiPlatformTelemetry {

    public void logUsage(UsageRecord record) {
        azureMonitorClient.trackEvent(
            "AIModelUsage",
            Map.of(
                "model_id", record.modelId(),
                "prompt_version", record.promptVersion(),
                "use_case", record.useCase(),
                "user_id", record.userId(),
                "team", record.team()),
            Map.of(
                "input_tokens", (double) record.inputTokens(),
                "output_tokens", (double) record.outputTokens(),
                "latency_ms", (double) record.latencyMs(),
                "cost_usd", record.costUsd().doubleValue())
        );

        cosmosRepository.save(record);
    }
}
```

**Cost Calculation:**
```java
public class CostCalculator {

    public BigDecimal calculateCost(String modelId, int inputTokens, int outputTokens) {
        ModelPricing pricing = modelRegistry.getPricing(modelId);

        BigDecimal inputCost = BigDecimal.valueOf(inputTokens)
            .divide(BigDecimal.valueOf(1000), RoundingMode.HALF_UP)
            .multiply(pricing.inputCostPer1k());
        BigDecimal outputCost = BigDecimal.valueOf(outputTokens)
            .divide(BigDecimal.valueOf(1000), RoundingMode.HALF_UP)
            .multiply(pricing.outputCostPer1k());

        return inputCost.add(outputCost);
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
│  ├─ gpt-5.2: $1,890 (80.7%)
│  ├─ gpt-4o-mini: $451.50 (19.3%)
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
```java
public class BudgetMonitor {

    public void checkBudgets() {
        List<DailyUsage> dailyUsage = telemetryClient.getDailyCost();

        for (Team team : organization.teams()) {
            BigDecimal teamCost = dailyUsage.stream()
                .filter(usage -> usage.team().equals(team.id()))
                .map(DailyUsage::cost)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

            BigDecimal dailyThreshold = team.monthlyAiBudget().divide(BigDecimal.valueOf(30), RoundingMode.HALF_UP);

            if (teamCost.compareTo(dailyThreshold.multiply(BigDecimal.valueOf(0.8d))) > 0) {
                alertService.notify(team.name() + " is at 80% of daily budget");
            }

            if (teamCost.compareTo(dailyThreshold) > 0) {
                throttleService.limitTeam(team.id());
            }
        }
    }
}
```

### Policy Enforcement Points

**Request-Time Validation:**
```java
public class AiRequestValidator {

    public void validateRequest(InvocationRequest request) {
        List<ModelPolicy> policies = policyStore.getPolicies();

        ModelPolicy modelPolicy = policies.stream()
            .filter(policy -> policy.modelId().equals(request.modelId()))
            .findFirst()
            .orElseThrow(() -> new PolicyViolationException("Model is not in the approved registry"));

        if (!modelPolicy.approvedUseCases().contains(request.useCase())) {
            throw new PolicyViolationException("Model %s is not approved for %s".formatted(request.modelId(), request.useCase()));
        }

        UserQuota userQuota = quotaService.getRemaining(request.userId());
        if (userQuota.monthlyTokens() < 1000) {
            throw new QuotaExceededException("Monthly token quota exceeded");
        }

        if (request.input().contains("SSN") || request.input().contains("password")) {
            throw new DataLeakageException("Prompt contains sensitive data");
        }
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
```java
public class ComplianceLogger {

    public void logAiAction(AiAction action) {
        ComplianceLog log = new ComplianceLog(
            Instant.now(),
            action.userId(),
            action.modelId(),
            action.useCase(),
            action.inputTokens(),
            action.outputTokens(),
            hash(action.input()),
            hash(action.output()),
            action.policyChecksPassed(),
            action.cost(),
            action.latency()
        );

        complianceRepository.save(log);

        if ("clinical_recommendation".equals(action.useCase())) {
            longTermArchive.save(log);
        }
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
- **Microsoft Foundry Models:** https://learn.microsoft.com/en-us/azure/foundry/foundry-models/
- **Responsible AI Principles:** https://www.microsoft.com/en-us/ai/responsible-ai

---

**Version:** 1.0  
**Last Updated:** 2024-01-15  
**Maintained By:** Josh (Domain Expert)
