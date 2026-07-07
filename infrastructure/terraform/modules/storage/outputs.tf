output "docs_bucket" {
  value = google_storage_bucket.docs.name
}

output "index_bucket" {
  value = google_storage_bucket.index.name
}

output "tfstate_bucket" {
  value = google_storage_bucket.tfstate.name
}
