#!/usr/bin/env python3

"""
Script simplificado para testar a conexão e inserção de dados
"""

import os
import psycopg2
import pandas as pd
from faker import Faker
from dotenv import load_dotenv
import logging

# Carregar .env
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializar Faker
fake = Faker('pt_BR')

# Configurações do banco
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'clinica_odonto'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root')
}

def conectar_db():
    """Conecta ao banco PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("✅ Conexão com PostgreSQL estabelecida")
        return conn
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com PostgreSQL: {e}")
        return None

def criar_tabela_teste(conn):
    """Cria uma tabela de teste."""
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS endereco (
                    id_endereco SERIAL PRIMARY KEY,
                    logradouro varchar(255) NOT NULL,
                    numero varchar(20),
                    bairro varchar(100) NOT NULL,
                    cidade varchar(100) NOT NULL,
                    estado char(2) NOT NULL,
                    cep varchar(9) NOT NULL,
                    pais varchar(200) NOT NULL
                );
            """)
        conn.commit()
        logger.info("✅ Tabela endereco criada/verificada")
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabela: {e}")

def gerar_dados_teste():
    """Gera alguns dados de teste."""
    dados = []
    for i in range(10):
        dados.append({
            'logradouro': fake.street_name(),
            'numero': fake.building_number(),
            'bairro': fake.bairro(),
            'cidade': fake.city(),
            'estado': fake.state_abbr(),
            'cep': fake.postcode(),
            'pais': 'Brasil'
        })
    return dados

def inserir_dados(conn, dados):
    """Insere dados na tabela."""
    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO endereco (logradouro, numero, bairro, cidade, estado, cep, pais)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            for registro in dados:
                cursor.execute(query, (
                    registro['logradouro'],
                    registro['numero'],
                    registro['bairro'],
                    registro['cidade'],
                    registro['estado'],
                    registro['cep'],
                    registro['pais']
                ))
        conn.commit()
        logger.info(f"✅ {len(dados)} registros inseridos")
    except Exception as e:
        logger.error(f"❌ Erro ao inserir dados: {e}")

def extrair_para_csv(conn):
    """Extrai dados para CSV."""
    try:
        df = pd.read_sql_query("SELECT * FROM endereco", conn)
        csv_path = "../data/raw/endereco_teste.csv"
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        logger.info(f"✅ Dados extraídos para {csv_path}")
        return csv_path
    except Exception as e:
        logger.error(f"❌ Erro ao extrair para CSV: {e}")
        return None

def main():
    logger.info("🚀 Iniciando teste de geração de dados...")
    
    # Conectar
    conn = conectar_db()
    if not conn:
        return
    
    try:
        # Criar tabela
        criar_tabela_teste(conn)
        
        # Limpar dados existentes
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM endereco;")
        conn.commit()
        logger.info("🧹 Dados limpos")
        
        # Gerar e inserir dados
        dados = gerar_dados_teste()
        inserir_dados(conn, dados)
        
        # Extrair para CSV
        csv_file = extrair_para_csv(conn)
        
        logger.info("✅ Teste concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro durante o teste: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
