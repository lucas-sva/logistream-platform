output "vpc_id" {
  value = module.network.vpc_id
}

output "bronze_bucket" {
  value = module.lake.bronze_bucket_id
}

output "silver_bucket" {
  value = module.lake.silver_bucket_id
}

output "gold_bucket" {
  value = module.lake.gold_bucket_id
}

output "msk_cluster_arn" {
  value = module.kafka.cluster_arn
}

output "databricks_instance_profile_arn" {
  value = module.iam.databricks_instance_profile_arn
}
