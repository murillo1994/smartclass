# Tarefas de Implementação: Unic Clinic System

**Entrada**: Documentos de design em `/specs/001-unic-clinic-system/`
**Prerrequisitos**: plan.md (necessário), spec.md (necessário), research.md, data-model.md, contracts/

## Formato: `[ID] [P?] [Caso de Uso] Descrição`

- **[P]**: Pode rodar em paralelo (arquivos distintos, sem dependência direta).
- **[Caso de Uso]**: Identificador correspondente (ex: US1, US2, US3).
- Caminhos completos de arquivos são especificados nas tarefas.

---

## Fase 1: Configuração (Setup - Infraestrutura Inicial)

**Objetivo**: Inicialização do projeto, dependências e estrutura de pastas.

- [x] T001 Criar a estrutura básica de pastas do backend e frontend conforme o plano de desenvolvimento em `backend/` e `frontend/`
- [x] T002 [P] Criar o arquivo `backend/requirements.txt` definindo dependências como Flask, OpenAI e SQLAlchemy
- [x] T003 [P] Criar o arquivo `frontend/package.json` contendo as dependências base do SvelteKit e Tailwind CSS
- [x] T004 [P] Criar o arquivo de variáveis de ambiente `.env` na raiz com base nas orientações de início rápido do quickstart.md

---

## Fase 2: Fundação (Foundational - Pré-requisitos Bloqueantes)

**Objetivo**: Infraestrutura base que deve ser concluída antes do início de qualquer caso de uso.

**⚠️ CRITICAL**: Nenhuma história de usuário ou caso de uso deve ser iniciado até o término desta fase.

- [x] T005 Configurar o orquestrador `docker-compose.yml` na raiz do projeto integrando os contêineres `unic_db`, `unic_backend` e `unic_frontend`
- [x] T006 [P] Configurar o arquivo de imagem Docker do backend em `backend/Dockerfile`
- [x] T007 [P] Configurar o arquivo de imagem Docker do frontend em `frontend/Dockerfile`
- [x] T008 Criar os modelos relacionais SQLAlchemy para banco de dados e conexão em `backend/src/database.py` (tabelas: Patient, Message, Procedure, Appointment)
- [x] T009 Criar o arquivo de leitura e validação de variáveis de ambiente em `backend/src/config.py`
- [x] T010 Configurar a inicialização do Flask e tratamento de erros global em `backend/src/app.py`

**Ponto de Controle**: Estrutura base pronta - a implementação das histórias de usuário pode começar em paralelo.

---

## Fase 3: Caso de Uso 1 - Captação e Agendamento Autônomo via WhatsApp (Prioridade: P1) 🎯 MVP

**Objetivo**: Integração com Evolution API e OpenAI Function Calling para conversas autônomas e reserva direta de horários no banco.

**Teste Independente**: Disparar requisições POST para a rota de webhook simulando o payload da Evolution API, confirmando respostas do agente de IA e a inserção/bloqueio correto de horários.

### Implementação para o Caso de Uso 1

- [x] T011 [P] [US1] Criar o serviço cliente HTTP de envio de mensagens e interação com a Evolution API em `backend/src/services/evolution_service.py`
- [x] T012 [P] [US1] Criar a lógica de conversação base da IA e chamadas à API da OpenAI em `backend/src/services/openai_service.py`
- [x] T013 [US1] Implementar ferramentas de Function Calling (`check_available_slots`, `book_appointment`, `get_procedures`) para busca e reserva de agendamentos em `backend/src/services/openai_service.py`
- [x] T014 [US1] Criar a rota de webhook `/webhook/evolution` para capturar os eventos `MESSAGES_UPSERT` e integrar ao loop da OpenAI em `backend/src/routes/webhook.py`
- [x] T015 [US1] Desenvolver o script de semeação do banco de dados `backend/seed_db.py` para popular a tabela de procedimentos iniciais

