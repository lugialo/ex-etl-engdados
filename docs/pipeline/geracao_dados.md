# Geração de Dados Brutos

O primeiro passo no nosso pipeline ETL é a geração de uma massa de dados simulada que servirá como as fontes de dados brutas para o projeto. Este processo é executado através do script Python `scripts/gerador_dados.py`, que foi significativamente aprimorado com novas funcionalidades.

## Propósito

* **Simulação de Fontes:** Criar um conjunto de dados realistas que imitam as operações de uma clínica odontológica, permitindo o desenvolvimento e teste do pipeline ETL sem depender de dados sensíveis ou complexos de sistemas reais.
* **Volumetria e Variedade:** Gerar um volume considerável de dados e uma variedade de entidades para demonstrar a capacidade do pipeline em lidar com diferentes tipos de informação e escala.
* **Integração Completa:** Conectar diretamente com banco de dados PostgreSQL e Azure Storage para simular um ambiente de produção.

## Novas Funcionalidades (Versão 2.0)

### 🔄 Integração com Banco de Dados
- **Conexão PostgreSQL**: Conecta automaticamente com o banco usando SQLAlchemy
- **Criação de Tabelas**: Cria estrutura completa do modelo físico
- **População Automática**: Insere dados diretamente nas tabelas
- **Limpeza Inteligente**: Remove dados antigos antes de gerar novos

### ☁️ Integração com Azure Storage
- **Upload Automático**: Envia CSVs para Azure Blob Storage
- **Configuração Flexível**: Usa variáveis de ambiente para credenciais
- **Estrutura Organizada**: Cria hierarquia de pastas apropriada

### 🔧 Configuração via Ambiente
- **Arquivo .env**: Configurações centralizadas
- **Flexibilidade**: Suporte a diferentes ambientes (dev, prod)
- **Segurança**: Credenciais não ficam no código

### 📊 Logging e Monitoramento
- **Logs Detalhados**: Acompanhe cada etapa do processo
- **Tratamento de Erros**: Mensagens claras em caso de problemas
- **Progresso Visual**: Indicadores de progresso para operações longas

## Ferramentas Utilizadas

* **Script Python:** `scripts/gerador_dados.py`
* **Bibliotecas:**
  - `Faker`: Geração de dados fictícios realistas
  - `SQLAlchemy`: Conexão e operações com banco de dados
  - `Azure Storage Blob`: Upload para nuvem Azure
  - `python-dotenv`: Gerenciamento de variáveis de ambiente
  - `logging`: Sistema de logs robusto

## Entidades Geradas

O script `gerador_dados.py` cria dados para as seguintes entidades:

| Entidade | Arquivo CSV | Descrição |
|----------|-------------|-----------|
| `endereco` | `endereco.csv` | Dados de endereço (CEP, rua, cidade, estado) |
| `odontologista` | `odontologista.csv` | Profissionais (nome, CRO, especialidade) |
| `paciente` | `paciente.csv` | Pacientes (nome, CPF, telefone, email) |
| `tipo_pagamento` | `tipo_pagamento.csv` | Métodos de pagamento (cartão, dinheiro, PIX) |
| `procedimento` | `procedimento.csv` | Catálogo de procedimentos odontológicos |
| `agendamento` | `agendamento.csv` | Agendamentos de consultas |
| `consulta` | `consulta.csv` | Consultas realizadas |
| `consulta_procedimento` | `consulta_procedimento.csv` | Relação consulta × procedimento |
| `pagamento` | `pagamento.csv` | Registros de pagamentos |
| `log_pagamento` | `log_pagamento.csv` | Logs de transações |

## Configuração

### 1. Variáveis de Ambiente

Configure o arquivo `.env`:

```bash
# Banco de Dados PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clinica_odonto
DB_USER=root
DB_PASSWORD=root

# Azure Storage (opcional)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_CONTAINER_NAME=landingzone
```

### 2. Parâmetros de Volume

No código, você pode ajustar a quantidade de dados:

