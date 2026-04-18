# AECF Domain Knowledge Packs

LAST_REVIEW: 2026-04-07
OWNER SEACHAD

This folder contains local-first knowledge assets that AECF injects into prompts to adapt its guidance to the real technical stack of the target repository.

The important distinction is this:

- Domains are the base layer. They answer: what broad language, platform, or ecosystem rules apply here?
- Semantic profiles are the refinement layer. They answer: within that domain, what extra rules apply for this concrete framework, ORM, database, architecture, platform, or workload?

Both are prompt guidance only. They are not executable skills, they do not replace AECF governance, and they must never become a runtime dependency on the internet.

## Why this folder exists

AECF works across very different repositories. A generic implementation prompt is often not enough because a Python Flask service, a Java Spring Boot service, a Business Central AL extension, and a COBOL modernization workflow should not receive the same architectural or testing guidance.

This knowledge layer lets AECF specialize prompts deterministically and locally:

- without depending on live web access,
- without copying project code into reusable assets,
- without changing the phase system, gates, or testing requirements.

## What a domain is

A domain is the base knowledge pack for a broad technical family.

In practice, a domain usually maps to a language, platform, or major ecosystem, for example:

- python
- java
- angular
- dotnet
- cobol
- businesscentral
- security

Each domain provides the baseline implementation guidance that should remain true across many repositories of that family. That is why the main file for a domain is its base pack:

- domains/<domain>/pack.md

You should think of a domain pack as the default operating manual for that ecosystem. It usually carries guidance such as:

- architectural boundaries that are usually expected,
- common coding conventions,
- testing expectations,
- security reminders,
- mistakes AECF should avoid when generating or reviewing code.

### What domains are for

Domains are useful when AECF needs a stable baseline before any finer stack specialization. For example:

- the python domain says what generally matters in Python repositories,
- the java domain says what generally matters in JVM repositories,
- the businesscentral domain says what generally matters in AL extension projects.

Without domains, AECF would either stay too generic or jump directly into framework-specific assumptions without a shared base.

### What domains are not for

Domains are not meant to encode project-specific decisions such as:

- your company naming conventions,
- your repository folder naming quirks,
- a specific customer architecture,
- one-off implementation details from a target codebase.

Those belong in the repository context, project memory, or execution-specific prompt, not in reusable knowledge packs.

## What a semantic profile is

A semantic profile is a narrower overlay that refines the base domain pack for a more concrete stack shape.

Its canonical path is:

- domains/<domain>/semantic_profiles/<profile_id>.md

Examples already present in this repository include:

- python/flask_web
- python/sqlalchemy_orm
- python/postgresql_db
- python/azure_functions_python
- python/aws_lambda_python
- java/spring_boot_service
- java/zkoss
- java/jpa_persistence
- java/maven
- java/lombok
- java/lts_compatibility
- java/modernization
- angular/standalone_components
- angular/ngrx_state_management
- businesscentral/al_extension_app
- cobol/cobol_batch_mainframe
- cobol/cobol_cics_online

If the domain pack is the base operating manual, the semantic profile is the specialized supplement.

Examples:

- The python domain can say how to think about Python code broadly.
- The flask_web profile adds HTTP-layer guidance specific to Flask applications.
- The sqlalchemy_orm profile adds persistence guidance for SQLAlchemy-based systems.
- The postgresql_db profile adds database-specific practices.

This means a run can use several layers at once:

- base domain guidance,
- framework guidance,
- ORM guidance,
- database guidance,
- cross-cutting security guidance.

### What semantic profiles are for

Semantic profiles exist to refine prompt behavior without turning each stack combination into a new skill.

They are especially useful for:

- frameworks such as Flask or Spring Boot,
- frontend frameworks and composition models such as Angular standalone applications,
- persistence technologies such as SQLAlchemy or JPA,
- databases such as PostgreSQL,
- workload targets such as AWS Lambda or Azure Functions,
- architecture overlays or cross-cutting concerns when evidence is strong enough.

### What semantic profiles are not for

Semantic profiles are not mini-skills and not hard requirements. They do not:

- execute code,
- own a phase,
- block a run,
- override governance rules,
- replace the base domain pack.

If a profile is missing, malformed, deprecated, or incompatible, AECF must warn and continue.

## How domains and semantic profiles work together

The intended layering is:

1. Load the broad stack understanding.
2. Load the base domain pack for the relevant ecosystem.
3. Refine that guidance with semantic profiles that match the explicit or detected stack.
4. Inject the merged result into prompts as DOMAIN_KNOWLEDGE.

Conceptually:

