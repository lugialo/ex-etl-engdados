# Camada Gold (Data Warehouse)

A camada Gold é a camada mais refinada e estratégica do nosso Data Lake. Ela contém dados que foram completamente processados, limpos, transformados, agregados e modelados em um formato otimizado para consumo por usuários de negócios, analistas de dados e ferramentas de Business Intelligence (BI). É aqui que os dados se transformam em informações acionáveis.

**Propósito:**

* **Consumo Analítico:** Fornecer um modelo de dados performático e intuitivo para consultas analíticas complexas e geração de relatórios e dashboards.
* **Decisão de Negócios:** Ser a fonte de verdade para todas as análises de negócio, KPIs (Key Performance Indicators) e métricas.
* **Simplicidade para o Usuário Final:** Apresentar os dados de forma desnormalizada e fácil de entender, minimizando a necessidade de conhecimento técnico em SQL ou modelagem de dados para os usuários de BI.

**Características:**

* **Modelagem Dimensional:** Os dados são organizados em um esquema estrela (Star Schema), composto por tabelas de fato e tabelas de dimensão.
    * **Tabelas de Fato:** Contêm as métricas e os fatos de negócio (por exemplo, valores de pagamento, duração da consulta, quantidade de procedimentos). Elas possuem chaves estrangeiras para as tabelas de dimensão.
    * **Tabelas de Dimensão:** Contêm os atributos descritivos do negócio (por exemplo, detalhes do paciente, informações do odontologista, datas).
* **Alta Qualidade e Consistência:** Herda a qualidade e padronização da camada Silver, com dados prontos para análise imediata.
* **Otimização para Leitura:** Estruturada para otimizar o desempenho de consultas de leitura e agregação.
* **Armazenamento:** Os dados da camada Gold são carregados em um **Banco de Dados Relacional (PostgreSQL)**, garantindo a integridade e a capacidade de consulta via SQL. Embora dados intermediários possam existir em `data/gold/`, o principal destino de consumo é o banco de dados.

**Exemplo de Modelo Dimensional (Schema Estrela - simplificado):**

Em nosso projeto, esperamos ter tabelas de fato e dimensão semelhantes a:

* **Fato:**
    * `fato_consultas_e_pagamentos`: Contém métricas sobre consultas e pagamentos (valor total, duração, quantidade de procedimentos) e chaves para dimensões.

* **Dimensões:**
    * `dim_tempo`: Detalhes sobre datas (ano, mês, dia, dia da semana, feriado, etc.).
    * `dim_paciente`: Informações detalhadas sobre os pacientes (nome, data de nascimento, gênero, telefone, endereço).
    * `dim_odontologista`: Dados sobre os profissionais (nome, especialidade, CRO).
    * `dim_procedimento`: Detalhes dos procedimentos (nome do procedimento, descrição, custo padrão).
    * `dim_tipo_pagamento`: Descrição dos tipos de pagamento.

**Processo Detalhado (via `notebook_silver_gold.ipynb`):**

O notebook `notebook_silver_gold.ipynb` executa as seguintes ações para construir e popular a camada Gold:

1.  **Leitura da Camada Silver:** Carrega os DataFrames limpos e transformados da pasta `data/silver/`.
2.  **Construção das Dimensões:**
    * Os dados de cada entidade são extraídos e transformados para se adequarem às tabelas de dimensão.
    * Garantia de unicidade para as dimensões.
    * Exemplo: A `dim_tempo` é geralmente gerada ou preenchida com antecedência, ou criada a partir das datas existentes nas transações.
3.  **Construção da Tabela de Fato:**
    * As tabelas de dimensão são unidas aos dados transacionais da camada Silver.
    * Cálculo de métricas (valores totais, contagens, etc.).
    * As chaves primárias das dimensões são obtidas e inseridas como chaves estrangeiras na tabela de fato.
4.  **Carregamento no Banco de Dados:**
    * Utiliza a biblioteca `SQLAlchemy` ou `psycopg2` (para PostgreSQL) para conectar ao banco de dados.
    * Os scripts SQL em `scripts/modelo_fisico.sql` e `scripts/modelo_dimensional.sql` são usados para criar as tabelas no banco de dados.
    * Os DataFrames resultantes das tabelas de fato e dimensão são carregados (inseridos) nas tabelas correspondentes do banco de dados PostgreSQL.

Esta camada é o produto final do pipeline ETL, fornecendo uma base sólida para qualquer necessidade de análise de dados.