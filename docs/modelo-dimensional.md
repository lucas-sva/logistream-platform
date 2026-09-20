# Modelo dimensional

Dois marts no Gold, dimensoes conformadas. Modelagem Kimball. Grao declarado em cada fato. Chaves surrogate numericas no warehouse, chaves naturais preservadas para auditoria.

O Silver entrega entidades. O Gold entrega perguntas de negocio.

## Dimensoes conformadas

Estas dimensoes servem os dois marts. Mudar o calendario em um mart e nao no outro e o jeito mais rapido de quebrar previsao de demanda versus prazo de entrega.

### dim_data

- Grao: dia civil (America/Sao_Paulo).
- Chave: `sk_data` (yyyymmdd).
- Atributos: data, ano, trimestre, mes, semana ISO, dia da semana, flag fim de semana, flag feriado nacional, flag data promocional (Black Friday, Natal, Dia das Maes).
- Motivo: sazonalidade e a primeira variavel que o modelo de demanda vai pedir.

### dim_localidade

- Grao: municipio + UF, com CEP de referencia do CD mais proximo.
- Atributos: uf, municipio, mesorregiao, macroregiao (N, NE, CO, SE, S), tipo (capital, interior, metropole), cd_preferencial.
- SCD: tipo 1. Municipio nao muda de UF na pratica operacional.

### dim_produto

- Grao: SKU.
- Atributos: sku, nome, categoria, subcategoria, marca, volume_m3, peso_kg, flag_refrigerado, flag_fragil.
- SCD: tipo 2. Categoria e volume mudam e a demanda historica precisa do SKU como era na data do pedido.

## Mart de demanda

Pergunta que o mart responde: quantas unidades, de qual produto, sairam de qual CD, para qual localidade, em qual dia, por qual canal.

### dim_canal

- Grao: canal de venda (site, app, marketplace).
- SCD tipo 1.

### dim_cliente_tokenizado

- Grao: cliente.
- Atributos: `sk_cliente`, `customer_token`, faixa de recencia, faixa de ticket. Sem nome, e-mail, telefone ou endereco.
- SCD tipo 1 sobre os atributos analiticos. O token e estavel.

### fato_pedido

- Grao: item de pedido.
- Chaves: `sk_data_pedido`, `sk_data_processamento`, `sk_produto`, `sk_localidade_entrega`, `sk_canal`, `sk_cliente`, `sk_cd`.
- Medidas: quantidade, valor_bruto, valor_desconto, valor_liquido, tempo_processamento_min, flag_cancelado.
- Degenerados: `order_id`, `order_item_id`.
- Regras: cancelado permanece no fato, com flag. Previsao de demanda usa a medida liquida filtrada.

## Mart de rotas

Pergunta que o mart responde: a entrega saiu no prazo, por qual rota, em qual veiculo, a que custo, e o produto viajou dentro da faixa ambiental.

### dim_cd

- Grao: centro de distribuicao.
- Atributos: codigo, municipio, uf, capacidade_m3, flag_camara_fria.
- SCD tipo 2 para capacidade.

### dim_veiculo

- Grao: veiculo da frota.
- Atributos: placa_tokenizada, tipo (van, toco, truck, bau refrigerado), capacidade_kg, capacidade_m3, flag_refrigerado.
- SCD tipo 2.

### dim_rota

- Grao: rota planejada do dia (CD origem + sequencia de zonas).
- Atributos: cd_origem, zona_principal, janela_inicio, janela_fim, distancia_planejada_km.
- SCD tipo 2. A malha muda.

### fato_entrega

- Grao: uma entrega (um pedido, um destino, um veiculo).
- Chaves: `sk_data_saida`, `sk_data_entrega`, `sk_cd`, `sk_veiculo`, `sk_rota`, `sk_localidade_destino`, `sk_produto` (produto predominante, quando a entrega e monoitem; em multiitem a analise de produto vai ao fato_pedido).
- Medidas: prazo_prometido_h, prazo_realizado_h, desvio_prazo_h, custo_transporte, distancia_km, ocupacao_peso_pct, ocupacao_volume_pct, flag_atraso, flag_ocorrencia.
- Degenerados: `delivery_id`, `order_id`.

### fato_leitura_sensor

- Grao: dispositivo + minuto.
- Origem: Silver de sensores, ja agregado pelo job de streaming (GPS permanece no Silver ponto a ponto; o fato ambiental e minutario para nao explodir o warehouse).
- Chaves: `sk_data`, `minuto_utc`, `sk_veiculo` (nulo se for sensor de CD), `sk_cd`.
- Medidas: lat, lon, velocidade_kmh, temperatura_c, umidade_pct, flag_fora_faixa, qtd_eventos.
- Uso: qualidade da carga refrigerada e input de tempo de deslocamento para o otimizador.

## Feature tables

Nao sao fatos de BI. Sao contratos com o time de ML, versionados.

### feat_demanda_diaria_sku_cd

- Grao: sku + cd + dia.
- Campos: quantidade, valor_liquido, cancelamentos, media_7d, media_28d, desvio_28d, flag_promocao, flag_ruptura_aproximada (quando quantidade cai a zero com estoque nao modelado, fica nulo; ruptura verdadeira depende de uma fonte de estoque que o briefing nao entregou).

### feat_rota_veiculo

- Grao: veiculo + dia.
- Campos: entregas, atraso_pct, tempo_medio_entre_paradas_min, km_total, ocupacao_media_pct, minutos_fora_faixa_temp.

## Relacionamento entre os marts

`order_id` e a ponte degenerada entre `fato_pedido` e `fato_entrega`. Nao se cria um fato unico "pedido-entrega" porque o grao quebra: um pedido pode ter varios itens e a entrega pode agrupar itens de pedidos diferentes na mesma viagem, a depender da operacao. Enquanto a LogiStream nao confirmar essa regra, os dois fatos permanecem separados e a analise conjunta se faz por `order_id`.

## Fontes de estoque e transito

O briefing nao cita estoque de CD nem manifesto de carga. Sem isso, ruptura e cubagem real sao aproximacoes. A proposta deixa duas tabelas previstas, sem implementacao neste repositorio:

- `fato_posicao_estoque` (grao: sku + cd + dia)
- `fato_manifesto` (grao: viagem + sku)

Elas entram quando a operacao entregar a fonte. O modelo atual nao inventa essas tabelas no Gold para nao fingir precisao.
