# Lab 5: Platform & Governance (Enterprise AI)

**Theme:** Many teams, one AI platform  
**Mindset:** Innovation locally, governance centrally  
**Duration:** ~9 hours  
**Prerequisites:** Completed Lab 4

---

## Context

Labs 1–4 proved you can build AI features—in isolation. Lab 3 and 4 showed what single and multi-agent systems can do. But here's the reality: In a week, you'll have three teams wanting to build three different agents. In a month, seven teams. In a year, fifty.

The question shifts from **"Can we build AI?"** to **"Can we scale it safely?"**

Without governance, you end up with:
- 50 teams writing 50 different prompts. No consistency. No reuse.
- Model costs exploding as each team discovers their own inefficient patterns.
- Safety gaps: one team handles PII correctly; another broadcasts it to an external model.
- Compliance nightmares: you can't audit decisions because there's no central log.

Lab 5 proves that **platform and governance don't constrain innovation—they accelerate it**. This lab introduces enterprise AI patterns: centralized infrastructure for model access, policy enforcement, cost tracking, and observability.

By the end of Lab 5, you'll have:
1. A model abstraction layer (no direct API calls; all requests go through a gateway)
2. A prompt library (versioned, approved prompts; production uses only these)
3. Policy enforcement (safety rules, data handling, cost controls built into the platform)
4. Telemetry (usage and cost dashboards; anomaly detection)
5. A playbook for onboarding new teams

---

## What This Lab Proves

### Proof 1: Governance Is Not Overhead—It's Foundation

You can build a fast, unsafe system in a day. Building a system that's both safe *and* fast at scale takes governance. Teams that skip governance pay the cost later: security incidents, compliance violations, runaway costs, or discovery that 10 teams solved the same problem 10 different ways.

**Teaching Moment:**
> "Governance doesn't slow down good teams. It accelerates them by eliminating reinvention and catching mistakes early."

### Proof 2: Centralization Enables Specialization

Without a shared platform, every team becomes experts in:
- Model API calls and error handling
- RAG implementation and tuning
- Safety and compliance
- Cost tracking and monitoring
- Operational incident response

With a shared platform, teams focus on *their domain problem*, not AI infrastructure. The platform team owns the hard, shared problems. Domain teams innovate locally.

**Teaching Moment:**
> "The best organizations don't have 50 AI teams. They have 1 AI platform team and 49 teams that use it."

### Proof 3: Observability Is Proactive Governance

You can't govern what you can't see. A centralized platform gives you a single window into what's happening:
- Which models are being used? By whom? For what?
- Where is spend concentrated? Where can we optimize?
- Are any teams hitting safety guardrails? Why?
- Which prompts are performing poorly? Which are golden?

This shifts governance from reactive (catching problems after they harm users) to proactive (catching drift before it happens).

**Teaching Moment:**
> "The safest systems aren't the ones with the most rules. They're the ones where you can see everything, detect anomalies, and act fast."

---

## Key Activities

### Activity 1: Centralize Model Access

**Current state (chaotic):** Each team calls OpenAI API, Microsoft Foundry / Azure OpenAI, or Anthropic directly.  
**Goal state (controlled):** All model requests route through a central gateway.

#### Step 1.1: Design the Gateway

Create an abstraction layer. Teams don't instantiate provider SDK clients directly. Instead:

```typescript
// Teams call the AI platform, not the model provider
const response = await aiPlatform.invoke({
  model: "approved_reasoning",  // Reference, not "gpt-4-turbo"
  message: "...",
  context: { teamId: "clinical-team", featureId: "diagnosis-assist" }
});
```

The gateway translates `approved_reasoning` to whichever model you've chosen (Claude 3.5 Sonnet, today; maybe something else tomorrow).

**Why this matters:**
- You can swap models without touching team code
- You can enforce authentication, rate limits, and cost controls in one place
- You can add telemetry without instrumenting 50 different codebases

#### Step 1.2: Implement Authentication & Rate Limiting

The gateway needs:
- **Microsoft Entra ID / workload identity validation:** Only approved teams/services can call the gateway
- **RBAC mapping:** Resolve the caller's principal to a team, service, and allowed use cases
- **Rate limiting:** Per-team, per-minute quotas (prevent runaway requests)
- **Quota management:** Monthly budgets; alert when approaching limits

For Azure-hosted services, prefer managed identities or workload identity federation. Keep API keys only as a temporary fallback for legacy callers that haven't migrated yet.

