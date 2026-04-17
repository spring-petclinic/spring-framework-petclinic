---
profile_id: aws_lambda_python
title: Python AWS Lambda Workloads
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: platform
stack_nodes:
  - aws
requires:
  - python
precedence: 70
fallback_mode: warn_continue
compatibility:
  - python
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=lambda
  - keyword=handler
  - path=lambda_function.py
max_lines_per_section: 6
tags:
  - python
  - aws
  - serverless
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

Python on AWS Lambda should be designed around small handlers, event contract clarity, environment-driven configuration, and explicit idempotency.

## ARCHITECTURE RULES

- Keep the Lambda handler as a thin adapter over reusable application logic.
- Separate event parsing, business logic, and AWS SDK integration boundaries.
- Make cold-start-sensitive initialization intentional and minimal.

## DESIGN PATTERNS

- Handler module plus service modules for reusable behavior.
- Explicit event validation before domain processing.
- Idempotent workflows around retried or duplicated events.

## CODING RULES

- Do not bury domain logic directly in the handler function.
- Keep boto3 or AWS-specific integrations behind focused adapters where complexity exists.
- Make timeout, retry, and serialization assumptions explicit.

## SECURITY RULES

- Prefer IAM role permissions over static credentials.
- Review event trust boundaries, secret usage, and public invocation exposure.
- Treat event payloads and environment variables as untrusted input channels.

## TESTING RULES

- Cover handler contract tests separately from internal service tests.
- Test invalid event payloads and retry/idempotency behavior.
- Include one non-regression assertion around AWS integration assumptions or configuration.

## COMMON MISTAKES

- Mixing event parsing, orchestration, and domain logic in one function.
- Treating retries as transparent when side effects are not idempotent.
- Assuming local invocation fully matches cloud event shape and IAM behavior.

## AECF AUDIT CHECKS

- Verify handler thinness and explicit event validation.
- Verify idempotency and retry-sensitive logic are addressed.
- Verify AWS integration code is isolated and testable.