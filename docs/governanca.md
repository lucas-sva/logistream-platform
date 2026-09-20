# Governanca, catalogo e dados pessoais

A plataforma so e entregavel se o Gold tiver dono, teste e acesso. Este documento fecha o que o Unity Catalog, o dbt e o juridico precisam ver no dia um.

## Catalogo

Unity Catalog no workspace Databricks, catalogo `logistream`, schemas `bronze`, `silver` e `gold`. External locations apontam para os buckets S3 correspondentes. Terraform cria o esqueleto. Grupos:

- `data-engineers`: CREATE, MODIFY e SELECT nas tres camadas.
- `bi-analysts`: SELECT no Gold.
- `ml-engineers`: SELECT no Gold e nas feature tables.
- `ops-readonly`: SELECT no Silver, sem Bronze.

BI e ML nao leem Bronze. Bronze e zona de retrabalho e de auditoria, nao de produto.

Linhagem: jobs Databricks + dbt. Cada mart Gold declara `ref()` para o Silver. O Unity Catalog fecha a linhagem de tabela. O contrato JSON em `data/contracts/` fecha a linhagem de origem.

## Qualidade

Testes dbt no Gold (unicidade de `order_item_id` e `delivery_id`, preenchimento de chaves, relacionamento com dimensoes). Regras de faixa no Silver (quantidade > 0, temperatura de bau frio entre 0 e 8 C, humidity 0-100). Jobs Spark falham fechados: particao com taxa de rejeicao acima de 2% nao promove Silver.

Freshness:

- Pedidos e TMS: Gold atualizado no maximo 30 minutos apos o lote Airbyte.
- Feedback: Gold no dia seguinte, 08:00 America/Sao_Paulo.
- Sensores: Silver com atraso alvo de 2 minutos (watermark do stream). Fato minutario no Gold a cada 5 minutos.

## Dados pessoais

Campos pessoais no briefing, mesmo sem schema oficial:

- Pedido: `customer_id`, e-mail, endereco, CEP.
- Feedback: `customer_id`, texto livre (pode conter nome, telefone, documento).
- Logistica: endereco de entrega.
- Sensores: placa aparece so tokenizada. GPS e dado de localizacao da operacao, nao do cliente final, mas ainda assim restrito.

Tratamento:

- Bronze guarda o payload original, com acesso so de engenharia e auditoria, retencao definida com o juridico (premissa: 12 meses, depois glacier).
- Silver substitui identificadores por token SHA-256 estavel (`customer_token`). E-mail e texto livre nao descem para o Gold.
- Feedback: o comentario vira `comment_hash` no Silver. Analise de texto, se o negocio pedir, ocorre em ambiente isolado, nao no mart de BI.
- Gold de demanda expoe `dim_cliente_tokenizado` sem contato.

Base legal e DPO ficam com o juridico. A engenharia nao publica Gold enquanto essa classificacao nao estiver assinada.

## Seguranca operacional

- Sem chave no Git. Terraform variables, Databricks secrets e Airbyte credentials no gerenciador da nuvem.
- Buckets com Block Public Access, KMS e versionamento.
- MSK so TLS, subnets privadas.
- Job clusters Databricks, nao cluster all-purpose ocioso.
- Este repositorio usa dados sinteticos. Relato de vulnerabilidade em SECURITY.md.

## Operacao

Runbooks minimos (a escrever com o time quando a landing zone subir):

- Reprocessar uma data de pedidos a partir do Bronze.
- Reposicionar o consumer de sensores sem duplicar o Gold minutario.
- Revogar um analista no Unity Catalog.
- Estimar custo Databricks + MSK da semana anterior.

Sem esses quatro, a plataforma vira um laboratorio. Com eles, vira operacao.
