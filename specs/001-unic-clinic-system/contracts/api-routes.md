# Contratos de API REST & SSE — Evolution CRM SaaS Multi-Tenant

**Base URL**: /api/v1  
**Autenticação Padrão**: Bearer JWT (Authorization: Bearer <token>)

---

## 1. Módulo de Autenticação & Sessão

### POST /auth/login
Autentica SuperAdmin, Admin ou Atendente.
- **Request Body**:
  `json
  {
    "email": "admin@empresa.com",
    "password": "senha_segura"
  }
  `
- **Response (200 OK)**:
  `json
  {
    "token": "jwt_token_com_tenant_e_role",
    "user": {
      "id": "uuid",
      "name": "Carlos Silva",
      "email": "admin@empresa.com",
      "role": "admin",
      "tenant": {
        "id": "tenant_uuid",
        "name": "Clínica Alpha",
        "slug": "clinica-alpha",
        "status": "active",
        "plan": "pro"
      }
    }
  }
  `

---

## 2. Camada de Tempo Real (Server-Sent Events — SSE)

### GET /crm/events/stream?token=<jwt_token>
Canal de streaming unidirecional em tempo real para o frontend SvelteKit receber atualizações sem F5.
- **Content-Type**: 	ext/event-stream
- **Eventos Disparados pelo Backend**:
  `	ext
  event: message.created
  data: {"conversation_id": "uuid", "message": {"id": "uuid", "sender_type": "contact", "content": "Olá!", "media_url": null, "created_at": "2026-08-30T10:00:00Z"}}

  event: conversation.updated
  data: {"conversation_id": "uuid", "unread_count": 1, "last_message_at": "2026-08-30T10:00:00Z", "status": "open"}

  event: card.moved
  data: {"contact_id": "uuid", "from_stage_id": "uuid", "to_stage_id": "uuid", "order_position": 1}

  event: typing.status
  data: {"conversation_id": "uuid", "is_typing": true}
  `

---

## 3. Webhook Seguro da Evolution API

### POST /webhooks/evolution
Recepção de eventos da Evolution API protegida por segredo criptográfico.
- **Headers Exigidos**:
  - X-Webhook-Secret: <segredo_da_instancia_ou_global> (ou Authorization: Bearer <segredo>)
- **Validação no Flask**: Se o segredo enviado não bater com a chave configurada no backend, retorna imediatamente HTTP 401.
- **Payload**: Formato padrão Evolution API v2 (messages.upsert, connection.update, etc.).
- **Processamento de Mídia**: A Evolution envia no payload a URL direta do objeto salvo no S3/R2.

---

## 4. Módulo Super Admin (Painel Mestre / Suporte)
*Acesso restrito*: ole === 'superadmin'

### GET /superadmin/tenants
Lista todos os Workspaces com status, contagem de atendentes e instâncias ativas.

### POST /superadmin/tenants
Cria nova empresa cliente com provisionamento do Workspace e usuário admin titular.

### PATCH /superadmin/tenants/{id}/status
Bloqueia ou suspende um cliente inadimplente (status: "suspended").

---

## 5. Módulo Admin da Empresa (Multi-Número & Equipe)
*Acesso*: dmin ou superadmin

### GET /tenant/whatsapp/instances
Lista todas as conexões de WhatsApp cadastradas no Workspace (ex: "Vendas", "Suporte").

### POST /tenant/whatsapp/instances
Cria uma nova conexão WhatsApp na Evolution API e devolve o QR Code para pareamento.
- **Request Body**:
  `json
  {
    "name": "Equipe de Vendas"
  }
  `
- **Response (201 Created)**:
  `json
  {
    "id": "uuid",
    "name": "Equipe de Vendas",
    "instance_name": "tenant_123_inst_1",
    "status": "connecting",
    "qrcode": "data:image/png;base64,iVBORw0KGgo..."
  }
  `

### GET /tenant/users & POST /tenant/users
Listagem e convite de novos atendentes da equipe com validação do limite (max_users).

---

## 6. Módulo Inbox & Multi-Atendimento
*Acesso*: dmin ou ttendant

### GET /crm/inbox/conversations
Filtra conversas do Workspace:
- Query Params: ?tab=mine|unassigned|all|resolved&instance_id=uuid&search=termo

### GET /crm/inbox/conversations/{id}/messages
Histórico de mensagens e anotações internas da conversa.

### POST /crm/inbox/conversations/{id}/messages
Envia mensagem de texto ou mídia para o WhatsApp do cliente através da instância correta (instance_id).

### POST /crm/inbox/conversations/{id}/notes
Insere uma **anotação interna privada** (destacada em amarelo para a equipe).

### PATCH /crm/inbox/conversations/{id}/assign
Transfere a conversa para outro atendente.

---

## 7. Módulo Kanban (Funil de Vendas)

### GET /crm/kanban/funnels
Retorna colunas e cards de contatos do funil da empresa.

### PATCH /crm/kanban/cards/{contact_id}/move
Move contato entre colunas com atualização imediata no banco e disparo via SSE para a equipe.
