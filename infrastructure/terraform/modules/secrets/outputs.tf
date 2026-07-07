output "db_password_id" {
  value = google_secret_manager_secret.db_password.id
}

output "db_url_id" {
  value = google_secret_manager_secret.db_url.id
}

output "admin_token_id" {
  value = google_secret_manager_secret.admin_token.id
}
