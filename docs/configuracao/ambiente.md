# Configuração de Ambiente

Este guia detalha como configurar o ambiente de desenvolvimento para o projeto ETL de clínicas odontológicas.

## Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para configuração flexível. Copie o arquivo `.env.example` para `.env` e configure as seguintes variáveis:

### Configurações do Banco de Dados

```bash
# Configurações do PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clinica_odonto
DB_USER=root
DB_PASSWORD=root
```

**Descrição das variáveis:**
- `DB_HOST`: Endereço do servidor PostgreSQL
- `DB_PORT`: Porta do PostgreSQL (padrão: 5432)
- `DB_NAME`: Nome do banco de dados
- `DB_USER`: Usuário do banco
- `DB_PASSWORD`: Senha do usuário

### Configurações do Azure Storage

```bash
# Azure Storage Account Configuration
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=seu_storage_account;AccountKey=sua_chave_de_acesso;EndpointSuffix=core.windows.net

# Nome do container no Azure Storage
AZURE_CONTAINER_NAME=landingzone
```

**Descrição das variáveis:**
- `AZURE_STORAGE_CONNECTION_STRING`: String de conexão completa do Azure Storage
- `AZURE_CONTAINER_NAME`: Nome do container onde os dados serão armazenados

## Obtendo Credenciais do Azure

### 1. Azure Storage Connection String

1. Acesse o [Portal Azure](https://portal.azure.com)
2. Navegue até sua Storage Account
3. No menu lateral, clique em **Access keys**
4. Copie a **Connection string** da Key1 ou Key2

### 2. Container Name

O container será criado automaticamente pelo script se não existir. Você pode usar:
- `landingzone` - para dados brutos
- `bronze` - para dados processados
- `silver` - para dados limpos
- `gold` - para dados agregados

## Estrutura de Arquivos de Configuração

```
.
├── .env                    # Suas configurações (não versionado)
├── .env.example           # Exemplo de configuração
├── docker/
│   └── docker-compose.yml # Configuração do PostgreSQL
└── terraform/
    ├── variables.tf       # Variáveis do Terraform
    └── terraform.tfvars   # Valores das variáveis (criar manualmente)
```

## Validação da Configuração

Após configurar as variáveis de ambiente, você pode validar a configuração:

```bash
# Testar conexão com banco de dados
python scripts/teste_db.py

# Testar geração de dados
python scripts/gerador_dados.py
```

## Troubleshooting

### Erro de Conexão com Banco

Se você receber erros de conexão com o PostgreSQL:

1. Verifique se o Docker está rodando:
   ```bash
   docker ps
   ```

2. Verifique os logs do container:
   ```bash
   docker-compose -f docker/docker-compose.yml logs db
   ```

3. Teste a conexão manualmente:
   ```bash
   psql -h localhost -U root -d clinica_odonto
   ```

### Erro de Azure Storage

Se você receber erros relacionados ao Azure Storage:

1. Verifique se a connection string está correta
2. Confirme se você tem permissões para criar containers
3. Teste a conexão usando Azure Storage Explorer

### Dependências Python

Se houver problemas com dependências:

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar versões instaladas
pip list
```
