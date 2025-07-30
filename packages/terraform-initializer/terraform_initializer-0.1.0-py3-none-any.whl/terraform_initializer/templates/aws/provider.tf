terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Optional: Configure backend
# terraform {
#   backend "s3" {
#     bucket         = "your-terraform-state-bucket"
#     key            = "terraform.tfstate"
#     region         = "us-west-2"
#     dynamodb_table = "terraform-state-lock"
#     encrypt        = true
#   }
# }
