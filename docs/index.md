# Boas-vindas à Documentação do Pipeline ETL de Clínicas Odontológicas

Este documento serve como guia completo para o nosso projeto de Engenharia de Dados, focado na construção de um pipeline ETL robusto para dados de clínicas odontológicas. Aqui você encontrará desde a visão geral da arquitetura até os detalhes técnicos de cada etapa de transformação de dados.

O objetivo principal deste projeto é simular um ambiente real de processamento de dados, aplicando conceitos de engenharia de dados para transformar informações brutas de diversas fontes (inicialmente arquivos CSV) em um formato estruturado e otimizado para análise. Utilizamos a metodologia de **arquitetura medalhão** para garantir a qualidade e a rastreabilidade dos dados em diferentes estágios:

* **Camada Landing (Raw):** Dados brutos, como foram recebidos das fontes.
* **Camada Bronze:** Dados brutos ingeridos, com mínimas validações de formato.
* **Camada Silver:** Dados limpos, transformados e padronizados, prontos para serem usados em análises mais detalhadas.
* **Camada Gold:** Dados agregados e modelados em um formato dimensional (Data Warehouse), otimizados para consumo por ferramentas de BI e análise de negócios.

Esta documentação irá guiá-lo através da arquitetura do pipeline, das ferramentas utilizadas, das transformações aplicadas em cada etapa e de como executar o projeto em seu ambiente local.