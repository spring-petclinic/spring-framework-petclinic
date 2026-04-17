---
profile_id: efcore_data
title: Entity Framework Core Data Access
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-16
profile_type: framework
stack_nodes:
  - csharp
  - dotnet
requires:
  - csharp
precedence: 85
fallback_mode: warn_continue
compatibility:
  - csharp
  - dotnet
conflicts_with: []
activation_mode: explicit_or_detected
evidence_hint:
  - keyword=entity framework
  - keyword=efcore
  - keyword=dbcontext
  - keyword=migration
  - keyword=DbSet
max_lines_per_section: 6
tags:
  - csharp
  - dotnet
  - efcore
  - orm
  - database
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## STACK

Entity Framework Core is the primary ORM for .NET, providing DbContext-based data access, code-first or database-first modeling, LINQ-based queries, change tracking, and migration management.

## ARCHITECTURE RULES

- Keep `DbContext` scoped to the unit of work; do not share across threads or long-lived services.
- Define entity configurations in separate `IEntityTypeConfiguration<T>` classes, not inline in `OnModelCreating`.
- Use repository or data-access abstractions to keep EF-specific code out of domain/application services.
- Treat migrations as versioned schema artifacts; review generated SQL before applying.
- Separate read-optimized queries (projections, no-tracking) from write paths with change tracking.

## DESIGN PATTERNS

- Repository pattern or thin data-access adapter around `DbContext`.
- Specification pattern for composable query filters.
- No-tracking queries (`AsNoTracking()`) for read-only data retrieval.
- Explicit loading or split queries for complex navigations to control SQL generation.
- Owned entity types for value objects embedded in aggregate tables.

## CODING RULES

- Use strongly-typed entity IDs (value objects or typed wrappers) when practical.
- Avoid `Include` chains deeper than two levels; prefer explicit joins or projections.
- Use `AsSplitQuery()` when loading multiple collections to avoid cartesian explosion.
- Never call `SaveChanges()` inside a loop; batch changes and save once.
- Configure cascade delete behavior explicitly; do not rely on convention defaults.

## SECURITY RULES

- Always use parameterized queries; never concatenate user input into raw SQL.
- Protect connection strings in configuration — use environment variables or Key Vault.
- Review migration scripts for unintended data exposure or destructive schema changes.
- Apply row-level filtering with global query filters for multi-tenant scenarios.

## TESTING RULES

- Use an in-memory provider or SQLite in-memory for fast unit tests of data-access logic.
- Test migration scripts against a real database in CI to catch provider-specific issues.
- Verify query behavior (filtering, paging, ordering) with deterministic seed data.
- Test concurrent update scenarios and optimistic concurrency handling.
- Keep test database state isolated per test with transactions or fresh databases.

## COMMON MISTAKES

- Using `DbContext` as a singleton, causing thread-safety and stale-data issues.
- Ignoring lazy-loading pitfalls and N+1 query problems.
- Not reviewing generated SQL for performance-critical queries.
- Calling `SaveChanges` multiple times in a single logical operation.
- Missing index definitions for frequently filtered or joined columns.

## AECF AUDIT CHECKS

- Verify `DbContext` lifetime is scoped, not singleton.
- Verify entity configurations are in dedicated configuration classes.
- Verify raw SQL uses parameterized queries, never string concatenation.
- Verify migrations are reviewed and tested against the target database provider.
- Verify read paths use no-tracking queries where appropriate.
