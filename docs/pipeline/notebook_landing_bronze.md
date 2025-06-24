# Stage 1: Ingestão de Landing para Bronze

O primeiro estágio de processamento no nosso pipeline ETL é a movimentação dos dados brutos da **Camada Landing (`data/raw/`)** para a **Camada Bronze (`data/bronze/`)**. Este processo é orquestrado e executado através do notebook Jupyter `notebooks/notebook_landing_bronze.ipynb`.

**Objetivo:**

* **Ingestão Segura:** Garantir que todos os arquivos CSV brutos da camada Landing sejam lidos com sucesso.
* **Validação de Leitura:** Confirmar que os dados podem ser carregados corretamente em DataFrames do Pandas, identificando problemas básicos de formato de arquivo, se existirem.
* **Persistência Consistente:** Salvar os dados lidos em novos arquivos CSV na camada Bronze, estabelecendo um ponto de partida limpo e validado para as transformações futuras.

**Ferramentas Utilizadas:**

* **Jupyter Notebook:** `notebooks/notebook_landing_bronze.ipynb`
* **Python:** Linguagem de programação para o script.
* **Pandas:** Biblioteca para manipulação e carregamento de DataFrames.

**Entrada:**

* Arquivos CSV localizados na pasta `data/raw/` (provenientes da geração de dados brutos).

**Saída:**

* Arquivos CSV idênticos aos de entrada, porém agora salvos na pasta `data/bronze/`.

**Processo Detalhado e Transformações Aplicadas:**

O `notebook_landing_bronze.ipynb` realiza as seguintes operações para cada arquivo CSV presente na camada Landing:

1.  **Iteração sobre Arquivos Raw:** O notebook itera sobre todos os arquivos `.csv` encontrados dentro da pasta `data/raw/`.
2.  **Leitura do CSV:** Para cada arquivo, o Pandas é utilizado para ler o conteúdo do CSV em um DataFrame.
    ```python
    import pandas as pd
    import os

    # Exemplo simplificado de leitura
    file_path_raw = 'data/raw/paciente.csv' # Caminho real seria dinâmico
    df = pd.read_csv(file_path_raw)
    ```
3.  **Criação da Pasta Bronze (se necessário):** Verifica se a pasta `data/bronze/` existe. Se não, ela é criada para armazenar os arquivos processados.
4.  **Persistência na Camada Bronze:** O DataFrame lido é então salvo como um novo arquivo CSV no caminho correspondente dentro da pasta `data/bronze/`. Isso assegura que a camada Bronze contenha uma cópia "limpa" dos dados brutos, pronta para a próxima etapa.
    ```python
    output_path_bronze = 'data/bronze/paciente.csv' # Caminho real seria dinâmico
    df.to_csv(output_path_bronze, index=False)
    ```
5.  **Verificação Básica (Implícita):** Embora não haja transformações complexas ou validações de dados nesta etapa, a simples operação de leitura e escrita do Pandas serve como uma validação implícita de que os arquivos não estão corrompidos e são legíveis. Qualquer erro na leitura ou escrita seria sinalizado neste ponto.

Esta etapa é crucial para estabelecer a camada Bronze como um ponto de controle e garantir a integridade básica dos dados antes de qualquer transformação complexa ser aplicada.