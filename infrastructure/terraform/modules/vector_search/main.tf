resource "google_vertex_ai_index" "targets" {
  provider     = google-beta
  region       = var.region
  display_name = "${var.env}-agente-targets"
  metadata {
    contents_delta_uri = "gs://${var.bucket}/index-delta/"
    config {
      dimensions                  = var.dimensions
      approximate_neighbors_count = 50
      distance_measure_type       = "DOT_PRODUCT_DISTANCE"
      algorithm_config {
        tree_ah_config {
          leaf_node_embedding_count = 500
        }
      }
    }
  }
  index_update_method = "STREAM_UPDATE"
}

resource "google_vertex_ai_index_endpoint" "ep" {
  provider     = google-beta
  region       = var.region
  display_name = "${var.env}-agente-ep"
  public_endpoint_enabled = true
}

resource "google_vertex_ai_index_endpoint_deployed_index" "dep" {
  provider          = google-beta
  index_endpoint    = google_vertex_ai_index_endpoint.ep.id
  index             = google_vertex_ai_index.targets.id
  deployed_index_id = "targets_v1"
}

variable "region" { type = string }
variable "env" { type = string }
variable "dimensions" { type = number }
variable "bucket" { type = string }

output "endpoint_id" { value = google_vertex_ai_index_endpoint.ep.name }
output "deployed_index_id" { value = google_vertex_ai_index_endpoint_deployed_index.dep.deployed_index_id }
