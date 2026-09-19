# Feature Specification: API de Ingestão de Dados IoT (Módulo 1)

**Feature Branch**: `003-iot-telemetry-ingestion`  
**Created**: 2026-09-13  
**Status**: Draft  
**Input**: User description: "API de Ingestão de Dados IoT (Módulo 1) - Implementar o serviço de backend responsável por receber, validar e persistir as medições de temperatura enviadas pelo sensor na sala de aula."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ingestão de Telemetria de Temperatura da Sala de Aula (Priority: P1) 🎯 MVP

Como hardware de sensoriamento IoT (ESP32) instalado na sala de aula,
Quero enviar leituras periódicas de temperatura para o serviço central via requisição estruturada,
Para que as medições térmicas do ambiente fiquem registradas historicamente com data e hora exatas de captura para análise de conforto.

**Why this priority**: É o fluxo principal (Golden Path) da aplicação. Sem a capacidade de receber e registrar medições válidas de temperatura no banco de dados, nenhum módulo downstream (dashboard, relatórios ou alertas) pode operar.

**Independent Test**: Enviar uma requisição HTTP POST simulada contendo `{"sala_id": "Sala 101", "temperatura": 24.5}` e verificar o retorno de status HTTP 201 Created com identificador do registro e a presença imediata do dado persistido com timestamp do servidor.

**Acceptance Scenarios**:

1. **Given** que o serviço de ingestão está ativo e o banco de dados acessível,
   **When** o sensor envia uma medição com `sala_id` válido e `temperatura` numérica válida,
   **Then** o sistema deve persistir a leitura de forma imutável, atribuir o timestamp de registro no banco de dados e retornar HTTP 201 Created com o identificador único gerado.

2. **Given** uma medição recém-inserida com sucesso,
   **When** a base de dados é consultada pelo identificador retornado,
   **Then** o registro deve conter exatamente a `sala_id`, o valor de `temperatura` informado, `umidade` como nula e a `data_registro` preenchida com o horário do sistema.

---

### User Story 2 - Validação Estrutural e Rejeição de Payloads Inválidos (Priority: P2)

Como mantenedor do sistema de monitoramento escolar,
Quero que o endpoint de ingestão rejeite sumariamente requisições malformadas ou com dados ausentes antes de qualquer tentativa de persistência,
Para garantir a integridade relacional, evitar dados corrompidos no banco e fornecer diagnóstico explícito de erro ao cliente HTTP.

**Why this priority**: Protege o sistema contra leituras inválidas causadas por instabilidades de firmware, ruído de rede ou pacotes truncados, garantindo a semântica de falhas exigida pela constituição.

**Independent Test**: Enviar requisições POST com payloads vazios, tipos incorretos ou sem as chaves obrigatórias (`sala_id` ou `temperatura`) e validar o retorno imediato de HTTP 400 Bad Request com descrição semântica do erro, sem inserções no banco.

**Acceptance Scenarios**:

1. **Given** que o sensor ou cliente envia uma requisição sem o campo obrigatório `temperatura` (ex: `{"sala_id": "Sala 101"}`),
   **When** o serviço processa a entrada,
   **Then** a requisição deve ser interceptada na camada de validação e retornar HTTP 400 Bad Request indicando a ausência do campo, sem gerar registro no banco de dados.

2. **Given** uma requisição com corpo vazio, JSON malformado ou tipo de dado não numérico para temperatura,
   **When** a requisição atinge o endpoint,
   **Then** o sistema deve retornar HTTP 400 Bad Request com mensagem detalhando a falha estrutural.

---

### User Story 3 - Suporte a Medições Combinadas com Umidade Opcional (Priority: P3)

Como gestor de infraestrutura da sala de aula com sensores avançados (temperatura e umidade conjugadas),
Quero poder transmitir o valor de umidade relativa do ar no mesmo payload de ingestão,
Para enriquecer a análise ambiental e climática da sala sem quebrar a compatibilidade com sensores legados que medem apenas temperatura.

**Why this priority**: Permite evolução do hardware sem exigir múltiplos endpoints ou criar inconsistências contratuais, mantendo o campo `umidade` estritamente opcional e retrocompatível.

**Independent Test**: Enviar requisição contendo `{"sala_id": "Lab 02", "temperatura": 22.0, "umidade": 65.5}` e verificar o retorno 201 Created com a persistência de ambos os valores decimais associados ao registro.

**Acceptance Scenarios**:

1. **Given** um hardware IoT capaz de medir umidade relativa,
   **When** a requisição inclui o campo `umidade` com valor float/decimal válido,
   **Then** o sistema deve validar tanto a temperatura quanto a umidade e persistir ambos os valores na tabela com HTTP 201 Created.

