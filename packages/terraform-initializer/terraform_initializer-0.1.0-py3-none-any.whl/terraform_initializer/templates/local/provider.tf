terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# Local provider doesn't require any configuration
# It's used for local file operations and testing

# Optional: Configure backend
# terraform {
#   backend "local" {
#     path = "terraform.tfstate"
#   }
# }