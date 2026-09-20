# ADR 0001. Lakehouse medalhao em vez de warehouse classico

Status: aceito

## Contexto

A LogiStream precisa de historia de pedidos (lote, alto volume, schema relativamente estavel) e de telemetria de frota (alta velocidade, JSON, reprocessamento). O briefing cita plataforma em nuvem com processamento em tempo real, BI e ML.

## Decisao

Adotar lakehouse em Delta Lake sobre S3, com camadas Bronze, Silver e Gold, processado no Databricks. O Gold e modelado como warehouse dimensional (Kimball). O warehouse nao e um produto separado. E uma camada do lakehouse.

## Motivo

- Bronze guarda a origem e torna o reprocessamento uma operacao de particao, nao uma nova extracao no ERP.
- Silver e Gold ganham ACID, evolucao de schema e Time Travel do Delta, o que um data lake cru nao oferece.
- O mesmo objeto S3 atende BI, ML e reprocessamento. Evita a copia eterna lake para warehouse.
- Unity Catalog governa as tres camadas com um catalogo so.

## Consequencias

- O time precisa de disciplina de camada. BI nao le Bronze.
- Custo de storage e baixo. Custo de compute Databricks precisa de dono (job clusters, nao all-purpose ocioso).
- Ferramentas que so falam SQL de warehouse continuam atendidas pelo SQL Warehouse do Databricks no Gold.

## Alternativa rejeitada

Warehouse classico (Redshift ou equivalente) alimentado por lote. Mais simples no primeiro mes, cego para GPS e para retrabalho da origem.
