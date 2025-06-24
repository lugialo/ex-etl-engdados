# Visão Geral do Projeto

Este projeto foi desenvolvido como parte da disciplina de Engenharia de Dados do curso de Engenharia de Software da UNISATC. Ele simula um cenário real de ingestão, transformação e carregamento de dados para um sistema de gestão de clínicas odontológicas. O objetivo é demonstrar a aplicação de conceitos e práticas de engenharia de dados, desde a coleta de dados brutos até a disponibilização de informações prontas para análise.

**Objetivos Principais:**

* **Ingestão de Dados:** Realizar a coleta de dados de diversas fontes (atualmente arquivos CSV simulados) para uma área de *landing zone*.
* **Pipeline de Transformação:** Implementar um pipeline de ETL (Extract, Transform, Load) utilizando a arquitetura medalhão (Landing, Bronze, Silver, Gold). Isso garante a progressiva limpeza, enriquecimento e estruturação dos dados.
* **Modelagem Dimensional:** Modelar os dados finais em um formato dimensional (Data Warehouse), otimizado para facilitar a análise de negócios e a criação de dashboards.
* **Ferramentas e Tecnologias:** Utilizar ferramentas e linguagens de programação comuns no ecossistema de engenharia de dados, como Python, Pandas e SQL, para manipular e transformar os conjuntos de dados.
* **Documentação:** Fornecer uma documentação clara e abrangente do pipeline, sua arquitetura e as transformações aplicadas, utilizando MkDocs.

Este projeto busca ser uma demonstração prática de como dados de diferentes fontes podem ser integrados e transformados para gerar insights valiosos para a gestão de uma clínica odontológica.