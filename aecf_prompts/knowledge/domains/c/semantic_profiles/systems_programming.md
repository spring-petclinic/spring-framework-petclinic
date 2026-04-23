---
profile_id: c_systems_programming
title: C Systems Programming (POSIX / Linux / Unix)
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-15
profile_type: framework
stack_nodes:
  - c
requires: []
precedence: 85
fallback_mode: warn_continue
compatibility:
  - c
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=posix
  - keyword=linux kernel
  - keyword=unix
  - keyword=system call
  - keyword=daemon
max_lines_per_section: 6
tags:
  - c
  - systems
  - posix
  - linux
  - unix
---

LAST_REVIEW: 2026-03-15
OWNER SEACHAD

## STACK

C systems programming targets POSIX-compatible environments with explicit system call usage, process/thread management, and resource lifecycle control.

## ARCHITECTURE RULES

- Separate system-level operations (file I/O, sockets, signals) from application logic through abstraction layers.
- Use opaque types and function-pointer-based interfaces for modularity in C.
- Keep signal handlers minimal and async-signal-safe.
- Design process and thread lifecycle explicitly; document resource ownership.
- Prefer composition of small focused modules over monolithic source files.

## DESIGN PATTERNS

- Opaque pointer pattern (PIMPL-like in C) for encapsulation.
- Callback-based event loops for I/O multiplexing (select/poll/epoll).
- Fork/exec with explicit cleanup for process management.
- Thread pool with work queue for concurrent processing.
- Structured error propagation using return codes and errno.

## CODING RULES

- Always check return values of system calls and handle errors explicitly.
- Use `EINTR`-safe wrappers for interruptible system calls.
- Pair every resource acquisition with a documented release path (open/close, malloc/free, lock/unlock).
- Prefer `snprintf` over `sprintf`, `strncat` over `strcat`, and bounded string operations throughout.
- Keep thread synchronization minimal and well-documented; avoid lock-order inversion.

## SECURITY RULES

- Validate all input from external sources (files, sockets, environment variables, command-line arguments).
- Drop unnecessary privileges as early as possible in daemon and setuid programs.
- Review file permissions, temporary file handling, and symbolic link races.
- Use secure coding practices for string handling to prevent buffer overflows.
- Protect against format string vulnerabilities; never pass user input as a format string.

## TESTING RULES

- Test system-interaction code with wrapper functions that can be mocked on host.
- Cover error paths for system calls (ENOMEM, EACCES, EINTR, EPIPE).
- Validate resource cleanup in both success and failure paths.
- Use ASan and UBSan in CI test builds.
- Include one regression test for signal handling or concurrency behavior.

## COMMON MISTAKES

- Ignoring return values from read(), write(), close(), and other system calls.
- Using unsafe string functions leading to buffer overflows.
- Leaking file descriptors or memory in error paths.
- Assuming signal-handler-safe behavior in functions that are not async-signal-safe.
- Creating race conditions with shared state between threads without proper synchronization.

## AECF AUDIT CHECKS

- Verify all system call return values are checked and errors are handled.
- Verify bounded string operations are used throughout.
- Verify resource cleanup occurs in both success and error paths.
- Verify privileges are dropped appropriately in privileged programs.
- Verify tests cover error paths and resource cleanup scenarios.
