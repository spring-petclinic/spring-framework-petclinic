# Lab 2: AI-Assisted Actions with Human-in-the-Loop

**Theme:** AI proposes, humans decide  
**Mindset:** AI drafts, people approve  
**Duration:** ~8 hours  
**Prerequisites:** Completed Labs 0–1

---

## Overview

Lab 1 was passive: AI answered questions. Lab 2 is active: AI drafts artifacts (summaries, plans, messages) that humans review and approve before execution.

This introduces the **human-in-the-loop pattern**—the most enterprise-safe approach to AI integration. It proves that enterprises don't fear AI; they fear *uncontrolled* AI. With explicit approval checkpoints, accountability, and transparency, humans regain control and trust increases.

---

## What This Lab Proves

1. **Enterprises don't fear AI—they fear uncontrolled AI.** Approval checkpoints eliminate liability and restore trust.
2. **Human-in-the-loop is a design feature, not a constraint.** It scales quality and accountability simultaneously.
3. **Explainability is not optional.** Every draft includes confidence, reasoning, and source context so humans can evaluate AI's work.
4. **The safest AI is not the least capable—it's the most accountable.** Logging, transparency, and approval are the governance mechanisms, not limitations.

---

## Learning Objectives

After completing Lab 2, learners will be able to:

- **Design HITL workflows** that capture human review and decision-making before persistence or communication
- **Implement approval gates** with role-based access and escalation paths
- **Build explainability systems** that surface confidence, reasoning, and source context for every AI suggestion
- **Log decision rationale** (both AI reasoning and human justification) for audit and continuous learning
- **Understand when HITL is a feature** (e.g., check-before-dispatch) vs. a crutch (e.g., AI too uncertain to be useful)
- **Iterate on AI quality** using human feedback and override data

---

## Key Teaching Moments

1. **Accountability is a feature:** "When a human signs off, they're liable. That's the safety mechanism."
2. **Feedback loops create learning:** "Every human decision teaches the AI. Capture it, don't waste it."
3. **Exceptions teach you:** "The cases where humans overrode the AI are your most valuable data."
4. **The captain and the co-pilot:** AI suggests; human decides. The human is always in command, always accountable.
5. **Audit trail as governance:** Every decision (human or AI) is logged. If something goes wrong, you can trace *exactly* where and why.

---

## Common Misconceptions to Address

- ❌ **"Human-in-the-loop means the AI is weak."** Reality: HITL is a design pattern, not a crutch. Some of the most powerful AI systems are HITL.
- ❌ **"Logging decisions is just compliance theater."** Reality: Logs are your feedback mechanism. They're how you improve.
- ❌ **"Users will always read explanations."** Reality: Humans skip details. Design HITL workflows that are *easy* to audit and approve quickly, not just possible.
- ❌ **"If approval is required, AI ownership is moot."** Reality: The human's *deliberate acceptance* of AI reasoning is the accountability mechanism.

---

## Mental Models & Analogies

**The Captain and the Co-Pilot:**  
The AI is a co-pilot: it analyzes data, proposes actions, and explains its reasoning. The captain (human) evaluates the proposal, asks clarifying questions, approves or modifies, and takes responsibility for the decision. The captain always remains in command.

**Audit Trail as Governance:**  
Every decision point is logged. If a recommendation leads to a poor outcome, you can trace *exactly*:
- What data the AI saw
- What the AI recommended
- What the human approved
- What changed between AI draft and human approval

This transparency is what enterprises need to adopt AI confidently.

---

## Key Activities

### Activity 1: Implement Draft Generation (Responsible AI)

**Goal:** AI generates high-quality draft artifacts with metadata.

#### Artifact Types

1. **Visit Summary Drafts**
   - Synthesize clinical notes from visit into concise summary
   - Extract key findings, treatments, follow-up actions
   - Ground every claim in source records

2. **Follow-Up Plan Drafts**
   - Recommend timing, scope, and specifics of next appointment
   - Suggest tests, medications, or referrals based on history
   - Explain rationale (e.g., "Bella's recurring ear infections suggest allergy testing")

