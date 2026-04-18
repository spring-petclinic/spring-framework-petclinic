# AECF Multi-Repo Surfaces — Proposal

LAST_REVIEW: 2026-04-17
OWNER SEACHAD
STATUS: proposal

---

## 1. Motivation

The current AECF surface model is scoped to a single repository. All paths in `AECF_SURFACES_INDEX`, `AECF_SURFACE_<id>.md`, and `AECF_RUN_CONTEXT.json` are relative to one `<workspace_root>`.

This is sufficient when a system lives in a monorepo or when cross-repo dependencies are minimal. It is insufficient when:

1. Multiple repositories collaborate to deliver a single business capability.
2. A change in one repository requires coordinated changes in another.
3. Shared contracts (APIs, message schemas, shared state like REDIS, data pipelines) span repository boundaries.
4. Context about the external dependency is needed to make safe decisions in the local repository.

## 2. Scope of this proposal

This document introduces two new concepts on top of the existing single-repo surface model:

| Concept | Purpose | Scope |
| --- | --- | --- |
| **Contract Boundary** | Describes the explicit interface between two repos | One boundary per shared contract |
| **Federation Manifest** | Indexes all repos and their contract boundaries for a multi-repo ecosystem | One manifest per ecosystem |

Neither concept replaces or modifies the existing intra-repo surface model. They add a layer above it.

## 3. Core Principle: Plan Together, Execute Sequentially

When a change spans multiple repositories, the recommended AECF strategy is:

1. **Plan jointly**: produce a single Cross-Repo Change Plan that identifies all affected repos, surfaces, and contract boundaries.
2. **Execute per-repo**: run AECF skills in one repo at a time, in dependency order (providers before consumers).
3. **Track coordination**: use the Federation Manifest or a shared artifact to track per-repo status.

Atomic cross-repo changes (editing two repos simultaneously) are NOT recommended because:

- Each repo has its own CI, test suite, and deployment pipeline.
- Independent rollback is safer.
- The expand-contract pattern handles most breaking changes without requiring simultaneous deployment.

### 3.1 Expand-Contract Pattern

For changes that affect a shared contract (e.g., REDIS key schema), the recommended sequence is:

1. **Provider repo (expand)**: implement the new contract while keeping backward compatibility with the old one.
2. **Consumer repo(s) (migrate)**: adopt the new contract.
3. **Provider repo (contract)**: remove support for the old contract.

This ensures zero-downtime and independent repo release cycles.

### 3.2 When Atomic Coordination Is Unavoidable

In rare cases (irreconcilable breaking change, same-cluster simultaneous deploy), the plan must:

1. Mark the change as `coordination: atomic` in the Cross-Repo Change Plan.
2. Define a deployment window.
3. Require human sign-off before execution in each repo.

## 4. Contract Boundary

A **Contract Boundary** is a document that describes the interface between two or more repositories.

It is NOT a surface. It does not describe internal implementation. It describes:

1. What is exposed and what is consumed.
2. The protocol or mechanism (REST API, REDIS shared state, file-based data pipeline, shared library, message queue, etc.).
3. Invariants that both sides must respect.
4. Change policy (backward-compatible required, versioned schema, expand-contract, etc.).
5. Ownership — who is responsible for the contract.

### 4.1 Where Contract Boundaries Live

Each repo that participates in a contract boundary SHOULD have a local copy or reference:

```
.aecf/runtime/documentation/contracts/
  AECF_CONTRACT_<contract_id>.md
```

The contract document is shared by convention — both the provider and consumer repos should have a copy or a reference to the canonical version.

### 4.2 Relationship to Surfaces

A Contract Boundary connects to intra-repo surfaces through the `Dependencies and Integrations` section of `AECF_SURFACE_<id>.md`:

| Dependency | Type | Direction | Notes |
| --- | --- | --- | --- |
| `contract:redis_entity_cache` | external_contract | outbound | See `AECF_CONTRACT_redis_entity_cache.md` |

This way, when a skill loads a surface and sees an external contract dependency, it can optionally load the Contract Boundary document for cross-repo awareness.

### 4.3 Contract Boundary Template

See [CONTRACT_BOUNDARY_TEMPLATE.md](../templates/CONTRACT_BOUNDARY_TEMPLATE.md).

## 5. Federation Manifest

A **Federation Manifest** is a lightweight YAML file that indexes all repositories and contract boundaries in a multi-repo ecosystem.

### 5.1 Purpose

