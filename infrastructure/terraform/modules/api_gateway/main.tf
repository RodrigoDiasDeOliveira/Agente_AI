resource "google_api_gateway_api" "api" {
  api_id  = "agente-ai-api"
  project = var.project
}

resource "google_api_gateway_api_config" "config" {
  api          = google_api_gateway_api.api.api_id
  api_config_id = "agente-ai-config-${var.env}"

  openapi_documents {
    document {
      path     = "spec.yaml"
      contents = base64encode(file("${path.module}/spec.yaml"))
    }
  }
}

resource "google_api_gateway_gateway" "gw" {
  api_config = google_api_gateway_api_config.config.id
  gateway_id = "agente-ai-gw"
  region     = var.region
}

variable "project" { type = string }
variable "env" { type = string }
variable "region" { type = string }

output "gateway_id" { value = google_api_gateway_gateway.gw.id }
