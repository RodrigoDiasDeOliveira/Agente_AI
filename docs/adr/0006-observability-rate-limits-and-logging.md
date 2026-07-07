# ADR-006: Observability, Rate Limiting, and Basic Logging

- Status: Accepted
- Date: 2026-07-06

## Context
The API needed operational visibility to debug requests and protect endpoints against abuse, without relying on complex external dependencies.

## Decision
Add simple request logging, expose basic metrics at `/metrics` endpoint, and implement basic rate limiting by IP for the main endpoints.

## Consequences
- The API operation becomes more observable.
- The system is more resilient to traffic spikes and abusive usage.
- The foundation is ready to evolve into a more complete observability solution.