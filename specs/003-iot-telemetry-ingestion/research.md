# Research: API de Ingestão de Dados IoT (Módulo 1)

**Feature**: API de Ingestão de Dados IoT (Módulo 1)  
**Branch**: `003-iot-telemetry-ingestion`  
**Date**: 2026-09-13  

---

## 1. Arquitetura de Camadas e Desacoplamento da API (Flask)

### Decisão
Estruturar o backend Flask em três camadas estritamente isoladas:
1. **Rotas / API Blueprint (`routes/telemetry.py`)**: Responsável unicamente pela recepção de requisições HTTP, extração do payload JSON e delegação para o validador/serviço.
2. **Validação & Serviço (`services/telemetry_service.py`)**: Validação de tipos, formatos e limites físicos; orquestração da regra de negócio sem executar queries SQL diretas.
3. **Repositório de Persistência (`repositories/telemetry_repository.py`)**: Encapsulamento de conexão e operações de banco de dados (`INSERT INTO leitura_sensores (...)`).

### Racional
- Cumpre a regra de **Isolamento de Domínio** da Constituição do SmartClass.
- Assegura que nenhuma query SQL ou detalhe de banco vaze para as funções de rota da API.
- Facilita testes unitários com mocks na camada de repositório.

### Alternativas Consideradas
- *Queries SQL diretas na rota do Flask*: Rejeitado por violação expressa da constituição e acoplamento prejudicial à manutenção.
- *Framework Django*: Rejeitado por ser excessivamente pesado para um microserviço focado em telemetria IoT.

---

## 2. Acesso a Dados, Integridade e Pool de Conexões (PostgreSQL)

### Decisão
Utilizar `psycopg2-binary` com pool de conexões thread-safe (`ThreadedConnectionPool` ou gerenciador de conexão singleton com `contextmanager`) e consultas estritamente parametrizadas (`%s`).

- **Tabela**: `leitura_sensores`
- **DDL Idempotente**:
  ```sql
  CREATE TABLE IF NOT EXISTS leitura_sensores (
      id SERIAL PRIMARY KEY,
      sala_id VARCHAR(50) NOT NULL,
      temperatura DECIMAL(5,2) NOT NULL,
      umidade DECIMAL(5,2),
      data_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
  );
  ```
- O controle de tempo é gerado exclusivamente pelo servidor de banco de dados (`DEFAULT CURRENT_TIMESTAMP`), garantindo integridade e imutabilidade dos dados históricos.

### Racional
- `DECIMAL(5,2)` acomoda perfeitamente leituras de temperatura (ex: `-20.50` a `999.99` °C) e umidade (`0.00` a `100.00` %) com precisão exata, sem distorções de ponto flutuante em agregações históricas.
- `TIMESTAMP WITH TIME ZONE` evita anomalias de fuso horário entre clientes IoT e o servidor.

### Alternativas Consideradas
- *FLOAT / REAL no PostgreSQL*: Rejeitado devido a pequenas imprecisões de arredondamento inerentes a IEEE 754.
- *Timestamp fornecido pelo cliente ESP32*: Rejeitado porque relógios internos de microcontroladores (RTCs) sofrem drift ou não possuem sincronização NTP confiável após perda de conexão.

---

## 3. Validação Estrutural e Semântica de Falhas (IoT Ingestion)

### Decisão
Implementar rotina de validação pré-persistência que verifica:
1. `Content-Type: application/json` obrigatório.
2. Presença e não-vazio de `sala_id` (string, max 50 caracteres).
3. Presença e conversibilidade de `temperatura` (numérico float/decimal, faixa física razoável de `-40.0` a `85.0` °C).
4. Opcionalidade de `umidade`: se presente, deve ser numérica entre `0.0` e `100.0` %.
5. Retorno de status HTTP semânticos:
   - `201 Created`: `{"status": "success", "data": {"id": 1, "sala_id": "Sala 101", "temperatura": 24.5, "umidade": null, "data_registro": "2026-09-13T18:50:00Z"}}`
   - `400 Bad Request`: `{"status": "error", "message": "Campo obrigatório ausente: 'temperatura'", "code": 400}`
   - `500 Internal Server Error`: `{"status": "error", "message": "Falha na persistência dos dados de telemetria.", "code": 500}`

### Racional
- Bloqueia payloads corrompidos antes de abrir transação no banco.
- Responde com JSON legível para facilitar depuração no monitor serial do microcontrolador ESP32.

---

## 4. Orquestração Docker e Gestão de Segredos (.env)

### Decisão
Orquestrar o ecossistema via `docker-compose.yml` contendo:
- **`db`**: Imagem `postgres:16-alpine` com volume persistente `postgres_data` e healthcheck configurado via `pg_isready`.
- **`backend`**: Imagem Python 3.11/3.12 Flask rodando com Gunicorn/Werkzeug, dependente do healthcheck do `db` (`condition: service_healthy`).
- **Segredos**: Configurações lidas do `.env` (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `PORT`, `FLASK_ENV`), sem credenciais fixadas no repositório.

### Racional
- Garante reprodução 1:1 entre o ambiente de desenvolvimento local e a VPS de produção na Hostinger.
- Permite subir todo o ambiente de forma zero-touch com `docker-compose up --build`.
