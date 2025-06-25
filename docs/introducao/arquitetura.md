# Arquitetura do Pipeline ETL

A arquitetura do nosso pipeline ETL para dados de clínicas odontológicas segue o padrão de **Data Lake com arquitetura medalhão**. Este modelo é fundamental para garantir a organização, a qualidade e a rastreabilidade dos dados em diferentes estágios de processamento, desde a sua origem até a camada de consumo.

![Diagrama da Arquitetura ETL](../img/arquitetura_etl.png)


**Componentes Chave da Arquitetura:**

1.  **Fontes de Dados (Simuladas):**
    * Atualmente, os dados são gerados programaticamente utilizando Python (via `scripts/gerador_dados.py`) e armazenados em arquivos CSV.
    * Esses arquivos CSV representam diversas entidades relacionadas a operações de clínicas, como pacientes, odontologistas, consultas, procedimentos, pagamentos, etc.

2.  **Camada Landing (Raw):**
    * **Localização:** `data/raw/`
    * **Propósito:** Esta é a área de recepção inicial dos dados. Os arquivos CSV gerados são colocados diretamente aqui, sem nenhuma transformação ou validação de conteúdo.
    * **Características:** Preserva a integridade e o formato original dos dados, servindo como uma fonte imutável e auditável.

3.  **Camada Bronze:**
    * **Localização:** `data/bronze/`
    * **Propósito:** Recebe os dados da camada Landing após uma ingestão inicial. Nesta etapa, os dados são lidos, validados em termos de formato básico (se são arquivos CSV válidos, por exemplo) e tipagem, e salvos novamente.
    * **Ferramenta:** `notebooks/notebook_landing_bronze.ipynb`
    * **Características:** Os dados ainda são brutos em sua essência, mas já passaram por um controle mínimo de qualidade para garantir que são legíveis e estruturados para as próximas etapas.

4.  **Camada Silver:**
    * **Localização:** `data/silver/`
    * **Propósito:** Esta camada é onde ocorrem as principais transformações e limpezas dos dados. Dados são padronizados, inconsistências são tratadas, valores nulos são manipulados e regras de negócio são aplicadas.
    * **Ferramenta:** `notebooks/notebook_bronze_silver.ipynb`
    * **Características:** Os dados estão limpos, padronizados e prontos para serem usados em análises mais complexas ou para serem modelados.

5.  **Camada Gold (Data Warehouse):**
    * **Localização:** `data/gold/` (para arquivos intermediários, se houver) e **Banco de Dados Relacional (PostgreSQL)** para consumo.
    * **Propósito:** A camada final do pipeline. Aqui, os dados limpos da camada Silver são agregados e modelados em um formato dimensional (estrela ou floco de neve), otimizado para consultas analíticas e ferramentas de Business Intelligence (BI).
    * **Ferramenta:** `notebooks/notebook_silver_gold.ipynb` e scripts SQL (`scripts/modelo_fisico.sql`, `scripts/modelo_dimensional.sql`).
    * **Características:** Dados consolidados, de alta qualidade, estruturados em tabelas de fato e dimensão, prontos para gerar insights de negócio e alimentar dashboards.

Este fluxo garante um processo robusto de ETL, onde cada camada adiciona valor e refinamento aos dados, culminando em um Data Warehouse confiável para a tomada de decisões.