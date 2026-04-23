# AECF_SURFACES_INDEX

## METADATA

| Field | Value |
| --- | --- |
| LAST_REVIEW | {{date}} |
| Owner | {{owner}} |
| Version | 1.0 |
| Allow multiple surfaces | Yes / No |
| Require primary surface | Yes / No |
| Human decision required for new surfaces | Yes / No |

## 1. Purpose

-

## 2. Selection Policy

| Rule | Value |
| --- | --- |
| Fallback to global only | Yes / No |
| Max recommended active surfaces | |
| Human confirmation required when ambiguous | Yes / No |

## 3. Surface Summary

| Surface ID | Type | Summary | Main Paths | Related Surfaces | Risk Level | Owners |
| --- | --- | --- | --- | --- | --- | --- |
| | business_surface / technical_surface | | | | low / medium / high | |

## 4. Selection Heuristics

1.
2.
3.

## 4.1 Human Confirmation Workflow

1. Proposed by IA:
2. Reviewed by human:
3. Human actions: accept / rename / merge / split / delete / add

## 5. Cross-Surface Dependencies

| Surface | Depends On | Dependency Type | Reason |
| --- | --- | --- | --- |
| | | technical / business / mixed | |

## 6. Multi-Surface Activation Rules

1.
2.
3.

## 7. Naming and Boundary Notes

1. Surface names should reflect a stable business or technical responsibility.
2. Do not create one surface per folder unless that folder is already a real operational boundary.
3. Prefer a small reusable set over many narrow one-off surfaces.

## Recommended JSON Contract

```json
{
  "version": "1.0",
  "generated_at": "{{timestamp_utc}}",
  "selection_policy": {
    "allow_multiple_surfaces": true,
    "require_primary_surface": true,
    "fallback_to_global_only": true,
    "max_recommended_active_surfaces": 3
  },
  "surfaces": [
    {
      "surface_id": "example_surface",
      "surface_type": "business_surface",
      "summary": "",
      "paths": [],
      "keywords": [],
      "upstream_dependencies": [],
      "related_surfaces": [],
      "owners": [],
      "risk_level": "medium"
    }
  ]
}
```
