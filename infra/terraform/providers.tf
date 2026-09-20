provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = var.project_name
      Env       = var.environment
      ManagedBy = "terraform"
    }
  }
}

provider "databricks" {
  alias = "workspace"
  host  = var.databricks_host
  token = var.databricks_token
}
