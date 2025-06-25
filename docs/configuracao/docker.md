# Docker e Containerização

Este projeto utiliza Docker para simplificar a configuração do ambiente de desenvolvimento, especialmente para o banco de dados PostgreSQL.

## Visão Geral

O arquivo `docker/docker-compose.yml` configura um container PostgreSQL pronto para uso com as seguintes características:

- **Imagem**: PostgreSQL 15
- **Container**: `clinica_odonto`
- **Porta**: 5432 (mapeada para o host)
- **Credenciais**: `root/root`
- **Banco**: `clinica_odonto`

## Configuração do Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: clinica_odonto
    restart: always
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: clinica_odonto
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Comandos Essenciais

### Iniciar os Serviços

```bash
# Navegar até a pasta docker
cd docker

# Subir os containers em background
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f
```

### Gerenciar os Serviços

```bash
# Parar os serviços
docker-compose down

# Reiniciar os serviços
docker-compose restart

# Ver status dos containers
docker-compose ps
```

### Acesso ao Banco de Dados

```bash
# Conectar via psql
psql -h localhost -U root -d clinica_odonto

# Executar comandos SQL direto
docker-compose exec db psql -U root -d clinica_odonto
```

## Volumes e Persistência

O Docker Compose cria um volume nomeado `postgres_data` que persiste os dados do banco entre reinicializações do container.

### Gerenciar Volumes

```bash
# Listar volumes
docker volume ls

# Inspecionar o volume
docker volume inspect docker_postgres_data

# Remover dados (cuidado!)
docker-compose down -v
```

## Portas e Networking

- **PostgreSQL**: Porta 5432 exposta no host
- **Network**: Rede padrão do Docker Compose
- **DNS**: Os serviços se comunicam pelo nome do serviço

## Configurações Customizadas

### Modificar Credenciais

Para usar credenciais diferentes, edite o `docker-compose.yml`:

```yaml
environment:
  POSTGRES_USER: seu_usuario
  POSTGRES_PASSWORD: sua_senha
  POSTGRES_DB: seu_banco
```

### Configurações Avançadas

Para configurações mais avançadas do PostgreSQL:

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: clinica_odonto
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=pt_BR.UTF-8"
    command: >
      postgres 
      -c shared_preload_libraries=pg_stat_statements
      -c max_connections=200
      -c shared_buffers=256MB
```

## Monitoramento e Logs

### Ver Logs

```bash
# Logs de todos os serviços
docker-compose logs

# Logs específicos do banco
docker-compose logs db

# Logs em tempo real
docker-compose logs -f db
```

### Monitorar Performance

```bash
# Ver processos do container
docker-compose exec db ps aux

# Ver conexões ativas
docker-compose exec db psql -U root -d clinica_odonto -c "SELECT * FROM pg_stat_activity;"
```

## Troubleshooting

### Container não inicia

1. Verificar se a porta 5432 está disponível:
   ```bash
   netstat -an | grep 5432
   ```

2. Ver logs detalhados:
   ```bash
   docker-compose logs db
   ```

3. Verificar recursos do sistema:
   ```bash
   docker system df
   ```

### Problemas de Conexão

1. Verificar se o container está rodando:
   ```bash
   docker-compose ps
   ```

2. Testar conectividade:
   ```bash
   telnet localhost 5432
   ```

3. Verificar configurações de rede:
   ```bash
   docker network ls
   docker network inspect docker_default
   ```

### Reset Completo

Se necessário, você pode fazer um reset completo:

```bash
# Parar e remover containers e volumes
docker-compose down -v

# Remover imagens (opcional)
docker rmi postgres:15

# Recriar tudo
docker-compose up -d
```

## Integração com o Pipeline ETL

O banco PostgreSQL no Docker integra perfeitamente com o pipeline ETL:

1. **Geração de Dados**: O `gerador_dados.py` se conecta automaticamente
2. **Notebooks**: Os Jupyter notebooks usam as mesmas credenciais
3. **Scripts SQL**: Podem ser executados diretamente no container

### Exemplo de Uso

```bash
# 1. Subir o banco
docker-compose -f docker/docker-compose.yml up -d

# 2. Executar scripts SQL
psql -h localhost -U root -d clinica_odonto -f scripts/modelo_fisico.sql

# 3. Gerar dados
python scripts/gerador_dados.py

# 4. Executar notebooks
jupyter lab
```

## Alternativas ao Docker

Se preferir não usar Docker:

1. **PostgreSQL Local**: Instale PostgreSQL nativamente
2. **PostgreSQL na Nuvem**: Use serviços como Azure Database for PostgreSQL
3. **SQLite**: Para desenvolvimento simples (requer modificações no código)
