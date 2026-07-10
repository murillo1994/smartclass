# Guia de Início Rápido: Configuração do Sistema Unic Clinic

Este guia orienta na configuração e execução local do ecossistema Unic Clinic usando Docker Compose.

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Uma chave de API ativa da OpenAI
- Uma instância funcional configurada na Evolution API (ex: `unic_clinic`)

---

## 1. Configurações de Ambiente

Crie um arquivo `.env` na raiz do projeto contendo as seguintes propriedades:

```env
# Configurações do Banco de Dados
POSTGRES_USER=unic_admin
POSTGRES_PASSWORD=unic_secure_pass
POSTGRES_DB=unic_clinic_db
DATABASE_URL=postgresql://unic_admin:unic_secure_pass@unic_db:5432/unic_clinic_db

# API da OpenAI
OPENAI_API_KEY=sua_chave_da_api_openai_aqui

# Configurações da Evolution API
EVOLUTION_API_URL=http://seu-servidor-evolution-api:8080
EVOLUTION_API_KEY=sua_chave_global_da_evolution_aqui
EVOLUTION_INSTANCE_NAME=unic_clinic
EVOLUTION_WEBHOOK_SECRET=seu_segredo_webhook_opcional

# Configurações do Flask
FLASK_ENV=development
PORT=5000

# Configurações do Frontend (SvelteKit)
PUBLIC_API_URL=http://localhost:5000/api
```

---

## 2. Executando a Aplicação

Para iniciar os contêineres do banco de dados, backend e frontend na ordem correta, execute:

```bash
docker-compose up --build
```

Isso inicializará:
1. **`unic_db`** (PostgreSQL) na porta 5432 (apenas rede interna).
2. **`unic_backend`** (Flask API) na porta 5000.
3. **`unic_frontend`** (Site e CRM SvelteKit) na porta 5173.

---

## 3. Semeando Procedimentos no Banco de Dados

Assim que os contêineres estiverem em execução, as migrações do banco serão aplicadas automaticamente. Você pode preencher os procedimentos da clínica no banco de dados executando o script de sementes (seed) do backend:

```bash
# Comando para rodar o script de inserção de dados iniciais do backend
docker-compose exec unic_backend python seed_db.py
```

---

## 4. Configurando Webhook no Painel da Evolution API

Configure o webhook na Evolution API apontando para o seu backend:
- **URL do Webhook**: `http://<ip-da-sua-vps>:5000/webhook/evolution`
- **Eventos**: Selecione `MESSAGES_UPSERT`
- **Status**: Ativo/Habilitado
