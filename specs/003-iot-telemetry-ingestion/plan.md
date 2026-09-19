# Implementation Plan: API de Ingestão de Dados IoT (Módulo 1)

**Branch**: `003-iot-telemetry-ingestion` | **Date**: 2026-09-13 | **Spec**: [specs/003-iot-telemetry-ingestion/spec.md](file:///c:/Users/muril/unic_clinic/specs/003-iot-telemetry-ingestion/spec.md)  
**Input**: Feature specification from `specs/003-iot-telemetry-ingestion/spec.md`

## Summary

Implementação do serviço de backend responsável por receber, validar e persistir medições de temperatura (e umidade opcional) enviadas por microcontroladores IoT (ESP32) em salas de aula. A solução expõe o endpoint RESTful `POST /api/v1/medicoes` em Python/Flask, com isolamento estrito da camada de persistência PostgreSQL via Repository Pattern, validação defensiva de payloads com semântica de erro explícita e conteinerização multi-container via Docker Compose.

## Technical Context

**Language/Version**: Python 3.11 / 3.12  
**Primary Dependencies**: Flask 3.x, psycopg2-binary (ou driver PostgreSQL compatível com pool), python-dotenv, gunicorn  
**Storage**: PostgreSQL 16 Alpine (tabela `leitura_sensores`)  
**Testing**: pytest, pytest-mock (testes de contrato e unitários de repositório/validador)  
**Target Platform**: Linux / Docker Engine (Hostinger VPS & Local Dev)  
**Project Type**: Web Service / RESTful Ingestion API  
**Performance Goals**: Latência p95 < 200ms por requisição de ingestão em rede local / banda padrão  
**Constraints**: Zero SQL em rotas web; isolamento total de credenciais via `.env`; tempo controlado exclusivamente pelo banco (`CURRENT_TIMESTAMP`)  
**Scale/Scope**: Ingestão periódica por ambiente escolar (leituras regulares a cada 30-60s)  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Fronteiras Arquiteturais e Persistência**:
  - Backend Flask atua estritamente como API RESTful (sem SSR).
  - Rotas web desacopladas de SQL: acesso a dados isolado em `TelemetryRepository`.
  - Contratos de dados em JSON estruturado com validação prévia.
  - Imutabilidade e integridade temporal: timestamps gerados pelo PostgreSQL (`CURRENT_TIMESTAMP`).
- [x] **II. Estado, Reatividade e Frontend**:
  - API preparada para consumo passivo via Fetch API por dashboards futuros.
  - Sem persistência de estado de sessão complexo no backend.
- [x] **III. Qualidade, Testes e Resiliência**:
  - Semântica de erros explícita (201 Created, 400 Bad Request, 500 Internal Server Error com payload JSON explicativo).
  - Gestão de segredos e credenciais de banco estritamente via `.env`.
  - Imutabilidade de ambiente garantida por `Dockerfile` e `docker-compose.yml`.

## Project Structure

### Documentation (this feature)

```text
specs/003-iot-telemetry-ingestion/
├── plan.md              # Este plano de implementação
├── research.md          # Decisões arquiteturais e de resiliência
├── data-model.md        # Esquema relacional e regras de integridade (leitura_sensores)
├── quickstart.md        # Guia rápido de execução e testes
├── contracts/
│   └── telemetry-ingestion.contract.json # Contrato JSON Schema / OpenAPI do endpoint
└── checklists/
    └── requirements.md  # Checklist de qualidade da especificação
```

### Source Code (repository layout)

```text
backend/
├── Dockerfile                  # Imagem Docker do backend Flask
├── requirements.txt            # Dependências Python (Flask, psycopg2-binary, etc.)
├── .env.example                # Template de variáveis de ambiente
├── src/
│   ├── app.py                  # Application Factory do Flask
│   ├── config.py               # Carregamento de configurações a partir do .env
│   ├── database.py             # Gerenciamento de pool de conexões com PostgreSQL
│   ├── models/
│   │   └── telemetry.py        # Objeto de domínio / dataclass LeituraSensor
│   ├── repositories/
│   │   └── telemetry_repo.py   # Camada de acesso a dados e queries SQL parametrizadas
│   ├── services/
│   │   └── telemetry_service.py # Validação estrutural de payloads e regras de negócio
│   └── routes/
│       └── telemetry_routes.py # Blueprint da API (/api/v1/medicoes)
└── tests/
    ├── conftest.py             # Fixtures e client de testes do Flask
    ├── test_contracts.py       # Testes de contrato do endpoint POST /api/v1/medicoes
    └── test_validation.py      # Testes unitários de validação e tratamento de erros

docker-compose.yml              # Orquestração dos serviços backend e PostgreSQL (db)
```

## Complexity Tracking

| Decisão Arquitetural | Por que é necessária | Alternativa mais simples rejeitada porque |
|---|---|---|
| Camada de Repositório (`TelemetryRepository`) | Isola completamente as queries SQL e manipulação de cursores da camada HTTP | Queries em rotas violam a constituição e dificultam manutenção/testes |
| Controle de timestamp no PostgreSQL (`CURRENT_TIMESTAMP`) | Garante integridade histórica imutável dos dados sem depender de relógios de hardware (ESP32) | Relógios de RTC em microcontroladores sofrem drift ou desincronização |
| Validação prévia de schema JSON | Bloqueia payloads corrompidos sem onerar o banco de dados | Deixar o banco lançar erro de integridade gera falhas 500 genéricas em vez de 400 semânticos |
