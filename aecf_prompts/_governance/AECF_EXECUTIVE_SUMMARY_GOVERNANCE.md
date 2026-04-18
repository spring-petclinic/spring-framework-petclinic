# AECF EXECUTIVE_SUMMARY GOVERNANCE PROMPT

## OBJECTIVE

Enforce mandatory documentation generation, checklist validation,
cumulative executive summary tracking, and **universal metadata compliance**.

This mechanism guarantees:

- Full traceability
- Historical control
- Auditability
- Executive visibility
- Correlated numbering
- Root prompt traceability
- Template enforcement consistency
- **Standardized metadata across ALL generated documents**

Scope clarification:

- Documentation governance applies to prompts and skills.
- EXECUTIVE_SUMMARY generation is on-demand only via `skill_executive_summary`.
- Other skills do NOT auto-generate EXECUTIVE_SUMMARY files.
- Standalone prompt execution (`prompts/...`) does NOT generate EXECUTIVE_SUMMARIES.

---

## 1. DOCUMENTATION IS MANDATORY (NOT SKILL RESPONSIBILITY)

Every prompt MUST:

- Generate its own documentation file.
- Specify file path.
- **Include the standard METADATA block** defined in `templates/TEMPLATE_HEADERS.md`
- Include:
  - Description of modification
  - Technical impact
  - Date
  - Context
  - Related prompts
- Reference previous documentation if applicable.

If documentation is not generated → PROCESS INVALID (NO-GO).

Documentation generation CANNOT be delegated to the skill.

---

## 2. CHECKLIST MUST VALIDATE DOCUMENTATION

Each prompt/skill must include a final checklist verifying:

[ ] Code generated or modified  
[ ] Documentation file created or updated  
[ ] Documentation includes impact analysis  
[ ] **METADATA block from TEMPLATE_HEADERS.md is present and complete**  
[ ] **Executed By field is filled**  
[ ] Correlative numbering verified  
[ ] Links to previous summaries verified  

If any item fails → STOP and correct.

---

## 3. EXECUTIVE_SUMMARY GENERATION (ON-DEMAND)

EXECUTIVE_SUMMARY files are generated only when this skill is explicitly invoked:

`skill: executive_summary TOPIC: <topic_name>`

Generated file:

/documentation/{{TOPIC}}/AECF_[NN]_EXECUTIVE_SUMMARY.md

Where:

- [NN] = next sequential AECF number within `documentation/{{TOPIC}}/`
- Numbering must NEVER reset

Mandatory metadata in the summary:

- **ALL fields defined in `templates/TEMPLATE_HEADERS.md`** (standard METADATA block)
- Executed By: user currently logged in VS Code (preferred source)
- Fallback when VS Code user is unavailable: OS user/session user
- Document-type specific extension fields as defined in the template's `@METADATA` directive

IMPORTANT:

The EXECUTIVE_SUMMARY MUST strictly follow the template located at:

/templates/EXECUTIVE_SUMMARY_TEMPLATE.md

No structural deviations are allowed.
No additional sections may be added.
No sections may be removed.
Only content fields may be filled.

If the template is not respected → EXECUTION INVALID.

Important execution rule:

- Standalone prompt execution (`prompts/...`) does not generate
  EXECUTIVE_SUMMARY files.
- Other skills do NOT auto-generate EXECUTIVE_SUMMARY files.
- Executive summaries are generated only through `skill_executive_summary`.

---

## 4. EXECUTIVE_SUMMARY TEMPLATE ENFORCEMENT

The template located at:

/templates/EXECUTIVE_SUMMARY_TEMPLATE.md

Is the single source of truth for summary structure.

The metadata block is defined centrally in:

/templates/TEMPLATE_HEADERS.md

Rules:

- The structure MUST be copied exactly.
- Headings MUST match exactly.
- Section order MUST match exactly.
- Only content placeholders may be filled.
- **The `## METADATA` section MUST follow the standard defined in TEMPLATE_HEADERS.md**
- The template's `@METADATA` directive specifies Document Type, Phase, and extension fields
- If the template is updated in the future, all new EXECUTIVE_SUMMARIES
  must follow the new version.
- If TEMPLATE_HEADERS.md is updated, all new documents must follow the new metadata version.
- Previous EXECUTIVE_SUMMARIES remain immutable.

Template version (if defined inside the template) must be recorded in METADATA.

---

## 5. ROOT PROMPT TRACEABILITY

Each EXECUTIVE_SUMMARY must include:

## ROOT PROMPT

Exact reference or copy of the original prompt that initiated the chain.

If multiple nested prompts exist:

- Document hierarchy
- Identify origin clearly

---

## 6. ACCUMULATIVE LOGIC RULES

- Each new EXECUTIVE_SUMMARY must:
  - Contain incremental changes since previous summary
  - Contain global consolidated summary since beginning
- The last EXECUTIVE_SUMMARY acts as the complete executive state snapshot.

---

## 7. FAILURE CONDITIONS (AUTOMATIC NO-GO)

Execution is INVALID if:

- Documentation is missing
- **METADATA block is missing or incomplete in ANY generated document**
- **`Executed By` or `Date` fields are empty**
- **Document does not follow `@METADATA` directive from its template**
- Numbering is incorrect
- Links are missing
- Root prompt is not referenced
- Checklist validation is incomplete
- Template structure differs from
  /templates/EXECUTIVE_SUMMARY_TEMPLATE.md

---

## 8. UNIVERSAL METADATA MANDATE (ALL DOCUMENTS)

**CRITICAL**: The metadata standard applies to ALL AECF-generated documents, not just EXECUTIVE_SUMMARIES.

The metadata standard is defined centrally in:

**templates/TEMPLATE_HEADERS.md**

This file is the SINGLE SOURCE OF TRUTH for the `## METADATA` block.

Rules:

- Every template in `templates/` includes an `@METADATA` directive referencing TEMPLATE_HEADERS.md
- When generating ANY document, the AI MUST:
  1. Read the `@METADATA` directive from the template
  2. Load `templates/TEMPLATE_HEADERS.md`
  3. Insert the full `## METADATA` table as the FIRST section after the H1 title
  4. Fill Document Type and Phase from the template's directive
  5. Add extension fields if specified in the directive
  6. Auto-resolve all other fields (TOPIC, Date, Executed By, etc.)
- If TEMPLATE_HEADERS.md is updated, all NEW documents must follow the updated version
- Previously generated documents remain immutable
- Missing metadata in any document → **DOCUMENT INVALID**

---

## 9. INTENDED GOVERNANCE OUTCOME

This system guarantees:

- Code evolution traceability
- Modification audit trail
- Change accountability
- Historical reconstruction capability
- Executive-level monitoring
- Prompt chain transparency
- Structural consistency across summaries

This governance model is mandatory for all AECF prompt executions.

Executive summary generation is on-demand via `skill_executive_summary` with explicit TOPIC.
