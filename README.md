# Pipeline ETL para Dados de Clínicas Odontológicas

[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://lugialo.github.io/ex-etl-engdados/) Este projeto acadêmico, desenvolvido para a disciplina de Engenharia de Dados da UNISATC, implementa um pipeline ETL completo para simular a ingestão, transformação e carregamento de dados de diversas fontes de um sistema de gestão de clínicas odontológicas. O objetivo é demonstrar a aplicação da arquitetura medalhão (Landing, Bronze, Silver, Gold) e preparar os dados para análise e geração de insights de negócio.

## Desenho de Arquitetura

![Diagrama da Arquitetura ETL](docs/img/arquitetura_etl.png) ## Pré-requisitos e Ferramentas Utilizadas

Para executar este projeto, você precisará de:

* **Linguagem:** Python 3.9+
* **Bibliotecas Python:** `pandas`, `faker`, `sqlalchemy`, `psycopg2-binary` (se usar PostgreSQL), entre outras listadas em `requirements.txt`.
* **Banco de Dados:** PostgreSQL (sugerido, mas pode ser adaptado para outro DB relacional como SQLite para fins de demonstração local).
* **Documentação:** MkDocs

## Estrutura do Projeto

.
├── data/
│   ├── raw/                  # Dados brutos originais (CSV gerados)
│   ├── bronze/               # Dados brutos ingeridos
│   ├── silver/               # Dados limpos e transformados
│   └── gold/                 # Dados agregados e modelados para consumo (Data Warehouse)
├── docs/                     # Arquivos fonte da documentação MkDocs
│   ├── img/                  # Imagens para a documentação (ex: arquitetura_etl.png)
│   ├── introducao/           # Documentação de introdução
│   ├── camadas/              # Documentação das camadas do Data Lake
│   ├── pipeline/             # Detalhes de cada etapa do pipeline
│   └── modelagem/            # Documentação da modelagem de dados
├── notebooks/
│   ├── notebook_landing_bronze.ipynb  # Notebook para ingestão de Landing para Bronze
│   ├── notebook_bronze_silver.ipynb   # Notebook para transformação de Bronze para Silver
│   └── notebook_silver_gold.ipynb     # Notebook para modelagem de Silver para Gold
├── scripts/
│   ├── gerador_dados.py      # Script para gerar dados de teste
│   ├── modelo_dimensional.sql # Script SQL para criar o modelo dimensional (Data Warehouse)
│   └── modelo_fisico.sql     # Script SQL para criar o modelo físico do banco de dados
├── requirements.txt          # Dependências do projeto Python
├── mkdocs.yml                # Configuração do MkDocs
└── README.md                 # Este arquivo

## Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/lugialo/ex-etl-engdados.git](https://github.com/lugialo/ex-etl-engdados.git)
    cd ex-etl-engdados
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # ou
    .\venv\Scripts\activate   # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuração do Banco de Dados (Exemplo com PostgreSQL):**
    * Certifique-se de ter um servidor PostgreSQL rodando.
    * Crie um banco de dados e um usuário conforme necessário.
    * Atualize as credenciais de conexão no notebook `notebook_silver_gold.ipynb` se necessário.
    * Execute os scripts SQL para criar o modelo físico e dimensional. Você pode usar um cliente SQL ou o comando `psql`:
        ```bash
        psql -h localhost -U seu_usuario -d seu_banco_de_dados -f scripts/modelo_fisico.sql
        psql -h localhost -U seu_usuario -d seu_banco_de_dados -f scripts/modelo_dimensional.sql
        ```

## Como Usar

1.  **Gerar Dados Brutos (Camada Landing - `data/raw`):**
    Execute o script Python para gerar os arquivos CSV simulados:
    ```bash
    python scripts/gerador_dados.py
    ```

2.  **Executar o Pipeline ETL (Jupyter Notebooks):**
    Abra os notebooks Jupyter na ordem e execute todas as células para processar os dados através das camadas do Data Lake:
    ```bash
    jupyter lab
    ```
    * `notebooks/notebook_landing_bronze.ipynb`: Realiza a ingestão dos dados brutos da pasta `data/raw` para a camada Bronze (`data/bronze`).
    * `notebooks/notebook_bronze_silver.ipynb`: Aplica limpeza, transformação e padronização dos dados da camada Bronze, movendo-os para a camada Silver (`data/silver`).
    * `notebooks/notebook_silver_gold.ipynb`: Agrega e modela os dados da camada Silver para o modelo dimensional final na camada Gold (`data/gold` e carregamento no banco de dados relacional).

## Documentação (MkDocs)

Toda a documentação detalhada do projeto, incluindo decisões de design, dicionário de dados e explicações sobre as transformações, está disponível via MkDocs.

Para visualizar a documentação localmente:

```bash
mkdocs build
mkdocs serve ```

Acesse o site em http://127.0.0.1:8000.

Para publicar o site estático no GitHub Pages (requer a ação mkdocs gh-deploy configurada ou manual):

mkdocs gh-deploy

Versão

Versão 1.0.0

Este projeto segue o Versionamento Semântico 2.0.0.

Autores
Anna Clara
Cauã Loch
Gabriel Antonin
Gabrielle Coelho

Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE.md para detalhes.