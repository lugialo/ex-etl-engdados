# Camada Landing (Raw)

A camada Landing, também conhecida como Raw, é a primeira etapa do nosso Data Lake. Seu principal objetivo é receber os dados diretamente das fontes de origem, sem qualquer tipo de transformação, limpeza ou validação de conteúdo.

**Propósito:**

* **Ingestão Bruta:** Servir como o ponto de entrada inicial para todos os dados provenientes das fontes.
* **Preservação:** Manter os dados em seu formato original e intacto, exatamente como foram gerados pela fonte. Isso é crucial para auditoria, rastreabilidade e para garantir que, se houver um erro em etapas posteriores, podemos sempre retornar à fonte original.
* **Imutabilidade:** Os dados nesta camada são considerados imutáveis. Uma vez que um arquivo é gravado na Landing Zone, ele não deve ser alterado.

**Características:**

* **Formato:** Os dados são armazenados em arquivos CSV, replicando a estrutura da fonte de origem.
* **Conteúdo:** Contém todos os dados, incluindo possíveis inconsistências, erros ou duplicações que existiam na fonte original.
* **Estrutura de Armazenamento:**
    * Os dados são organizados em subpastas, como `data/raw/`.
    * Cada tipo de entidade (por exemplo, `paciente.csv`, `consulta.csv`, `odontologista.csv`, `procedimento.csv`, `pagamento.csv`, `tipo_pagamento.csv`, `endereco.csv`, `agendamento.csv`, `consulta_procedimento.csv`, `log_pagamento.csv`) tem seu próprio arquivo CSV correspondente na pasta `data/raw/`.

Nesta fase, o foco é apenas na coleta eficiente e segura dos dados, deixando as etapas de refinamento para as camadas subsequentes do Data Lake.