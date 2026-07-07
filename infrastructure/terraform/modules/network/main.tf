resource "google_compute_network" "vpc" {
  name                            = "${var.env}-vpc"
  auto_create_subnetworks         = false
  delete_default_routes_on_create = true
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.env}-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
}

resource "google_vpc_access_connector" "connector" {
  name          = "${var.env}-connector"
  region        = var.region
  network       = google_compute_network.vpc.id
  ip_cidr_range = "10.8.0.0/28"
  machine_type  = "e2-micro"
  min_instances = 2
  max_instances = 10
}

variable "project" { type = string }
variable "region" { type = string }
variable "env" { type = string }

output "vpc_id" { value = google_compute_network.vpc.id }
output "connector_id" { value = google_vpc_access_connector.connector.id }
output "subnet_id" { value = google_compute_subnetwork.subnet.id }
