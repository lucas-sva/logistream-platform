# ADR 0002. Ingestao hibrida: Airbyte no lote, Kafka no sensor

Status: aceito

## Contexto

Quatro fontes, dois ritmos. Pedidos, TMS e feedback ja tendem a viver em API ou banco. Sensores de GPS e ambiente nascem como evento.

## Decisao

- Airbyte para pedidos, logistica e feedback, destino Bronze em S3.
- Apache Kafka (Amazon MSK) para sensores de frota e de CD, com sink Spark Structured Streaming no Bronze.

## Motivo

Airbyte reduz coletor artesanal onde o atraso de 15 minutos e aceitavel e o conector de API ja resolve autenticacao, paginacao e checkpoint. Kafka reduz perda e atraso onde o otimizador de rota precisa do ponto recente do veiculo, e permite replay curto sem recarregar o lake.

Misturar os dois no mesmo produto (tudo Airbyte ou tudo Kafka) e pior nos dois lados: Airbyte nao e barramento de IoT; Kafka nao e a ferramenta mais barata para um dump diario de avaliacoes.

## Consequencias

- Dois modos operacionais para monitorar (conexoes Airbyte e consumer lag no MSK).
- Contratos JSON das quatro fontes precisam ser versionados juntos, mesmo com ingestao diferente.
- A demo local substitui Airbyte por um loader Python com o mesmo schema, porque o Airbyte OSS nao cabe bem em notebook.

## Alternativas rejeitadas

- Tudo via Kafka (Kappa): custo e complexidade sem ganho no lote diario.
- Tudo via Airbyte: a posicao da frota chega tarde demais para a rota.
