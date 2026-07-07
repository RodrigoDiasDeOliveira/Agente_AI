resource "google_secret_manager_secret" "db_password" {
  secret_id = "db-password-${var.env}"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "db_url" {
  secret_id = "db-url-${var.env}"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "admin_token" {
  secret_id = "admin-token-${var.env}"
  replication {
    auto {}
  }
}

variable "project" { type = string }
variable "env" { type = string }

output "db_password_id" { value = google_secret_manager_secret.db_password.id }
output "db_url_id" { value = google_secret_manager_secret.db_url.id }
output "admin_token_id" { value = google_secret_manager_secret.admin_token.id }