3. **Owner Message Drafts**
   - Write clear, empathetic post-visit messages for pet owners
   - Include care instructions (medications, activity restrictions, diet)
   - Balance professional tone with reassurance

#### Draft Metadata (Every Artifact Must Include)

Each draft includes:

```json
{
  "draft_id": "draft-visit-2024-002",
  "artifact_type": "visit_summary",
  "timestamp": "2024-01-15T14:32:00Z",
  "pet_id": "bella",
  "clinician_id": "dr_smith",
  
  "content": {
    "summary": "Bella presented with ear inflammation and discharge. Physical exam revealed bilateral otitis. Prescribed antibiotic drops and oral pain management.",
    "follow_up": "Recheck in 2 weeks; if recurrent, refer to dermatology for allergy testing",
    "owner_message": "Bella's ears are inflamed and likely infected. We've prescribed medicine to help. Please apply drops twice daily..."
  },
  
  "confidence": {
    "overall": 0.89,
    "by_statement": [
      {
        "statement": "Bella presented with ear inflammation and discharge",
        "confidence": 0.95,
        "reasoning": "Explicitly documented in clinical notes"
      },
      {
        "statement": "Recurrent infections suggest allergy",
        "confidence": 0.72,
        "reasoning": "Inference from 3 ear infections in 12 months; not explicitly stated in records"
      }
    ]
  },
  
  "sources": [
    {
      "entity_type": "visit",
      "entity_id": "visit-2024-002",
      "pet_name": "Bella",
      "visit_date": "2024-01-15",
      "clinician": "Dr. Smith",
      "excerpt": "Otitis bilateralis; initiated antibiotic drops"
    },
    {
      "entity_type": "visit",
      "entity_id": "visit-2023-009",
      "visit_date": "2023-10-22",
      "excerpt": "Ear infection treated with antibiotics"
    }
  ],
  
  "reasoning_trace": {
    "step_1_retrieval": {
      "query": "Bella recent visit notes ear",
      "records_found": 3,
      "summary": "Found current visit and 2 historical visits mentioning ear infection"
    },
    "step_2_analysis": {
      "observations": ["Otitis noted in clinical notes", "Antibiotic prescribed", "Recurring pattern over 12 months"],
      "pattern": "Recurrent ear infections suggest chronic condition",
      "confidence": 0.72
    },
    "step_3_recommendation": {
      "suggestion": "Refer to dermatology for allergy testing",
      "basis": "Recurring infections often indicate underlying allergy; not yet tested",
      "confidence": 0.68
    }
  },
  
  "approved": false,
  "status": "pending_review"
}
```

#### Implementation Guidance

