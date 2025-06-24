# Stage 3: Modelagem e Carregamento de Silver para Gold

O `notebooks/notebook_silver_gold.ipynb` é o estágio final do nosso pipeline ETL, responsável por transformar os dados limpos e padronizados da Camada Silver em um modelo dimensional otimizado para análise (Camada Gold). Esta etapa envolve a criação de tabelas de dimensão e tabelas de fato, e o carregamento desses dados em um banco de dados relacional (PostgreSQL, conforme o projeto).

**Objetivo:**

* **Modelagem Dimensional:** Construir um esquema estrela (Star Schema) ou floco de neve (Snowflake Schema) que seja intuitivo para usuários de negócio e eficiente para consultas analíticas.
* **Agregação de Dados:** Realizar agregações e sumarizações necessárias para as métricas de negócio.
* **Carregamento no Data Warehouse:** Persistir os dados modelados em um banco de dados relacional que servirá como o Data Warehouse final para consumo por ferramentas de BI.

**Ferramentas Utilizadas:**

* **Jupyter Notebook:** `notebooks/notebook_silver_gold.ipynb`
* **Python:** Linguagem de programação principal.
* **Pandas:** Para manipulação e transformação de DataFrames.
* **SQLAlchemy / Psycopg2:** Para conexão e interação com o banco de dados PostgreSQL.
* **SQL:** Scripts `scripts/modelo_fisico.sql` e `scripts/modelo_dimensional.sql` para criação da estrutura do banco de dados.

**Entrada:**

* Arquivos CSV limpos e transformados, localizados na pasta `data/silver/`.

**Saída:**

* Tabelas de fato e dimensão populadas no banco de dados PostgreSQL (camada Gold).
* (Opcional: arquivos Parquet ou CSV da camada Gold em `data/gold/` para persistência local antes do carregamento no DB).

**Processo Detalhado e Principais Transformações:**

O notebook `notebook_silver_gold.ipynb` executa as seguintes operações:

1.  **Carregamento dos Dados da Camada Silver:**
    * Todos os arquivos CSV da pasta `data/silver/` são carregados em DataFrames do Pandas. Isso inclui dados já limpos de pacientes, consultas, pagamentos, procedimentos, etc.

2.  **Preparação das Tabelas de Dimensão:**
    * Para cada dimensão (por exemplo, `dim_paciente`, `dim_odontologista`, `dim_procedimento`, `dim_tempo`, `dim_tipo_pagamento`), os dados relevantes são selecionados e transformados para se tornarem atributos da dimensão.
    * **Remoção de Duplicatas:** Garante que cada dimensão contenha apenas entradas únicas.
    * **Criação de Chaves Suplicadas (Surrogate Keys - Opcional, mas comum):** Se não houver chaves de negócio adequadas, novas chaves numéricas sequenciais podem ser geradas para as dimensões.
    * **Modelagem da Dimensão Tempo:** Uma dimensão de tempo pode ser construída a partir das datas das transações (consultas, agendamentos), extraindo atributos como ano, mês, dia, dia da semana, trimestre, etc.

3.  **Construção da Tabela de Fato:**
    * A tabela de fato é construída a partir dos dados transacionais (principalmente de consultas e pagamentos) da camada Silver.
    * **Junção com Dimensões:** As chaves de negócio da tabela de fato são usadas para buscar as chaves suplicadas das dimensões correspondentes. Isso conecta a tabela de fato às suas dimensões.
    * **Cálculo de Métricas:** As métricas de negócio são calculadas e agregadas. Exemplos:
        * `valor_total_consulta` (soma dos pagamentos e procedimentos de uma consulta)
        * `quantidade_procedimentos`
        * `duracao_consulta` (se aplicável)
    * A tabela de fato é projetada para ser granular, contendo uma linha por evento de negócio (ex: uma consulta, um pagamento).

4.  **Criação/Atualização da Estrutura do Banco de Dados:**
    * O notebook pode primeiro verificar se as tabelas da camada Gold existem no banco de dados.
    * É comum que os scripts SQL `scripts/modelo_fisico.sql` (para criar o DB, schemas, etc.) e `scripts/modelo_dimensional.sql` (para criar as tabelas de fato e dimensão) sejam executados antes de carregar os dados. O notebook pode orquestrar essa execução via `psycopg2` ou `SQLAlchemy`.

5.  **Carregamento dos Dados no Banco de Dados (Load):**
    * As tabelas de dimensão são carregadas primeiro no PostgreSQL.
    * A tabela de fato é carregada em seguida, após suas dimensões correspondentes já estarem populadas.
    * Isso pode ser feito usando `df.to_sql()` do Pandas (via SQLAlchemy) ou inserções diretas com `psycopg2`.
    * Exemplo:
        ```python
        from sqlalchemy import create_engine
        engine = create_engine('postgresql://user:password@host:port/database') # Ajustar credenciais

        # Carregar dimensão paciente
        df_dim_paciente.to_sql('dim_paciente', engine, if_exists='replace', index=False)

        # Carregar fato consultas_e_pagamentos
        df_fato_consultas.to_sql('fato_consultas_e_pagamentos', engine, if_exists='replace', index=False)
        ```
    * É importante considerar a estratégia de carregamento (completa ou incremental, para projetos mais complexos). Neste caso, um carregamento completo (`if_exists='replace'`) para fins de demonstração é comum.

Este estágio finaliza o processo de ETL, disponibilizando os dados em um formato que é diretamente consumível para relatórios e dashboards analíticos, fechando o ciclo da jornada do dado.