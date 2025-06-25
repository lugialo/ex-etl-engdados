#!/usr/bin/env python3

"""
Script para testar a conexão com Azure Storage
Usage: python test_azure_connection.py
"""

import os
import logging
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_azure_connection():
    """Testa a conexão com Azure Storage."""
    
    # Obter configurações
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING', '')
    container_name = os.getenv('AZURE_CONTAINER_NAME', 'data')
    
    if not connection_string:
        logger.error("❌ AZURE_STORAGE_CONNECTION_STRING não configurada!")
        logger.info("Configure com: export AZURE_STORAGE_CONNECTION_STRING='sua_connection_string'")
        return False
    
    try:
        logger.info("🔄 Testando conexão com Azure Storage...")
        
        # Criar cliente
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Testar listagem de containers
        logger.info("📋 Listando containers disponíveis...")
        containers = blob_service_client.list_containers()
        container_list = [c.name for c in containers]
        
        if container_list:
            logger.info(f"✅ Containers encontrados: {', '.join(container_list)}")
        else:
            logger.info("📭 Nenhum container encontrado")
        
        # Verificar se o container especificado existe
        try:
            container_client = blob_service_client.get_container_client(container_name)
            container_client.get_container_properties()
            logger.info(f"✅ Container '{container_name}' existe e está acessível")
        except ResourceNotFoundError:
            logger.info(f"📁 Container '{container_name}' não existe (será criado automaticamente)")
        
        # Testar criação de um blob de teste
        test_blob_name = "test_connection.txt"
        test_content = "Teste de conexão realizado com sucesso!"
        
        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=test_blob_name
        )
        
        # Criar container se não existir
        try:
            container_client = blob_service_client.get_container_client(container_name)
            container_client.get_container_properties()
        except ResourceNotFoundError:
            logger.info(f"🆕 Criando container '{container_name}'...")
            container_client.create_container()
        
        # Upload de teste
        blob_client.upload_blob(test_content, overwrite=True)
        logger.info(f"✅ Upload de teste bem-sucedido: {test_blob_name}")
        
        # Cleanup - remover arquivo de teste
        blob_client.delete_blob()
        logger.info("🗑️  Arquivo de teste removido")
        
        logger.info("🎉 Teste de conexão Azure Storage: SUCESSO!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro na conexão com Azure: {str(e)}")
        logger.info("🔧 Verifique:")
        logger.info("   1. Se a connection string está correta")
        logger.info("   2. Se o Storage Account existe")
        logger.info("   3. Se as credenciais têm permissão de acesso")
        return False

if __name__ == "__main__":
    print("🧪 Teste de Conexão Azure Storage")
    print("="*40)
    
    success = test_azure_connection()
    
    print("\n" + "="*40)
    if success:
        print("✅ CONEXÃO OK - Pode usar o gerador de dados!")
    else:
        print("❌ CONEXÃO FALHOU - Configure as credenciais")
    print("="*40)
