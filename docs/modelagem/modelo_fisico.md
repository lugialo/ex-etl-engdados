# Modelo Físico do Banco de Dados

O modelo físico do banco de dados descreve a implementação real das tabelas, colunas, tipos de dados, chaves primárias e chaves estrangeiras que compõem o nosso Data Warehouse na camada Gold. Este modelo é criado e gerenciado pelo script SQL `scripts/modelo_fisico.sql`.

**Propósito:**

* **Estrutura da Base de Dados:** Definir a estrutura exata das tabelas que armazenarão os dados finais, garantindo a integridade e a consistência dos dados.
* **Otimização:** Estabelecer índices e restrições que otimizem o desempenho das consultas analíticas e a integridade referencial.
* **Base para Carregamento:** Fornecer a estrutura necessária para que o pipeline ETL (`notebook_silver_gold.ipynb`) possa carregar os dados transformados.

**Ferramenta Utilizada:**

* **Script SQL:** `scripts/modelo_fisico.sql` (executado no PostgreSQL ou outro SGBD relacional).

**Visão Geral das Tabelas Criadas:**

O script `modelo_fisico.sql` é responsável por criar as tabelas que servirão de base para as dimensões e fatos do nosso modelo dimensional. Embora a camada Gold use um modelo dimensional, as tabelas físicas podem ser criadas com base na estrutura final que receberá os dados.

Abaixo, descrevemos a estrutura provável das tabelas que este script cria, com base nas entidades do seu projeto:

### Tabela `dim_paciente`
* **Descrição:** Armazena informações detalhadas sobre os pacientes da clínica.
* **Colunas:**
    * `id_paciente` (PRIMARY KEY): Identificador único do paciente.
    * `nome_paciente`: Nome completo do paciente.
    * `data_nascimento`: Data de nascimento do paciente.
    * `genero`: Gênero do paciente.
    * `telefone`: Número de telefone de contato.
    * `email`: Endereço de e-mail.
    * `endereco_completo`: Endereço combinado (rua, número, bairro, cidade, estado, CEP).
    * `idade`: Idade calculada do paciente.
    * *(Outras colunas relevantes do paciente)*

### Tabela `dim_odontologista`
* **Descrição:** Contém os dados dos profissionais odontologistas.
* **Colunas:**
    * `id_odontologista` (PRIMARY KEY): Identificador único do odontologista.
    * `nome_odontologista`: Nome completo do odontologista.
    * `especialidade`: Especialidade do profissional.
    * `CRO`: Número de registro no Conselho Regional de Odontologia.
    * *(Outras colunas relevantes do odontologista)*

### Tabela `dim_procedimento`
* **Descrição:** Detalhes sobre os procedimentos odontológicos oferecidos.
* **Colunas:**
    * `id_procedimento` (PRIMARY KEY): Identificador único do procedimento.
    * `nome_procedimento`: Nome descritivo do procedimento.
    * `descricao_procedimento`: Descrição detalhada do procedimento.
    * `custo_base`: Custo padrão do procedimento.
    * *(Outras colunas relevantes do procedimento)*

### Tabela `dim_tipo_pagamento`
* **Descrição:** Detalhes sobre os métodos de pagamento.
* **Colunas:**
    * `id_tipo_pagamento` (PRIMARY KEY): Identificador único do tipo de pagamento.
    * `descricao_tipo_pagamento`: Descrição do tipo de pagamento (ex: "Cartão de Crédito", "Dinheiro", "Plano de Saúde").

### Tabela `dim_tempo`
* **Descrição:** Tabela de dimensão de tempo para análises baseadas em período.
* **Colunas:**
    * `data_sk` (PRIMARY KEY): Chave suplicada para a data (ex: YYYYMMDD).
    * `data_completa`: Data no formato `YYYY-MM-DD`.
    * `ano`: Ano da data.
    * `mes`: Número do mês (1-12).
    * `nome_mes`: Nome do mês (ex: "Janeiro").
    * `dia_do_mes`: Dia do mês.
    * `dia_da_semana`: Dia da semana (ex: "Segunda-feira").
    * `trimestre`: Trimestre do ano.
    * `semestre`: Semestre do ano.
    * `feriado`: Indica se a data é um feriado (booleano/texto).
    * *(Outras colunas relevantes de tempo)*

### Tabela `fato_consultas_e_pagamentos`
* **Descrição:** Tabela de fato central que registra eventos de consultas e pagamentos, com métricas e chaves para as dimensões.
* **Colunas:**
    * `id_consulta_fato` (PRIMARY KEY): Identificador único da linha de fato (pode ser gerado).
    * `id_consulta_origem`: ID da consulta na origem (para rastreabilidade).
    * `data_sk` (FOREIGN KEY para `dim_tempo`): Chave da dimensão tempo.
    * `id_paciente_sk` (FOREIGN KEY para `dim_paciente`): Chave da dimensão paciente.
    * `id_odontologista_sk` (FOREIGN KEY para `dim_odontologista`): Chave da dimensão odontologista.
    * `id_procedimento_sk` (FOREIGN KEY para `dim_procedimento`): Chave da dimensão procedimento.
    * `id_tipo_pagamento_sk` (FOREIGN KEY para `dim_tipo_pagamento`): Chave da dimensão tipo de pagamento.
    * `valor_total_pago`: Métrica: Valor total pago pela consulta/procedimento.
    * `quantidade_procedimentos`: Métrica: Número de procedimentos realizados na consulta.
    * `duracao_minutos`: Métrica: Duração da consulta em minutos.
    * *(Outras métricas e chaves estrangeiras relevantes)*

**Exemplo de SQL (Estrutura Básica):**

```sql
-- Exemplo de criação de tabela dim_paciente
CREATE TABLE IF NOT EXISTS dim_paciente (
    id_paciente_sk SERIAL PRIMARY KEY,
    id_paciente VARCHAR(50) UNIQUE, -- ID da fonte original
    nome_paciente VARCHAR(255),
    data_nascimento DATE,
    genero VARCHAR(10),
    telefone VARCHAR(20),
    email VARCHAR(100),
    endereco_completo TEXT,
    idade INT
);

-- Exemplo de criação de tabela fato_consultas_e_pagamentos
CREATE TABLE IF NOT EXISTS fato_consultas_e_pagamentos (
    id_consulta_fato SERIAL PRIMARY KEY,
    id_consulta_origem VARCHAR(50),
    data_sk INT,
    id_paciente_sk INT,
    id_odontologista_sk INT,
    id_procedimento_sk INT,
    id_tipo_pagamento_sk INT,
    valor_total_pago NUMERIC(10, 2),
    quantidade_procedimentos INT,
    duracao_minutos INT,
    FOREIGN KEY (data_sk) REFERENCES dim_tempo(data_sk),
    FOREIGN KEY (id_paciente_sk) REFERENCES dim_paciente(id_paciente_sk),
    FOREIGN KEY (id_odontologista_sk) REFERENCES dim_odontologista(id_odontologista_sk),
    FOREIGN KEY (id_procedimento_sk) REFERENCES dim_procedimento(id_procedimento_sk),
    FOREIGN KEY (id_tipo_pagamento_sk) REFERENCES dim_tipo_pagamento(id_tipo_pagamento_sk)
);
-- ... (outras tabelas dim e fato)