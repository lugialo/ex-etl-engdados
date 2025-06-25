import csv
from faker import Faker
from datetime import datetime, timedelta
import random
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
import logging
from dotenv import load_dotenv


# Carregar o .env
load_dotenv()

# Inicializar o Faker. Usaremos 'pt_BR' para dados mais localizados.
fake = Faker('pt_BR')

# --- Configurações do PostgreSQL ---
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'clinica_odonto'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root')
}

# URL de conexão para SQLAlchemy
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# --- Configurações do Azure Storage ---
# Configure estas variáveis com suas credenciais do Azure
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING', '')
AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME', 'data')
AZURE_BLOB_PREFIX = ''  # Pasta dentro do container

# --- Configuração de logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Funções de Banco de Dados ---
def conectar_db():
    """Conecta ao banco PostgreSQL usando SQLAlchemy."""
    try:
        engine = create_engine(DATABASE_URL)
        # Testar conexão
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Conexão com PostgreSQL estabelecida via SQLAlchemy")
        return engine
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com PostgreSQL: {e}")
        return None

def criar_e_limpar_tabelas(engine):
    """Cria as tabelas através do modelo físico e limpa dados existentes."""
    try:
        # 1. Primeiro, executar o modelo físico para criar as tabelas
        modelo_fisico_path = os.path.join(os.path.dirname(__file__), 'modelo_fisico.sql')
        if os.path.exists(modelo_fisico_path):
            logger.info("📋 Criando tabelas através do modelo físico...")
            with open(modelo_fisico_path, 'r', encoding='utf-8') as file:
                sql_commands = file.read()
            
            # Dividir comandos SQL e executar um por vez
            commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]
            
            with engine.connect() as conn:
                trans = conn.begin()
                try:
                    for command in commands:
                        if command.upper().startswith(('CREATE', 'ALTER', 'CREATE INDEX')):
                            try:
                                conn.execute(text(command))
                            except Exception as e:
                                # Ignorar erros de "já existe" 
                                if "already exists" in str(e) or "já existe" in str(e):
                                    logger.info(f"Tabela/índice já existe, continuando...")
                                else:
                                    logger.warning(f"Aviso ao executar comando: {e}")
                    trans.commit()
                except Exception as e:
                    trans.rollback()
                    raise e
            
            logger.info("✅ Modelo físico executado com sucesso")
        else:
            logger.error("❌ Arquivo modelo_fisico.sql não encontrado")
            return False
        
        # 2. Limpar dados existentes das tabelas
        tabelas = [
            'log_pagamento', 'consulta_procedimento', 'pagamento', 
            'consulta', 'agendamento', 'paciente', 'endereco', 
            'odontologista', 'procedimento', 'tipo_pagamento'
        ]
        
        logger.info("🧹 Limpando dados existentes das tabelas...")
        
        # Fazer limpeza em uma transação separada
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                # Desabilitar constraints temporariamente
                conn.execute(text("SET session_replication_role = replica;"))
                
                # Limpar dados das tabelas
                for tabela in tabelas:
                    try:
                        conn.execute(text(f"DELETE FROM {tabela};"))
                        logger.info(f"Dados da tabela {tabela} removidos")
                    except Exception as e:
                        logger.warning(f"Erro ao limpar tabela {tabela}: {e}")
                
                # Habilitar constraints novamente
                conn.execute(text("SET session_replication_role = DEFAULT;"))
                trans.commit()
                logger.info("✅ Dados das tabelas limpos com sucesso")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"Erro durante limpeza: {e}")
                raise e
        
        # 3. Resetar sequences em uma transação separada
        logger.info("🔄 Resetando sequences...")
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                for tabela in tabelas:
                    sequence_names = [
                        f"{tabela}_id_{tabela.replace('_', '')}_seq",
                        f"{tabela}_id_{tabela}_seq"
                    ]
                    
                    # Casos especiais para sequences com nomes diferentes
                    if tabela == "consulta_procedimento":
                        sequence_names.append("consulta_procedimento_id_consulta_procedimento_seq")
                    elif tabela == "log_pagamento":
                        sequence_names.append("log_pagamento_id_log_seq")
                    elif tabela == "tipo_pagamento":
                        sequence_names.append("tipo_pagamento_id_tipo_pagamento_seq")
                    
                    sequence_reset = False
                    for seq_name in sequence_names:
                        try:
                            conn.execute(text(f"ALTER SEQUENCE {seq_name} RESTART WITH 1;"))
                            logger.info(f"Sequence {seq_name} resetada")
                            sequence_reset = True
                            break
                        except Exception:
                            continue
                    
                    if not sequence_reset:
                        logger.warning(f"Não foi possível resetar sequence para {tabela}")
                
                trans.commit()
                logger.info("✅ Sequences resetadas com sucesso")
                
            except Exception as e:
                trans.rollback()
                logger.warning(f"Erro ao resetar sequences: {e}")
                # Não falhar o processo por causa das sequences
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar/limpar tabelas: {e}")
        return False

