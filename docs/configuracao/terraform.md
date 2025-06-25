# Terraform e Azure

Este projeto inclui configurações Terraform para provisionar infraestrutura na Azure, criando um ambiente completo de Data Lake com Azure Storage e Azure Databricks.

## Visão Geral da Infraestrutura

O Terraform cria os seguintes recursos na Azure:

### Recursos Principais

- **Resource Group**: `rgdata{company}{env}01`
- **Storage Account**: `stacdata{company}{env}01`
- **Storage Containers**: `landingzone`, `bronze`, `silver`, `gold`
- **Azure Databricks Workspace**: Para processamento de big data
- **Key Vault**: Para gerenciamento seguro de credenciais

### Organização por Camadas

```
Azure Storage Account
├── landingzone/     # Dados brutos ingeridos
├── bronze/          # Dados estruturados
├── silver/          # Dados limpos e validados
└── gold/            # Dados agregados e prontos para análise
```

## Arquivos Terraform

### main.tf
Contém a definição dos recursos principais:

```hcl
# Resource Group
resource "azurerm_resource_group" "rgdata01" {
  name     = "rgdata${var.company}${var.env}01"
  location = var.default_location
}

# Storage Account
resource "azurerm_storage_account" "stacdata01" {
  name                     = local.stgaccname
  resource_group_name      = azurerm_resource_group.rgdata01.name
  location                 = azurerm_resource_group.rgdata01.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true
}
```

### variables.tf
Define as variáveis configuráveis:

```hcl
variable "env" {
  type    = string
  default = ""
  description = "Ambiente (dev, prod, etc.)"
}

variable "company" {
  default = "trabalhoed"
  type    = string
  description = "Nome da empresa/projeto"
}

variable "default_location" {
  default = "Brazil South"
  type    = string
  description = "Região do Azure"
}
```

### providers.tf
Configura os provedores necessários:

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~>2.0"
    }
  }
}

provider "azurerm" {
  features {}
}
```

## Configuração e Deploy

### 1. Pré-requisitos

```bash
# Instalar Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Instalar Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Fazer login na Azure
az login
```

### 2. Configurar Variáveis

Crie um arquivo `terraform.tfvars`:

```hcl
env              = "dev"
company          = "suaempresa"
default_location = "Brazil South"
```

### 3. Executar Terraform

```bash
# Navegar para a pasta terraform
cd terraform

# Inicializar Terraform
terraform init

# Validar configuração
terraform validate

# Ver plano de execução
terraform plan

# Aplicar mudanças
terraform apply
```

## Recursos Criados

### Storage Account

- **Nome**: `stacdatatrabalhoeddev01` (exemplo)
- **Tipo**: Standard LRS
- **Hierarquia**: Habilitada (Data Lake Gen2)
- **Containers**: landingzone, bronze, silver, gold

### Azure Databricks

- **SKU**: Standard
- **Managed Resource Group**: Criado automaticamente
- **Integração**: Key Vault para secrets

### Key Vault

- **Policies**: Configuradas para Databricks
- **Secrets**: Conexões de banco e storage
- **Acesso**: Baseado em roles

## Configuração de Secrets

### Connection Strings

O Terraform configura automaticamente os secrets necessários:

```hcl
resource "azurerm_key_vault_secret" "storage_connection" {
  name         = "storage-connection-string"
  value        = azurerm_storage_account.stacdata01.primary_connection_string
  key_vault_id = azurerm_key_vault.kvdata01.id
}
```

### Databricks Secrets

```bash
# Configurar CLI do Databricks
databricks configure --token

# Criar scope de secrets
databricks secrets create-scope --scope "azkvscope"

# Listar secrets
databricks secrets list --scope "azkvscope"
```

## Customização

### Ambientes Múltiplos

Para criar ambientes separados:

```bash
# Desenvolvimento
terraform workspace new dev
terraform apply -var="env=dev"

# Produção
terraform workspace new prod
terraform apply -var="env=prod"
```

### Configurações Regionais

Para outras regiões:

```hcl
# terraform.tfvars
default_location = "East US"
# ou
default_location = "West Europe"
```

## Monitoramento e Gestão

### Outputs Importantes

O Terraform expõe informações úteis:

```hcl
output "storage_account_name" {
  value = azurerm_storage_account.stacdata01.name
}

output "storage_connection_string" {
  value     = azurerm_storage_account.stacdata01.primary_connection_string
  sensitive = true
}

output "databricks_workspace_url" {
  value = azurerm_databricks_workspace.dbw01.workspace_url
}
```

### Ver Outputs

```bash
# Ver todos os outputs
terraform output

# Ver output específico
terraform output storage_account_name

# Ver outputs sensíveis
terraform output -raw storage_connection_string
```

## Integração com o Pipeline ETL

### Atualizar .env

Após o deploy, atualize seu `.env`:

```bash
# Usar outputs do Terraform
export STORAGE_NAME=$(terraform output -raw storage_account_name)
export CONNECTION_STRING=$(terraform output -raw storage_connection_string)

# Atualizar .env
echo "AZURE_STORAGE_CONNECTION_STRING=$CONNECTION_STRING" >> .env
echo "AZURE_CONTAINER_NAME=landingzone" >> .env
```

### Configurar Databricks

1. Acesse o workspace do Databricks
2. Configure clusters para processamento
3. Import notebooks do projeto
4. Configure secrets para conexões

## Troubleshooting

### Erro de Autenticação

```bash
# Verificar login
az account show

# Refazer login se necessário
az login --tenant YOUR_TENANT_ID
```

### Erro de Recursos

```bash
# Verificar quotas da subscription
az vm list-usage --location "Brazil South" -o table

# Verificar providers registrados
az provider list --query "[?registrationState=='Registered']" -o table
```

### Rollback

```bash
# Ver histórico de state
terraform show

# Rollback específico (cuidado!)
terraform import azurerm_storage_account.stacdata01 /subscriptions/.../resourceGroups/.../providers/Microsoft.Storage/storageAccounts/...
```

## Limpeza de Recursos

### Destruir Infraestrutura

```bash
# Ver o que será destruído
terraform plan -destroy

# Destruir recursos
terraform destroy

# Confirmar destruição
# Digite "yes" quando solicitado
```

### Limpeza Manual

Se necessário, remova recursos manualmente:

```bash
# Listar resource groups
az group list -o table

# Deletar resource group (remove todos os recursos)
az group delete --name rgdatatrabalhoeddev01 --yes --no-wait
```

## Melhores Práticas

1. **Versionamento**: Use tags Git para versionar infraestrutura
2. **State Backend**: Configure backend remoto para produção
3. **Terraform Cloud**: Use para equipes maiores
4. **Modules**: Modularize código para reutilização
5. **Security**: Nunca commite `terraform.tfvars` com dados sensíveis
