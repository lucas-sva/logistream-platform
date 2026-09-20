variable "project_name" {
  type        = string
  description = "Short name used in resource prefixes."
  default     = "logistream"
}

variable "environment" {
  type        = string
  description = "Environment name."
  default     = "prod"
}

variable "aws_region" {
  type        = string
  description = "AWS region for the landing zone."
  default     = "sa-east-1"
}

variable "vpc_cidr" {
  type        = string
  default     = "10.40.0.0/16"
}

variable "private_subnet_cidrs" {
  type        = list(string)
  default     = ["10.40.1.0/24", "10.40.2.0/24"]
}

variable "public_subnet_cidrs" {
  type        = list(string)
  default     = ["10.40.10.0/24", "10.40.11.0/24"]
}

variable "databricks_host" {
  type        = string
  description = "Databricks workspace URL. Empty skips workspace objects."
  default     = ""
}

variable "databricks_token" {
  type        = string
  description = "Databricks PAT. Never commit a real value."
  default     = ""
  sensitive   = true
}

variable "msk_broker_nodes" {
  type        = number
  default     = 2
}
