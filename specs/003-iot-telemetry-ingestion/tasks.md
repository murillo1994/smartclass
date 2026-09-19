# Tasks: API de Ingestão de Dados IoT (Módulo 1)

**Input**: Design documents from `specs/003-iot-telemetry-ingestion/`  
**Prerequisites**: [plan.md](file:///c:/Users/muril/unic_clinic/specs/003-iot-telemetry-ingestion/plan.md), [spec.md](file:///c:/Users/muril/unic_clinic/specs/003-iot-telemetry-ingestion/spec.md), [data-model.md](file:///c:/Users/muril/unic_clinic/specs/003-iot-telemetry-ingestion/data-model.md), [contracts/telemetry-ingestion.contract.json](file:///c:/Users/muril/unic_clinic/specs/003-iot-telemetry-ingestion/contracts/telemetry-ingestion.contract.json), [research.md](file:///c:/Users/muril/unic_clinic/specs/003-iot-telemetry-ingestion/research.md), [quickstart.md](file:///c:/Users/muril/unic_clinic/specs/003-iot-telemetry-ingestion/quickstart.md)

**Tests**: Testes automatizados incluídos para validação de contratos, rejeição de payloads inválidos e persistência.

**Organization**: Tarefas agrupadas por User Story para implementação e validação independentes.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Inicialização do projeto, configuração de dependências e orquestração Docker.

- [X] T001 Configure environment variables template in `backend/.env.example`
- [X] T002 [P] Update Python backend dependencies in `backend/requirements.txt`
- [X] T003 [P] Configure multi-container orchestration in `docker-compose.yml`
- [X] T004 [P] Configure Python container build in `backend/Dockerfile`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Infraestrutura de banco de dados, pool de conexões e base do backend Flask.

**⚠️ CRITICAL**: Nenhuma User Story pode ser iniciada até a conclusão desta fase.

- [X] T005 Implement environment configuration loader in `backend/src/config.py`
- [X] T006 [P] Implement thread-safe PostgreSQL connection pool and DDL migration in `backend/src/database.py`
- [X] T007 [P] Create domain entity data model `LeituraSensor` in `backend/src/models/telemetry.py`
- [X] T008 Implement `TelemetryRepository` for parameterized SQL queries in `backend/src/repositories/telemetry_repo.py`
- [X] T009 Configure Flask Application Factory and global error handling in `backend/src/app.py`

**Checkpoint**: Base de persistência e container Flask inicializados e testáveis.

---

## Phase 3: User Story 1 - Ingestão de Telemetria de Temperatura da Sala de Aula (Priority: P1) 🎯 MVP

**Goal**: Permitir que o hardware IoT (ESP32) envie medições de temperatura via `POST /api/v1/medicoes` e receba `201 Created` com registro imutável persistido no PostgreSQL.

**Independent Test**: Enviar requisição POST com `{"sala_id": "Sala 101", "temperatura": 24.5}` e validar retorno 201 com id e timestamp gravado no banco de dados.

### Tests for User Story 1
- [X] T010 [P] [US1] Create contract and integration test suite for valid ingestion in `backend/tests/test_ingestion_us1.py`

### Implementation for User Story 1
- [X] T011 [US1] Implement core measurement registration logic in `backend/src/services/telemetry_service.py`
- [X] T012 [US1] Implement route handler `POST /api/v1/medicoes` in `backend/src/routes/telemetry_routes.py`
- [X] T013 [US1] Register `telemetry_bp` blueprint in Flask app in `backend/src/app.py`

**Checkpoint**: User Story 1 funcional de ponta a ponta (MVP concluído).

---

## Phase 4: User Story 2 - Validação Estrutural e Rejeição de Payloads Inválidos (Priority: P2)

**Goal**: Interceptar payloads malformados ou incompletos antes da persistência, retornando HTTP `400 Bad Request` com detalhamento semântico do erro.

**Independent Test**: Enviar POST sem a chave `temperatura` ou com JSON malformado e verificar retorno HTTP 400 imediato sem inserção no banco de dados.

### Tests for User Story 2
- [X] T014 [P] [US2] Create test suite for validation failures and error responses in `backend/tests/test_validation_us2.py`

### Implementation for User Story 2
- [X] T015 [US2] Implement structural schema validator and boundary checks in `backend/src/services/telemetry_service.py`
- [X] T016 [US2] Connect validation layer and 400 error payload responses in `backend/src/routes/telemetry_routes.py`

**Checkpoint**: User Stories 1 e 2 funcionais e blindadas contra entradas inválidas.

---

## Phase 5: User Story 3 - Suporte a Medições Combinadas com Umidade Opcional (Priority: P3)

**Goal**: Permitir envio simultâneo de temperatura e umidade relativa (%) mantendo o campo opcional para sensores legados.

**Independent Test**: Enviar POST com `{"sala_id": "Lab 02", "temperatura": 22.0, "umidade": 65.5}` e verificar persistência de ambos os valores decimais com HTTP 201.

### Tests for User Story 3
- [X] T017 [P] [US3] Create test suite for optional humidity ingestion in `backend/tests/test_humidity_us3.py`

### Implementation for User Story 3
- [X] T018 [US3] Extend `TelemetryService` and `TelemetryRepository` to process and persist optional `umidade` in `backend/src/services/telemetry_service.py` and `backend/src/repositories/telemetry_repo.py`

**Checkpoint**: Todas as User Stories (P1, P2 e P3) completas e testadas.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Resiliência de falha no banco de dados, script de teste de hardware e validação final.

- [X] T019 [P] Implement resilient database exception handling (500 Internal Server Error) in `backend/src/routes/telemetry_routes.py` and `backend/src/app.py`
- [X] T020 [P] Create automated ESP32 hardware simulation script in `backend/scripts/simulate_sensor.py`
- [X] T021 Execute full end-to-end validation via `specs/003-iot-telemetry-ingestion/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sem dependências — execução imediata.
- **Foundational (Phase 2)**: Depende do Setup — **BLOQUEIA** todas as User Stories.
- **User Story 1 (Phase 3)**: Depende da Fase Foundational — Entrega o MVP.
- **User Story 2 (Phase 4)**: Depende de US1 (enriquece o endpoint com validações robustas).
- **User Story 3 (Phase 5)**: Depende de US1 e US2 (expande suporte a campos opcionais).
- **Polish (Phase 6)**: Depende da conclusão das User Stories.

### Parallel Execution Opportunities

- T002, T003 e T004 (Setup) podem rodar em paralelo.
- T006 e T007 (Foundational) podem rodar em paralelo.
- T010, T014 e T017 (Testes) podem ser desenvolvidos em paralelo às suas respectivas implementações.
- T019 e T020 (Polish) podem rodar em paralelo.

---

## Implementation Strategy

### MVP First (User Story 1)
1. Concluir Fase 1 (Setup) e Fase 2 (Foundational).
2. Implementar Fase 3 (User Story 1).
3. Validar fluxo principal com POST válido gerando registro no PostgreSQL (Status 201).

### Incremental Delivery
1. Adicionar validações defensivas e semântica de erros (User Story 2).
2. Adicionar suporte a umidade opcional (User Story 3).
3. Adicionar simulação de hardware e validação com Docker (Polish).
