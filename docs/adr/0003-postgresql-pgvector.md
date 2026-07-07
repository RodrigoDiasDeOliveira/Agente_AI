# ADR-003: Use of PostgreSQL with pgvector

- Status: Accepted
- Date: 2026-07-06

## Context
The project needed a database prepared for semantic vector search, but the initial migration only created tables without enabling the necessary extension.

## Decision
Adopt PostgreSQL + pgvector as the main backend and enable the `vector` extension during database initialization via migration.

## Consequences
- Vector search is now supported natively.
- Both development and production environments have a foundation better aligned with semantic retrieval workflows.
- The configuration requires a database compatible with pgvector.