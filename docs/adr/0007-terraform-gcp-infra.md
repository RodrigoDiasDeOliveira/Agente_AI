# ADR-007: Adoption of Terraform for GCP Infrastructure

## Status
Accepted (2026-07)

## Context
The Agente_AI project currently uses Docker Compose for local development but lacks reproducible, versioned, and secure infrastructure definition for cloud environments (dev/prod).

## Decision
Adopt **Terraform** as the Infrastructure as Code (IaC) tool to provision all infrastructure on Google Cloud Platform.

## Considered Options
1. Terraform (chosen)
2. Pulumi / Crossplane
3. Only gcloud + Cloud Build scripts
4. Manual provisioning

## Rationale
- Terraform is the de-facto standard in GCP consultancies (including Devoteam).
- Excellent support for Vertex AI, Cloud Run, Vector Search, etc.
- Strong multi-environment support.
- Native integration with Workload Identity Federation (no service account keys in GitHub).
- Remote state with versioning in GCS.

## Consequences
**Positive:**
- Fully versioned and auditable infrastructure.
- Consistent environments across dev/prod.
- Secure CI/CD with manual approval in production.
- Strong differentiator in technical interviews.

**Negative / Mitigations:**
- Initial learning curve → mitigated with reusable modules.
- State management → solved with GCS backend + locking.

## Implementation Details
- Structure: `infrastructure/terraform/envs/{dev,prod}` + reusable `modules/`
- Workload Identity Federation for GitHub Actions
- `deletion_protection = true` on critical resources
- Secrets managed via Secret Manager

## References
- Google Cloud Terraform Best Practices
- HashiCorp Google Terraform Provider