resource "google_sql_database_instance" "pg" {
  name             = "agente-pg"
  database_version = "POSTGRES_16"
  region           = var.region

  settings {
    tier              = "db-custom-2-4096"
    availability_type = "REGIONAL"
    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
    }
    ip_configuration {
      ipv4_enabled    = false
      private_network = var.private_network
    }
    database_flags {
      name  = "cloudsql.enable_pgvector"
      value = "on"
    }
  }

  deletion_protection = true
}

resource "google_sql_database" "app" {
  name     = "agente"
  instance = google_sql_database_instance.pg.name
}

resource "google_sql_user" "app" {
  name     = "appuser"
  instance = google_sql_database_instance.pg.name
  password = "changeme"
}

variable "region" { type = string }
variable "private_network" { type = string }
variable "db_password_id" { type = string }

output "connection_name" { value = google_sql_database_instance.pg.connection_name }
