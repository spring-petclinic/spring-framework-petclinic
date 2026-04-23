---
profile_id: requests_http_client
title: Python Requests HTTP Client
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-19
profile_type: library
stack_nodes:
  - requests
requires:
  - python
precedence: 65
fallback_mode: warn_continue
compatibility:
  - python
  - flask
  - aws
  - azure
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=requests
  - keyword=session
  - keyword=base_url
  - library=requests
max_lines_per_section: 6
tags:
  - http
  - api
  - client
---

LAST_REVIEW: 2026-03-19
OWNER SEACHAD

## STACK

The `requests` library is the outbound HTTP client boundary for Python services and scripts. Keep remote-call policy, authentication, retries, timeouts, and response validation explicit.

## ARCHITECTURE RULES

- Centralize outbound HTTP access behind a client or adapter instead of scattering raw `requests` calls.
- Make base URL, auth scheme, and timeout policy configurable outside call sites.
- Separate transport concerns from domain orchestration and response mapping.

## DESIGN PATTERNS

- Dedicated API client modules or adapters per external site or service.
- Reusable `requests.Session` only when lifecycle, headers, and retry behavior are explicit.
- Typed response parsing or validation before data reaches business logic.

## CODING RULES

- Always pass explicit timeouts; do not rely on library defaults.
- Use `raise_for_status()` or equivalent explicit status handling before consuming payloads.
- Avoid building URLs, headers, and auth logic ad hoc across unrelated modules.

## SECURITY RULES

- Keep tokens, cookies, API keys, and credentials outside source code.
- Validate TLS expectations and avoid disabling certificate verification except in tightly controlled test contexts.
- Treat remote responses as untrusted input and validate schema-critical fields.

## TESTING RULES

- Mock or stub outbound HTTP at the client boundary; do not depend on live external sites in routine tests.
- Cover timeout, non-2xx, malformed payload, and retry-sensitive paths.
- Add one non-regression assertion that transport failures do not leak partial state into the domain flow.

## COMMON MISTAKES

- Missing timeout values that can hang worker threads or CLI commands.
- Direct `requests.get()` or `post()` calls scattered across business logic.
- Assuming JSON shape or success status without explicit validation.

## AECF AUDIT CHECKS

- Verify outbound HTTP is centralized behind a client or adapter boundary.
- Verify timeouts, status handling, and response validation are explicit.
- Verify secrets, TLS behavior, and network failure handling follow policy.