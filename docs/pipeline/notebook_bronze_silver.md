# Stage 2: Transformação de Bronze para Silver

O `notebooks/notebook_bronze_silver.ipynb` é o coração do nosso pipeline de ETL, onde os dados da Camada Bronze são submetidos a um processo rigoroso de limpeza, validação e transformação. O objetivo final é produzir dados de alta qualidade na Camada Silver (`data/silver/`), prontos para análises e modelagem dimensional.

**Objetivo:**

* **Limpeza de Dados:** Tratar valores nulos, inconsistências, duplicatas e erros de digitação.
* **Padronização de Formatos:** Uniformizar o formato de datas, strings e outros tipos de dados.
* **Enriquecimento de Dados:** Adicionar informações derivadas ou combinar datasets para criar um conjunto de dados mais completo e útil.
* **Aplicação de Regras de Negócio:** Implementar lógicas específicas que garantam a consistência e a validade dos dados conforme os requisitos do negócio da clínica.

**Ferramentas Utilizadas:**

* **Jupyter Notebook:** `notebooks/notebook_bronze_silver.ipynb`
* **Python:** Linguagem de programação principal.
* **Pandas:** Biblioteca essencial para manipulação e transformação de DataFrames.

**Entrada:**

* Arquivos CSV localizados na pasta `data/bronze/` (dados após a ingestão básica).

**Saída:**

* Arquivos CSV transformados e limpos, salvos na pasta `data/silver/`.

**Processo Detalhado e Principais Transformações:**

Para cada entidade (Pacientes, Consultas, Odontologistas, etc.), o notebook `notebook_bronze_silver.ipynb` executa uma série de transformações. Abaixo estão os tipos de operações que tipicamente são realizadas:

1.  **Carregamento dos Dados:**
    * Todos os arquivos CSV da pasta `data/bronze/` são carregados em DataFrames do Pandas.
    * Exemplo: Carregamento de `paciente.csv`, `consulta.csv`, `agendamento.csv`, `procedimento.csv`, `pagamento.csv`, `tipo_pagamento.csv`, `odontologista.csv`, `endereco.csv`, `consulta_procedimento.csv`, `log_pagamento.csv`.

2.  **Tratamento de Valores Nulos (Missing Values):**
    * **Identificação:** Verificação de colunas com alta porcentagem de valores nulos.
    * **Imputação/Remoção:** Decisões são tomadas com base na relevância da coluna:
        * Preencher nulos com valores padrão (e.g., `telefone` com "Não Informado", `email` com "email_nao_informado@dominio.com").
        * Preencher valores numéricos nulos com média, mediana ou zero, se aplicável.
        * Remover linhas inteiras se valores críticos (como `id_paciente` ou `data_consulta`) estiverem nulos.
    * Exemplo: `df_pacientes['telefone'].fillna('Não Informado', inplace=True)`.

3.  **Padronização de Formatos de Dados:**
    * **Datas:** Conversão de colunas de data (e.g., `data_consulta`, `data_agendamento`, `data_nascimento`) para o formato `YYYY-MM-DD` e tipo `datetime`.
        * Exemplo: `pd.to_datetime(df_consultas['data_consulta'], errors='coerce')`.
    * **Strings:** Padronização de case (minúsculas, maiúsculas, título), remoção de espaços extras, caracteres especiais indesejados.
        * Exemplo: `df_pacientes['nome'].str.strip().str.title()`.
    * **Valores Numéricos:** Garantir que colunas como `valor_pago`, `custo` estejam no tipo numérico correto (float ou int) e sem caracteres inválidos.

4.  **Remoção de Duplicatas:**
    * Identificação e remoção de registros duplicados em tabelas que devem ter entradas únicas (e.g., `paciente`, `odontologista`, `procedimento`).
    * Exemplo: `df_pacientes.drop_duplicates(subset=['id_paciente'], inplace=True)`.

5.  **Validação e Consistência de Dados:**
    * Verificações de sanidade:
        * Idades de pacientes razoáveis (e.g., não negativas ou muito altas).
        * Valores de pagamento positivos.
        * Integridade referencial básica (garantir que IDs referenciados em uma tabela existam em outra, antes de uni-las).
    * Correção de inconsistências lógicas se identificadas.

6.  **Enriquecimento de Dados e Criação de Novas Features:**
    * **Cálculo de Idade:** Adicionar uma coluna `idade` na tabela de pacientes.
    * **Derivação de Tempo:** Extrair `ano`, `mes`, `dia_semana` de colunas de data.
    * **Combinar Dados:** Realizar `merges` ou `joins` entre DataFrames para consolidar informações.
        * Exemplo: Unir `df_pagamentos` com `df_tipo_pagamento` para adicionar a descrição do tipo de pagamento diretamente nos registros de pagamento.
        * Exemplo: Unir `df_consultas` com `df_pacientes` e `df_odontologistas` para consolidar informações em uma única tabela de eventos de consulta.

7.  **Persistência na Camada Silver:**
    * Após todas as transformações, os DataFrames resultantes são salvos como novos arquivos CSV na pasta `data/silver/`. Cada arquivo reflete a entidade correspondente, agora limpa e padronizada.
    * Exemplo: `df_pacientes_clean.to_csv('data/silver/paciente_silver.csv', index=False)`.

Esta etapa é a mais intensiva em termos de processamento de dados e garante que a camada Gold receberá dados de alta qualidade e consistência para a modelagem analítica.