If the gateway fronts Microsoft Foundry models, assign the gateway's managed identity the **Cognitive Services User** role at the Foundry resource scope. If the gateway also provisions or updates Azure AI Search indexes, give that same identity **Search Service Contributor** plus **Search Index Data Contributor** for write paths, and reduce query-only callers to **Search Index Data Reader**.

Example:
```java
@Service
public class AiGateway {

  public GatewayResponse invoke(InvocationRequest request) {
    TeamContext team = authService.validate(request.principalId())
      .orElseThrow(UnauthorizedException::new);

    if (!rateLimiter.allow(team.id())) {
      throw new RateLimitExceededException();
    }

    if (telemetry.getMonthlySpend(team.id()).compareTo(team.monthlyBudget()) > 0) {
      throw new BudgetExceededException();
    }

    GatewayResponse result = modelClient.call(request);
    telemetry.logInvocation(team.id(), request, result);
    return result;
  }
}
```

#### Step 1.3: Define Approved Models

Create a policy:

```yaml
approvedModels:
  reasoning:
    provider: "anthropic"
    model: "claude-3-5-sonnet"
    rationale: "Best for clinical reasoning and complex analysis"
    maxTokens: 4000
    
  classification:
    provider: "foundry_models"
    model: "gpt-4o-mini"
    rationale: "Fast, cheap, good for routine categorization"
    maxTokens: 500
    
  vision:
    provider: "foundry_models"
    model: "gpt-4-vision"
    rationale: "Only approved model for image analysis"
    maxTokens: 1000
    
modelRequestProcess:
  - To use a new model, teams submit a PR to this file
  - Platform team reviews: cost/benefit, licensing, compliance
  - If approved, added to the list; if rejected, documented why
  - Removal process: deprecate, notify teams, give 30-day migration window
```

#### Checkpoint 1.1
Before moving forward:
- [ ] Gateway accepts requests from registered teams
- [ ] Unauthenticated requests are rejected
- [ ] Rate limiting is enforced (test by exceeding quota)
- [ ] Monthly budgets are tracked and enforced
- [ ] All approved models are available through the gateway

---

### Activity 2: Introduce Prompt Governance

**Current state (chaotic):** Prompts live in 50 different codebases, hardcoded, inconsistent.  
**Goal state (controlled):** One prompt library, versioned like code, with approval gates.

#### Step 2.1: Create a Prompt Library

A shared repository where all production prompts live:

```
prompts/
├── README.md
├── clinical/
│   ├── diagnosis-assistant/
│   │   ├── v1.0.md
│   │   ├── v1.1.md (current)
│   │   ├── v2.0-rc1.md (in review)
│   │   └── CHANGELOG.md
│   └── treatment-recommendation/
│       ├── v1.0.md
│       └── v1.1-rc1.md
├── communication/
│   └── owner-message/
│       └── v1.0.md
└── governance/
    ├── APPROVAL_PROCESS.md
    └── TEMPLATE.md
```

Each prompt includes:
- **Clear purpose:** What is this prompt for? Who uses it?
- **Model & settings:** Which model? Temperature, max tokens?
- **Example inputs/outputs:** Demonstrate the expected behavior
- **Safety considerations:** What guardrails does this prompt enforce?
- **Performance metrics:** How does it perform in production?
- **Changelog:** Why did v1.1 change from v1.0?

Example prompt file:

```markdown
# Diagnosis Assistant Prompt

**Version:** 1.1  
**Author:** Clinical Team  
**Approved by:** Dr. Sarah Chen (Clinical Lead), AI Governance Board  
**Approval Date:** 2024-11-15  
**Status:** Active  
**Model:** claude-3-5-sonnet  
**Cost per 1k tokens:** ~$3 input, ~$15 output  

## Purpose
Help vets synthesize patient history and treatment notes to identify possible diagnoses and next-step recommendations.

## Prompt
```
You are a veterinary clinical assistant. Your role is to help vets think through diagnosis possibilities and treatment options based on patient history.

You have access to the patient's medical records:
{MEDICAL_RECORDS}

The vet has observed:
{CLINICAL_OBSERVATION}

Your task:
1. Identify the top 3 possible diagnoses based on the records and observation
2. For each diagnosis, cite which records support it
3. Recommend next diagnostic steps
4. Flag any contraindications or safety concerns

**Important constraints:**
- You are not making the diagnosis; the vet is. You are a thinking partner.
- If you're uncertain, say so. Never confidently guess.
- If records are incomplete (e.g., no recent bloodwork), call that out.
- If the observation contradicts the records, flag the discrepancy.
```

## Example Input
```
Medical Records:
- Bella, 4-year-old Golden Retriever
- Last 3 visits: ear infections (Sept, Oct, Nov)
- Current medications: None
- Allergies: No known allergies documented

