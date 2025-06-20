import csv
from faker import Faker
from datetime import datetime, timedelta
import random

# Inicializar o Faker. Usaremos 'pt_BR' para dados mais localizados.
fake = Faker('pt_BR')

# --- Configurações ---
NUM_ENDERECOS = 20000
NUM_ODONTOLOGISTAS = 70 # Número mais realista para odontologistas
NUM_PACIENTES = 20000
NUM_TIPOS_PAGAMENTO = 5
NUM_PROCEDIMENTOS = 60
NUM_AGENDAMENTOS = 50000 # Tabela transacional principal
# Assumindo que 90% dos agendamentos viram consultas
NUM_CONSULTAS = int(NUM_AGENDAMENTOS * 0.9)
# Assumindo que 95% das consultas geram um pagamento
NUM_PAGAMENTOS = int(NUM_CONSULTAS * 0.95)
# Cada consulta pode ter de 1 a 3 procedimentos
MIN_PROC_POR_CONSULTA = 1
MAX_PROC_POR_CONSULTA = 3

# IDs gerados para manter a consistência entre tabelas
enderecos_ids = []
odontologistas_ids = []
pacientes_ids = []
tipos_pagamento_ids = []
procedimentos_ids = []
agendamentos_ids = []
consultas_ids = []
pagamentos_ids = []

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
    for i in range(1, num_registros + 1):
        enderecos_ids.append(i)
        dados_endereco.append({
            'id_endereco': i,
            'logradouro': fake.street_name(),
            'numero': fake.building_number(),
            'complemento': fake.text(max_nb_chars=30) if random.choice([True, False, False]) else None, # LINHA CORRIGIDA (aumentei a chance de ser None)
            'bairro': fake.bairro(),
            'cidade': fake.city(),
            'estado': fake.state_abbr(),
            'cep': fake.postcode(),
            'pais': 'Brasil' # Fixo para simplificar
        })
    print(f"{len(dados_endereco)} registros de ENDERECO gerados.")
    return dados_endereco

# 2. Tabela odontologista
def gerar_odontologistas(num_registros):
    """Gera dados para a tabela odontologista."""
    dados_odontologista = []
    especialidades = ['Clínico Geral', 'Ortodontia', 'Periodontia', 'Endodontia', 'Implantodontia', 'Odontopediatria', 'Prótese Dentária']
    for i in range(1, num_registros + 1):
        odontologistas_ids.append(i)
        dados_odontologista.append({
            'id_odontologista': i,
            'nome_odontologista': fake.name(),
            'especialidade': random.choice(especialidades),
            'cro': f"{fake.random_number(digits=5)}-{fake.state_abbr()}"
        })
    print(f"{len(dados_odontologista)} registros de ODONTOLOGISTA gerados.")
    return dados_odontologista

# 3. Tabela paciente
def gerar_pacientes(num_registros, ids_enderecos_disponiveis):
    """Gera dados para a tabela paciente."""
    dados_paciente = []
    generos = ['M', 'F', 'O'] # Masculino, Feminino, Outro
    for i in range(1, num_registros + 1):
        pacientes_ids.append(i)
        dados_paciente.append({
            'id_paciente': i,
            'nome_paciente': fake.name(),
            'cpf_paciente': fake.unique.cpf().replace('.', '').replace('-', ''), # CPF sem formatação
            'telefone': fake.phone_number(),
            'genero': random.choice(generos),
            'data_nasc': gerar_data_nascimento(),
            'email': fake.unique.email(),
            'endereco_id_endereco': random.choice(ids_enderecos_disponiveis) if ids_enderecos_disponiveis else None
        })
    print(f"{len(dados_paciente)} registros de PACIENTE gerados.")
    return dados_paciente

