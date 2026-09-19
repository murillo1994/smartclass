# Quickstart: API de Ingestão de Dados IoT (Módulo 1)

Guia de execução rápida e validação do serviço de ingestão de telemetria IoT do SmartClass em ambiente de desenvolvimento local.

---

## 1. Pré-Requisitos

- **Docker** e **Docker Compose** instalados e em execução.
- **cURL**, **HTTPie** ou **Postman** para envio de requisições de teste.
- **Python 3.10+** (opcional, para execução de testes unitários locais sem Docker).

---

## 2. Configuração de Variáveis de Ambiente

Crie o arquivo `.env` na raiz do projeto (baseado em `.env.example`):

```bash
# Banco de Dados PostgreSQL
POSTGRES_DB=smartclass_db
POSTGRES_USER=smartclass_user
POSTGRES_PASSWORD=smartclass_secret
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Aplicação Flask
FLASK_ENV=development
FLASK_APP=src.app:create_app
PORT=5000
DATABASE_URL=postgresql://smartclass_user:smartclass_secret@db:5432/smartclass_db
```

---

## 3. Subir o Ambiente Multi-Container

Execute o comando de inicialização com build automático:

```bash
docker-compose up --build -d
```

Verifique se os contêineres `backend` e `db` estão saudáveis e operacionais:

```bash
docker-compose ps
```

---

## 4. Testes de Validação Prática

### Cenário 1: Ingestão de Temperatura com Sucesso (Status 201)

Simule o envio periódico de telemetria pelo microcontrolador ESP32:

```bash
curl -X POST http://localhost:5000/api/v1/medicoes \
  -H "Content-Type: application/json" \
  -d '{
    "sala_id": "Sala 101",
    "temperatura": 23.75
  }'
```

**Resposta esperada (HTTP 201 Created):**
```json
{
  "status": "success",
  "message": "Medição registrada com sucesso.",
  "data": {
    "id": 1,
    "sala_id": "Sala 101",
    "temperatura": 23.75,
    "umidade": null,
    "data_registro": "2026-09-13T18:55:00.000Z"
  }
}
```

---

### Cenário 2: Ingestão Combinada com Umidade Opcional (Status 201)

```bash
curl -X POST http://localhost:5000/api/v1/medicoes \
  -H "Content-Type: application/json" \
  -d '{
    "sala_id": "Lab 02",
    "temperatura": 21.50,
    "umidade": 58.20
  }'
```

**Resposta esperada (HTTP 201 Created):**
```json
{
  "status": "success",
  "message": "Medição registrada com sucesso.",
  "data": {
    "id": 2,
    "sala_id": "Lab 02",
    "temperatura": 21.50,
    "umidade": 58.20,
    "data_registro": "2026-09-13T18:55:30.000Z"
  }
}
```

---

### Cenário 3: Rejeição de Payload sem Temperatura (Status 400)

```bash
curl -X POST http://localhost:5000/api/v1/medicoes \
  -H "Content-Type: application/json" \
  -d '{
    "sala_id": "Sala 101"
  }'
```

**Resposta esperada (HTTP 400 Bad Request):**
```json
{
  "status": "error",
  "message": "Campo obrigatório ausente: 'temperatura'",
  "code": 400
}
```

---

## 5. Inspeção Direta no Banco de Dados

Verifique a persistência imutável dos registros no PostgreSQL:

```bash
docker-compose exec db psql -U smartclass_user -d smartclass_db -c "SELECT * FROM leitura_sensores ORDER BY id DESC;"
```

---

## 6. Parar e Limpar o Ambiente

```bash
docker-compose down
```