**Ponto de Controle**: O Caso de Uso 1 está totalmente funcional de forma autônoma.

---

## Fase 4: Caso de Uso 2 - Painel Administrativo de CRM Kanban (Prioridade: P2)

**Objetivo**: Quadro Kanban interativo com os leads e visualização de chat completo com interrupção manual da IA (Handoff).

**Teste Independente**: Acessar o painel CRM no SvelteKit, mover um card no Kanban, entrar na sala de chat e enviar mensagens manuais que pausam a resposta automática do bot.

### Implementação para o Caso de Uso 2

- [ ] T016 [P] [US2] Criar os endpoints REST em `backend/src/routes/api.py` para recuperar leads (etapas Kanban) e histórico de conversas do paciente
- [ ] T017 [P] [US2] Criar endpoint de envio de mensagem manual que desativa `ai_enabled` do paciente (Handoff) em `backend/src/routes/api.py`
- [ ] T018 [US2] Configurar o cliente HTTP para a API do backend Flask em `frontend/src/routes/services/api.js`
- [ ] T019 [US2] Criar a visualização e rota principal do painel CRM com a visualização Kanban em `frontend/src/routes/admin/crm/+page.svelte`
- [ ] T020 [US2] Criar a tela de chat interativo do lead com controles de handoff em `frontend/src/routes/admin/crm/[leadId]/+page.svelte`
- [ ] T021 [US2] Implementar os componentes reativos reutilizáveis `KanbanColumn.svelte`, `LeadCard.svelte` e `ChatWindow.svelte` em `frontend/src/components/`

**Ponto de Controle**: O CRM de recepção e o Handoff de IA funcionam em conjunto com o WhatsApp.

---

## Fase 5: Caso de Uso 3 - Site Institucional Premium (Prioridade: P3)

**Objetivo**: Landing page elegante, rápida e otimizada para encaminhamento de leads ao WhatsApp da clínica.

**Teste Independente**: Acessar a página raiz do SvelteKit, inspecionar a responsividade visual boutique e testar o link com chamada de ação para agendamento via WhatsApp.

### Implementação para o Caso de Uso 3

- [ ] T022 [US3] Desenvolver a página de destino (landing page) boutique com microanimações e CTA de agendamento em `frontend/src/routes/+page.svelte`
- [ ] T023 [US3] Configurar a folha de estilo e paleta de cores Tailind CSS em `frontend/tailwind.config.js`
- [ ] T024 [US3] Definir o layout global e importações de fontes sofisticadas (Outfit/Inter) em `frontend/src/routes/+layout.svelte`

---

## Fase 6: Polimento e Testes Finais

**Objetivo**: Melhorias visuais, auditoria e validações de build.

- [ ] T025 Executar o build final do frontend e testar todos os contêineres ativos via Docker Compose
- [ ] T026 Validar o guia de início rápido e criar o walkthrough.md demonstrativo das funcionalidades desenvolvidas

---

## Dependências e Ordem de Execução

### Dependências das Fases
- **Fase 1 (Configuração)**: Sem dependências - inicia imediatamente.
- **Fase 2 (Fundação)**: Depende do término da Fase 1 - BLOQUEIA todas as histórias de usuário.
- **Histórias de Usuário (Fases 3, 4 e 5)**: Todas dependem da conclusão da Fase 2.
  - Podem ser desenvolvidas em paralelo ou sequencialmente (P1 → P2 → P3).
- **Polimento (Fase 6)**: Depende da conclusão de todas as histórias de usuário desejadas.

---

## Oportunidades de Trabalho em Paralelo

- Todas as tarefas marcadas com `[P]` na Fase 1 e Fase 2 podem rodar simultaneamente.
- Assim que a Fase 2 (Fundação) for concluída, o desenvolvimento do Backend da IA (Caso de Uso 1) e o Design Visual/Site (Caso de Uso 3) podem rodar em paralelo.
