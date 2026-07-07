# Deployment no Google Cloud Platform

Este documento descreve o fluxo recomendado para implantar o projeto Agente AI no GCP usando Terraform, Cloud Run, Secret Manager, BigQuery e Vertex AI.

## 1. Pré-requisitos

- Conta Google Cloud com billing habilitado
- Projeto GCP criado
- gcloud instalado e autenticado
- Terraform >= 1.6
- Bucket GCS para o estado remoto com versionamento habilitado

## 2. Criar projeto e habilitar billing

```bash
gcloud projects create agente-ai-prod --name="Agente AI"
gcloud beta billing projects link agente-ai-prod --billing-account=XXXX
```

## 3. Criar bucket para o state remoto

```bash
gsutil mb -l southamerica-east1 gs://agente-ai-tfstate
gsutil versioning set on gs://agente-ai-tfstate
```

## 4. Habilitar APIs mínimas

```bash
gcloud services enable \
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
```

## 5. Autenticação para o primeiro apply

```bash
gcloud auth application-default login
```

## 6. Terraform

### Dev

```bash
cd infrastructure/terraform/envs/dev
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

### Prod

```bash
cd infrastructure/terraform/envs/prod
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

## 7. Secrets

Crie as versões dos secrets manualmente após o primeiro apply, por exemplo:

```bash
gcloud secrets versions add db-password-dev --data-file=/path/to/password
```

## 8. CI/CD

O repositório já possui workflows para:
- validar Terraform em PR
- aplicar Terraform com approval via GitHub Environment

## 9. Observações

- O state remoto nunca deve ficar local; sempre use GCS com versionamento.
- Imagens de container devem ser construídas e publicadas pelo CI/CD.
- Dados da aplicação e informações sensíveis devem ser mantidos fora do state do Terraform.
