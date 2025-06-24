# Modelo Dimensional (Data Warehouse)

O modelo dimensional é a estrutura final dos dados na camada Gold, projetada especificamente para análise de negócios e geração de relatórios. Ele adota o padrão de **Esquema Estrela (Star Schema)**, que é otimizado para consultas de agregação e facilidade de entendimento por usuários de negócio.

**Propósito:**

* **Análise Simplificada:** Oferecer uma estrutura de dados intuitiva que permite aos analistas de negócio consultar facilmente as informações sem a necessidade de entender complexidades de normalização.
* **Desempenho de Consulta:** Otimizar o desempenho de consultas agregadas, que são comuns em ferramentas de Business Intelligence (BI).
* **Flexibilidade:** Permitir a adição de novas métricas e atributos dimensionais com impacto mínimo na estrutura existente.

**Visão Geral do Esquema Estrela:**

O Esquema Estrela consiste em uma **Tabela de Fato** central e várias **Tabelas de Dimensão** que se conectam diretamente a ela.

* **Tabelas de Fato:** Contêm as métricas quantitativas (o "o quê" aconteceu) e as chaves estrangeiras que apontam para as tabelas de dimensão.
* **Tabelas de Dimensão:** Contêm os atributos descritivos (o "quem", "quando", "onde", "como") que fornecem contexto às métricas da tabela de fato.

**Detalhes das Tabelas do Modelo Dimensional:**

### Tabela de Fato: `fato_consultas_e_pagamentos`

* **Descrição:** Esta é a tabela de fato principal que captura os eventos de consultas e os pagamentos associados. Ela contém as métricas de negócio e as chaves estrangeiras para as dimensões que fornecem o contexto desses eventos.
* **Granularidade:** Uma linha por evento de consulta/pagamento.
* **Métricas (Exemplos):**
    * `valor_total_pago`: O valor monetário total transacionado.
    * `quantidade_procedimentos`: O número de procedimentos realizados em uma consulta.
    * `duracao_minutos`: A duração estimada da consulta em minutos.
* **Chaves Estrangeiras (para Dimensões):**
    * `id_tempo_sk`: Chave para a `dim_tempo`.
    * `id_paciente_sk`: Chave para a `dim_paciente`.
    * `id_odontologista_sk`: Chave para a `dim_odontologista`.
    * `id_procedimento_sk`: Chave para a `dim_procedimento`.
    * `id_tipo_pagamento_sk`: Chave para a `dim_tipo_pagamento`.

### Dimensões:

As tabelas de dimensão fornecem o contexto para as métricas da tabela de fato, permitindo a análise por diferentes perspectivas.

#### 1. `dim_paciente`
* **Descrição:** Detalhes dos pacientes.
* **Atributos (Exemplos):** `nome_paciente`, `data_nascimento`, `genero`, `telefone`, `email`, `endereco_completo`, `idade`, etc.

#### 2. `dim_odontologista`
* **Descrição:** Detalhes dos profissionais odontologistas.
* **Atributos (Exemplos):** `nome_odontologista`, `especialidade`, `CRO`, etc.

#### 3. `dim_procedimento`
* **Descrição:** Informações sobre os procedimentos oferecidos pela clínica.
* **Atributos (Exemplos):** `nome_procedimento`, `descricao_procedimento`, `custo_base`, etc.

#### 4. `dim_tipo_pagamento`
* **Descrição:** Detalhes sobre os tipos de pagamento.
* **Atributos (Exemplos):** `descricao_tipo_pagamento`.

#### 5. `dim_tempo`
* **Descrição:** Dimensão de tempo para análise temporal de eventos.
* **Atributos (Exemplos):** `data_completa`, `ano`, `mes`, `nome_mes`, `dia_do_mes`, `dia_da_semana`, `trimestre`, `semestre`, `feriado`, etc. (Permite fatiar e agregar dados por qualquer período de tempo).

**Benefícios do Modelo Dimensional:**

* **Performance:** Consultas que envolvem agregações e filtros são muito mais rápidas devido à desnormalização e menor número de joins complexos.
* **Simplicidade:** O modelo é intuitivo e fácil de entender, o que empodera os usuários de negócio a fazerem suas próprias análises com menor dependência de TI.
* **Manutenibilidade:** Adicionar novas métricas ou atributos a dimensões existentes geralmente não requer mudanças drásticas no modelo.

Este modelo representa a forma final como os dados são apresentados para consumo, tornando a análise de dados sobre as operações da clínica odontológica eficiente e acessível.