Clinical Observation:
Vet notes: "Bella is scratching her ears and shaking her head. Ear canal is inflamed but no visible discharge."
```

## Example Output
```
**Top 3 Possible Diagnoses:**

1. Recurring Otitis Externa (Ear Infection)
   - **Supporting evidence:** 3 ear infections in past 3 months; current inflammation
   - **Confidence:** High (92%)
   - **Next step:** Ear swab culture to identify organism and antibiotic sensitivity

2. Allergic Otitis (Allergy-Driven Ear Inflammation)
   - **Supporting evidence:** Recurring pattern; no documented allergies yet
   - **Confidence:** Medium-High (78%)
   - **Next step:** Allergy testing if infection doesn't resolve; consider dietary trial

3. Aural Hematoma (Ear Flap Swelling)
   - **Supporting evidence:** Head shaking behavior; inflamed canal
   - **Confidence:** Low (35%)
   - **Next step:** Physical exam for fluctuant swelling; ultrasound if needed

**Safety Flags:**
⚠️ No antihistamines in records, but recurrence suggests possible allergic component—confirm no allergies before prescribing.

**Data Gaps:**
- No recent bloodwork to rule out systemic infection
- Allergy history not documented; ask owner about dietary changes
```

## Approval Checklist
- [x] Prompt tested with 10+ realistic patient scenarios
- [x] Performance meets benchmark (diagnosis accuracy >85%, zero hallucinatory recommendations)
- [x] Safety constraints are clear; no medically risky guidance
- [x] Cost-per-invocation estimated and acceptable
- [x] Clinical lead and AI governance board approved

## Changelog
**v1.1 (2024-11-15):**
- Added explicit constraint: "You are not making the diagnosis"
- Changed to cite records for each diagnosis (improves explainability)
- Added "Data Gaps" section to call out incomplete information
- Removed temperature setting guidance (using default 0.7)

**v1.0 (2024-11-01):**
- Initial approved version
```

#### Step 2.2: Implement Prompt Versioning & Approval Workflow

Prompts are code. Treat them like code:

1. **All prompts start as PRs.** A team wants to introduce a new prompt or update an existing one → PR to `prompts/` repo.
2. **Automated checks:**
   - Verify prompt has required metadata (purpose, model, approval checklist)
   - Run prompt through example test cases (catch obvious failures)
   - Estimate token cost (warn if too expensive)
3. **Human review:**
   - Clinical lead reviews safety (is this medically sound?)
   - AI governance board reviews scope (does this fall within policy?)
   - Platform team reviews cost & performance
4. **Approval & deployment:**
   - Once approved, tag as v1.0 (or v1.1, etc.)
   - Teams automatically download the latest approved version from the library
   - Removal of prompts is via deprecation notice + 30-day migration window

#### Step 2.3: Enforce "No Ad-Hoc Prompts in Production"

The gateway rejects any invocation with an unapproved prompt:

```java
public GatewayResponse invoke(InvocationRequest request) {
  if (StringUtils.hasText(request.prompt())) {
    throw new PolicyViolationException(
      "Direct prompts are not allowed. Use an approved prompt from the library and submit a PR to prompts/ for new prompts."
    );
  }

  PromptDefinition prompt = promptLibrary
    .find(request.promptName(), request.promptVersion())
    .filter(PromptDefinition::approved)
    .orElseThrow(() -> new PolicyViolationException(
      "Prompt '%s' was not found or is not approved. View approved prompts at https://prompts.petclinic.dev/."
        .formatted(request.promptName())
    ));

  return modelClient.call(request.withResolvedPrompt(prompt));
}
```

#### Checkpoint 2.1
Before moving forward:
- [ ] Prompt library exists and is version-controlled
- [ ] At least 3 approved prompts are in the library (diagnosis, treatment, communication)
- [ ] Each prompt has clear purpose, examples, and approval checklist
- [ ] Gateway enforces: only approved prompts allowed
- [ ] Attempt to use an unapproved prompt is rejected with clear guidance

---

### Activity 3: Implement Policy Enforcement

**Current state (chaotic):** No centralized rules. Each team implements safety differently.  
**Goal state (controlled):** Platform enforces non-negotiable policies automatically.

#### Step 3.1: Define Safety Policies

Create a policy document:

