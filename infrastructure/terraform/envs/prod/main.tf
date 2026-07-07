terraform {
  required_version = ">= 1.6"

  required_providers {
    google      = { source = "hashicorp/google",      version = "~> 6.0" }
    google-beta = { source = "hashicorp/google-beta", version = "~> 6.0" }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "ID do projeto GCP"
  type        = string
  default     = "agente-ai-prod"
}

variable "region" {
  description = "Região principal da infraestrutura"
  type        = string
  default     = "southamerica-east1"
}

variable "env" {
  description = "Nome do ambiente"
  type        = string
  default     = "prod"
}

variable "github_repo" {
  description = "Repositório GitHub para Workload Identity Federation"
  type        = string
  default     = "RodrigoDiasDeOliveira/Agente_AI"
}

variable "backend_image" {
  description = "Imagem do backend para Cloud Run"
  type        = string
  default     = "southamerica-east1-docker.pkg.dev/agente-ai-prod/agente-ai/api:latest"
}

variable "web_image" {
  description = "Imagem do frontend para Cloud Run"
  type        = string
  default     = "southamerica-east1-docker.pkg.dev/agente-ai-prod/agente-ai/web:latest"
}

variable "ingest_image" {
  description = "Imagem do job de ingestão"
  type        = string
  default     = "southamerica-east1-docker.pkg.dev/agente-ai-prod/agente-ai/ingest:latest"
}

variable "notification_email" {
  description = "E-mail para notificações de alertas"
  type        = string
  default     = "seuemail@empresa.com"
}

locals {
  project = var.project_id
  region  = var.region
  env     = var.env
}

resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "aiplatform.googleapis.com",
    "sqladmin.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "bigquery.googleapis.com",
    "eventarc.googleapis.com",
    "cloudbuild.googleapis.com",
    "vpcaccess.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
    "apigateway.googleapis.com",
    "iap.googleapis.com",
    "dlp.googleapis.com",
  ])

  service            = each.value
  disable_on_destroy = false
}

module "network" {
  source  = "../../modules/network"
  project = local.project
  region  = local.region
  env     = local.env
}

module "registry" {
  source  = "../../modules/registry"
  project = local.project
  region  = local.region
  env     = local.env
}

module "storage" {
  source  = "../../modules/storage"
  project = local.project
  region  = local.region
  env     = local.env
}

module "bigquery" {
  source  = "../../modules/bigquery"
  region  = local.region
  env     = local.env
  project = local.project
}

module "secrets" {
  source  = "../../modules/secrets"
  project = local.project
  env     = local.env
}

module "iam" {
  source      = "../../modules/iam"
  project     = local.project
  github_repo = var.github_repo
}

module "database" {
  source          = "../../modules/database"
  region          = local.region
  private_network = module.network.vpc_id
  db_password_id  = module.secrets.db_password_id
}

module "vector_search" {
  source     = "../../modules/vector_search"
  region     = local.region
  env        = local.env
  dimensions = 768
  bucket     = module.storage.index_bucket
}

module "cloud_run_api" {
  source          = "../../modules/cloud_run"
  name            = "agente-ai-api"
  region          = local.region
  image           = var.backend_image
  service_account = module.iam.api_sa_email
  vpc_connector   = module.network.connector_id
  cloudsql_instance = module.database.connection_name
  secrets = {
    DATABASE_URL = module.secrets.db_url_id
    ADMIN_TOKEN  = module.secrets.admin_token_id
  }
  env = {
    GCP_PROJECT    = local.project
    GCP_REGION     = local.region
    VS_ENDPOINT_ID = module.vector_search.endpoint_id
    VS_DEPLOYED_ID = module.vector_search.deployed_index_id
    LLM_PROVIDER   = "vertex"
    BQ_DATASET     = module.bigquery.dataset_id
  }
}

module "cloud_run_web" {
  source          = "../../modules/cloud_run"
  name            = "agente-ai-web"
  region          = local.region
  image           = var.web_image
  service_account = module.iam.web_sa_email
  env = {
    VITE_AGENT_API_URL = module.cloud_run_api.url
  }
}

module "eventarc" {
  source         = "../../modules/eventarc"
  bucket         = module.storage.docs_bucket
  ingest_job     = "agente-ai-ingest"
  ingest_image   = var.ingest_image
  region         = local.region
  env            = local.env
  service_account = module.iam.api_sa_email
}

module "monitoring" {
  source             = "../../modules/monitoring"
  api_service        = module.cloud_run_api.name
  notification_email = var.notification_email
  region             = local.region
  env                = local.env
}

module "api_gateway" {
  source  = "../../modules/api_gateway"
  project = local.project
  region  = local.region
  env     = local.env
}
