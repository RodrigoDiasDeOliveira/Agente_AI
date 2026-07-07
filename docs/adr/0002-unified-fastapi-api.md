# ADR-002: Unified FastAPI Application with Standardized Endpoint

- Status: Accepted
- Date: 2026-07-06

## Context
The repository maintained two separate FastAPI apps, and the frontend expected a different endpoint from the backend, causing integration inconsistency.

## Decision
Unify the main API by mounting the admin under the same app and standardize the query endpoint at `/api/ask`, keeping `/api/query` as a compatible alias.

## Consequences
- The backend exposes a more consistent interface for the frontend and external clients.
- Administrative routes are now available under `/admin`.
- Compatibility with legacy integrations is preserved.