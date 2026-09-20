# ADR 0003. AWS com Databricks, Azure como alternativa

Status: aceito

## Contexto

O briefing fala em plataforma de dados em nuvem, sem nomear o provedor. A pos-graduacao cobre Terraform, AWS, Azure e Databricks. O repositorio precisa de um alvo concreto de IaC.

## Decisao

Producao de referencia: AWS (VPC, S3, IAM, KMS, MSK) + Databricks workspace, Unity Catalog e jobs. Terraform neste repositorio descreve esse alvo.

Azure (ADLS Gen2, Event Hubs, Azure Databricks, Unity Catalog) e alternativa documentada, nao implementada em codigo.

## Motivo

Os dois desenhos sao equivalentes em capacidade. Escolher os dois no mesmo Terraform deixa o projeto genérico e dificil de operar. AWS + Databricks e o alvo mais comum para lakehouse com Kafka gerenciado (MSK) e objeto S3 como camada unica de storage. Databricks permanece portavel: o mesmo Delta, o mesmo catalogo e o mesmo dbt mudam pouco se a empresa estiver no Azure.

## Consequencias

- Modulos Terraform nao sao multi-cloud.
- Se o contrato corporativo for Microsoft, o mapeamento e direto: S3 vira ADLS, MSK vira Event Hubs (ou Kafka no HDInsight/Confluent), IAM vira Entra ID + RBAC. A modelagem Gold nao muda.
- A demo local nao depende de nenhum dos dois provedores.

## Alternativa rejeitada

Terraform multi-cloud no dia um. Duplica modulo, duplica IAM e nao ajuda a previsao de demanda.