```yaml
# AI Platform Safety Policies

policies:
  data_handling:
    pii_redaction:
      description: "PII (name, phone, email, SSN) must be redacted before sending to external models"
      applies_to: ["openai", "anthropic"]  # Not for on-prem models
      enforcement: "AUTOMATIC (platform redacts before sending)"
      exception_process: "Submit exception request to security team; requires legal review"
      
    pet_record_isolation:
      description: "Query results for Pet A must not leak data from Pet B"
      applies_to: ["all_rag_queries"]
      enforcement: "AUTOMATIC (filters results by entity_id)"
      
  safety_guardrails:
    medical_domain_only:
      description: "Clinical AI can only answer medical questions; must refuse non-medical queries"
      enforcement: "PROMPT constraint + API validation"
      violation_handling: "Log attempt, alert compliance team"
      
    confidence_threshold:
      description: "If confidence < 60%, AI must surface uncertainty to user"
      enforcement: "AUTOMATIC (response blocked if confidence too low)"
      
  cost_controls:
    budget_enforcement:
      description: "Teams cannot exceed monthly AI spend budget"
      budget_assignment: "Per-team in configuration"
      enforcement: "AUTOMATIC (requests rejected when budget exceeded)"
      
    token_limits:
      description: "Individual prompts have max token limits"
      limits_defined_in: "Prompt library (per prompt)"
      enforcement: "AUTOMATIC (response truncated if exceeding limit)"
      
  audit_trails:
    logging_requirements:
      description: "Every AI invocation must be logged with: team, user, feature, model, prompt, input, output, cost, decision (approved/escalated/rejected)"
      enforcement: "AUTOMATIC (gateway logs all)"
      retention: "90 days in hot storage, 7 years in cold archive"
      
    clinical_decision_log:
      description: "Clinical recommendations must be logged in patient record with timestamp, AI confidence, clinician decision"
      enforcement: "Application code (not gateway); checked in code review"
```

#### Step 3.2: Implement Enforcement Points

Add policy checks to the gateway:

```java
@Component
public class PolicyEnforcer {

  public String redactPii(String input) {
    return input
      .replaceAll("[\\w.+-]+@[\\w.-]+", "[EMAIL]")
      .replaceAll("\\b\\d{3}-\\d{2}-\\d{4}\\b", "[SSN]");
  }

  public List<SearchResult> isolateData(List<SearchResult> results, String requestedPetId) {
    List<SearchResult> filtered = results.stream()
      .filter(result -> requestedPetId.equals(result.entityId()))
      .toList();

    if (filtered.size() < results.size()) {
      logger.warn("Filtered {} records due to isolation policy", results.size() - filtered.size());
    }

    return filtered;
  }

  public void validateConfidence(double confidence) {
    double minimumConfidence = 0.6d;
    if (confidence < minimumConfidence) {
      throw new ConfidenceThresholdViolationException(
        "Confidence %.2f below minimum %.2f. Escalate this request to a human reviewer."
          .formatted(confidence, minimumConfidence)
      );
    }
  }

  public void validateBudget(String teamId) {
    BigDecimal monthlySpend = telemetry.getMonthlySpend(teamId);
    BigDecimal budget = config.getTeamBudget(teamId);

    if (monthlySpend.compareTo(budget) >= 0) {
      throw new BudgetExceededException("Team %s has exhausted its monthly budget of %s".formatted(teamId, budget));
    }

    if (monthlySpend.compareTo(budget.multiply(BigDecimal.valueOf(0.8d))) > 0) {
      alerts.send("Team %s is at %s of budget".formatted(teamId, monthlySpend.divide(budget)));
    }
  }
}
```

#### Step 3.3: Make Violations Visible

When a policy is violated, don't silently drop the request. Make it visible:

```java
@ControllerAdvice
public class GatewayErrorHandler {

  @ExceptionHandler(PolicyViolationException.class)
  public ResponseEntity<ErrorResponse> handlePolicyViolation(
    PolicyViolationException ex,
    InvocationRequest request
  ) {
    String errorId = UUID.randomUUID().toString().substring(0, 8);

    logger.error(
      "POLICY_VIOLATION {}: {} | Team: {} | Feature: {} | Reason: {}",
      errorId,
      ex.policyName(),
      request.teamId(),
      request.featureId(),
      ex.getMessage()
    );

    if (ex.severity() == PolicyViolationSeverity.CRITICAL) {
      alerts.sendToSecurityTeam(new SecurityAlert(errorId, request.teamId(), ex.policyName(), ex.getMessage(), Instant.now()));
    }

    return ResponseEntity.badRequest().body(
      new ErrorResponse(errorId, ex.userMessage(), ex.suggestedAction(), ex.documentationUrl())
    );
  }
}
```

