# Camada Bronze

A camada Bronze do nosso Data Lake representa o primeiro estágio de ingestão e validação inicial dos dados brutos que vêm da camada Landing. Embora os dados aqui ainda sejam "crus" em termos de transformações de negócio, eles já passaram por um processo básico de garantia de que são legíveis e válidos em seu formato.

**Propósito:**

* **Ingestão Validada:** Ler os arquivos da camada Landing e salvá-los novamente, garantindo que o processo de leitura e escrita não introduziu erros e que os dados estão em um formato acessível para processamento posterior.
* **Armazenamento Consistente:** Padronizar o formato de armazenamento (se houver necessidade de conversão, por exemplo, de CSV para Parquet, embora neste projeto mantenhamos CSV para simplicidade).
* **Ponto de Partida:** Servir como o ponto de partida para todas as transformações de limpeza e enriquecimento que ocorrerão na camada Silver.

**Características:**

* **Conteúdo Quase Bruto:** Os dados são quase idênticos aos da camada Landing, mas com a garantia de que foram lidos e escritos com sucesso. Pequenas correções de formatação de arquivo podem ocorrer, mas nenhuma regra de negócio é aplicada nesta fase.
* **Rastreabilidade:** Permite a rastreabilidade entre os dados brutos e os dados prontos para transformação.
* **Estrutura de Armazenamento:**
    * Os dados são persistidos na pasta `data/bronze/`.
    * Cada tipo de entidade (paciente, consulta, etc.) terá seu arquivo CSV correspondente aqui, espelhando a estrutura da camada Landing.

**Processo Detalhado (via `notebook_landing_bronze.ipynb`):**

O notebook `notebook_landing_bronze.ipynb` é responsável por esta etapa. Ele realiza as seguintes operações:

1.  **Leitura da Camada Landing:** Lê os arquivos CSV presentes na pasta `data/raw/`.
2.  **Verificação Básica:** Realiza uma verificação básica da estrutura dos arquivos, garantindo que eles podem ser carregados corretamente em DataFrames do Pandas.
3.  **Persistência na Camada Bronze:** Salva os DataFrames resultantes como novos arquivos CSV na pasta `data/bronze/`. Isso garante que qualquer erro de formato que impeça a leitura do arquivo raw seja identificado, e que a próxima etapa não dependa da leitura direta dos arquivos originais.