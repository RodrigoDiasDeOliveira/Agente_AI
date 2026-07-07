# ADR-008: Separation of Docker (Local) and Terraform (Cloud)

## Status
Accepted (2026-07)

## Decision
- Keep `docker-compose.yml` and Dockerfile for local development.
- Use Terraform exclusively for cloud (GCP) infrastructure.

## Rationale
- Docker Compose is fast and lightweight for local development and testing.
- Terraform provides production-grade control, reproducibility, and best practices for GCP.
- Clear separation of concerns improves maintainability.

## Consequences
- Local environment remains simple (`docker-compose up`).
- Production uses Cloud Run + managed services.
- Dockerfile optimized for Cloud Run (multi-stage, non-root user).
- CI/CD pipelines are clearly separated (image build vs. infra apply).