Example error response to a team:

```json
{
  "error": {
    "id": "pol_9f2x8k",
    "message": "Policy Violation: PII Redaction",
    "details": "Your input contains an email address. PII must be redacted before sending to external models.",
    "suggested_action": "Redact PII from input and retry",
    "documentation": "https://docs.petclinic.dev/policies/data-handling",
    "contact": "ai-governance@petclinic.dev"
  }
}
```

#### Checkpoint 3.1
Before moving forward:
- [ ] Policy document is written and shared with teams
- [ ] At least 3 policies are enforced by the gateway (PII, data isolation, budget)
- [ ] Policy violations are logged and cause requests to be rejected
- [ ] Security team is alerted on critical violations
- [ ] Teams receive clear, actionable error messages

---

### Activity 4: Add Cost & Usage Telemetry

**Current state (unknown):** You don't know what you're spending or on what.  
**Goal state (visible):** Real-time dashboards showing spend, usage patterns, anomalies.

#### Step 4.1: Log Every Invocation

The gateway logs everything:

```java
@Component
public class TelemetryLogger {

  public void logInvocation(
    String teamId,
    String featureId,
    String promptName,
    String model,
    int inputTokens,
    int outputTokens,
    BigDecimal costUsd,
    String responseStatus,
    long durationMs,
    Map<String, Object> metadata
  ) {
    InvocationRecord record = new InvocationRecord(
      UUID.randomUUID(),
      Instant.now(),
      teamId,
      featureId,
      promptName,
      model,
      inputTokens,
      outputTokens,
      inputTokens + outputTokens,
      costUsd,
      responseStatus,
      durationMs,
      metadata == null ? Map.of() : metadata
    );

    timeSeries.write(record);
    dataWarehouse.insert(record);
  }
}
```

Each record captures:
- **Team:** Who is using the AI?
- **Feature:** What problem are they solving (diagnosis-assist, owner-message, etc.)?
- **Prompt:** Which approved prompt was used?
- **Model:** Which model provider and model?
- **Tokens:** Input + output token count (basis for cost calculation)
- **Cost:** USD cost for this invocation
- **Duration:** How long did the request take?
- **Status:** Success, error, or policy violation?
- **Metadata:** Custom fields (patient_id for anonymized correlation, etc.)

#### Step 4.2: Build Dashboards

Create dashboards for different audiences:

**Dashboard 1: Executive Summary**
- Total spend this month (vs. budget, vs. last month)
- Top 5 features by cost
- Cost trend (30-day rolling)
- Cost per user (how much are we spending per clinic staff member?)

**Dashboard 2: Cost by Team**
- Spend per team (ranked)
- Budget utilization % per team
- Month-to-date spend + forecast for end of month
- Cost per invocation by team (efficiency metric)

**Dashboard 3: Cost by Feature**
- Spend per feature (diagnosis-assist, owner-message, etc.)
- Invocation count per feature
- Average cost per invocation
- Cost trend (is this feature getting cheaper as we optimize?)

**Dashboard 4: Performance & Quality**
- Success rate by feature (% invocations that succeed vs. fail/error)
- Average response time by model
- Policy violations by type (PII, data isolation, budget, etc.)
- Error trends (are errors increasing? decreasing?)

**Dashboard 5: Model Usage**
- Invocations per model (Claude, GPT-4, etc.)
- Cost per model
- Model popularity trend (shifting to cheaper models?)
- Distribution of invocation sizes by model (token histogram)

#### Step 4.3: Implement Alerting

Set up automated alerts:

```yaml
alerts:
  # Budget alerts
  team_approaching_budget:
    condition: "monthly_spend > budget * 0.8"
    notification: "Email team lead + cost-accountability-owners"
    frequency: "Once per day"
    
  team_exceeded_budget:
    condition: "monthly_spend > budget"
    notification: "Email team lead + CFO + AI governance board"
    severity: "HIGH"
    auto_action: "Requests from this team rejected until budget reset"
    
  # Anomaly alerts
  feature_cost_spike:
    condition: "daily_cost > 2x rolling_avg"
    notification: "Email feature owner + platform team"
    example: "diagnosis-assist cost jumped from $120/day to $250/day"
    action: "Investigate; revert prompt if needed"
    
  model_error_rate_spike:
    condition: "error_rate > 5% (when baseline is 0.5%)"
    notification: "Email platform team"
    severity: "MEDIUM"
    action: "Check model status; may indicate outage or drift"
    
  policy_violation_spike:
    condition: "violations_per_hour > baseline"
    notification: "Email security team"
    example: "PII redaction policy violations increased from 0.1/hr to 5/hr"
    severity: "HIGH"
    action: "Investigate team; may indicate misconfiguration or malicious use"
```

