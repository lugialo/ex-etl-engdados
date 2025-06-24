# Geração de Dados Brutos

O primeiro passo no nosso pipeline ETL é a geração de uma massa de dados simulada que servirá como as fontes de dados brutas para o projeto. Este processo é executado através do script Python `scripts/gerador_dados.py`.

**Propósito:**

* **Simulação de Fontes:** Criar um conjunto de dados realistas que imitam as operações de uma clínica odontológica, permitindo o desenvolvimento e teste do pipeline ETL sem depender de dados sensíveis ou complexos de sistemas reais.
* **Volumetria e Variedade:** Gerar um volume considerável de dados e uma variedade de entidades para demonstrar a capacidade do pipeline em lidar com diferentes tipos de informação e escala.

**Ferramenta Utilizada:**

* **Script Python:** `scripts/gerador_dados.py`
* **Biblioteca:** `Faker` (para gerar dados fictícios como nomes, endereços, datas, etc.)

**Entidades Geradas:**

O script `gerador_dados.py` cria arquivos CSV para as seguintes entidades, que representam as principais informações de uma clínica odontológica:

* `agendamento.csv`: Detalhes sobre os agendamentos de consultas.
* `consulta.csv`: Informações sobre as consultas realizadas.
* `consulta_procedimento.csv`: Relação entre consultas e procedimentos realizados.
* `endereco.csv`: Dados de endereço dos pacientes e odontologistas.
* `log_pagamento.csv`: Registros de logs relacionados a pagamentos.
* `odontologista.csv`: Informações sobre os profissionais odontologistas.
* `paciente.csv`: Dados cadastrais dos pacientes.
* `pagamento.csv`: Registros dos pagamentos efetuados pelos pacientes.
* `procedimento.csv`: Catálogo de procedimentos oferecidos pela clínica.
* `tipo_pagamento.csv`: Tipos de métodos de pagamento.

**Processo Detalhado:**

1.  **Geração de Dados Fictícios:** O script utiliza a biblioteca `Faker` para criar dados realistas para cada campo de cada entidade (e.g., nomes de pacientes, datas de agendamento, valores de procedimentos).
2.  **Criação de Relacionamentos:** O script é projetado para gerar dados de forma que os relacionamentos entre as entidades sejam mantidos (e.g., um `agendamento` referencia um `paciente` e um `odontologista` válidos).
3.  **Exportação para CSV:** Após a geração, os dados de cada entidade são exportados para arquivos `.csv` individuais e salvos na pasta `data/raw/`, que serve como a camada Landing do nosso pipeline.

Para executar a geração de dados, basta rodar o script Python:

```bash
python scripts/gerador_dados.py