# Proposta de solucao: plataforma de dados da LogiStream Solutions

Documento de referencia da proposta apresentada no projeto pratico final da pos-graduacao em Engenharia de Dados. O objetivo e descrever como integrar as fontes da empresa para previsao de demanda e otimizacao de rotas, justificando as escolhas, nomeando as ferramentas e expondo beneficios, desafios e tempo estimado de implementacao.

O repositorio que acompanha este texto materializa a proposta com contratos, codigo, Terraform e uma demo local. A avaliacao do curso pede a descricao da solucao. O codigo e complementar.

## 1. Contexto e objetivo

A LogiStream Solutions e uma empresa de varejo online que precisa melhorar a eficiencia das entregas e reduzir custo operacional. Hoje ela coleta pedidos, dados logisticos, feedback de clientes e telemetria de armazens e veiculos. Esses dados existem, mas nao formam uma base unica o suficiente para prever demanda e otimizar rotas.

O problema de negocio, em uma frase: integrar fontes com volume e velocidade diferentes, sem perder qualidade, para alimentar dois produtos analiticos que a empresa ja pretende operar (previsao de demanda e otimizacao de rotas) sobre a infraestrutura que ela ja possui (plataforma em nuvem, BI, machine learning e APIs).

Nao faz parte desta proposta treinar o modelo de previsao nem escrever o solver de rotas. A empresa declara que ja tem sistemas de machine learning e ferramentas de BI. A engenharia de dados entrega a materia prima: dados conformados, pontuais, auditaveis e com contrato.

## 2. Leitura do problema

O briefing descreve quatro familias de dados:

1. Pedidos: produto, quantidade, local de entrega e tempo de processamento.
2. Logistica: rotas, custo de transporte e prazo.
3. Feedback: comentarios e avaliacoes de produto e de experiencia de entrega.
4. Sensores: temperatura, umidade e GPS em armazens e na frota, em tempo real.

Tambem descreve a infraestrutura ja disponivel:

- Plataforma de dados em nuvem, com armazenamento elastico e processamento em tempo real.
- Ferramentas de BI e analytics.
- Sistemas de machine learning para modelagem preditiva.
- APIs para integracao entre sistemas.

Duas tensoes atravessam o cenario. A primeira e de velocidade: pedido e feedback toleram lote; GPS e sensor de camara fria nao. A segunda e de uso: previsao de demanda olha historia agregada por produto, canal e territorio; otimizacao de rota olha estado recente da frota, janela de entrega e restricao do veiculo. Uma arquitetura so de lote atende a primeira e falha na segunda. Uma arquitetura so de streaming atende a segunda e encarece a primeira.

A leitura correta, portanto, nao e "construir um data warehouse" nem "construir um cluster de streaming". E construir uma plataforma que aceite os dois ritmos e publique dois contratos de saida, um para cada produto analitico.

## 3. Informacao que o briefing nao traz

O enunciado omite, de proposito, o que um engenheiro encontraria no primeiro mes de um projeto real. Sem essas respostas nao se dimensiona cluster, janela de SLA nem custo. A proposta segue com premissas explicitas, para ser contestavel, e lista o que precisa ser validado com as areas de negocio antes de qualquer compra de capacidade.

Perguntas em aberto:

- Qual o pais, a malha de centros de distribuicao e o recorte geografico das entregas?
- Quantos pedidos por dia, no pico e na media? Qual a sazonalidade?
- Quantos veiculos, motoristas e rotas ativas existem hoje?
- Qual o sistema de origem de cada fonte (ERP, e-commerce, TMS, CRM, IoT) e qual API ja existe?
- Qual a frequencia real dos sensores e o volume em bytes por hora?
- Qual o SLA de entrega prometido ao cliente final?
- Quem e o dono de cada dado, e quais campos sao pessoais?
- O modelo de ML ja tem contrato de features ou a plataforma precisa propo-lo?

Enquanto essas respostas nao chegam, a arquitetura precisa ser elastica o bastante para corrigir ordem de grandeza sem trocar o desenho.

## 4. Premissas de trabalho

Premissas adotadas para dimensionar a solucao. Todas devem ser revistas com operacao, logistica, produto e juridico.

- Operacao no Brasil, com oito centros de distribuicao (Sao Paulo, Campinas, Rio de Janeiro, Belo Horizonte, Curitiba, Porto Alegre, Salvador e Recife) e entregas em todo o territorio nacional.
- Volume de referencia: cerca de 50 mil pedidos por dia, com pico de 2,5 vezes essa media em datas promocionais.
- Frota de referencia: cerca de 200 veiculos em operacao simultanea.
- Pedidos e eventos do TMS chegam por API em lotes de 15 minutos.
- Feedback de clientes chega uma vez ao dia, a partir do canal de avaliacao pos-entrega.
- GPS da frota emite posicao a cada 30 segundos. Temperatura e umidade de baú e de camara fria emitem a cada 60 segundos.
- Endereco de entrega, contato do cliente e texto livre da avaliacao sao dados pessoais.
- Os times de BI e de ML ja existem. A plataforma publica marts e tabelas de features. Nao substitui essas equipes.
- A nuvem de producao e AWS, com Databricks como motor do lakehouse. Azure permanece documentada como alternativa.

Esses numeros cabem em um lakehouse Databricks de porte medio, com Kafka (Amazon MSK) so na via de sensores. Se a frota for dez vezes maior, o desenho se mantem e a conta de particionamento e de autoscaling muda. Se a frota for dez vezes menor, Kafka ainda se justifica pela natureza do dado, nao pelo volume.