- domains answer the broad question,
- semantic profiles answer the narrower question,
- AECF composes both into a single prompt block.

For a Flask API backed by SQLAlchemy and PostgreSQL, the useful mental model is:

- domain: python
- semantic profiles: flask_web + sqlalchemy_orm + postgresql_db
- cross-cutting addition: security when applicable

For an Angular application using standalone bootstrapping and NgRx, the useful mental model is:

- domain: angular
- semantic profiles: standalone_components + ngrx_state_management
- cross-cutting addition: security when applicable

## Runtime resolution model

AECF can reach the same knowledge in two ways:

- by explicit stack passed on the skill invocation,
- by detected stack evidence persisted by repo intelligence or codebase intelligence.

Both paths ultimately feed the same runtime resolution logic.

### 1. Explicit stack path

If the user invokes a skill with a stack parameter, that stack becomes the per-execution override.

Example:

aecf next skill=new_feature topic=orders_api stack=python-flask-sqlalchemy-postgresql prompt="Add idempotent order creation"

In that case AECF can resolve explicit stack nodes such as:

- python
- flask
- sqlalchemy
- postgresql

Then it can load:

- the python base pack,
- compatible semantic profiles for Flask, SQLAlchemy, and PostgreSQL,
- cross-cutting profiles such as security when configured to apply.

This is the most direct way to force the knowledge selection you want for a single execution.

### 2. Detected stack path via repo intelligence or codebase intelligence

If the user does not pass stack explicitly, AECF can still infer it from persisted stack artifacts and local evidence.

The important artifact is STACK_JSON.json.

Codebase intelligence can generate and persist that artifact under .aecf/context/. Repo intelligence can also provide stack evidence consumed by the same resolver. Knowledge loading also checks persisted stack artifacts under the AECF runtime/context folders.

That allows a workflow like this:

1. Run codebase_intelligence on the target repository.
2. Let it persist STACK_JSON.json and the rest of the analysis artifacts.
3. Run another skill, such as new_feature, refactor, explain_behavior, or audit-related flows.
4. AECF reads the detected stack evidence and automatically selects the relevant domain pack and semantic profiles.

Example:

aecf next skill=codebase_intelligence topic=repo_inventory prompt="Analyze the repository and emit deterministic stack artifacts"

Then later:

aecf next skill=refactor topic=orders_api prompt="Separate HTTP transport from business logic"

If STACK_JSON.json says the repository is Python + Flask + PostgreSQL, the later skill can inherit that knowledge even without a new stack argument.

## What codebase_intelligence contributes

Codebase intelligence is important because it gives AECF a durable, machine-readable description of the repository, not just a one-off text summary.

For this knowledge system, its most relevant contribution is that it can persist structured artifacts such as:

- STACK_JSON
- PROJECT_STRUCTURE_JSON
- ENTRYPOINTS_JSON
- MODULE_INDEX_JSON
- DEPENDENCY_GRAPH_JSON
- SENSITIVE_AREAS_JSON
- DYNAMIC_PROJECT_CONTEXT

From the perspective of domains and semantic profiles, STACK_JSON is the key bridge. It turns repository analysis into reusable stack evidence that later skills can consume.

This matters because:

- the user does not need to repeat the stack on every later invocation,
- the knowledge selection can stay consistent across runs,
- prompt specialization becomes evidence-based instead of guess-based.

## What passing stack directly contributes

Passing stack directly to a skill is the best option when you want an intentional override for one run.

Use it when:

- the repository is mixed and you want to focus on one sub-stack,
- codebase intelligence has not been run yet,
- you want deterministic specialization immediately,
- you want to overrule ambiguous detection for a single execution.

Examples:

aecf next skill=new_feature topic=billing stack=java-spring-jpa prompt="Add invoice retry scheduling"

aecf next skill=hotfix topic=auth stack=python-flask-postgresql prompt="Fix token refresh race condition"

aecf next skill=document_legacy topic=shipment_edi stack=cobol-cics prompt="Document online transaction flow"

The explicit stack is therefore the strongest user-controlled signal for prompt specialization in that run.

## Resolution order in practice

When the stack graph flow is enabled, the selection model is intended to be read like this:

1. Resolve explicit nodes from the stack argument if present.
2. Resolve detected nodes from strong repository evidence and persisted stack artifacts.
3. Expand graph activations from those nodes.
4. Load base domain knowledge for the loaded stack nodes.
5. Load semantic profiles that are valid, compatible, and supported by explicit nodes, detected nodes, or required evidence.
6. Skip deprecated, invalid, or conflicting profiles with warnings.
7. Build a DOMAIN_KNOWLEDGE prompt block and inject it into the execution prompt.

