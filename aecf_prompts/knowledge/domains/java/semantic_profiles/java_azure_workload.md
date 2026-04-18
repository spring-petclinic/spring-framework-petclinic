---
profile_id: java_azure_workload
title: Java on Azure Workloads
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: platform
stack_nodes:
  - azure
requires:
  - java
precedence: 65
fallback_mode: warn_continue
compatibility:
  - java
  - spring
  - kubernetes
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=azure
  - keyword=app service
  - keyword=aks
max_lines_per_section: 6
tags:
  - java
  - azure
  - cloud
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

Java on Azure should emphasize environment separation, managed identity, operational observability, and deployment predictability.

## ARCHITECTURE RULES

- Keep Azure SDK and platform bindings behind adapters where business logic must remain portable.
- Separate application configuration from environment and tenant-specific settings.
- Model deployment topology explicitly when using App Service, AKS, or Functions-based workloads.

## DESIGN PATTERNS

- Managed identity or federated identity for service-to-service access.
- IaC-backed provisioning and environment promotion.
- Health, metrics, and logging aligned with Azure monitoring surfaces.

## CODING RULES

- Do not hardcode subscription, tenant, or endpoint assumptions.
- Keep cloud-specific integration code isolated from domain services.
- Make retry, timeout, and resiliency behavior explicit for remote Azure dependencies.

## SECURITY RULES

- Prefer managed identity over embedded connection secrets.
- Review Key Vault, RBAC, network exposure, and tenant boundaries.
- Treat configuration and deployment metadata as sensitive operational inputs.

## TESTING RULES

- Cover cloud adapter behavior with targeted integration tests or contract tests.
- Validate configuration fallback and secret resolution paths.
- Include one explicit non-regression around deployment or identity assumptions.

## COMMON MISTAKES

- Mixing domain logic with Azure SDK calls.
- Assuming local configuration maps directly to production cloud setup.
- Leaving observability as an afterthought instead of part of workload design.

## AECF AUDIT CHECKS

- Verify managed identity and configuration separation are explicit.
- Verify Azure-specific adapters are isolated from domain logic.
- Verify observability and environment assumptions are production-aware.