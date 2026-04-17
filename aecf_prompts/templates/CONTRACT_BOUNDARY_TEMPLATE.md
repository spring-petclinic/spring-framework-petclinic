# AECF_CONTRACT_{{contract_id}}

## METADATA

| Field | Value |
| --- | --- |
| LAST_REVIEW | {{date}} |
| Owner | {{owner}} |
| Contract ID | {{contract_id}} |
| Contract Type | api / shared_state / data_pipeline / shared_library / message_queue / file_exchange |
| Status | active / draft / deprecated |
| Change Policy | expand_contract / versioned_schema / backward_compatible_only / coordinated_deploy |

## 1. Summary

Brief description of what this contract represents and why it exists.

## 2. Participants

| Repo (logical ID) | Role | Surface (if known) | Notes |
| --- | --- | --- | --- |
| {{provider_repo}} | provider | {{surface_id or "—"}} | |
| {{consumer_repo}} | consumer | {{surface_id or "—"}} | |

## 3. Contract Specification

### 3.1 Protocol / Mechanism

Describe the technical mechanism: REST API, REDIS keys, shared database tables, file format, message schema, etc.

### 3.2 Exposed Interface

What the provider makes available. Be specific:

- For APIs: endpoints, methods, request/response schemas.
- For shared state: key patterns, data structures, TTL policies.
- For data pipelines: file formats, column schemas, delivery cadence.
- For shared libraries: public API surface, version constraints.

### 3.3 Consumer Expectations

What consumers depend on. Document the minimum contract consumers rely on, so the provider knows what cannot break without coordination.

## 4. Invariants

Non-negotiable rules that both sides must respect:

1.
2.
3.

## 5. Change Rules

### 5.1 Allowed Without Coordination

Changes the provider can make unilaterally without notifying consumers:

- (e.g., internal refactoring that does not alter exposed interface)

### 5.2 Requires Notification

Changes that require consumer awareness but not simultaneous deployment:

- (e.g., adding a new optional field to an API response)

### 5.3 Requires Coordinated Change

Changes that require the expand-contract pattern or synchronized deployment:

- (e.g., renaming a REDIS key pattern, removing an API field)

## 6. Versioning

| Field | Value |
| --- | --- |
| Current Version | {{version}} |
| Versioning Strategy | semver / date-based / schema-hash / none |
| Backward Compatibility Window | {{e.g., "2 minor versions" or "30 days"}} |

## 7. Observability

How to detect contract violations or degradation at runtime:

- Monitoring: {{describe}}
- Alerting: {{describe}}
- Health checks: {{describe}}

## 8. Testing

### 8.1 Provider-Side Tests

What the provider tests to ensure the contract is met:

1.
2.

### 8.2 Consumer-Side Tests

What consumers test to verify they consume the contract correctly:

1.
2.

### 8.3 Contract Tests (if any)

Shared test suites or schema validators that run independently:

1.

## 9. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| | | |

## 10. History

| Date | Change | Actor |
| --- | --- | --- |
| {{date}} | Contract created | {{actor}} |