Important consequences:

- explicit stack is the clearest per-run override,
- detected stack is the automatic fallback when no explicit stack is given,
- semantic profiles enrich the run but do not hard-fail it,
- governance, gates, and testing rules still come from AECF itself, not from these packs.

## Workspace extensions for domains and semantic profiles

The component ships with a default knowledge tree under `aecf_prompts/knowledge/`, but the client workspace can extend that tree locally under `.aecf/knowledge/`.

The intended workspace layout is:

- `.aecf/knowledge/<domain>/pack.md`
- `.aecf/knowledge/<domain>/semantic_profiles/<profile_id>.md`

Examples:

- `.aecf/knowledge/legacyerp/pack.md`
- `.aecf/knowledge/legacyerp/semantic_profiles/batch_modernization.md`
- `.aecf/knowledge/python/semantic_profiles/company_batch.md`

This is a workspace-local extension mechanism, not a replacement mechanism.

### Precedence rule

AECF resolves knowledge in this order:

1. Component default knowledge included with AECF.
2. Workspace-local `.aecf/knowledge/` fallback when the component does not provide that domain or semantic profile.

That means:

- a workspace pack can add a brand new domain,
- a workspace semantic profile can add a brand new refinement for an existing domain,
- a workspace pack must not silently replace a homonymous component pack,
- a workspace semantic profile with the same identity as a component profile is ignored in favor of the component copy.

### When to use workspace knowledge

Use `.aecf/knowledge/` when you need guidance that belongs to a customer or company context, for example:

- a proprietary platform or internal architecture family,
- company-specific operational constraints,
- cross-repository conventions that should stay in the client workspace,
- domain refinements that do not belong in the public/default component.

Do not use it for one-off ticket details or temporary execution context; those still belong in project context, project memory, or the prompt of the current run.

### Contract expectations

For workspace semantic profiles, keep the same contract used by the component:

- frontmatter with `profile_id`, `precedence`, `stack_nodes`, and optional `requires`,
- the mandatory ordered sections from `SEMANTIC_PROFILE_CONTRACT.md`,
- deterministic wording suitable for prompt injection.

### Provenance in generated documentation

Every generation that uses domain knowledge must leave a trace in the generated documentation.

AECF records at least:

- which domain packs or semantic profiles were loaded,
- whether each one came from `component_default` or `workspace_custom`,
- the effective source file used,
- and, when prompt extensions are active, which `_ext` prompt file was applied.

This provenance is written into the generated Markdown metadata so reviewers can distinguish default AECF knowledge from customer-authored knowledge.

## How to think about the two usage modes

Use codebase_intelligence first when:

- you want the repository analyzed once and reused across subsequent executions,
- you want stack inference to be evidence-based,
- you want future skills to inherit the same detected context.

Pass stack directly to the skill when:

- you already know the intended stack,
- you need a per-run override,
- you are working in a polyglot or ambiguous repository,
- you want exact prompt specialization without a prior analysis step.

Use both together when:

- you want automatic defaults from repository analysis,
- but still want the option to override a later run intentionally.

## Current layout

- DOMAIN_CATALOG.json: deterministic catalog-based domain matching.
- STACK_GRAPH.json: graph of languages, frameworks, architectures, and cross-cutting defaults.
- SEMANTIC_PROFILE_CONTRACT.md: canonical file contract for semantic profiles.
- SEMANTIC_PROFILE_PRECEDENCE.md: normative composition, compatibility, and fallback rules.
- sources.json: curated external refresh sources.
- domains/: base packs and semantic profiles.

## Domain folder convention

- domains/<domain>/pack.md: primary base pack loaded into prompts.
- domains/<domain>/semantic_profiles/: stack refinements for that domain.
- domains/security/: shared cross-cutting guidance that can be composed with other domains.

## Current semantic profile coverage

- python: Flask web, SQLAlchemy ORM, PostgreSQL, Azure workloads, AWS workloads
- java: Spring Boot services, ZKoss, JPA persistence, Lombok, LTS compatibility, modernization, Azure workloads, AWS workloads
- businesscentral: AL extension application
- cobol: batch-oriented mainframe modernization, CICS online workloads

## Key rules to keep clear

- Domains are the reusable base layer.
- Semantic profiles are the reusable refinement layer.
- Codebase intelligence can persist stack evidence so later skills auto-load the right knowledge.
- Passing stack directly to a skill is the per-execution override.
- Both paths can converge on the same DOMAIN_KNOWLEDGE block.
- None of this overrides AECF governance, phase gates, or mandatory testing behavior.
