# ADR-004: Minimal Administrative Panel Authentication and Controlled CORS

- Status: Accepted
- Date: 2026-07-06

## Context
The administrative routes were exposed without any protection, and CORS was broadly enabled, which is not suitable for production environments.

## Decision
Add minimal authentication via the `X-Admin-Token` header for routes under `/admin/*` and restrict allowed origins using the `CORS_ORIGINS` environment variable.

## Consequences
- The administrative panel is protected by default.
- API exposure to browsers becomes more secure.
- The environment can be configured differently for dev, staging, and production.