```python
# Configurações de volume
NUM_ENDERECOS = 10000
NUM_ODONTOLOGISTAS = 50
NUM_PACIENTES = 20000
NUM_PROCEDIMENTOS = 200
NUM_AGENDAMENTOS = 30000
NUM_CONSULTAS = 25000
NUM_PAGAMENTOS = 25000
NUM_LOGS_PAGAMENTO = 30000
```

## Processo de Execução

### 1. Preparação do Ambiente

```bash
# Verificar conexão com banco
python scripts/teste_db.py

# Executar gerador
python scripts/gerador_dados.py
```

### 2. Fluxo de Execução

1. **Inicialização**
   - Carrega variáveis de ambiente
   - Conecta ao banco PostgreSQL
   - Configura Azure Storage (se disponível)

2. **Preparação do Banco**
   - Cria estrutura de tabelas
   - Limpa dados existentes
   - Configura constraints

3. **Geração de Dados**
   - Gera dados para cada entidade
   - Mantém integridade referencial
   - Aplica regras de negócio

4. **Persistência**
   - Insere dados no banco PostgreSQL
   - Exporta para CSV local (`data/raw/`)
   - Upload para Azure Storage (se configurado)

5. **Validação**
   - Verifica integridade dos dados
   - Gera relatório de contagem
   - Registra logs de sucesso/erro

### 3. Saídas Geradas

#### Arquivos Locais
```
data/raw/
├── agendamento.csv
├── consulta.csv
├── consulta_procedimento.csv
├── endereco.csv
├── log_pagamento.csv
├── odontologista.csv
├── paciente.csv
├── pagamento.csv
├── procedimento.csv
└── tipo_pagamento.csv
```

#### Banco PostgreSQL
- Tabelas populadas com dados
- Índices e constraints aplicados
- Dados prontos para análise

#### Azure Storage (se configurado)
```
landingzone/
└── raw/
    ├── agendamento.csv
    ├── consulta.csv
    └── ... (outros arquivos)
```

## Logs e Monitoramento

### Exemplo de Log de Execução

```
2024-12-25 10:30:15 - INFO - Iniciando geração de dados...
2024-12-25 10:30:16 - INFO - Conectado ao banco PostgreSQL
2024-12-25 10:30:17 - INFO - Azure Storage configurado
2024-12-25 10:30:18 - INFO - Criando e limpando tabelas...
2024-12-25 10:30:25 - INFO - Gerando 10000 endereços...
2024-12-25 10:30:28 - INFO - Gerando 50 odontologistas...
2024-12-25 10:30:30 - INFO - ✅ Dados inseridos com sucesso no banco
2024-12-25 10:30:32 - INFO - ✅ CSVs exportados para data/raw/
2024-12-25 10:30:35 - INFO - ✅ Upload para Azure Storage concluído
2024-12-25 10:30:35 - INFO - 🎉 Processo concluído com sucesso!
```

## Tratamento de Erros

### Problemas Comuns

1. **Erro de Conexão com Banco**
   ```bash
   ERROR - Erro ao conectar ao banco: connection refused
   # Solução: Verificar se PostgreSQL está rodando
   docker-compose -f docker/docker-compose.yml up -d
   ```

2. **Erro do Azure Storage**
   ```bash
   WARNING - Azure Storage não configurado, pulando upload
   # Solução: Configurar AZURE_STORAGE_CONNECTION_STRING no .env
   ```

3. **Erro de Dependências**
   ```bash
   ModuleNotFoundError: No module named 'azure'
   # Solução: Instalar dependências
   pip install -r requirements.txt
   ```

## Para Executar

```bash
# Execução simples
python scripts/gerador_dados.py

# Com logs detalhados
python scripts/gerador_dados.py 2>&1 | tee gerador.log

# Verificar resultados
ls -la data/raw/
psql -h localhost -U root -d clinica_odonto -c "SELECT COUNT(*) FROM paciente;"
```

Este processo garante que tenhamos uma base sólida de dados para alimentar todo o pipeline ETL, desde a camada Landing até o Data Warehouse final.