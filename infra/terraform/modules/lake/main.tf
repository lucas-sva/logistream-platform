variable "project_name" { type = string }
variable "environment" { type = string }

resource "aws_kms_key" "lake" {
  description             = "LogiStream lakehouse encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

resource "aws_kms_alias" "lake" {
  name          = "alias/${var.project_name}-${var.environment}-lake"
  target_key_id = aws_kms_key.lake.id
}

resource "aws_s3_bucket" "bronze" {
  bucket = "${var.project_name}-${var.environment}-bronze"
}

resource "aws_s3_bucket" "silver" {
  bucket = "${var.project_name}-${var.environment}-silver"
}

resource "aws_s3_bucket" "gold" {
  bucket = "${var.project_name}-${var.environment}-gold"
}

resource "aws_s3_bucket" "logs" {
  bucket = "${var.project_name}-${var.environment}-access-logs"
}

locals {
  buckets = {
    bronze = aws_s3_bucket.bronze.id
    silver = aws_s3_bucket.silver.id
    gold   = aws_s3_bucket.gold.id
    logs   = aws_s3_bucket.logs.id
  }
}

resource "aws_s3_bucket_versioning" "this" {
  for_each = local.buckets
  bucket   = each.value
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  for_each = local.buckets
  bucket   = each.value
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.lake.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  for_each                = local.buckets
  bucket                  = each.value
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "bronze" {
  bucket = aws_s3_bucket.bronze.id
  rule {
    id     = "raw-to-glacier"
    status = "Enabled"
    filter {}
    transition {
      days          = 90
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 365
      storage_class = "GLACIER"
    }
  }
}

output "bronze_bucket_id" { value = aws_s3_bucket.bronze.id }
output "silver_bucket_id" { value = aws_s3_bucket.silver.id }
output "gold_bucket_id" { value = aws_s3_bucket.gold.id }
output "bronze_bucket_arn" { value = aws_s3_bucket.bronze.arn }
output "silver_bucket_arn" { value = aws_s3_bucket.silver.arn }
output "gold_bucket_arn" { value = aws_s3_bucket.gold.arn }
output "kms_key_arn" { value = aws_kms_key.lake.arn }
