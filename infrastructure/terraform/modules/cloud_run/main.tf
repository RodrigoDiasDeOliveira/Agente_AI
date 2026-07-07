resource "google_cloud_run_v2_service" "svc" {
  name     = var.name
  location = var.region
  template {
    service_account = var.service_account
    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }
    dynamic "vpc_access" {
      for_each = var.vpc_connector == null ? [] : [1]
      content {
        connector = var.vpc_connector
        egress    = "PRIVATE_RANGES_ONLY"
      }
    }
    containers {
      image = var.image
      resources {
        limits = {
          cpu    = "1"
          memory = "1Gi"
        }
      }
      dynamic "env" {
        for_each = var.env
        content {
          name  = env.key
          value = env.value
        }
      }
      dynamic "env" {
        for_each = var.secrets
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value
              version = "latest"
            }
          }
        }
      }
    }
    dynamic "volumes" {
      for_each = var.cloudsql_instance == null ? [] : [1]
      content {
        name = "cloudsql"
        cloud_sql_instance {
          instances = [var.cloudsql_instance]
        }
      }
    }
  }
}

variable "name" { type = string }
variable "region" { type = string }
variable "image" { type = string }
variable "service_account" { type = string }
variable "vpc_connector" { type = string, default = null }
variable "cloudsql_instance" { type = string, default = null }
variable "secrets" { type = map(string), default = {} }
variable "env" { type = map(string), default = {} }

output "url" { value = google_cloud_run_v2_service.svc.uri }
output "name" { value = google_cloud_run_v2_service.svc.name }
