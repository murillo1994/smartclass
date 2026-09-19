# Tasks: CRM de WhatsApp SaaS Multi-Tenant (Estilo Evolution CRM)

## Phase 1: Setup (Dependências e Configuração de Ambiente)
- [x] T001 Instalar dependências de autenticação e criptografia (PyJWT, crypt) no ambiente Python
- [x] T002 Atualizar ackend/src/config.py com suporte a JWT_SECRET_KEY, EVOLUTION_WEBHOOK_SECRET e configurações multi-tenant

## Phase 2: Foundational (Modelagem Multi-Tenant, Soft Deletes e Segurança)
- [x] T003 Implementar novos modelos ORM em ackend/src/database.py (Tenant, User, WhatsAppInstance, Contact, Funnel, FunnelStage, Conversation, Message, InternalNote, Tag, QuickReply) com soft deletes (deleted_at) e vínculo por instance_id
- [x] T004 Implementar middleware de autenticação JWT e RBAC em ackend/src/middleware/auth.py
- [x] T005 Implementar middleware de isolamento de tenant em ackend/src/middleware/tenant.py
- [x] T006 Implementar validação de assinatura de webhook em ackend/src/middleware/webhook_auth.py
- [x] T007 Criar script de semeação ackend/seed_saas.py com SuperAdmin, 2 empresas clientes com múltiplos números e conversas de teste

## Phase 3: [US1] Autenticação e Painel Mestre Super Admin
- [x] T008 [US1] Implementar endpoints de login e perfil em ackend/src/routes/auth.py
- [x] T009 [US1] Implementar endpoints de gestão de empresas e limites em ackend/src/routes/superadmin.py
- [x] T010 [US1] Atualizar tela de login rontend/src/routes/admin/login/+page.svelte para rotear conforme o papel (superadmin, dmin, ttendant)
- [x] T011 [US1] Criar visualização do Super Admin em rontend/src/routes/admin/superadmin/+page.svelte para gerenciar empresas e status de assinaturas

## Phase 4: [US2] Gateway Evolution API Multi-Instância e Webhook Protegido
- [x] T012 [US2] Implementar serviço ackend/src/services/evolution_service.py para criar instâncias, gerar QR Codes e enviar mensagens
- [x] T013 [US2] Implementar endpoints de gerenciamento de instâncias WhatsApp em ackend/src/routes/tenant_admin.py
- [x] T014 [US2] Implementar webhook seguro em ackend/src/routes/webhook.py com roteamento automático por instance_name e ingestão de mídias S3/R2

## Phase 5: [US3] Camada de Tempo Real (Server-Sent Events — SSE)
- [x] T015 [US3] Implementar despachante de eventos ackend/src/services/event_dispatcher.py
- [x] T016 [US3] Implementar endpoint de streaming SSE em ackend/src/routes/sse.py
- [x] T017 [US3] Criar cliente de tempo real rontend/src/routes/services/sse.js com auto-reconexão

## Phase 6: [US4] Caixa de Entrada Compartilhada (Multi-Atendimento e Notas Internas)
- [x] T018 [US4] Implementar endpoints de conversas, mensagens e notas internas em ackend/src/routes/inbox.py
- [x] T019 [US4] Implementar endpoints de respostas rápidas em ackend/src/routes/quick_replies.py
- [x] T020 [US4] Criar tela do Inbox Compartilhado em rontend/src/routes/admin/inbox/+page.svelte com abas, notas internas amarelas e atalho /

## Phase 7: [US5] Funil de Vendas (Kanban) e Gestão de Contatos
- [x] T021 [US5] Implementar endpoints de funil e movimentação de cards em ackend/src/routes/kanban.py
- [x] T022 [US5] Implementar endpoints de contatos e tags em ackend/src/routes/contacts.py
- [x] T023 [US5] Atualizar tela do Kanban em rontend/src/routes/admin/crm/+page.svelte com colunas customizáveis e sincronização via SSE

## Phase 8: Polimento e Validação E2E
- [x] T024 Integrar navegação lateral e barra superior adaptativa por papel em rontend/src/components/Header.svelte
- [x] T025 Executar testes ponta a ponta do fluxo multi-tenant (SuperAdmin ➔ Admin ➔ Atendente ➔ WhatsApp)
