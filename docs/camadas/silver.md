# Camada Silver

A camada Silver (também conhecida como camada Refinada ou Consolidada) é onde os dados brutos da camada Bronze são transformados em um formato limpo, padronizado e validado, pronto para ser consumido em análises mais detalhadas ou para a construção do Data Warehouse na camada Gold. Esta camada é o coração do nosso processo de ETL, pois é aqui que as principais regras de negócio para tratamento de dados são aplicadas.

**Propósito:**

* **Limpeza e Padronização:** Remover inconsistências, tratar valores nulos, padronizar formatos (datas, textos, números) e corrigir erros de digitação ou formatação.
* **Enriquecimento:** Adicionar novas colunas ou derivar informações a partir dos dados existentes, aplicando regras de negócio específicas.
* **Consistência:** Garantir que os dados estejam em um formato consistente e confiável para as etapas subsequentes do pipeline.
* **Consolidação:** Integrar dados de diferentes fontes (se aplicável), criando um conjunto de dados unificado e coerente.

**Características:**

* **Qualidade Assegurada:** Os dados nesta camada possuem alta qualidade, sendo confiáveis para uso analítico.
* **Estrutura Definida:** Embora ainda possam estar em formato de arquivo (CSV), a estrutura de cada entidade já está bem definida e padronizada.
* **Rastreabilidade:** É possível rastrear os dados até a camada Bronze e, consequentemente, até a Landing.

**Processo Detalhado (via `notebook_bronze_silver.ipynb`):**

O notebook `notebook_bronze_silver.ipynb` é o responsável por orquestrar as transformações necessárias para mover os dados da camada Bronze para a Silver. As operações realizadas incluem, mas não se limitam a:

1.  **Carregamento:** Todos os arquivos CSV da pasta `data/bronze/` são carregados em DataFrames do Pandas.
2.  **Tratamento de Valores Nulos:**
    * Identificação e substituição de valores nulos em colunas como `telefone`, `email` ou `data_nascimento` (por exemplo, preenchendo com "Não Informado" ou um valor padrão, ou removendo registros se a informação for crítica).
    * Exemplo: Colunas de endereço podem ter nulos preenchidos com "N/A" ou inferidos.
3.  **Padronização de Formatos:**
    * **Datas:** Conversão de todas as colunas de data (e.g., `data_consulta`, `data_agendamento`, `data_nascimento`) para um formato uniforme (Ex: `YYYY-MM-DD`).
    * **Strings:** Normalização de campos de texto (e.g., `nome_paciente`, `nome_odontologista`) para um padrão consistente (Ex: título, maiúsculas, minúsculas).
    * **Valores Numéricos:** Garantir que colunas numéricas estejam no tipo de dado correto e sem valores inválidos.
4.  **Remoção de Duplicatas:** Eliminação de registros duplicados com base em chaves de identificação (e.g., `id_paciente`, `id_odontologista`) para garantir a unicidade.
5.  **Validação e Consistência de Dados:**
    * Verificação de integridade referencial básica (e.g., se um `id_paciente` em `agendamento` realmente existe na tabela de pacientes).
    * Aplicação de regras de negócio (e.g., verificar se a `data_agendamento` é anterior à `data_consulta`).
6.  **Enriquecimento de Dados:**
    * Criação de novas colunas derivadas, como `idade` a partir de `data_nascimento` ou `dia_semana` a partir de `data_consulta`.
    * Combinação de tabelas (joins) para adicionar informações relevantes. Por exemplo, unindo `pagamento` com `tipo_pagamento` para adicionar a descrição do tipo de pagamento.
7.  **Persistência:** Os DataFrames transformados e limpos são salvos como novos arquivos CSV na pasta `data/silver/`, prontos para a próxima etapa.