#### Checkpoint 4.1
Before moving forward:
- [ ] Every invocation is logged (timestamp, team, feature, model, tokens, cost, status)
- [ ] At least 3 dashboards exist (executive summary, cost by team, cost by feature)
- [ ] Cost per invocation and per team can be calculated
- [ ] Alerts are configured for budget overspend and anomalies
- [ ] A budget alert has been triggered and received

---

### Activity 5: Test Platform Adoption

**Current state:** Platform exists in isolation. Does it actually work for teams?  
**Goal state:** Verified that new teams can adopt the platform with minimal friction.

#### Step 5.1: Onboard a Test Team

Pick one team from Labs 1–4 (e.g., the team that built the diagnosis-assist agent in Lab 3) and ask: *"Can you use this platform?"*

The team should:
1. Authenticate with Microsoft Entra ID (user) or workload identity federation / managed identity (service)
2. Pick an approved model from the list
3. Use an approved prompt from the prompt library
4. Make an invocation through the gateway
5. See telemetry in the dashboard

Document friction points:
- Was authentication easy to set up?
- Did teams find the right prompt?
- Did error messages help or confuse?
- How long did onboarding take?

#### Step 5.2: Test Common Scenarios

**Scenario 1: Happy Path (Success)**
- Team makes a valid invocation with approved prompt/model
- Request succeeds, response is returned, telemetry is logged
- Team can see the invocation in the cost dashboard

**Scenario 2: Policy Violation (PII Redaction)**
- Team makes an invocation with PII in the input (e.g., owner email)
- Request is rejected with clear error message
- Team redacts PII and retries successfully
- Violation is logged

**Scenario 3: Policy Violation (Budget Exceeded)**
- Team has exhausted its monthly budget
- Next request is rejected
- Team is directed to request budget increase
- Attempt is logged as policy violation

**Scenario 4: Unapproved Prompt**
- Team tries to use a custom prompt not in the library
- Request is rejected; directed to approval process
- Team submits PR to prompt library
- Governance board approves, team can now use it

**Scenario 5: Model Drift (Error Rate Spike)**
- A model is misbehaving (returning errors or low-quality results)
- Alert fires
- Platform team investigates, considers reverting to previous prompt version
- Affected team is notified of issue + workaround

#### Step 5.3: Measure Adoption Friction

Create a rubric:

| Criterion | Measure | Target |
|-----------|---------|--------|
| Time to first invocation | From access request to first successful call | < 2 hours |
| Onboarding documentation clarity | "Was the setup guide clear?" | ≥ 4/5 score |
| Error message clarity | "When something broke, did you know how to fix it?" | ≥ 4/5 score |
| Approval process speed | Time from prompt PR to approval | < 24 hours |
| Cost transparency | "Can you see what you're spending?" | ≥ 4/5 score |
| Policy clarity | "Do you understand the governance policies?" | ≥ 4/5 score |

After onboarding, conduct a brief retrospective with the test team:
- What worked well?
- What was confusing?
- What policies felt fair? Which felt like obstacles?
- Would you recommend this platform to another team?

#### Step 5.4: Document the Adoption Playbook

Based on the test team's experience, create a playbook:

