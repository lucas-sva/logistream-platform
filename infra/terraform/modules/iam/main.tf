variable "project_name" { type = string }
variable "environment" { type = string }
variable "bronze_bucket_arn" { type = string }
variable "silver_bucket_arn" { type = string }
variable "gold_bucket_arn" { type = string }

data "aws_iam_policy_document" "assume_ec2" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "databricks" {
  name               = "${var.project_name}-${var.environment}-databricks"
  assume_role_policy = data.aws_iam_policy_document.assume_ec2.json
}

data "aws_iam_policy_document" "lake_access" {
  statement {
    sid     = "ListBuckets"
    actions = ["s3:ListBucket", "s3:GetBucketLocation"]
    resources = [
      var.bronze_bucket_arn,
      var.silver_bucket_arn,
      var.gold_bucket_arn,
    ]
  }

  statement {
    sid = "ObjectAccess"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:AbortMultipartUpload",
      "s3:ListMultipartUploadParts",
    ]
    resources = [
      "${var.bronze_bucket_arn}/*",
      "${var.silver_bucket_arn}/*",
      "${var.gold_bucket_arn}/*",
    ]
  }
}

resource "aws_iam_policy" "lake_access" {
  name   = "${var.project_name}-${var.environment}-lake-access"
  policy = data.aws_iam_policy_document.lake_access.json
}

resource "aws_iam_role_policy_attachment" "lake_access" {
  role       = aws_iam_role.databricks.name
  policy_arn = aws_iam_policy.lake_access.arn
}

resource "aws_iam_instance_profile" "databricks" {
  name = "${var.project_name}-${var.environment}-databricks"
  role = aws_iam_role.databricks.name
}

output "databricks_role_arn" {
  value = aws_iam_role.databricks.arn
}

output "databricks_instance_profile_arn" {
  value = aws_iam_instance_profile.databricks.arn
}
