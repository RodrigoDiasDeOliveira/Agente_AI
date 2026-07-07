resource "google_eventarc_trigger" "ingest" {
  name     = "${var.ingest_job}-trigger"
  location = var.region

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.storage.object.finalize"
  }

  destination {
    cloud_run_service {
      service = var.ingest_job
      region  = var.region
    }
  }

  transport {
    pubsub {}
  }

  service_account = var.service_account
}

resource "google_cloud_run_v2_job" "ingest" {
  name     = var.ingest_job
  location = var.region
  template {
    template {
      containers {
        image = var.ingest_image
      }
    }
  }
}

variable "bucket" { type = string }
variable "ingest_job" { type = string }
variable "ingest_image" { type = string }
variable "region" { type = string }
variable "env" { type = string }
variable "service_account" { type = string }

output "ingest_bucket" { value = var.bucket }
