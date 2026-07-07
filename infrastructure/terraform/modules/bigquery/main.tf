resource "google_bigquery_dataset" "d" {
  dataset_id = "agente_ai_${var.env}"
  location   = var.region
  description = "Dataset para analytics e feedback"
}

resource "google_bigquery_table" "feedback" {
  dataset_id = google_bigquery_dataset.d.dataset_id
  table_id   = "feedback"

  time_partitioning {
    type = "DAY"
    field = "created_at"
  }

  schema = jsonencode([
    { name = "created_at", type = "TIMESTAMP" },
    { name = "target_id", type = "STRING" },
    { name = "query", type = "STRING" },
    { name = "similarity", type = "FLOAT" },
    { name = "feedback_type", type = "STRING" },
    { name = "user_hash", type = "STRING" }
  ])
}

variable "project" { type = string }
variable "region" { type = string }
variable "env" { type = string }

output "dataset_id" { value = google_bigquery_dataset.d.dataset_id }
