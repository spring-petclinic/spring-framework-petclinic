---
profile_id: java_aws_workload
title: Java on AWS Workloads
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: platform
stack_nodes:
  - aws
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
  - keyword=aws
  - keyword=lambda
  - keyword=ecs
  - keyword=eks
max_lines_per_section: 6
tags:
  - java
  - aws
  - cloud
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

Java on AWS should emphasize account separation, IAM discipline, observable integrations, and deployment reproducibility across managed services.

## ARCHITECTURE RULES

- Keep AWS service clients and event integrations behind infrastructure adapters.
- Separate runtime workload assumptions for Lambda, ECS, EKS, and EC2-based hosting.
- Make account, region, and environment boundaries explicit in configuration.

## DESIGN PATTERNS

- IAM role-based access instead of static credentials.
- Infrastructure as code and repeatable environment promotion.
- Event-driven integrations with explicit retry and failure semantics.

## CODING RULES

- Do not leak AWS-specific SDK types into core domain contracts.
- Keep timeout, retry, and idempotency choices explicit around remote calls.
- Avoid configuration sprawl spread across code and deployment descriptors.

## SECURITY RULES

- Prefer IAM roles and short-lived credentials.
- Review KMS, Secrets Manager, network exposure, and public surface area.
- Treat event payloads and cloud metadata as untrusted inputs.

## TESTING RULES

- Cover adapter contracts for the AWS services that matter to the workload.
- Validate fallback behavior when cloud configuration is incomplete or invalid.
- Include non-regression around IAM or event contract assumptions.

## COMMON MISTAKES

- Embedding account and environment logic directly into application services.
- Treating retry behavior as infrastructure-only and not a business concern.
- Assuming local mocks represent production IAM and network conditions accurately.

## AECF AUDIT CHECKS

- Verify IAM-based access and environment separation are explicit.
- Verify AWS adapter logic is isolated from domain flows.
- Verify event, retry, and observability assumptions are documented and testable.