# 4. Tabela tipo_pagamento
def gerar_tipos_pagamento():
    """Gera dados para a tabela tipo_pagamento."""
    descricoes = ['Dinheiro', 'Cartão de Crédito', 'Cartão de Débito', 'PIX', 'Boleto Bancário', 'Convênio']
    dados_tipo_pagamento = []
    # Garantir que o NUM_TIPOS_PAGAMENTO não seja maior que a lista de descrições
    num_a_gerar = min(NUM_TIPOS_PAGAMENTO, len(descricoes))
    for i in range(1, num_a_gerar + 1):
        tipos_pagamento_ids.append(i)
        dados_tipo_pagamento.append({
            'id_tipo_pagamento': i,
            'descricao_tipo_pagamento': descricoes[i-1]
        })
    print(f"{len(dados_tipo_pagamento)} registros de TIPO_PAGAMENTO gerados.")
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
    for i in range(1, num_registros + 1):
        procedimentos_ids.append(i)
        nome_proc = lista_final_procedimentos[i-1] if i-1 < len(lista_final_procedimentos) else f"Procedimento Genérico {i}"
        dados_procedimento.append({
            'id_procedimento': i,
            'nome_procedimento': nome_proc,
            'descricao_procedimento': f"Descrição detalhada para {nome_proc}"
        })
    print(f"{len(dados_procedimento)} registros de PROCEDIMENTO gerados.")
    return dados_procedimento

# 6. Tabela agendamento
def gerar_agendamentos(num_registros, ids_pacientes, ids_odontologistas):
    """Gera dados para a tabela agendamento."""
    dados_agendamento = []
    status_agendamento = ['Confirmado', 'Realizado', 'Cancelado', 'Remarcado', 'Não Compareceu']
    if not ids_pacientes or not ids_odontologistas:
        print("AVISO: Não há pacientes ou odontologistas suficientes para gerar agendamentos.")
        return []
    for i in range(1, num_registros + 1):
        agendamentos_ids.append(i)
        dados_agendamento.append({
            'id_agendamento': i,
            'data_agendamento': gerar_datas_tres_anos(),
            'status_agendamento': random.choice(status_agendamento),
            'paciente_id_paciente': random.choice(ids_pacientes),
            'odontologista_id_odontologista': random.choice(ids_odontologistas)
        })
    print(f"{len(dados_agendamento)} registros de AGENDAMENTO gerados.")
    return dados_agendamento

# 7. Tabela consulta
def gerar_consultas(num_registros, ids_agendamentos_disponiveis, agendamentos_data):
    """Gera dados para a tabela consulta, baseando-se em agendamentos 'Realizado'."""
    dados_consulta = []
    diagnosticos_exemplo = ["Cárie dentária", "Gengivite", "Periodontite", "Necessidade de extração", "Bruxismo", "Alinhamento dental necessário"]
    tratamentos_exemplo = ["Restauração", "Limpeza profunda", "Tratamento periodontal", "Extração do siso", "Placa de bruxismo", "Indicação para ortodontista"]

    # Filtrar agendamentos que foram 'Realizado' para gerar consultas
    agendamentos_realizados_ids = [
        ag['id_agendamento'] for ag in agendamentos_data if ag['status_agendamento'] == 'Realizado'
    ]

    if not agendamentos_realizados_ids:
        print("AVISO: Nenhum agendamento 'Realizado' para gerar consultas.")
        return []

    # Limitar o número de consultas ao número de agendamentos realizados ou ao NUM_CONSULTAS desejado
    num_registros_efetivo = min(num_registros, len(agendamentos_realizados_ids))
    agendamentos_para_consulta = random.sample(agendamentos_realizados_ids, num_registros_efetivo)


    for i in range(1, num_registros_efetivo + 1):
        consultas_ids.append(i)
        id_agendamento_ref = agendamentos_para_consulta[i-1]
        # Encontrar a data do agendamento correspondente para a data_hora da consulta
        data_agendamento_original = next((ag['data_agendamento'] for ag in agendamentos_data if ag['id_agendamento'] == id_agendamento_ref), datetime.now())
        # A consulta ocorre no mesmo dia do agendamento, mas pode ser em hora diferente
        data_hora_consulta = data_agendamento_original.replace(hour=random.randint(8, 18), minute=random.choice([0, 15, 30, 45]))


        dados_consulta.append({
            'id_consulta': i,
            'data_hora': data_hora_consulta,
            'diagnostico': random.choice(diagnosticos_exemplo) + f" (Paciente {i})",
            'tratamento': random.choice(tratamentos_exemplo) + f" (Paciente {i})",
            'agendamento_id_agendamento': id_agendamento_ref
        })
    print(f"{len(dados_consulta)} registros de CONSULTA gerados.")
    return dados_consulta


