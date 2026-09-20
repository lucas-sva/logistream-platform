# Terraform da landing zone de producao (AWS + Databricks).

Nao precisa aplicar esta pasta para avaliar a proposta. Os modulos descrevem VPC, S3 medalhao, IAM, MSK e objetos do Unity Catalog.

```sh
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
```

O modulo `databricks` so e criado quando `databricks_host` esta preenchido.
