terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Optional: Configure backend
# terraform {
#   backend "gcs" {
#     bucket = "terraform-state-bucket"
#     prefix = "terraform/state"
#   }
# }
