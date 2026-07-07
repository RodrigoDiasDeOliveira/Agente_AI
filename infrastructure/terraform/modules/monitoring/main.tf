resource "google_monitoring_notification_channel" "email" {
  display_name = "Ops email"
  type         = "email"
  labels = {
    email_address = var.notification_email
  }
}

resource "google_monitoring_alert_policy" "latency" {
  display_name = "API p95 > 2s"
  combiner     = "OR"
  conditions {
    display_name = "p95 latency"
    condition_threshold {
      filter          = "resource.type=\"cloud_run_revision\" AND resource.label.service_name=\"${var.api_service}\" AND metric.type=\"run.googleapis.com/request_latencies\""
      comparison      = "COMPARISON_GT"
      threshold_value = 2000
      duration        = "300s"
      aggregations {
        alignment_period = "60s"
        per_series_aligner = "ALIGN_PERCENTILE_95"
      }
    }
  }
  notification_channels = [google_monitoring_notification_channel.email.id]
}

variable "api_service" { type = string }
variable "notification_email" { type = string }
variable "region" { type = string }
variable "env" { type = string }

output "alert_policy_id" { value = google_monitoring_alert_policy.latency.id }
