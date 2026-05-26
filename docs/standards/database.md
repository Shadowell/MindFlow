# Database Design Standard

## Purpose

Use this standard when designing schemas, migrations, indexes, constraints, or data-access patterns. The default posture is: model the business truth clearly, enforce integrity where it matters, and scale the design only when the project scale justifies it.

## Source Baseline

- [Microsoft: Database design basics](https://support.microsoft.com/en-us/office/database-design-basics-eb2159cf-1e30-401a-8084-bd4f9c9ca1f5)
- [Microsoft Learn: database normalization basics](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description)
- [PostgreSQL documentation: constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL documentation: indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL documentation: performance tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [OWASP: SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

## Universal Rules

1. Start from the product workflow and data ownership, not from a fashionable architecture.
2. Define entities, relationships, primary keys, required fields, and business constraints before optimizing.
3. Prefer normalized OLTP schemas for transactional systems. Denormalize only with a documented read or performance reason.
4. Use foreign keys, unique constraints, not-null constraints, and check constraints when they protect business correctness.
5. Add indexes for known query patterns, uniqueness, joins, and ordering needs. Do not add speculative indexes.
6. Every non-obvious index must have a short reason: the query, join, filter, or ordering it supports.
7. Keep migrations reviewable and reversible when feasible. If rollback is unsafe, document the recovery plan.
8. Never build SQL through string concatenation with untrusted input. Use parameterized queries or the selected framework's safe query API.
9. Do not introduce sharding, read replicas, CQRS, event sourcing, data warehouses, or cache-as-source-of-truth without explicit project need and user approval.

## Scale-Based Design

### Small Project or MVP

Use this level for prototypes, internal tools, early SaaS products, or projects without proven load.

- Model only the current core workflow.
- Use a small number of clear tables.
- Add primary keys, required fields, unique constraints, and foreign keys for core relationships.
- Add indexes only for actual lookup paths, unique constraints, and obvious foreign-key joins.
- Prefer simple migrations and clear naming over advanced database features.

Avoid:

- Premature table partitioning.
- Generic metadata tables for unknown future features.
- Read/write splitting.
- Event sourcing.
- Multiple databases for one bounded workflow.

### Medium Project

Use this level when the project has multiple user roles, recurring reporting needs, background jobs, or measurable growth.

- Maintain an ERD or schema relationship note for core tables.
- Document ownership for shared tables and important write paths.
- Add constraints for cross-field business invariants where the database can enforce them safely.
- Review indexes against actual queries.
- Use `EXPLAIN` or equivalent planner output before adding complex indexes for performance.
- Separate transactional tables from reporting projections when reporting starts to distort OLTP design.

Avoid:

- Adding indexes without a query.
- Reusing one overloaded table for unrelated entity types.
- Introducing asynchronous projections without documenting freshness expectations.

### Large Project

Use this level when the project has high traffic, large tables, strict uptime needs, multiple teams, or regulated data.

- Record capacity assumptions: row counts, write rate, read patterns, retention, and recovery expectations.
- Use `EXPLAIN ANALYZE`, slow query logs, or production-like benchmarks before structural performance changes.
- Consider partitioning, archival, materialized views, read models, or denormalization only with evidence.
- Document operational impact for migrations that rewrite large tables, lock hot paths, or backfill data.
- Define retention, backup, restore, and privacy requirements explicitly.

Avoid:

- Treating large-system patterns as defaults.
- Denormalizing before identifying the exact query and consistency trade-off.
- Creating irreversible migrations without a tested recovery path.

## Naming

- Use stable, descriptive table names based on domain concepts.
- Use consistent primary key naming within a project.
- Name foreign keys and indexes clearly enough to diagnose errors.
- Avoid abbreviations unless they are standard in the domain.

## Verification

Database changes should be checked through the selected migration tool and, where relevant, query planner evidence. At minimum, record:

- Migration command and result.
- Affected tables.
- New constraints and indexes.
- Manual or automated checks for the main workflow.