**In Semantic Kernel (C#):**

```csharp
[KernelFunction("generate_visit_summary")]
[Description("Generate a draft visit summary with explainability metadata")]
public async Task<DraftArtifact> GenerateVisitSummary(
    [Description("Pet ID from PetClinic database")] string petId,
    [Description("Visit ID")] string visitId
)
{
    // Step 1: Retrieve clinical context
    var visit = await _petClinicDb.GetVisitAsync(visitId);
    var clinicalNotes = await _searchClient.SearchAsync(
        new SearchOptions 
        { 
            Filter = $"entity_id eq '{petId}' and entity_type eq 'visit'",
            Size = 10
        }
    );
    
    // Step 2: Generate draft with chain-of-thought reasoning
    var systemPrompt = @"
You are a veterinary assistant drafting visit summaries.

RULES:
1. ONLY use facts from the provided clinical records.
2. Clearly separate observations (facts) from inferences.
3. Every statement must cite a source record.
4. If you recommend follow-up, explain why based on pet's history.
5. Tone: professional, clear, evidence-based.

For each statement, provide:
- The statement itself
- Confidence (0.0-1.0)
- Reasoning (fact vs. inference)
- Source records that support it
";

    var userPrompt = $@"
Pet: {visit.PetName}
Visit Date: {visit.VisitDate}
Clinician: {visit.ClinicianName}

Clinical Notes:
{visit.ClinicalNotes}

Pet History (last 12 months):
{string.Join("\n", clinicalNotes.Select(r => $"- {r.VisitDate}: {r.Summary}"))}

Draft:
1. A one-paragraph visit summary
2. Key findings and treatments
3. Recommended follow-up (with reasoning)
4. Confidence levels and reasoning for each claim
";

    var response = await _kernel.InvokeAsync<string>(
        systemPrompt,
        userPrompt
    );
    
    // Step 3: Parse response and build metadata structure
    var draft = ParseDraftResponse(response, visitId, petId);
    
    // Step 4: Compute confidence scores
    draft.Confidence.Overall = ComputeOverallConfidence(draft.Confidence.ByStatement);
    
    // Step 5: Attach source citations
    draft.Sources = await ExtractSourceCitations(clinicalNotes, draft);
    
    // Step 6: Persist as "pending_review"
    await _draftRepository.SaveAsync(draft);
    
    return draft;
}

private double ComputeOverallConfidence(List<StatementConfidence> statements)
{
    // Average of statement confidences
    double avg = statements.Average(s => s.Confidence);
    
    // Adjust based on reasoning types
    bool hasInferences = statements.Any(s => s.Reasoning.Contains("inference"));
    if (hasInferences) avg -= 0.1; // Lower confidence if inferences present
    
    bool allGrounded = statements.All(s => !s.Reasoning.Contains("hallucination"));
    if (allGrounded) avg += 0.05; // Boost if all grounded
    
    return Math.Min(Math.Max(avg, 0.0), 1.0); // Clamp to [0, 1]
}
```

---

### Activity 2: Design Approval Workflows

**Goal:** Implement UI and business logic for human review before persistence.

#### Approval States & Transitions

```
[PENDING_REVIEW] 
    ↓ (User clicks "Approve")
[APPROVED] → [PERSISTED] → [ARCHIVED]
    ↓ (User clicks "Edit" → re-submit)
[PENDING_REVIEW]
    ↓ (User clicks "Reject")
[REJECTED]
```

#### Role-Based Approval

Define who can approve what:

```json
{
  "approval_rules": {
    "visit_summary": {
      "can_approve": ["veterinarian", "senior_staff"],
      "can_reject": ["veterinarian", "senior_staff"],
      "can_edit": ["veterinarian", "senior_staff"],
      "requires_review_for_low_confidence": true,
      "auto_approve_threshold": 0.90
    },
    "follow_up_plan": {
      "can_approve": ["veterinarian"],
      "requires_explicit_review": true,
      "auto_approve_threshold": null
    },
    "owner_message": {
      "can_approve": ["veterinarian", "senior_staff"],
      "can_edit": ["veterinarian", "senior_staff"],
      "requires_review_for_low_confidence": false
    }
  }
}
```

#### Approval UI Pattern

**For High-Confidence Drafts (≥ 0.85):**

```
┌─────────────────────────────────────────────────┐
│ [DRAFT] Bella Visit Summary                      │
├─────────────────────────────────────────────────┤
│                                                 │
│ Bella presented with bilateral otitis. Exam    │
│ revealed ear inflammation and discharge.       │
│ Prescribed antibiotic drops and pain mgmt.     │
│                                                 │
│ Follow-up: Recheck in 2 weeks                   │
│                                                 │
├─────────────────────────────────────────────────┤
│ Confidence: 89%  [why?]                         │
│                                                 │
│ ☑ I've reviewed this draft                      │
│ [Approve]  [Edit]  [Reject]                     │
└─────────────────────────────────────────────────┘
```

**For Medium-Confidence Drafts (0.60–0.85):**

```
┌─────────────────────────────────────────────────┐
│ ⚠ [DRAFT] Bella Follow-Up Plan                  │
├─────────────────────────────────────────────────┤
│                                                 │
│ Recommended: Dermatology referral for           │
│ allergy testing (recurring ear infections)      │
│                                                 │
│ Confidence: 68%                                 │
│ ⚠ This is a clinical inference, not in records │
│                                                 │
│ Reasoning:                                      │
│ • Bella has had 3 ear infections in 12 months   │
│ • Pattern suggests chronic condition            │
│ • Not yet tested for allergies                  │
│ • Recurring otitis often allergy-related        │
│                                                 │
│ Sources:                                        │
│ • Visit 2024-01-15: Otitis bilateralis          │
│ • Visit 2023-10-22: Ear infection               │
│ • Visit 2023-09-10: Ear infection               │
│                                                 │
├─────────────────────────────────────────────────┤
│ ☑ I've reviewed the reasoning                   │
│ ☑ I approve this recommendation                 │
│ [Approve]  [Edit]  [Reject]  [Ask AI to...]    │
└─────────────────────────────────────────────────┘
```

**For Low-Confidence Drafts (< 0.60):**

```
┌─────────────────────────────────────────────────┐
│ ⚠⚠ [DRAFT] Bella Follow-Up Plan                 │
├─────────────────────────────────────────────────┤
│                                                 │
│ Recommended: Consider orthopedic evaluation     │
│ for hip dysplasia                               │
│                                                 │
│ Confidence: 52%                                 │
│ ⚠ Low confidence. Manual review required.       │
│                                                 │
│ Reasoning:                                      │
│ • Bella is a Golden Retriever (breed risk)      │
│ • Recent visit mentioned "mild limping"         │
│ • No explicit hip dysplasia diagnosis           │
│ • This is speculative                           │
│                                                 │
├─────────────────────────────────────────────────┤
│ REQUIRED: You must take explicit action         │
│                                                 │
│ [Edit and approve]  [Reject]  [Request AI...]  │
│                                                 │
│ Notes: ____________________________________     │
└─────────────────────────────────────────────────┘
```

#### Implementation: Approval API

```csharp
[KernelFunction("request_approval")]
[Description("Request human approval for a draft artifact")]
public async Task<ApprovalRequest> RequestApproval(
    [Description("Draft ID")] string draftId,
    [Description("Who is approving")] string userId,
    [Description("Approval action: approve | reject | edit")] string action,
    [Description("Optional: user's edits to the draft")] string? editedContent = null,
    [Description("Optional: user's reasoning if rejecting")] string? rejectionReason = null
)
{
    var draft = await _draftRepository.GetAsync(draftId);
    var user = await _userService.GetAsync(userId);
    
    // Validate user has permission to approve this artifact type
    var canApprove = _authorizationService.CanApprove(user.Role, draft.ArtifactType);
    if (!canApprove)
        throw new UnauthorizedAccessException($"User role '{user.Role}' cannot approve {draft.ArtifactType}");
    
    var approval = new ApprovalRequest
    {
        DraftId = draftId,
        ApproverId = userId,
        ApproverRole = user.Role,
        ApprovalTime = DateTime.UtcNow,
        Action = action, // approve | reject | edit
        EditedContent = editedContent,
        RejectionReason = rejectionReason
    };
    
    // Log the approval decision (audit trail)
    await _auditLog.LogAsync(new AuditEntry
    {
        EventType = "approval_decision",
        DraftId = draftId,
        UserId = userId,
        Action = action,
        Timestamp = DateTime.UtcNow,
        Details = new
        {
            OriginalConfidence = draft.Confidence.Overall,
            UserEdited = !string.IsNullOrEmpty(editedContent),
            RejectionReason = rejectionReason
        }
    });
    
    if (action == "approve")
    {
        // If user edited content, update confidence to 1.0 (human override)
        if (!string.IsNullOrEmpty(editedContent))
        {
            draft.Content = editedContent;
            draft.Confidence.Overall = 1.0; // Human sign-off = high confidence
            draft.Status = DraftStatus.ApprovedWithEdits;
        }
        else
        {
            draft.Status = DraftStatus.Approved;
        }
        
        // Persist the artifact
        await _petClinicDb.SaveArtifactAsync(draft);
        
        // If it's an owner message, mark for delivery
        if (draft.ArtifactType == "owner_message")
        {
            await _messageQueue.EnqueueAsync(new OutboundMessage
            {
                DraftId = draftId,
                OwnerId = draft.OwnerId,
                Message = draft.Content,
                Status = MessageStatus.ReadyToSend,
                ApprovedBy = userId,
                ApprovedAt = DateTime.UtcNow
            });
        }
    }
    else if (action == "reject")
    {
        draft.Status = DraftStatus.Rejected;
        
        // Log rejection reason for feedback
        await _feedbackRepository.LogAsync(new Feedback
        {
            DraftId = draftId,
            FeedbackType = "rejection",
            Reason = rejectionReason,
            UserId = userId,
            Timestamp = DateTime.UtcNow
        });
    }
    else if (action == "edit")
    {
        // User edited; draft goes back to pending review
        draft.Content = editedContent;
        draft.Status = DraftStatus.PendingReview;
        draft.LastEditedBy = userId;
        draft.LastEditedAt = DateTime.UtcNow;
    }
    
    await _draftRepository.UpdateAsync(draft);
    return approval;
}
```

---

### Activity 3: Surface Explainability

**Goal:** Make AI reasoning transparent so humans can evaluate confidence and make informed decisions.

#### What to Surface

For every draft, show:

1. **Confidence Score** (0–100%)
   - Overall confidence
   - Per-statement breakdown
   - Why some parts are less confident

2. **Reasoning Trace** (Step-by-step AI thinking)
   - What data was retrieved
   - What patterns were identified
   - What inferences were made
   - Which claims are facts vs. inferences

3. **Source Context** (Specific records cited)
   - Exact visit dates, clinician names
   - Direct excerpts from records
   - Links to view full source records

4. **Uncertainty Indicators**
   - "This is based on only 1 visit" (vs. 3)
   - "Data is 6+ months old" (freshness concern)
   - "This is an inference, not stated in records"

#### UI Example: Explainability Panel

```
┌──────────────────────────────────────────────────────────┐
│ [DRAFT] Bella Follow-Up Plan                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ RECOMMENDATION:                                          │
│ "Schedule 2-week recheck appointment"                    │
│                                                          │
│ ────────────────────────────────────────────────────────│
│ WHY?                                                     │
│                                                          │
│ This visit treated acute otitis with antibiotics.       │
│ Standard protocol for acute bacterial infection is      │
│ recheck in 2 weeks to confirm resolution.               │
│                                                          │
│ ────────────────────────────────────────────────────────│
│ CONFIDENCE: 92%                                          │
│                                                          │
│ ✓ Explicit in clinical guidelines                        │
│ ✓ 3 prior visits show same pattern (recheck after Rx)   │
│ ✓ Current visit clearly documents "acute otitis"        │
│                                                          │
│ ────────────────────────────────────────────────────────│
│ SOURCES:                                                 │
│                                                          │
│ Visit 2024-01-15 (Today)                                │
│  "Otitis bilateralis; initiated antibiotic drops"        │
│  Dr. Smith, Veterinarian                                │
│  [View full record]                                      │
│                                                          │
│ Similar cases in history:                                │
│  • Visit 2023-10-22: Ear infection → 2-week recheck ✓  │
│  • Visit 2023-05-10: Ear infection → 2-week recheck ✓  │
│                                                          │
│ ────────────────────────────────────────────────────────│
│ CONFIDENCE FACTORS:                                      │
│                                                          │
│ ✓ +0.1 (Multiple source agreement)                      │
│ ✓ +0.1 (Explicit in clinical records)                   │
│ ✓ +0.05 (Recent data, within 6 months)                  │
│ - 0.0 (Not an inference; clear pattern)                 │
│                                                          │
│ = 92% overall confidence                                │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ [Approve]  [Edit]  [Reject]                             │
└──────────────────────────────────────────────────────────┘
```

#### Implementation: Confidence Computation

```csharp
public class ConfidenceComputation
{
    public static double ComputeStatementConfidence(
        string statement,
        List<SourceRecord> supportingSources,
        bool isInference,
        DateTime? dataFreshness = null)
    {
        double confidence = 0.5; // baseline
        
        // Factor 1: Source agreement
        if (supportingSources.Count >= 3)
            confidence += 0.15;
        else if (supportingSources.Count == 2)
            confidence += 0.10;
        else if (supportingSources.Count == 1)
            confidence += 0.05;
        
        // Factor 2: Data freshness
        if (dataFreshness != null)
        {
            var age = DateTime.UtcNow - dataFreshness.Value;
            if (age.TotalDays < 30)
                confidence += 0.1;
            else if (age.TotalDays < 180)
                confidence += 0.05;
            else if (age.TotalDays > 365)
                confidence -= 0.15; // stale data
        }
        
        // Factor 3: Fact vs. inference
        if (isInference)
            confidence -= 0.15;
        else
            confidence += 0.1; // explicit fact
        
        // Factor 4: Statement clarity
        // (longer, more specific statements score higher)
        if (statement.Length > 50)
            confidence += 0.05;
        
        return Math.Min(Math.Max(confidence, 0.0), 1.0);
    }
    
    public static double ComputeArtifactConfidence(DraftArtifact draft)
    {
        double avg = draft.Confidence.ByStatement.Average(s => s.Confidence);
        
        // Adjust based on composition
        int inferenceCount = draft.Confidence.ByStatement
            .Count(s => s.Reasoning.Contains("inference"));
        
        if (inferenceCount > 0)
            avg -= 0.05 * inferenceCount; // penalize each inference
        
        // Boost if all statements are grounded
        bool allGrounded = draft.Confidence.ByStatement
            .All(s => s.Sources.Count > 0);
        
        if (allGrounded)
            avg += 0.05;
        
        return Math.Min(Math.Max(avg, 0.0), 1.0);
    }
}
```

---

### Activity 4: Test Approval Flows

**Goal:** Validate that clinicians can quickly review and approve, and understand user behavior.

#### Metrics to Measure

1. **Approval Time:** How long does it take to approve a draft?
   - Target: < 1 minute for high-confidence
   - Target: 2–5 minutes for medium-confidence

2. **Approval Rate:** What % of drafts get approved as-is?
   - Track by artifact type
   - Track by confidence level

3. **Edit Patterns:** What types of edits do clinicians make?
   - Tone/clarity corrections
   - Safety/medical adjustments
   - Source/citation fixes

4. **Rejection Patterns:** When do clinicians reject?
   - Track rejection reasons
   - Look for systematic issues with AI reasoning

5. **Confidence Alignment:** Does AI confidence match human confidence?
   - For "low-confidence" drafts, how often do humans reject?
   - For "high-confidence" drafts, how often do humans approve?

#### Test Cases

```
Test Case 1: High-Confidence, Straightforward Draft
- Artifact: Visit summary for routine checkup
- AI Confidence: 0.95
- Expected: User approves in < 30 seconds

Test Case 2: Medium-Confidence with Inference
- Artifact: Follow-up plan recommending allergy testing
- AI Confidence: 0.72 (inference-heavy)
- Expected: User takes 2–5 min, may request clarification

Test Case 3: Low-Confidence, Ambiguous Data
- Artifact: Recommendation for specialist referral
- AI Confidence: 0.55
- Expected: User either rejects, edits heavily, or escalates

Test Case 4: Batch Approval of Multiple Drafts
- Artifact: 5 owner messages from clinic
- Mix of confidences
- Expected: User groups by confidence, fast-approves high ones

Test Case 5: Rejection and Feedback
- Artifact: AI draft with tone issues
- User rejects with reason: "Too clinical; needs warmth"
- Expected: Rejection logged; used to retrain prompts
```

#### Implementation: Telemetry

```csharp
public class ApprovalMetrics
{
    public static void LogApprovalEvent(
        string draftId,
        string artifactType,
        double aiConfidence,
        string userAction, // approve | reject | edit
        TimeSpan reviewTime,
        string? editCategory = null,
        string? rejectionReason = null)
    {
        var @event = new ApprovalEvent
        {
            DraftId = draftId,
            ArtifactType = artifactType,
            AiConfidence = aiConfidence,
            UserAction = userAction,
            ReviewTimeSeconds = (int)reviewTime.TotalSeconds,
            EditCategory = editCategory,
            RejectionReason = rejectionReason,
            Timestamp = DateTime.UtcNow
        };
        
        _telemetryClient.TrackEvent("approval_completed", new Dictionary<string, string>
        {
            { "artifact_type", artifactType },
            { "user_action", userAction },
            { "ai_confidence_bucket", GetConfidenceBucket(aiConfidence) }
        }, new Dictionary<string, double>
        {
            { "ai_confidence", aiConfidence },
            { "review_time_seconds", @event.ReviewTimeSeconds }
        });
        
        // Store in database for analysis
        _approvalMetricsRepository.SaveAsync(@event);
    }
    
    private static string GetConfidenceBucket(double confidence)
    {
        if (confidence >= 0.85) return "high";
        if (confidence >= 0.60) return "medium";
        return "low";
    }
    
    // Query: Approval rate by confidence level
    public async Task<ApprovalStats> GetApprovalRates()
    {
        return new ApprovalStats
        {
            HighConfidenceApprovalRate = await _repository.GetApprovalRateAsync(
                minConfidence: 0.85,
                maxConfidence: 1.0),
            MediumConfidenceApprovalRate = await _repository.GetApprovalRateAsync(
                minConfidence: 0.60,
                maxConfidence: 0.85),
            LowConfidenceApprovalRate = await _repository.GetApprovalRateAsync(
                minConfidence: 0.0,
                maxConfidence: 0.60)
        };
    }
}
```

---

## Checkpoint 1: Draft Generation & Approval

Before moving forward, verify that your implementation includes:

### Draft Generation
- [ ] AI generates draft summaries from clinical notes and visit history
- [ ] AI generates draft follow-up recommendations with explicit reasoning
- [ ] AI generates draft owner messages in appropriate tone
- [ ] All drafts include confidence scores and reasoning traces
- [ ] All drafts include citations to source records
- [ ] Confidence computation accounts for data freshness, source agreement, and inference vs. fact

### Approval Workflows
- [ ] UI displays drafts with edit/approve/reject options
- [ ] High-confidence drafts (≥0.85) can be approved quickly
- [ ] Medium-confidence drafts require deliberate review
- [ ] Low-confidence drafts require explicit action (no quick-approvals)
- [ ] Role-based access controls prevent unauthorized approvals
- [ ] Unapproved artifacts are never persisted or communicated
- [ ] Approval audit trail logs *who* approved, *when*, and *what* changed

### Explainability & Transparency
- [ ] Confidence scores are displayed prominently
- [ ] Reasoning traces show step-by-step AI thinking
- [ ] Source citations link to actual clinical records
- [ ] Uncertainty indicators flag inferences, old data, and single-source claims
- [ ] Users can drill down from summary to detailed reasoning to source records

### Metrics & Feedback
- [ ] Approval decisions are logged (approve/reject/edit)
- [ ] Approval time is measured by confidence level
- [ ] Edit patterns are tracked and categorized
- [ ] Rejection reasons are captured for feedback loops
- [ ] System can answer: "What % of high-confidence drafts do vets approve?"

---

## Outputs from This Lab

### Output 1: Draft Features
A deployed capability within PetClinic that automatically generates high-quality draft artifacts:

- **Visit Summary Drafts:** One-paragraph summary of visit, key findings, treatments, follow-up actions
- **Follow-Up Plan Drafts:** Specific recommendations for next appointment (timing, scope, tests, referrals)
- **Owner Message Drafts:** Clear, empathetic post-visit communication with care instructions

Each draft includes:
- Confidence scores (overall and per-statement)
- Explicit reasoning (fact vs. inference)
- Full citation trail to source records
- Metadata for audit and improvement

### Output 2: Approval Workflow Design
Comprehensive documentation covering:

- **Approval States & Transitions:** How drafts flow through pending → approved → persisted
- **Role-Based Authorization:** Who can approve which artifact types
- **UI Patterns:** How clinicians review, edit, approve, and reject drafts
- **Escalation Paths:** How to handle ambiguous or low-confidence recommendations
- **Audit Trail:** Every decision is logged with timestamp, user, action, and reasoning

### Output 3: Explainability Framework
Definition and measurement of:

- **Confidence Scoring:** How AI assigns confidence to recommendations
- **Confidence Factors:** Data freshness, source agreement, fact vs. inference
- **Reasoning Transparency:** Users see exactly why the AI made each suggestion
- **Source Attribution:** Every claim is traceable to specific clinical records

### Output 4: Metrics Dashboard
Operational visibility into approval behavior:

- **Approval Rates:** By artifact type, confidence level, clinician role
- **Review Time:** How long clinicians spend reviewing drafts
- **Edit Patterns:** Which types of edits are most common
- **Feedback Loops:** How rejection reasons guide AI improvement
- **Confidence Calibration:** Does AI confidence match human acceptance rates?

---

## Mental Models & Analogies Revisited

**The Captain and the Co-Pilot:**
Throughout this lab, reinforce: The AI is a competent co-pilot. It analyzes data, proposes actions, and explains its reasoning. But the *captain* (human) always makes the final decision. The captain is accountable. Accountability is what enterprises need to adopt AI confidently.

**Audit Trail as Governance:**
Every decision point is logged. This transparency allows you to:
- Trace any outcome back to its decision point
- Understand human judgment and override patterns
- Improve the AI by learning from rejections
- Prove accountability if something goes wrong

**Exceptions Are Opportunities:**
When humans override or edit AI recommendations, that's not a failure—it's your most valuable learning data. Capture it, analyze it, and use it to improve.

---

## Reflection Questions

Before moving to Lab 3:

1. **What draft types are clinicians most willing to trust?** (Visit summaries vs. recommendations?)
2. **What edit patterns do clinicians show?** (Tone, safety, clarity, domain expertise?)
3. **Would you let non-vet staff approve drafts?** Under what conditions? For which artifact types?
4. **If a mistake slips through despite approval, how would you detect it?** What's your failure detection strategy?
5. **How does confidence score affect human approval rate?** Do humans trust high-confidence drafts more? Should they?
6. **What rejection reasons are most common?** Can you address them by improving the AI, or are they inherent to the task?
7. **How long can approval workflows remain in production?** At what scale do they become a bottleneck?

---

## Teaching Moment: Accountability as Safety

> **"The safest AI is not the least capable—it's the most accountable."**

Many enterprises resist AI because they fear *uncontrolled* automation. But the safeguard is not to limit AI; it's to make every decision *traceable and accountable*.

When a human explicitly approves an AI recommendation, they take ownership. That accountability is the safety mechanism. Combined with explainability (why did the AI suggest this?) and audit trails (what changed between draft and approval?), you have governance.

This is why HITL is not a constraint—it's a feature. It's how you scale AI responsibly.

---

## Next Steps

Move to **Lab 3: Single-Agent Workflows (Goal-Oriented AI)** when ready.

Lab 3 stops treating AI as a tool that generates static drafts. Instead, we introduce an **Agent**—an AI system that can reason across multiple steps, call tools, and work toward a goal—while remaining bounded by role contracts and escalation rules.

In Lab 2, a human approved every draft before it persisted. In Lab 3, the agent will have the authority to make some bounded decisions autonomously—but only because we've proven in Lab 2 that humans can trust the reasoning, even when the human doesn't explicitly approve each step.

---

## Summary

Lab 2 proves that **human-in-the-loop is not a constraint; it's a design pattern for enterprise-safe AI**. By adding explicit approval checkpoints, confidence scoring, and explainability, you:

1. Restore human control and accountability
2. Make AI reasoning transparent and auditable
3. Capture feedback loops that improve AI over time
4. Build enterprise trust through accountability, not limitation

The teaching moment—*"The safest AI is the most accountable"*—applies far beyond this lab. It's the foundation for all responsible AI systems.