1. Map logical repo identifiers to canonical URLs (never to local paths).
2. List all contract boundaries and their participants.
3. Define roles (provider, consumer, transformer) for each repo.
4. Enable cross-repo change planning.

### 5.2 Where It Lives

The Federation Manifest can live:

- In a dedicated orchestration/meta repository.
- In each participating repo (with a convention to keep copies synchronized).
- In a shared documentation location.

Recommended path:

```
.aecf/runtime/federation/AECF_FEDERATION.yaml
```

### 5.3 Local Path Resolution

Because developers clone repos into different local paths, the manifest MUST NOT contain local filesystem paths.

Instead, each developer maintains a local, gitignored resolution file:

```
.aecf/local/federation_paths.yaml    # gitignored
```

This file maps logical repo identifiers to local absolute paths. AECF resolves cross-repo references through this indirection.

If a repo is not cloned locally, AECF treats it as "context unavailable" and works only with the Contract Boundary documentation.

### 5.4 Federation Manifest Template

See [FEDERATION_MANIFEST_TEMPLATE.yaml](../templates/FEDERATION_MANIFEST_TEMPLATE.yaml).

## 6. Impact on Existing AECF Concepts

### 6.1 Surface Discovery

No change. Surface discovery remains single-repo. It MAY additionally detect outbound contract boundaries by analyzing imports, connection strings, or shared library references.

### 6.2 Project Context Generator

The `external_integrations` section of `AECF_PROJECT_CONTEXT.md` MAY reference known contract boundaries.

### 6.3 RUN_CONTEXT Extension

`AECF_RUN_CONTEXT.json` MAY include an optional field:

```json
{
  "federation_context": {
    "federation_id": "seachad-analytics",
    "relevant_contracts": ["redis_entity_cache", "preprocessed_data"],
    "cross_repo_plan_ref": "path/to/CROSS_REPO_PLAN.md"
  }
}
```

### 6.4 Skill Execution

Skills operate in ONE repo at a time. If a skill detects that a change crosses a contract boundary, it SHOULD:

1. Emit a **coordination note** in its output.
2. Reference the Contract Boundary document.
3. Suggest the next repo and surface to work on.
4. NOT attempt to modify files outside the current workspace.

## 7. Cross-Repo Change Plan

When a change spans multiple repos, the recommended artifact is a **Cross-Repo Change Plan**:

| Section | Content |
| --- | --- |
| Change Summary | What is changing and why |
| Affected Repos | Logical repo IDs from the Federation Manifest |
| Affected Contracts | Which contract boundaries are impacted |
| Execution Order | Ordered list of per-repo steps (provider first, consumers second) |
| Per-Repo Plan Reference | Link to the AECF plan artifact in each repo |
| Coordination Type | `sequential` (default) or `atomic` |
| Status Tracker | Per-repo status: `pending` / `in_progress` / `done` / `blocked` |

This artifact is human-maintained and referenced from each repo's `AECF_RUN_CONTEXT.json`.

## 8. Summary of New Artifacts

| Artifact | Type | Location |
| --- | --- | --- |
| `AECF_CONTRACT_<id>.md` | Contract Boundary document | `.aecf/runtime/documentation/contracts/` |
| `AECF_FEDERATION.yaml` | Federation Manifest | `.aecf/runtime/federation/` |
| `federation_paths.yaml` | Local path resolver (gitignored) | `.aecf/local/` |
| Cross-Repo Change Plan | Coordination artifact | Human-chosen location |

## 9. Open Questions

1. Should the Federation Manifest be auto-discoverable or always manually created?
2. Should AECF enforce contract boundary validation (provider schema vs consumer expectations)?
3. Should there be a dedicated skill for cross-repo change planning, or is it a mode of existing skills like `aecf_new_feature`?
4. How should contract boundary versioning interact with existing surface versioning?

## 10. References

- [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md) — current single-repo surface model
- [AECF_SKILL_SURFACE_CONTRACT.md](AECF_SKILL_SURFACE_CONTRACT.md) — skill consumption contract for surfaces
- [AECF_RUN_CONTEXT_CONTRACT.md](AECF_RUN_CONTEXT_CONTRACT.md) — runtime context contract
- [CONTRACT_BOUNDARY_TEMPLATE.md](../templates/CONTRACT_BOUNDARY_TEMPLATE.md) — template for contract boundaries
- [FEDERATION_MANIFEST_TEMPLATE.yaml](../templates/FEDERATION_MANIFEST_TEMPLATE.yaml) — template for federation manifests
