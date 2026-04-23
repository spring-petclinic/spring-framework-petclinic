---
profile_id: spring_boot_service
title: Spring Boot Service
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-14
profile_type: framework
stack_nodes:
  - spring
requires:
  - java
precedence: 90
fallback_mode: warn_continue
compatibility:
  - java
  - jpa
  - kafka
  - microservices
  - azure
  - aws
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=@springbootapplication
  - keyword=spring boot
  - manifest=pom.xml
  - manifest=build.gradle
max_lines_per_section: 6
tags:
  - java
  - spring
  - service
---

LAST_REVIEW: 2026-03-14
OWNER SEACHAD

## STACK

Spring Boot should be treated as an opinionated service runtime for production-grade Java applications with explicit configuration and operational endpoints.

## ARCHITECTURE RULES

- Keep controllers, application services, domain logic, and infrastructure clearly separated.
- Prefer constructor injection and explicit configuration over hidden framework magic.
- Keep externalized configuration and health/metrics endpoints intentional.

## DESIGN PATTERNS

- Thin REST controllers delegating to application services.
- Configuration properties objects for typed settings.
- Module boundaries aligned with bounded contexts, not with technical layers only.

## CODING RULES

- Avoid business logic inside controllers or transport DTOs.
- Keep startup wiring clear and avoid broad component scanning surprises.
- Do not mix blocking and asynchronous integration styles without explicit boundaries.

## SECURITY RULES

- Make authentication, authorization, and secret sourcing explicit.
- Review actuator exposure and management endpoints before production rollout.
- Do not assume starter dependencies enforce complete security by themselves.

## TESTING RULES

- Cover controller contract tests separately from service behavior.
- Prefer focused slice tests before broad full-context integration tests.
- Include negative-path validation and security behavior where endpoints mutate state.

## COMMON MISTAKES

- Fat service classes that mix orchestration, domain logic, and persistence.
- Over-reliance on framework defaults without explicit operational review.
- Expanding the dependency tree with starters that are not actually needed.

## AECF AUDIT CHECKS

- Verify controller-to-service separation and explicit configuration ownership.
- Verify actuator, config, and dependency choices are production-aware.
- Verify tests cover both success and failure contracts.