# 8. Tabela pagamento
def gerar_pagamentos(num_registros, ids_consultas_disponiveis, ids_tipos_pagamento, consultas_data):
    """Gera dados para a tabela pagamento."""
    dados_pagamento = []
    if not ids_consultas_disponiveis or not ids_tipos_pagamento or not consultas_data:
        print("AVISO: Não há consultas ou tipos de pagamento para gerar pagamentos.")
        return []

    # Limitar o número de pagamentos ao número de consultas disponíveis
    num_registros_efetivo = min(num_registros, len(ids_consultas_disponiveis))
    consultas_para_pagamento = random.sample(ids_consultas_disponiveis, num_registros_efetivo)

    for i in range(1, num_registros_efetivo + 1):
        pagamentos_ids.append(i)
        id_consulta_ref = consultas_para_pagamento[i-1]
        # Encontrar a data da consulta correspondente para a data_pagamento
        data_consulta_original = next((c['data_hora'] for c in consultas_data if c['id_consulta'] == id_consulta_ref), datetime.now())
        # Pagamento pode ocorrer no mesmo dia ou alguns dias depois
        data_pagamento_val = data_consulta_original + timedelta(days=random.randint(0, 5))


        dados_pagamento.append({
            'id_pagamento': i,
            'valor_pago': round(random.uniform(50.0, 800.0), 2),
            'data_pagamento': data_pagamento_val,
            'tipo_pagamento_id_tipo_pagamento': random.choice(ids_tipos_pagamento),
            'consulta_id_consulta': id_consulta_ref
        })
    print(f"{len(dados_pagamento)} registros de PAGAMENTO gerados.")
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
                'id_consulta_procedimento': id_pk_consulta_procedimento,
                'consulta_id_consulta': id_consulta,
                'procedimento_id_procedimento': id_procedimento
            })
            id_pk_consulta_procedimento += 1
    print(f"{len(dados_consulta_procedimento)} registros de CONSULTA_PROCEDIMENTO gerados.")
    return dados_consulta_procedimento

# 10. Tabela log_pagamento
def gerar_log_pagamentos(num_registros_pagamento, pagamentos_data):
    """Gera dados para a tabela log_pagamento."""
    dados_log_pagamento = []
    tipos_acao = ['INSERT', 'UPDATE'] # Supondo que podem haver atualizações nos pagamentos
    if not pagamentos_data:
        print("AVISO: Não há dados de pagamento para gerar logs.")
        return []

    id_log_pk = 1
    for pag in pagamentos_data:
        # Para cada pagamento, gerar um log de INSERT
        dados_log_pagamento.append({
            'id_log': id_log_pk,
            'tipo_acao': 'INSERT',
            'id_pagamento': pag['id_pagamento'],
            'tipo_pagamento_id_tipo_pagamento': pag['tipo_pagamento_id_tipo_pagamento'],
            'valor_pago': pag['valor_pago'],
            'data_pagamento': pag['data_pagamento'],
            'DataHoraOperacao': pag['data_pagamento'] + timedelta(seconds=random.randint(1, 300)), # Log um pouco depois do pagamento
            'ExecutedBy': fake.user_name()
        })
        id_log_pk +=1

        # Opcional: Gerar alguns logs de UPDATE para alguns pagamentos
        if random.random() < 0.1: # 10% de chance de ter um update
            dados_log_pagamento.append({
                'id_log': id_log_pk,
                'tipo_acao': 'UPDATE',
                'id_pagamento': pag['id_pagamento'],
                'tipo_pagamento_id_tipo_pagamento': pag['tipo_pagamento_id_tipo_pagamento'], # Poderia mudar
                'valor_pago': round(pag['valor_pago'] * random.uniform(0.8, 1.2), 2), # Valor pode ser alterado
                'data_pagamento': pag['data_pagamento'], # Data do pagamento original
                'DataHoraOperacao': pag['data_pagamento'] + timedelta(days=random.randint(1,5), seconds=random.randint(1, 300)), # Update dias depois
                'ExecutedBy': fake.user_name()
            })
            id_log_pk +=1

    print(f"{len(dados_log_pagamento)} registros de LOG_PAGAMENTO gerados.")
    return dados_log_pagamento

