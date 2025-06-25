# Como Executar o Projeto

Este guia completo mostra como executar o projeto ETL de clínicas odontológicas do início ao fim.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.9+
- Docker e Docker Compose
- Git
- Azure CLI (para deploy na nuvem)
- Terraform (para infraestrutura)

## Configuração Inicial

### 1. Clone e Configure o Projeto

```bash
# Clonar o repositório
git clone https://github.com/lugialo/ex-etl-engdados.git
cd ex-etl-engdados

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou .\venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar configurações (use seu editor preferido)
nano .env
```

**Configuração mínima para execução local:**
```bash
# Configurações do PostgreSQL (usando Docker)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clinica_odonto
DB_USER=root
DB_PASSWORD=root

# Azure Storage (opcional - deixe vazio para usar apenas localmente)
AZURE_STORAGE_CONNECTION_STRING=
AZURE_CONTAINER_NAME=landingzone
```

### 3. Subir o Banco de Dados

```bash
# Subir PostgreSQL via Docker
cd docker
docker-compose up -d
cd ..

# Verificar se está rodando
docker-compose -f docker/docker-compose.yml ps
```

### 4. Criar Estrutura do Banco

```bash
# Executar scripts de criação
psql -h localhost -U root -d clinica_odonto -f scripts/modelo_fisico.sql
psql -h localhost -U root -d clinica_odonto -f scripts/modelo_dimensional.sql
```

## Execução do Pipeline

### Opção 1: Execução Completa Automatizada

```bash
# Gerar dados e executar todo o pipeline
python scripts/gerador_dados.py

# Abrir Jupyter Lab
jupyter lab

# Executar notebooks na ordem:
# 1. notebook_landing_bronze.ipynb
# 2. notebook_bronze_silver.ipynb  
# 3. notebook_silver_gold.ipynb
```

### Opção 2: Execução Passo a Passo

#### Passo 1: Gerar Dados Brutos

```bash
python scripts/gerador_dados.py
```

**O que acontece:**
- ✅ Conecta ao banco PostgreSQL
- ✅ Cria e popula tabelas com dados sintéticos
- ✅ Exporta dados para CSV na pasta `data/raw/`
- ✅ Upload para Azure Storage (se configurado)
- ✅ Logs detalhados do processo

#### Passo 2: Landing → Bronze

```bash
jupyter lab notebooks/notebook_landing_bronze.ipynb
```

**O que acontece:**
- 📂 Lê CSVs da pasta `data/raw/`
- 🔧 Aplica tipagem básica aos dados
- 💾 Salva dados estruturados em `data/bronze/`

#### Passo 3: Bronze → Silver

```bash
jupyter lab notebooks/notebook_bronze_silver.ipynb
```

**O que acontece:**
- 🧹 Limpa e valida dados
- 🔄 Padroniza formatos
- ✅ Remove duplicatas e inconsistências
- 💾 Salva dados limpos em `data/silver/`

#### Passo 4: Silver → Gold

```bash
jupyter lab notebooks/notebook_silver_gold.ipynb
```

**O que acontece:**
- 📊 Agrega dados por dimensões de negócio
- 🏗️ Cria modelo dimensional (fatos e dimensões)
- 💾 Carrega dados no Data Warehouse (PostgreSQL)
- 💾 Salva agregações em `data/gold/`

## Validação dos Resultados

### Verificar Dados Gerados

```bash
# Ver arquivos CSV criados
ls -la data/raw/

# Ver estrutura das camadas
tree data/
```

### Consultar Banco de Dados

```bash
# Conectar ao banco
psql -h localhost -U root -d clinica_odonto

# Exemplos de queries
SELECT COUNT(*) FROM dim_paciente;
SELECT COUNT(*) FROM fato_consulta;
SELECT * FROM dim_tempo LIMIT 5;
```

### Verificar Logs

```bash
# Ver logs do Docker
docker-compose -f docker/docker-compose.yml logs -f

# Ver logs do gerador de dados
# (logs são exibidos no terminal durante execução)
```

## Execução com Azure (Opcional)

### 1. Deploy da Infraestrutura

```bash
# Fazer login na Azure
az login

# Configurar Terraform
cd terraform
terraform init
terraform plan
terraform apply

# Obter connection string
terraform output -raw storage_connection_string
```

### 2. Atualizar Configuração

```bash
# Atualizar .env com credenciais da Azure
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=..."
AZURE_CONTAINER_NAME=landingzone
```

### 3. Executar com Azure Storage

```bash
# Gerar dados (agora com upload para Azure)
python scripts/gerador_dados.py

# Os CSVs serão salvos localmente E na Azure
```

## Monitoramento e Debugging

### Verificar Status dos Serviços

```bash
# Docker
docker-compose -f docker/docker-compose.yml ps

# Conectividade com banco
python scripts/teste_db.py

# Azure Storage (se configurado)
az storage container list --connection-string "sua_connection_string"
```

### Logs Detalhados

```bash
# Logs do PostgreSQL
docker-compose -f docker/docker-compose.yml logs db

# Logs específicos do gerador
python scripts/gerador_dados.py 2>&1 | tee gerador.log
```

### Resolver Problemas Comuns

#### Erro de Conexão com Banco
```bash
# Verificar se container está rodando
docker ps | grep postgres

# Reiniciar se necessário
docker-compose -f docker/docker-compose.yml restart
```

#### Erro de Permissão no Azure
```bash
# Verificar login
az account show

# Verificar acesso ao storage
az storage account show --name seu_storage_account
```

#### Erro de Dependências Python
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar versões
pip list | grep -E "(pandas|sqlalchemy|azure)"
```

## Performance e Otimização

### Configurações para Datasets Maiores

No arquivo `scripts/gerador_dados.py`, ajuste:

```python
# Aumentar número de registros
NUM_ENDERECOS = 50000
NUM_PACIENTES = 100000
NUM_CONSULTAS = 500000
```

### Paralelização com Databricks

1. Deploy infraestrutura Terraform
2. Configure cluster Databricks
3. Upload notebooks para Databricks
4. Execute com maior poder computacional

## Documentação e Visualização

### Gerar Documentação

```bash
# Servidor local da documentação
mkdocs serve

# Acesse: http://127.0.0.1:8000
```

### Build para Produção

```bash
# Build estático
mkdocs build

# Deploy para GitHub Pages
mkdocs gh-deploy
```

## Limpeza do Ambiente

### Parar Serviços

```bash
# Parar Docker
docker-compose -f docker/docker-compose.yml down

# Desativar ambiente virtual
deactivate
```

### Limpeza Completa

```bash
# Remover dados locais
rm -rf data/bronze/ data/silver/ data/gold/

# Remover volumes Docker
docker-compose -f docker/docker-compose.yml down -v

# Destruir infraestrutura Azure
cd terraform
terraform destroy
```