terraform {
  required_version = ">= 1.6"

  backend "gcs" {
    bucket = "agente-ai-tfstate"
    prefix = "dev"
  }

  required_providers {
    google      = { source = "hashicorp/google",      version = "~> 6.0" }
    google-beta = { source = "hashicorp/google-beta", version = "~> 6.0" }
  }
}
