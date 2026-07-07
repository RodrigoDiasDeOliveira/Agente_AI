# Deployment on Google Cloud Platform

This document describes the recommended workflow to deploy the Agente AI project on GCP using Terraform, Cloud Run, Secret Manager, BigQuery, and Vertex AI.

## 1. Prerequisites

- Google Cloud account with billing enabled
- GCP project created
- gcloud CLI installed and authenticated
- Terraform >= 1.6
- GCS bucket for remote state with versioning enabled

## 2. Create Project and Enable Billing

```bash
gcloud projects create agente-ai-prod --name="Agente AI"
gcloud beta billing projects link agente-ai-prod --billing-account=XXXX

3. Create Bucket for Remote State
Bashgsutil mb -l southamerica-east1 gs://agente-ai-tfstate
gsutil versioning set on gs://agente-ai-tfstate

4. Enable Minimum APIs
Bashgcloud services enable \
  cloudresourcemanager.googleapis.com \
  serviceusage.googleapis.com \
  iam.googleapis.com \
  run.googleapis.com \
  aiplatform.googleapis.com \
  sqladmin.googleapis.com \
  secretmanager.googleapis.com \
  artifactregistry.googleapis.com \
  bigquery.googleapis.com \
  eventarc.googleapis.com \
  cloudbuild.googleapis.com \
  vpcaccess.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com \
  apigateway.googleapis.com \
  iap.googleapis.com \
  dlp.googleapis.com \
  --project=agente-ai-prod

5. Authentication for First Apply
Bashgcloud auth application-default login
6. Terraform
Dev
Bashcd infrastructure/terraform/envs/dev
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
Prod
Bashcd infrastructure/terraform/envs/prod
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
7. Secrets
Create secret versions manually after the first apply, for example:
Bashgcloud secrets versions add db-password-dev --data-file=/path/to/password
8. CI/CD
The repository already includes workflows for:

Validating Terraform on Pull Requests
Applying Terraform with approval via GitHub Environments

9. Notes

The remote state should never be local; always use GCS with versioning enabled.
Container images must be built and published by the CI/CD pipeline.
Application data and sensitive information must be kept outside of the Terraform state.