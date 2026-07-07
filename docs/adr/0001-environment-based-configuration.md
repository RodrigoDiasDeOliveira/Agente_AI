# ADR-001: Environment Variables Based Configuration

- Status: Accepted
- Date: 2026-07-06

## Context
The project relied on hardcoded absolute paths and fixed values in the code, which broke execution in environments different from the original Codespaces.

## Decision
Centralize configuration using environment variables with safe defaults. The configuration module now reads values such as `DATABASE_URL`, `DOCS_PATH`, `CORS_ORIGINS`, `ADMIN_API_TOKEN`, and `LLM_PROVIDER`.

## Consequences
- The project becomes more portable.
- Onboarding is simpler across local, Docker, and CI environments.
- Runtime configuration is explicit and documented in the example `.env` file.