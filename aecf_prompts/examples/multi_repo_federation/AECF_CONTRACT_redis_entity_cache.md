# AECF_CONTRACT_redis_entity_cache

## METADATA

| Field | Value |
| --- | --- |
| LAST_REVIEW | 2026-04-17 |
| Owner | SEACHAD — API_ROBOT team |
| Contract ID | redis_entity_cache |
| Contract Type | shared_state |
| Status | active |
| Change Policy | expand_contract |

## 1. Summary

API_ROBOT writes entity data to a shared REDIS instance as a caching layer. Flask_Dashboards reads from this cache to render dashboards without hitting the upstream data sources directly. This contract defines the key schema, value format, TTL policy, and cache-miss behavior.

## 2. Participants

| Repo (logical ID) | Role | Surface (if known) | Notes |
| --- | --- | --- | --- |
| api_robot | provider | data_integration | Writes entities to REDIS after retrieval/processing |
| flask_dashboards | consumer | dashboard_rendering | Reads entity cache for dashboard data |

## 3. Contract Specification

### 3.1 Protocol / Mechanism

- **Type**: REDIS shared state (read/write over TCP)
- **REDIS instance**: Configured per environment via `REDIS_URL` environment variable
- **Database**: `db=0` (production), `db=1` (staging)

### 3.2 Exposed Interface

**Key pattern**:

```
robot:{entity_type}:{entity_id}
```

Examples:

```
robot:customer:12345
robot:invoice:2026-001
robot:product:SKU-789
```

**Value format** (JSON string):

```json
{
  "data": {
    "id": "12345",
    "name": "Acme Corp",
    "status": "active"
  },
  "updated_at": "2026-04-17T10:30:00Z",
  "source": "api_robot",
  "schema_version": "1.0"
}
```

**TTL policy**:

- Default TTL: 3600 seconds (1 hour)
- Entity-specific TTL overrides configured in API_ROBOT's `config/cache_ttl.yaml`
- TTL is set exclusively by API_ROBOT at write time

**Operations**:

| Operation | Actor | REDIS Command |
| --- | --- | --- |
| Write entity | API_ROBOT | `SET` with `EX` (TTL) |
| Read entity | Flask_Dashboards | `GET` |
| Delete entity | API_ROBOT | `DEL` (on source deletion) |
| List by type | Flask_Dashboards | `SCAN` with pattern `robot:{type}:*` |

### 3.3 Consumer Expectations

Flask_Dashboards depends on:

1. Key pattern `robot:{entity_type}:{entity_id}` is stable.
2. Value is always a JSON string with at least `data` and `updated_at` fields.
3. `schema_version` in the value indicates the structure of `data`.
4. Cache miss (key not found) is normal — dashboard falls back to REST API call.
5. `SCAN` with pattern `robot:{type}:*` returns all cached entities of a type.

## 4. Invariants

1. Keys MUST follow pattern `robot:{entity_type}:{entity_id}`.
2. Values MUST be valid JSON with `data`, `updated_at`, and `schema_version` fields.
3. TTL is managed exclusively by API_ROBOT. Flask_Dashboards MUST NOT set or modify TTL.
4. Flask_Dashboards MUST NOT write to REDIS keys matching the `robot:*` pattern.
5. Flask_Dashboards MUST handle cache misses gracefully (fallback to REST API or show stale-data indicator).
6. New fields MAY be added to the value JSON without breaking the contract.

## 5. Change Rules

### 5.1 Allowed Without Coordination

- Adding new entity types (new `{entity_type}` values).
- Adding new fields inside the `data` object.
- Adding new top-level fields to the value JSON (consumers must ignore unknown fields).
- Changing TTL values.

### 5.2 Requires Notification

- Adding a new top-level field that consumers should start using (e.g., `expires_at`).
- Changing the REDIS database number.
- Introducing per-environment key prefixes.

### 5.3 Requires Coordinated Change

- Renaming the key pattern (e.g., `robot:` → `apirobot:`).
- Removing or renaming fields in the value JSON (`data`, `updated_at`, `schema_version`).
- Changing the value format (e.g., JSON → MessagePack).
- Moving to a different REDIS instance.

For all items in 5.3, use the **expand-contract** pattern:

1. API_ROBOT writes to both old and new format/keys.
2. Flask_Dashboards migrates to read from new format/keys.
3. API_ROBOT stops writing old format/keys.

## 6. Versioning

| Field | Value |
| --- | --- |
| Current Version | 1.0 |
| Versioning Strategy | semver (via `schema_version` in value JSON) |
| Backward Compatibility Window | 2 minor versions |

## 7. Observability

- **Monitoring**: REDIS `INFO` command tracked via Prometheus exporter for key count, memory, and hit/miss ratio.
- **Alerting**: Alert if cache hit ratio drops below 70% for >10 minutes (may indicate write failure in API_ROBOT).
- **Health checks**: Flask_Dashboards `/health` endpoint includes a REDIS connectivity check.

## 8. Testing

### 8.1 Provider-Side Tests (API_ROBOT)

1. Unit tests verify key pattern and value format on every write.
2. Integration test writes a known entity, reads it back, verifies format.
3. TTL test verifies key expires after configured time.

### 8.2 Consumer-Side Tests (Flask_Dashboards)

1. Unit tests verify dashboard renders correctly with a mocked REDIS value.
2. Cache-miss test verifies fallback to REST API.
3. Unknown-field test verifies consumer ignores extra fields in value JSON.

### 8.3 Contract Tests

1. Shared JSON schema file (`contract_schemas/redis_entity_cache_v1.json`) validated in both repos' CI pipelines.

## 9. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| REDIS instance unavailable | Dashboards show stale or missing data | Flask_Dashboards has REST API fallback |
| Key pattern changed without coordination | Flask_Dashboards reads empty cache | Expand-contract policy; CI schema validation |
| TTL too aggressive | Frequent cache misses, API overload | Monitoring + alerting on hit ratio |
| Value format drift | Consumer parsing errors | `schema_version` field + contract tests |

## 10. History

| Date | Change | Actor |
| --- | --- | --- |
| 2026-04-17 | Contract boundary created as AECF example | SEACHAD |
