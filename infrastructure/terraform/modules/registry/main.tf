resource "google_artifact_registry_repository" "docker" {
  location      = var.region
  repository_id = "${var.env}-agente-ai-repo"
  description   = "Repositório de imagens para o projeto"
  format        = "DOCKER"
}

variable "project" { type = string }
variable "region" { type = string }
variable "env" { type = string }

output "repository_id" { value = google_artifact_registry_repository.docker.id }
