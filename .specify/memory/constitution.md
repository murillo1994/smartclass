<!--
Sync Impact Report:
- Version change: 1.1.0 -> 1.0.0 (SmartClass initial adoption)
- List of modified principles:
  - PRINCIPLE_1: I. Fronteiras Arquiteturais e Persistência (Definido)
  - PRINCIPLE_2: II. Estado, Reatividade e Frontend (Definido)
  - PRINCIPLE_3: III. Qualidade, Testes e Resiliência (Definido)
- Added sections:
  - I. Fronteiras Arquiteturais e Persistência
  - II. Estado, Reatividade e Frontend
  - III. Qualidade, Testes e Resiliência
  - Arquitetura e Contratos de Dados (IoT & REST API)
  - Infraestrutura e Ambientes de Execução
- Removed sections:
  - Seções e princípios legados da Unic Clinic
- Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ verificado (alinhado)
  - .specify/templates/spec-template.md: ✅ verificado (alinhado)
  - .specify/templates/tasks-template.md: ✅ verificado (alinhado)
- Follow-up TODOs: Nenhum
-->

# SmartClass (IoT & Web App) Constitution

## Core Principles

### I. Fronteiras Arquiteturais e Persistência
- **Isolamento de Domínio**: O backend Python atua estritamente como uma API RESTful. A camada de rotas web não deve conter consultas SQL diretas ou lógica de negócio bruta; o acesso ao PostgreSQL deve ser obrigatoriamente isolado em uma camada estruturada de repositório ou ORM.
- **Contratos e Comunicação**: A ingestão de dados capturados pelo hardware ESP32 e o consumo de métricas pelo dashboard devem ocorrer obrigatoriamente via payloads JSON estruturados, validados e tipados.
- **Integridade Relacional**: Os registros de telemetria de temperatura e umidade são estritamente imutáveis após a inserção. O modelo de dados deve garantir marcações precisas de tempo (*timestamps* UTC/ISO 8601) para viabilizar a análise histórica e cálculo de médias da sala de aula.

### II. Estado, Reatividade e Frontend
- **UI Estática e Desacoplada**: O frontend HTML/JS atua de forma passiva e desacoplada, requisitando históricos e agregações da API REST de forma assíncrona (Fetch API). O backend é proibido de realizar Server-Side Rendering (SSR) de páginas HTML ou reter estado complexo de sessão.
- **Composição Utilitária**: A construção visual e estilização do dashboard devem ser resolvidas exclusivamente na própria marcação estrutural utilizando classes utilitárias (Tailwind CSS). É estritamente proibido o acúmulo de regras CSS globais arbitrárias ou folhas de estilo customizadas que dificultem a manutenção.

### III. Qualidade, Testes e Resiliência
- **Semântica de Falhas**: Leituras ausentes do hardware IoT, payloads corrompidos ou quebras de conexão com o banco de dados não podem gerar falhas silenciosas. O sistema deve emitir status HTTP semânticos (ex: 400 Bad Request para erro de formato, 422 Unprocessable Entity para validação de campos, 500/503 para falhas de infraestrutura) acompanhados de payload JSON detalhando a causa explícita do erro.
- **Gestão de Segredos**: Credenciais de banco de dados, chaves de API e variáveis de rede/Wi-Fi do microcontrolador estão proibidas no código-fonte sob controle de versão. Todas as configurações sensíveis devem ser geridas por isolamento estrito via variáveis de ambiente (`.env`).
- **Imutabilidade de Ambiente**: A arquitetura do backend e do banco de dados deve ser 100% conteinerizada com Docker / Docker Compose. O ambiente de desenvolvimento local deve ser reproduzível de maneira idêntica em produção, orientando os Pull Requests do GitHub diretamente para os contêineres hospedados na VPS da Hostinger.

## Arquitetura e Contratos de Dados (IoT & REST API)

1. **Ingestão IoT (ESP32 -> API)**:
   - Endpoint dedicado para recepção de telemetria via `POST /api/telemetry` (ou equivalente).
   - Validação obrigatória de payload contendo identificador do dispositivo/sensor, temperatura (°C), umidade (%) e timestamp.
   - Tratamento resiliente de desconexões e timeouts da rede sem travamento do firmware do sensor ou da API.

2. **Consumo Dashboard (Frontend -> API)**:
   - Endpoints para listagem de leituras recentes (`GET /api/telemetry/recent`) e agregações históricas/médias (`GET /api/telemetry/metrics`).
   - Respostas padronizadas em JSON com headers CORS devidamente configurados.

## Infraestrutura e Ambientes de Execução

- **Docker Compose**: Orquestração multi-contêiner contendo os serviços da API Python e instância do PostgreSQL com volumes persistentes para dados.
- **Deploy na VPS Hostinger**: Pipeline de integração e entrega contínua baseada em contêineres Docker, garantindo paridade absoluta entre desenvolvimento e produção.

## Governance

A presente constituição estabelece os padrões arquiteturais, técnicos e de qualidade mandatórios para o projeto **SmartClass (IoT & Web App)**. 

- **Supremacia**: Todas as especificações (`spec.md`), planos de implementação (`plan.md`) e listas de tarefas (`tasks.md`) devem estar em total conformidade com estes princípios.
- **Emendas**: Qualquer alteração ou extensão destes princípios exige proposta documentada, justificativa técnica e atualização deste arquivo com incremento semântico de versão (MAJOR para quebras/remoções estruturais, MINOR para novos princípios ou expansões, PATCH para ajustes textuais).
- **Verificação**: Todo pull request e revisão de código deve validar explicitamente a aderência às fronteiras arquiteturais, tipagem de contratos e políticas de segredos/conteinerização.

**Version**: 1.0.0 | **Ratified**: 2026-09-13 | **Last Amended**: 2026-09-13
