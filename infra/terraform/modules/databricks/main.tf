terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
  }
}

variable "project_name" { type = string }
variable "environment" { type = string }
variable "bronze_bucket_id" { type = string }
variable "silver_bucket_id" { type = string }
variable "gold_bucket_id" { type = string }
variable "instance_profile_arn" { type = string }

resource "databricks_catalog" "logistream" {
  name    = var.project_name
  comment = "LogiStream lakehouse catalogs for demand and routing."
}

resource "databricks_schema" "layers" {
  for_each     = toset(["bronze", "silver", "gold"])
  catalog_name = databricks_catalog.logistream.name
  name         = each.value
  comment      = "Medalhao ${each.value}"
}

resource "databricks_external_location" "layers" {
  for_each        = {
    bronze = var.bronze_bucket_id
    silver = var.silver_bucket_id
    gold   = var.gold_bucket_id
  }
  name            = "${var.project_name}-${each.key}"
  url             = "s3://${each.value}/"
  credential_name = databricks_storage_credential.lake.name
}

resource "databricks_storage_credential" "lake" {
  name = "${var.project_name}-${var.environment}-lake"
  aws_iam_role {
    role_arn = var.instance_profile_arn
  }
}

resource "databricks_grants" "gold_bi" {
  schema = databricks_schema.layers["gold"].id
  grant {
    principal  = "bi-analysts"
    privileges = ["USE_SCHEMA", "SELECT"]
  }
}
