resource "google_storage_bucket" "docs" {
  name                        = "${var.project}-docs-${var.env}"
  location                    = var.region
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 90
    }
  }
}

resource "google_storage_bucket" "tfstate" {
  name                        = "${var.project}-tfstate"
  location                    = var.region
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "index" {
  name                        = "${var.project}-index-${var.env}"
  location                    = var.region
  uniform_bucket_level_access = true
}

variable "project" { type = string }
variable "region" { type = string }
variable "env" { type = string }

output "docs_bucket" { value = google_storage_bucket.docs.name }
output "index_bucket" { value = google_storage_bucket.index.name }
output "tfstate_bucket" { value = google_storage_bucket.tfstate.name }
