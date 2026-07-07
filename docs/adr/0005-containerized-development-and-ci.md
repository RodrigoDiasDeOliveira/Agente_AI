# ADR-005: Containerized Stack with Docker Compose and CI

- Status: Accepted
- Date: 2026-07-06

## Context
The project lacked a consistent onboarding flow for local development and automated validation in CI.

## Decision
Add Dockerfile, Docker Compose with services for database, API, and frontend, plus a GitHub Actions workflow to run tests and build the frontend.

## Consequences
- Project setup becomes simpler and more reproducible.
- Onboarding experience improves for new developers.
- Changes go through automatic validation on every push or pull request.