variable "bucket" {
  description = "Nome do bucket de documentos"
  type        = string
}

variable "ingest_job" {
  description = "Nome do Cloud Run Job de ingestão"
  type        = string
}

variable "ingest_image" {
  description = "Imagem do Cloud Run Job"
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

variable "service_account" {
  description = "Service account usada pelo trigger"
  type        = string
}