# --- Função para salvar em CSV ---
def salvar_csv(dados, nome_arquivo, cabecalho):
    """Salva uma lista de dicionários em um arquivo CSV."""
    with open(f'{nome_arquivo}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cabecalho)
        writer.writeheader()
        writer.writerows(dados)
    print(f"Dados salvos em {nome_arquivo}.csv")

# --- Orquestração da Geração e Salvamento ---
if __name__ == "__main__":
    print("Iniciando geração de dados...")

    # Gerar dados para tabelas independentes primeiro
    dados_endereco = gerar_enderecos(NUM_ENDERECOS)
    salvar_csv(dados_endereco, 'endereco', ['id_endereco', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep', 'pais'])

    dados_odontologista = gerar_odontologistas(NUM_ODONTOLOGISTAS)
    salvar_csv(dados_odontologista, 'odontologista', ['id_odontologista', 'nome_odontologista', 'especialidade', 'cro'])

    dados_tipos_pagamento = gerar_tipos_pagamento() # Usa NUM_TIPOS_PAGAMENTO
    salvar_csv(dados_tipos_pagamento, 'tipo_pagamento', ['id_tipo_pagamento', 'descricao_tipo_pagamento'])

    dados_procedimentos = gerar_procedimentos(NUM_PROCEDIMENTOS)
    salvar_csv(dados_procedimentos, 'procedimento', ['id_procedimento', 'nome_procedimento', 'descricao_procedimento'])

    # Gerar dados para tabelas dependentes
    dados_pacientes = gerar_pacientes(NUM_PACIENTES, enderecos_ids)
    salvar_csv(dados_pacientes, 'paciente', ['id_paciente', 'nome_paciente', 'cpf_paciente', 'telefone', 'genero', 'data_nasc', 'email', 'endereco_id_endereco'])

    dados_agendamentos = gerar_agendamentos(NUM_AGENDAMENTOS, pacientes_ids, odontologistas_ids)
    salvar_csv(dados_agendamentos, 'agendamento', ['id_agendamento', 'data_agendamento', 'status_agendamento', 'paciente_id_paciente', 'odontologista_id_odontologista'])

    dados_consultas = gerar_consultas(NUM_CONSULTAS, agendamentos_ids, dados_agendamentos) # Passa os dados_agendamentos para pegar status e data
    salvar_csv(dados_consultas, 'consulta', ['id_consulta', 'data_hora', 'diagnostico', 'tratamento', 'agendamento_id_agendamento'])

    dados_pagamentos = gerar_pagamentos(NUM_PAGAMENTOS, consultas_ids, tipos_pagamento_ids, dados_consultas) # Passa dados_consultas para pegar data
    salvar_csv(dados_pagamentos, 'pagamento', ['id_pagamento', 'valor_pago', 'data_pagamento', 'tipo_pagamento_id_tipo_pagamento', 'consulta_id_consulta'])

    dados_consulta_procedimento = gerar_consulta_procedimento(consultas_ids, procedimentos_ids, MIN_PROC_POR_CONSULTA, MAX_PROC_POR_CONSULTA)
    salvar_csv(dados_consulta_procedimento, 'consulta_procedimento', ['id_consulta_procedimento', 'consulta_id_consulta', 'procedimento_id_procedimento'])

    dados_log_pagamento = gerar_log_pagamentos(len(dados_pagamentos), dados_pagamentos) # O número de logs pode ser relacionado aos pagamentos
    salvar_csv(dados_log_pagamento, 'log_pagamento', ['id_log', 'tipo_acao', 'id_pagamento', 'tipo_pagamento_id_tipo_pagamento', 'valor_pago', 'data_pagamento', 'DataHoraOperacao', 'ExecutedBy'])

    print("Geração de dados concluída!")