```markdown
# Platform Adoption Playbook

## For New Teams: Getting Started

### Step 1: Request Platform Access (30 min)
- Contact: ai-platform@petclinic.dev
- Provide: Team name, team lead, primary AI use case
- Receive: Entra group membership or RBAC assignment, documentation

### Step 2: Review Approved Resources (1 hour)
- Browse approved models: https://platform.petclinic.dev/models
- Browse prompt library: https://platform.petclinic.dev/prompts
- Can you solve your problem with existing resources?
  - **Yes?** → Go to Step 3
  - **No?** → Go to "Request New Prompt/Model" (see below)

### Step 3: Integrate with Gateway (1-2 hours)
- Install SDK: `npm install @petclinic/ai-sdk`
- Sign in with `az login` for local development, or configure managed identity / workload identity federation for automated callers
- Make first invocation (example code provided)
- Verify invocation appears in cost dashboard

### Step 4: Set up Monitoring (30 min)
- Subscribe to budget alerts
- Set up feature-specific alerts if needed
- Review monthly cost forecast

## Request New Prompt

1. **Check if it exists:** Browse prompt library first
2. **Start a PR:** Create prompt file following template
3. **Describe the need:** Why do you need this prompt?
4. **Include examples:** Show input/output pairs
5. **Governance board review:** 1-2 business days
6. **Once approved:** Available to all teams

## Request New Model

1. **Fill out request form:** Why do you need this model?
2. **Provide cost analysis:** Expected usage volume + cost
3. **Identify compliance needs:** Any special data handling?
4. **Finance review:** Does budget exist?
5. **Security review:** Any new risks?
6. **Platform team decision:** Approved, rejected, or conditional

## Troubleshooting

**"Access Denied"**
- Verify your Entra role or group assignment for the gateway
- If access was just granted, allow a few minutes for RBAC propagation
- If using federation, confirm the workload identity subject matches the platform configuration

**"Prompt Not Found"**
- Prompt doesn't exist or is not approved. Browse library: https://platform.petclinic.dev/prompts
- To request a new prompt, see "Request New Prompt" above

**"Budget Exceeded"**
- Your team has used up its monthly AI budget
- Request budget increase from your finance contact
- Or: Optimize prompt/model choices to reduce spending

**"Policy Violation: PII Detected"**
- You're sending personally identifiable information to an external model
- Redact PII before sending: remove names, emails, phone numbers, SSNs
- Use platform.redact() utility function: https://docs.petclinic.dev/pii-redaction
```

#### Checkpoint 5.1
Before moving forward:
- [ ] At least one team successfully onboarded to the platform
- [ ] Team used an approved model, approved prompt, and went through the gateway
- [ ] All 5 scenarios (happy path, PII violation, budget, unapproved prompt, error spike) were tested
- [ ] Adoption friction was measured; areas for improvement identified
- [ ] Adoption playbook is written and shared with organization

---

## Verification Checkpoints

After completing all activities, verify the platform is ready:

### Checkpoint A: Model Abstraction
- [ ] All model requests route through the central gateway
- [ ] Teams cannot call model APIs directly (verified by network policies)
- [ ] Authentication is enforced; unauthenticated requests are rejected
- [ ] Rate limiting works (exceed quota → request rejected)

### Checkpoint B: Prompt Governance
- [ ] Approved prompt library exists with ≥5 prompts
- [ ] Each prompt has metadata (purpose, model, examples, approval date)
- [ ] Gateway rejects requests with unapproved prompts
- [ ] Teams can request new prompts via PR; PR gets reviewed within 1 business day

### Checkpoint C: Policy Enforcement
- [ ] At least 3 policies are enforced by the gateway (PII, data isolation, budget)
- [ ] Policy violations are logged and visible in dashboards
- [ ] Teams receive clear, actionable error messages
- [ ] Security team receives alerts on critical violations

### Checkpoint D: Telemetry
- [ ] Every invocation is logged with full context
- [ ] Cost dashboards are available and accurate
- [ ] Spend can be broken down by team, feature, and model
- [ ] Alerts are configured and have fired at least once

### Checkpoint E: Adoption
- [ ] At least 2 teams have successfully onboarded
- [ ] New teams can set up in < 2 hours
- [ ] Adoption playbook is complete and clear
- [ ] No blockers preventing a 3rd team from adopting

---

## Outputs from This Lab

### Output 1: Enterprise AI Platform
A centralized infrastructure providing:
- **Model access control:** All models routed through gateway; approved models only
- **Prompt governance:** Shared library with versioning and approval workflow
- **Policy enforcement:** Automatic checks for PII, data isolation, budgets, compliance
- **Telemetry:** Comprehensive logging; cost, usage, and performance dashboards
- **Error handling:** Clear, actionable error messages for policy violations

### Output 2: Governance Framework Document
Defines:
- **Approved models:** Which models can be used, by whom, for what?
- **Approval process:** How do teams request new models or prompts?
- **Safety policies:** Non-negotiable rules (PII, data isolation, audit trails)
- **Cost controls:** Budget assignment, alerting, overspend handling
- **Audit requirements:** What must be logged? For how long? Who can access?
- **Incident response:** If something goes wrong (model misbehavior, policy violation, security issue), what's the playbook?

Example sections:

