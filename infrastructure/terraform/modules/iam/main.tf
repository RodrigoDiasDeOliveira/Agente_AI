resource "google_iam_workload_identity_pool" "gh" {
  workload_identity_pool_id = "github-pool"
}

resource "google_iam_workload_identity_pool_provider" "gh" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.gh.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
  }
  attribute_condition = "assertion.repository == '${var.github_repo}'"
}

resource "google_service_account" "deployer" {
  account_id   = "gh-deployer"
  display_name = "Service account para deploy via GitHub Actions"
}

resource "google_service_account_iam_member" "wif_bind" {
  service_account_id = google_service_account.deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.gh.name}/attribute.repository/${var.github_repo}"
}

resource "google_project_iam_member" "roles" {
  for_each = toset([
    "roles/run.admin",
    "roles/artifactregistry.writer",
    "roles/iam.serviceAccountUser"
  ])
  project = var.project
  role    = each.value
  member  = "serviceAccount:${google_service_account.deployer.email}"
}

resource "google_service_account" "api" {
  account_id   = "agente-ai-api"
  display_name = "Service account da API"
}

resource "google_service_account" "web" {
  account_id   = "agente-ai-web"
  display_name = "Service account do frontend"
}

variable "project" { type = string }
variable "github_repo" { type = string }

output "api_sa_email" { value = google_service_account.api.email }
output "web_sa_email" { value = google_service_account.web.email }
