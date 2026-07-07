variable "project" {
  description = "ID do projeto GCP"
  type        = string
}

variable "region" {
  description = "Região da infraestrutura"
  type        = string
}

variable "env" {
  description = "Ambiente (dev/prod)"
  type        = string
}