def inserir_dados_tabela(engine, tabela, dados):
    """Insere dados em uma tabela específica usando SQLAlchemy."""
    if not dados:
        return
    
    try:
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                # Construir query de inserção dinamicamente
                colunas = list(dados[0].keys())
                placeholders = ', '.join([f':{col}' for col in colunas])
                query = text(f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({placeholders})")
                
                # Executar inserção em lote
                conn.execute(query, dados)
                trans.commit()
                
                logger.info(f"✅ {len(dados)} registros inseridos na tabela {tabela}")
                
            except Exception as e:
                trans.rollback()
                raise e
                
    except Exception as e:
        logger.error(f"❌ Erro ao inserir dados na tabela {tabela}: {e}")
        raise

def extrair_dados_para_csv(engine, tabela, diretorio_saida):
    """Extrai dados de uma tabela e salva em CSV usando SQLAlchemy."""
    try:
        # Determinar o nome da coluna ID dinamicamente
        id_column = f"id_{tabela}"
        if tabela == "consulta_procedimento":
            id_column = "id_consulta_procedimento"
        elif tabela == "log_pagamento":
            id_column = "id_log"
        elif tabela == "tipo_pagamento":
            id_column = "id_tipo_pagamento"
        
        query = text(f"SELECT * FROM {tabela} ORDER BY {id_column}")
        
        with engine.connect() as conn:
            result = conn.execute(query)
            rows = result.fetchall()
            columns = result.keys()
        
        # Criar diretório se não existir
        os.makedirs(diretorio_saida, exist_ok=True)
        
        # Salvar CSV
        arquivo_csv = os.path.join(diretorio_saida, f"{tabela}.csv")
        
        with open(arquivo_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Escrever cabeçalho
            writer.writerow(columns)
            # Escrever dados
            writer.writerows(rows)
        
        logger.info(f"✅ Dados da tabela {tabela} salvos em {arquivo_csv} ({len(rows)} registros)")
        return arquivo_csv
    except Exception as e:
        logger.error(f"❌ Erro ao extrair dados da tabela {tabela}: {e}")
        return None

# --- Configurações de dados ---
NUM_ENDERECOS = 20000
NUM_ODONTOLOGISTAS = 70 # Número mais realista para odontologistas
NUM_PACIENTES = 30000
NUM_TIPOS_PAGAMENTO = 5
NUM_PROCEDIMENTOS = 60
NUM_AGENDAMENTOS = 70000 # Tabela transacional principal
# Assumindo que 90% dos agendamentos viram consultas
NUM_CONSULTAS = int(NUM_AGENDAMENTOS * 0.9)
# Assumindo que 95% das consultas geram um pagamento
NUM_PAGAMENTOS = int(NUM_CONSULTAS * 0.95)
# Cada consulta pode ter de 1 a 3 procedimentos
MIN_PROC_POR_CONSULTA = 1
MAX_PROC_POR_CONSULTA = 3

# --- Funções de Geração ---

def gerar_datas_tres_anos():
    """Gera uma data aleatória nos últimos 3 anos."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)
    return fake.date_time_between(start_date=start_date, end_date=end_date)

def gerar_data_nascimento():
    """Gera uma data de nascimento aleatória para adultos (18-80 anos)."""
    end_date = datetime.now() - timedelta(days=18*365) # Mínimo 18 anos
    start_date = datetime.now() - timedelta(days=80*365) # Máximo 80 anos
    return fake.date_of_birth(minimum_age=18, maximum_age=80)

# 1. Tabela endereco
def gerar_enderecos(num_registros):
    """Gera dados para a tabela endereco."""
    dados_endereco = []
    for i in range(num_registros):
        dados_endereco.append({
            'logradouro': fake.street_name(),
            'numero': fake.building_number(),
            'complemento': fake.text(max_nb_chars=30) if random.choice([True, False, False]) else None,
            'bairro': fake.bairro(),
            'cidade': fake.city(),
            'estado': fake.state_abbr(),
            'cep': fake.postcode(),
            'pais': 'Brasil'
        })
    logger.info(f"{len(dados_endereco)} registros de ENDERECO gerados.")
    return dados_endereco

# 2. Tabela odontologista
def gerar_odontologistas(num_registros):
    """Gera dados para a tabela odontologista."""
    dados_odontologista = []
    especialidades = ['Clínico Geral', 'Ortodontia', 'Periodontia', 'Endodontia', 'Implantodontia', 'Odontopediatria', 'Prótese Dentária']
    for i in range(num_registros):
        dados_odontologista.append({
            'nome_odontologista': fake.name(),
            'especialidade': random.choice(especialidades),
            'cro': f"{fake.random_number(digits=5)}-{fake.state_abbr()}"
        })
    logger.info(f"{len(dados_odontologista)} registros de ODONTOLOGISTA gerados.")
    return dados_odontologista

# 3. Tabela paciente
def gerar_pacientes(num_registros, ids_enderecos_disponiveis):
    """Gera dados para a tabela paciente."""
    dados_paciente = []
    generos = ['M', 'F', 'O'] # Masculino, Feminino, Outro
    for i in range(num_registros):
        # Gerar telefone mais curto para caber no varchar(15)
        # Formato: (XX) XXXXX-XXXX = 14 caracteres
        ddd = fake.random_int(min=11, max=99)
        numero = fake.random_int(min=90000, max=99999)
        final = fake.random_int(min=1000, max=9999)
        telefone_curto = f"({ddd:02d}){numero}{final}"
        
        dados_paciente.append({
            'nome_paciente': fake.name(),
            'cpf_paciente': fake.unique.cpf().replace('.', '').replace('-', ''), # CPF sem formatação
            'telefone': telefone_curto,
            'genero': random.choice(generos),
            'data_nasc': gerar_data_nascimento(),
            'email': fake.unique.email(),
            'endereco_id_endereco': random.choice(ids_enderecos_disponiveis) if ids_enderecos_disponiveis else None
        })
    logger.info(f"{len(dados_paciente)} registros de PACIENTE gerados.")
    return dados_paciente

# 4. Tabela tipo_pagamento
def gerar_tipos_pagamento():
    """Gera dados para a tabela tipo_pagamento."""
    descricoes = ['Dinheiro', 'Cartão de Crédito', 'Cartão de Débito', 'PIX', 'Boleto Bancário', 'Convênio']
    dados_tipo_pagamento = []
    # Garantir que o NUM_TIPOS_PAGAMENTO não seja maior que a lista de descrições
    num_a_gerar = min(NUM_TIPOS_PAGAMENTO, len(descricoes))
    for i in range(num_a_gerar):
        dados_tipo_pagamento.append({
            'descricao_tipo_pagamento': descricoes[i]
        })
    logger.info(f"{len(dados_tipo_pagamento)} registros de TIPO_PAGAMENTO gerados.")
    return dados_tipo_pagamento

# 5. Tabela procedimento
def gerar_procedimentos(num_registros):
    """Gera dados para a tabela procedimento."""
    nomes_procedimentos = [
        "Limpeza Dental", "Restauração (Obturação)", "Extração Simples", "Tratamento de Canal",
        "Clareamento Dental", "Instalação de Aparelho Ortodôntico", "Manutenção de Aparelho",
        "Implante Dentário", "Prótese Fixa", "Prótese Removível", "Raspagem Periodontal",
        "Aplicação de Flúor", "Consulta de Avaliação", "Radiografia Panorâmica"
    ]
    # Expandir a lista se num_registros for maior, ou limitar
    lista_final_procedimentos = (nomes_procedimentos * (num_registros // len(nomes_procedimentos) + 1))[:num_registros]

    dados_procedimento = []
    for i in range(num_registros):
        nome_proc = lista_final_procedimentos[i] if i < len(lista_final_procedimentos) else f"Procedimento Genérico {i+1}"
        dados_procedimento.append({
            'nome_procedimento': nome_proc,
            'descricao_procedimento': f"Descrição detalhada para {nome_proc}"
        })
    logger.info(f"{len(dados_procedimento)} registros de PROCEDIMENTO gerados.")
    return dados_procedimento

# 6. Tabela agendamento
def gerar_agendamentos(num_registros, ids_pacientes, ids_odontologistas):
    """Gera dados para a tabela agendamento."""
    dados_agendamento = []
    status_agendamento = ['Confirmado', 'Realizado', 'Cancelado', 'Remarcado', 'Não Compareceu']
    if not ids_pacientes or not ids_odontologistas:
        logger.warning("AVISO: Não há pacientes ou odontologistas suficientes para gerar agendamentos.")
        return []
    for i in range(num_registros):
        dados_agendamento.append({
            'data_agendamento': gerar_datas_tres_anos(),
            'status_agendamento': random.choice(status_agendamento),
            'paciente_id_paciente': random.choice(ids_pacientes),
            'odontologista_id_odontologista': random.choice(ids_odontologistas)
        })
    logger.info(f"{len(dados_agendamento)} registros de AGENDAMENTO gerados.")
    return dados_agendamento

# 7. Tabela consulta
def gerar_consultas(num_registros, ids_agendamentos_disponiveis):
    """Gera dados para a tabela consulta, baseando-se em agendamentos disponíveis."""
    dados_consulta = []
    diagnosticos_exemplo = ["Cárie dentária", "Gengivite", "Periodontite", "Necessidade de extração", "Bruxismo", "Alinhamento dental necessário"]
    tratamentos_exemplo = ["Restauração", "Limpeza profunda", "Tratamento periodontal", "Extração do siso", "Placa de bruxismo", "Indicação para ortodontista"]

    if not ids_agendamentos_disponiveis:
        logger.warning("AVISO: Nenhum agendamento disponível para gerar consultas.")
        return []

    # Limitar o número de consultas ao número de agendamentos disponíveis ou ao NUM_CONSULTAS desejado
    num_registros_efetivo = min(num_registros, len(ids_agendamentos_disponiveis))
    agendamentos_para_consulta = random.sample(ids_agendamentos_disponiveis, num_registros_efetivo)

    for i in range(num_registros_efetivo):
        id_agendamento_ref = agendamentos_para_consulta[i]
        # Gerar data e hora da consulta (últimos 3 anos)
        data_hora_consulta = gerar_datas_tres_anos()

        dados_consulta.append({
            'data_hora': data_hora_consulta,
            'diagnostico': random.choice(diagnosticos_exemplo) + f" (Consulta {i+1})",
            'tratamento': random.choice(tratamentos_exemplo) + f" (Consulta {i+1})",
            'agendamento_id_agendamento': id_agendamento_ref
        })
    logger.info(f"{len(dados_consulta)} registros de CONSULTA gerados.")
    return dados_consulta


# 8. Tabela pagamento
def gerar_pagamentos(num_registros, ids_consultas_disponiveis, ids_tipos_pagamento):
    """Gera dados para a tabela pagamento."""
    dados_pagamento = []
    if not ids_consultas_disponiveis or not ids_tipos_pagamento:
        logger.warning("AVISO: Não há consultas ou tipos de pagamento para gerar pagamentos.")
        return []

    # Limitar o número de pagamentos ao número de consultas disponíveis
    num_registros_efetivo = min(num_registros, len(ids_consultas_disponiveis))
    consultas_para_pagamento = random.sample(ids_consultas_disponiveis, num_registros_efetivo)

    for i in range(num_registros_efetivo):
        id_consulta_ref = consultas_para_pagamento[i]
        # Gerar data de pagamento (últimos 3 anos)
        data_pagamento_val = gerar_datas_tres_anos()

        dados_pagamento.append({
            'valor_pago': round(random.uniform(50.0, 800.0), 2),
            'data_pagamento': data_pagamento_val,
            'tipo_pagamento_id_tipo_pagamento': random.choice(ids_tipos_pagamento),
            'consulta_id_consulta': id_consulta_ref
        })
    logger.info(f"{len(dados_pagamento)} registros de PAGAMENTO gerados.")
    return dados_pagamento

# 9. Tabela consulta_procedimento (Tabela de Junção)
def gerar_consulta_procedimento(ids_consultas_disponiveis, ids_procedimentos_disponiveis, min_proc, max_proc):
    """Gera dados para a tabela de junção consulta_procedimento."""
    dados_consulta_procedimento = []
    if not ids_consultas_disponiveis or not ids_procedimentos_disponiveis:
        print("AVISO: Não há consultas ou procedimentos para gerar consulta_procedimento.")
        return []

    id_pk_consulta_procedimento = 1
    for id_consulta in ids_consultas_disponiveis:
        num_procedimentos_para_consulta = random.randint(min_proc, max_proc)
        # Garante que não tentemos escolher mais procedimentos do que os disponíveis
        num_procedimentos_para_consulta = min(num_procedimentos_para_consulta, len(ids_procedimentos_disponiveis))
        procedimentos_escolhidos = random.sample(ids_procedimentos_disponiveis, num_procedimentos_para_consulta)
        for id_procedimento in procedimentos_escolhidos:
            dados_consulta_procedimento.append({
                'consulta_id_consulta': id_consulta,
                'procedimento_id_procedimento': id_procedimento
            })
    logger.info(f"{len(dados_consulta_procedimento)} registros de CONSULTA_PROCEDIMENTO gerados.")
    return dados_consulta_procedimento

# 10. Tabela log_pagamento
def gerar_log_pagamentos(pagamentos_ids_db):
    """Gera dados para a tabela log_pagamento usando IDs reais do banco."""
    dados_log_pagamento = []
    tipos_acao = ['INSERT', 'UPDATE'] # Supondo que podem haver atualizações nos pagamentos
    if not pagamentos_ids_db:
        logger.warning("AVISO: Não há dados de pagamento para gerar logs.")
        return []

    for i, id_pagamento in enumerate(pagamentos_ids_db):
        # Para cada pagamento, gerar um log de INSERT
        data_operacao = gerar_datas_tres_anos()
        dados_log_pagamento.append({
            'tipo_acao': 'INSERT',
            'id_pagamento': id_pagamento,
            'tipo_pagamento_id_tipo_pagamento': random.randint(1, 5),  # Assumindo 5 tipos de pagamento
            'valor_pago': round(random.uniform(50.0, 800.0), 2),
            'data_pagamento': data_operacao,
            'DataHoraOperacao': data_operacao + timedelta(seconds=random.randint(1, 300)),
            'ExecutedBy': fake.user_name()
        })

        # Opcional: Gerar alguns logs de UPDATE para alguns pagamentos
        if random.random() < 0.1: # 10% de chance de ter um update
            data_update = data_operacao + timedelta(days=random.randint(1,5))
            dados_log_pagamento.append({
                'tipo_acao': 'UPDATE',
                'id_pagamento': id_pagamento,
                'tipo_pagamento_id_tipo_pagamento': random.randint(1, 5),
                'valor_pago': round(random.uniform(50.0, 800.0), 2),
                'data_pagamento': data_update,
                'DataHoraOperacao': data_update + timedelta(seconds=random.randint(1, 300)),
                'ExecutedBy': fake.user_name()
            })

    logger.info(f"{len(dados_log_pagamento)} registros de LOG_PAGAMENTO gerados.")
    return dados_log_pagamento

# --- Função para upload para Azure Storage ---
def upload_to_azure(local_file_path, blob_name):
    """Faz upload de um arquivo para o Azure Blob Storage."""
    if not AZURE_STORAGE_CONNECTION_STRING:
        logger.warning("AZURE_STORAGE_CONNECTION_STRING não configurada. Upload para Azure ignorado.")
        return False
    
    try:
        # Criar o cliente do serviço blob
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        
        # Obter o cliente do container
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        
        # Verificar se o container existe, se não, criar
        try:
            container_client.get_container_properties()
        except ResourceNotFoundError:
            logger.info(f"Container '{AZURE_CONTAINER_NAME}' não existe. Criando...")
            container_client.create_container()
        
        # Fazer upload do arquivo (sobrescreve se já existir)
        blob_client = blob_service_client.get_blob_client(
            container=AZURE_CONTAINER_NAME, 
            blob=blob_name
        )
        
        with open(local_file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)
        
        logger.info(f"Upload bem-sucedido: {blob_name}")
        return True
        
    except Exception as e:
        logger.error(f"Erro no upload para Azure: {str(e)}")
        return False

# --- Função para salvar em CSV ---
def salvar_csv(dados, nome_arquivo, cabecalho):
    """Salva uma lista de dicionários em um arquivo CSV localmente e faz upload para Azure."""
    # Criar diretório local se não existir
    local_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')
    os.makedirs(local_dir, exist_ok=True)
    
    # Caminho do arquivo local
    local_file_path = os.path.join(local_dir, f'{nome_arquivo}.csv')
    
    # Salvar arquivo localmente
    with open(local_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cabecalho)
        writer.writeheader()
        writer.writerows(dados)
    
    logger.info(f"Dados salvos localmente em {local_file_path}")
    
    # Nome do blob no Azure (incluindo o prefixo da pasta)
    blob_name = f"{AZURE_BLOB_PREFIX}{nome_arquivo}.csv"
    
    # Fazer upload para Azure
    upload_success = upload_to_azure(local_file_path, blob_name)
    
    if upload_success:
        logger.info(f"Arquivo {nome_arquivo}.csv salvo localmente e enviado para Azure Storage")
    else:
        logger.warning(f"Arquivo {nome_arquivo}.csv salvo apenas localmente")

def verificar_configuracao_azure():
    """Verifica se as configurações do Azure estão corretas."""
    if not AZURE_STORAGE_CONNECTION_STRING:
        logger.warning("⚠️  AZURE_STORAGE_CONNECTION_STRING não configurada!")
        logger.info("Para fazer upload para Azure, configure a variável de ambiente:")
        logger.info("export AZURE_STORAGE_CONNECTION_STRING='sua_connection_string_aqui'")
        logger.info("export AZURE_CONTAINER_NAME='nome_do_container'")
        logger.info("")
        logger.info("Os arquivos serão salvos apenas localmente.")
        return False
    return True

# --- Orquestração da Geração e Salvamento ---
def main():
    logger.info("🚀 Iniciando geração de dados...")
    
    # 1. Conectar ao banco
    engine = conectar_db()
    if not engine:
        logger.error("❌ Falha na conexão com o banco. Verifique se o PostgreSQL está rodando.")
        return
    
    try:
        # 2. Criar tabelas e limpar dados existentes
        logger.info("🏗️ Criando tabelas e limpando dados...")
        if not criar_e_limpar_tabelas(engine):
            logger.error("❌ Falha ao criar/limpar tabelas")
            return
        
        # 3. Gerar e inserir dados (tabelas independentes primeiro)
        logger.info("📊 Gerando e inserindo dados...")
        
        # Tabelas independentes
        logger.info("Gerando tabela: endereco")
        dados_endereco = gerar_enderecos(NUM_ENDERECOS)
        inserir_dados_tabela(engine, 'endereco', dados_endereco)
        
        logger.info("Gerando tabela: odontologista")
        dados_odontologista = gerar_odontologistas(NUM_ODONTOLOGISTAS)
        inserir_dados_tabela(engine, 'odontologista', dados_odontologista)
        
        logger.info("Gerando tabela: tipo_pagamento")
        dados_tipos_pagamento = gerar_tipos_pagamento()
        inserir_dados_tabela(engine, 'tipo_pagamento', dados_tipos_pagamento)
        
        logger.info("Gerando tabela: procedimento")
        dados_procedimentos = gerar_procedimentos(NUM_PROCEDIMENTOS)
        inserir_dados_tabela(engine, 'procedimento', dados_procedimentos)
        
        # Buscar IDs reais do banco para manter referências
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id_endereco FROM endereco ORDER BY id_endereco"))
            enderecos_ids_db = [row[0] for row in result.fetchall()]
            
            result = conn.execute(text("SELECT id_odontologista FROM odontologista ORDER BY id_odontologista"))
            odontologistas_ids_db = [row[0] for row in result.fetchall()]
            
            result = conn.execute(text("SELECT id_tipo_pagamento FROM tipo_pagamento ORDER BY id_tipo_pagamento"))
            tipos_pagamento_ids_db = [row[0] for row in result.fetchall()]
            
            result = conn.execute(text("SELECT id_procedimento FROM procedimento ORDER BY id_procedimento"))
            procedimentos_ids_db = [row[0] for row in result.fetchall()]
        
        # Tabelas dependentes
        logger.info("Gerando tabela: paciente")
        dados_pacientes = gerar_pacientes(NUM_PACIENTES, enderecos_ids_db)
        inserir_dados_tabela(engine, 'paciente', dados_pacientes)
        
        # Buscar IDs dos pacientes
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id_paciente FROM paciente ORDER BY id_paciente"))
            pacientes_ids_db = [row[0] for row in result.fetchall()]
        
        logger.info("Gerando tabela: agendamento")
        dados_agendamentos = gerar_agendamentos(NUM_AGENDAMENTOS, pacientes_ids_db, odontologistas_ids_db)
        inserir_dados_tabela(engine, 'agendamento', dados_agendamentos)
        
        # Buscar IDs dos agendamentos
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id_agendamento FROM agendamento ORDER BY id_agendamento"))
            agendamentos_ids_db = [row[0] for row in result.fetchall()]
        
        logger.info("Gerando tabela: consulta")
        dados_consultas = gerar_consultas(NUM_CONSULTAS, agendamentos_ids_db)
        inserir_dados_tabela(engine, 'consulta', dados_consultas)
        
        # Buscar IDs das consultas
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id_consulta FROM consulta ORDER BY id_consulta"))
            consultas_ids_db = [row[0] for row in result.fetchall()]
        
        logger.info("Gerando tabela: pagamento")
        dados_pagamentos = gerar_pagamentos(NUM_PAGAMENTOS, consultas_ids_db, tipos_pagamento_ids_db)
        inserir_dados_tabela(engine, 'pagamento', dados_pagamentos)
        
        # Buscar IDs dos pagamentos
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id_pagamento FROM pagamento ORDER BY id_pagamento"))
            pagamentos_ids_db = [row[0] for row in result.fetchall()]
        
        logger.info("Gerando tabela: consulta_procedimento")
        dados_consulta_procedimento = gerar_consulta_procedimento(consultas_ids_db, procedimentos_ids_db, MIN_PROC_POR_CONSULTA, MAX_PROC_POR_CONSULTA)
        inserir_dados_tabela(engine, 'consulta_procedimento', dados_consulta_procedimento)
        
        logger.info("Gerando tabela: log_pagamento")
        dados_log_pagamento = gerar_log_pagamentos(pagamentos_ids_db)
        inserir_dados_tabela(engine, 'log_pagamento', dados_log_pagamento)
        
        # 4. Extrair dados para CSVs
        logger.info("📄 Extraindo dados para arquivos CSV...")
        tabelas = [
            'endereco', 'odontologista', 'tipo_pagamento', 'procedimento',
            'paciente', 'agendamento', 'consulta', 'pagamento', 
            'consulta_procedimento', 'log_pagamento'
        ]
        
        diretorio_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
        arquivos_gerados = []
        
        for tabela in tabelas:
            arquivo = extrair_dados_para_csv(engine, tabela, diretorio_csv)
            if arquivo:
                arquivos_gerados.append(arquivo)
        
        # 5. Upload para Azure (se configurado)
        if verificar_configuracao_azure():
            logger.info("☁️  Fazendo upload dos CSVs para Azure Storage...")
            for arquivo in arquivos_gerados:
                nome_arquivo = os.path.basename(arquivo)
                upload_to_azure(arquivo, f"{nome_arquivo}")
        
        logger.info("✅ Processo concluído com sucesso!")
        logger.info(f"📊 Dados inseridos no PostgreSQL:")
        logger.info(f"   • {NUM_ENDERECOS:,} endereços")
        logger.info(f"   • {NUM_ODONTOLOGISTAS:,} odontologistas") 
        logger.info(f"   • {NUM_PACIENTES:,} pacientes")
        logger.info(f"   • {NUM_AGENDAMENTOS:,} agendamentos")
        logger.info(f"   • {NUM_CONSULTAS:,} consultas")
        logger.info(f"   • {NUM_PAGAMENTOS:,} pagamentos")
        logger.info(f"📄 {len(arquivos_gerados)} arquivos CSV gerados em {diretorio_csv}")
        
    except Exception as e:
        logger.error(f"❌ Erro durante o processo: {e}")
    finally:
        engine.dispose()
        logger.info("🔌 Conexão com banco fechada")

if __name__ == "__main__":
    main()