```markdown
# Governance Framework: PetClinic AI Platform

## Approval Authority

| Resource | Authority | SLA |
|----------|-----------|-----|
| New prompt | Clinical Lead + AI Governance Board | 1 business day |
| New model | CFO + Security Team + Platform Team | 3 business days |
| Budget increase | Team Finance Contact + VP Finance | 5 business days |
| Exception to policy | Security Team + AI Governance Board | 1 business day |

## Mandatory Audit Trail

Every invocation must log:
- Timestamp (UTC, millisecond precision)
- TeamId, UserId, FeatureId
- Model, Prompt, Input Tokens, Output Tokens
- Cost (USD)
- Response Status (success, error, policy_violation)
- Policy violations (if any)

Retention:
- Hot storage: 90 days (real-time access)
- Archive: 7 years (legal compliance)

## Incident Response

If a policy violation occurs:
1. Log the violation (automatic)
2. Alert relevant stakeholders:
   - Severity "CRITICAL" (security): Alert security team within 5 min
   - Severity "HIGH" (compliance): Alert governance board within 1 hour
   - Severity "MEDIUM" (other): Alert team lead within 1 business day
3. Investigate:
   - Is this team misconfigured? Malicious? Or a platform bug?
   - What's the blast radius? (How many other teams affected?)
4. Remediate:
   - For teams: Guide to fix configuration
   - For platform: Roll back or patch if needed
5. Post-mortem: Document lessons learned
```

### Output 3: Adoption Playbook
Step-by-step guidance for new teams:
- How to request platform access
- How to find and use approved resources
- How to request new prompts/models
- Troubleshooting common issues
- Escalation contacts

### Output 4: Operational Runbook
For the platform team:
- How to monitor platform health
- How to respond to common alerts
- How to add new models (process + checklist)
- How to deprecate old prompts
- How to investigate policy violations
- Backup/recovery procedures

---

## Teaching Moment

> **"The question is no longer 'can we build AI?'—it's 'can we scale it safely?'"**

This is the core insight of Lab 5. Early in a project, governance feels like overhead. One team, one agent, one prompt—you don't need governance.

But the moment you have two teams, governance becomes essential. Without it:
- Teams reinvent solutions (duplicate effort)
- Safety is inconsistent (one team handles PII correctly; another doesn't)
- Costs spiral (no visibility into what you're spending)
- Compliance is a nightmare (you can't audit decisions)

The platform and governance patterns in this lab aren't constraints—they're accelerators. They let teams innovate locally while enforcing safety and consistency globally.

The best organizations don't have 50 AI teams building 50 different agents. They have 1 platform team building infrastructure and 49 teams using it to solve their domain problems faster, safer, and cheaper.

---

## Reflection Questions

Before moving to Lab 6, consider:

1. **What safety policies were hardest to enforce? Why?** Were the policies themselves unclear, or was implementation difficult? Did teams resist any particular policy?

2. **Did platform overhead discourage adoption?** Did any team avoid using the platform because the approval process was too slow? How would you balance speed with safety?

3. **Cost visibility changed behavior. How?** Did teams optimize their prompts/models once they could see costs? Which teams? Which features?

4. **If a team wants to use an unapproved model, how do you decide?** What's your process? Who has the final say? How do you balance innovation with safety?

5. **What metrics would convince you the platform is working?** Is it adoption rate? Cost control? Safety incidents averted? A combination?

6. **How does governance change the culture?** Do engineers feel trusted, or surveilled? Are they excited about building AI, or frustrated by policies?

---

## Success Criteria

You've completed Lab 5 when:

- [ ] **Model abstraction:** All teams request models through the gateway; direct API calls are not possible
- [ ] **Prompt governance:** All production prompts come from an approved library; custom prompts are rejected
- [ ] **Policy enforcement:** At least 3 policies (PII, data isolation, budget) are automatically enforced
- [ ] **Telemetry:** You have real-time visibility into cost, usage, and performance
- [ ] **Adoption:** At least 2 teams have onboarded to the platform with minimal friction
- [ ] **Documentation:** Governance framework and adoption playbook are complete and clear
- [ ] **Incident response:** You have a process for responding to policy violations and anomalies

---

## Next Steps

Move to **Lab 6: AI-Native Product Re-Thinking (Optional Capstone)** when ready.

Labs 1–5 assumed the product stays mostly the same; you're adding AI features to it. Lab 6 asks a different question:

**If we were building PetClinic from scratch today, knowing everything we know about AI, what would we build differently?**

This is where AI stops being a feature and becomes the foundation of how the system works. It's optional—focus on operationalizing Labs 1–5 if you're more interested in execution. But if you want to understand AI maturity, Lab 6 is where that journey leads.

---

*Lab 5 content authored by CJ. Pedagogical framework and technical patterns by Toby and Josh.*