2. **Given** um hardware legado sem sensor de umidade enviando payload sem a chave `umidade`,
   **When** o payload é processado,
   **Then** o sistema deve aceitar a medição, gravando o campo de umidade como nulo sem gerar erros ou advertências.

---

### Edge Cases

- **Valores Extremos de Temperatura/Umidade**: Como o sistema lida com leituras fisicamente improváveis (ex: temperatura de -50°C ou +150°C, ou umidade negativa / acima de 100%)? O sistema deve validar limites razoáveis ou registrar o valor com integridade decimal de 2 casas decimais.
- **Indisponibilidade Temporária do Banco de Dados**: Caso a conexão com o PostgreSQL falhe ou sofra timeout, o serviço não deve travar silenciosamente; deve capturar a exceção e retornar HTTP 500 Internal Server Error com payload explicativo.
- **Caracteres Especiais e Tamanho de `sala_id`**: O identificador da sala deve suportar até 50 caracteres (alfanuméricos, espaços, hífens) e rejeitar strings excessivamente longas (>50 caracteres) com HTTP 400.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE expor um endpoint HTTP no caminho `POST /api/v1/medicoes` para ingestão de telemetria.
- **FR-002**: O endpoint DEVE exigir payload no formato `application/json`.
- **FR-003**: O payload DEVE conter obrigatoriamente os campos `sala_id` (string de até 50 caracteres) e `temperatura` (valor numérico com precisão de até 2 casas decimais).
- **FR-004**: O payload PODE conter opcionalmente o campo `umidade` (valor numérico com precisão de até 2 casas decimais).
- **FR-005**: O sistema DEVE validar o formato e presença dos campos obrigatórios antes de delegar a gravação para a camada de persistência.
- **FR-006**: O sistema DEVE rejeitar requisições sem `sala_id`, sem `temperatura`, com JSON inválido ou campos fora de tipo com status HTTP 400 Bad Request e mensagem de erro estruturada em JSON.
- **FR-007**: O sistema DEVE persistir os dados validados na tabela `leitura_sensores` com `id`, `sala_id`, `temperatura`, `umidade` (ou null) e `data_registro` gerado automaticamente pelo banco de dados (`CURRENT_TIMESTAMP`).
- **FR-008**: O sistema DEVE retornar status HTTP 201 Created contendo o identificador do registro gerado e mensagem de sucesso ao concluir a persistência.
- **FR-009**: Em caso de falha de conexão ou erro no banco de dados, o sistema DEVE retornar status HTTP 500 Internal Server Error sem expor credenciais ou rastros sensíveis no payload de resposta.
- **FR-010**: A lógica de persistência e acesso a dados DEVE ser estritamente desacoplada das funções de rota da API (Repository Pattern / Service Layer).

### Key Entities

- **LeituraSensor (Telemetria)**:
  - `id`: Identificador único do registro (Primary Key, numérico sequencial ou UUID).
  - `sala_id`: Código/nome identificador da sala de aula (Texto, max 50 chars, obrigatório).
  - `temperatura`: Valor térmico medido em graus Celsius (Numérico decimal 5,2, obrigatório).
  - `umidade`: Valor da umidade relativa do ar em porcentagem (Numérico decimal 5,2, opcional/anulável).
  - `data_registro`: Carimbo de data/hora da persistência no servidor (Timestamp UTC com timezone, preenchido automaticamente pelo banco, imutável).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O envio de uma requisição válida via cliente HTTP/ESP32 é persistido e responde com código HTTP 201 em menos de 200ms sob condições normais de rede local.
- **SC-002**: 100% das requisições com campos obrigatórios ausentes ou tipos incompatíveis são barradas com código HTTP 400 antes de executar qualquer query no banco.
- **SC-003**: 100% dos registros persistidos possuem carimbo temporal de inserção confiável gerado pelo servidor/banco de dados, sem discrepâncias de fuso.
- **SC-004**: Todo o ambiente de backend e banco de dados sobe e fica operacional de forma autônoma e determinística através de um único comando `docker-compose up --build`.

## Assumptions

- O dispositivo IoT (ESP32) conecta-se via Wi-Fi e é capaz de efetuar requisições HTTP POST com cabeçalho `Content-Type: application/json`.
- A granularidade de envio das medições pelo sensor ocorre em intervalos regulares (ex: a cada 30 segundos ou 1 minuto), volume bem suportado pela API síncrona.
- Os fusos horários e marcações temporais no PostgreSQL utilizam UTC como padrão interno de integridade.
- Variáveis de ambiente sensíveis (credenciais de banco, portas, hosts) serão fornecidas via arquivo `.env` local e em produção.
