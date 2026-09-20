module "network" {
  source = "./modules/network"

  project_name         = var.project_name
  environment          = var.environment
  vpc_cidr             = var.vpc_cidr
  private_subnet_cidrs = var.private_subnet_cidrs
  public_subnet_cidrs  = var.public_subnet_cidrs
}

module "lake" {
  source = "./modules/lake"

  project_name = var.project_name
  environment  = var.environment
}

module "iam" {
  source = "./modules/iam"

  project_name     = var.project_name
  environment      = var.environment
  bronze_bucket_arn = module.lake.bronze_bucket_arn
  silver_bucket_arn = module.lake.silver_bucket_arn
  gold_bucket_arn   = module.lake.gold_bucket_arn
}

module "kafka" {
  source = "./modules/kafka"

  project_name     = var.project_name
  environment      = var.environment
  vpc_id           = module.network.vpc_id
  private_subnet_ids = module.network.private_subnet_ids
  broker_nodes     = var.msk_broker_nodes
}

module "databricks" {
  source = "./modules/databricks"
  count  = var.databricks_host == "" ? 0 : 1

  project_name      = var.project_name
  environment       = var.environment
  bronze_bucket_id  = module.lake.bronze_bucket_id
  silver_bucket_id  = module.lake.silver_bucket_id
  gold_bucket_id    = module.lake.gold_bucket_id
  instance_profile_arn = module.iam.databricks_instance_profile_arn

  providers = {
    databricks = databricks.workspace
  }
}
