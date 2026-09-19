# Modelo de Dados Multi-Tenant (PostgreSQL) — Evolution CRM SaaS

**Versão**: 2.1.0  
**Arquitetura**: Shared Database, Isolated Tenant Context com Soft Deletes e Vínculo por Instância WhatsApp

---

## 1. Diagrama de Relacionamento Entidade (ERD Textual)

`
[Tenants (Workspaces)] ───1:N───> [Users] (Soft Delete: deleted_at)
         │
         ├───1:N───> [WhatsApp Instances] (Múltiplos números por Workspace)
         │                   │
         │                   └───1:N───┐
         │                             │
         ├───1:N───> [Funnels] ───1:N───> [Funnel Stages (Kanban)] (Soft Delete: deleted_at)
         │                                       │
         │                                       └───1:N (SET NULL)──┐
         │                                                           │
         ├───1:N───> [Contacts] (Soft Delete: deleted_at) <──────────┤
         │                │                                          │
         │                ├───1:N───> [Conversations] <──────────────┘
         │                │           (Instance ID + Soft Delete)
         │                │                │
         │                │                ├───1:N───> [Messages] (Soft Delete)
         │                │                └───1:N───> [Internal Notes]
         │                │
         │                └───N:M───> [Tags] (via ContactTags)
         │
         ├───1:N───> [Quick Replies] (Respostas Rápidas)
         └───1:N───> [Chatbot Rules] (Triagem & Boas-Vindas)
`

---

## 2. Dicionário de Dados e Entidades

### 2.1. 	enants (Workspaces / Empresas Clientes)
| Campo | Tipo | Nulo? | Descrição |
| :--- | :--- | :--- | :--- |
| id | UUID (PK) | Não | Identificador único global do Workspace |
| 
ame | VARCHAR(255) | Não | Razão Social ou Nome Fantasia da empresa |
| slug | VARCHAR(100) | Não | Slug único para identificação (ex: clinica-alpha) |
| document | VARCHAR(20) | Sim | CNPJ ou CPF do titular |
| status | ENUM | Não | ctive, suspended, 	rial, cancelled (Default: 	rial) |
| max_users | INT | Não | Limite contratado de atendentes (Default: 3) |
| max_instances | INT | Não | Limite contratado de números WhatsApp (Default: 1) |
| plan_name | VARCHAR(50) | Não | starter, pro, enterprise |
| 	rial_ends_at | TIMESTAMP WITH TIME ZONE | Sim | Data de expiração do período de testes |
| created_at | TIMESTAMP WITH TIME ZONE | Não | Data de criação |
| updated_at | TIMESTAMP WITH TIME ZONE | Não | Data de atualização |

---

### 2.2. users (Usuários e Atendentes)
| Campo | Tipo | Nulo? | Descrição |
| :--- | :--- | :--- | :--- |
| id | UUID (PK) | Não | ID único do usuário |
| 	enant_id | UUID (FK) | Sim | Vínculo com 	enants.id (NULL exclusivo para superadmin, ON DELETE CASCADE) |
| 
ame | VARCHAR(255) | Não | Nome completo do usuário |
| email | VARCHAR(255) | Não | E-mail único para login no sistema |
| password_hash | VARCHAR(255) | Não | Hash da senha (bcrypt/argon2) |
| ole | ENUM | Não | superadmin, dmin, ttendant |
| vatar_url | TEXT | Sim | Foto de perfil do atendente |
| ctive | BOOLEAN | Não | Ativo ou inativado pela empresa (Default: true) |
| deleted_at | TIMESTAMP WITH TIME ZONE | Sim | **Soft Delete**: Data da exclusão lógica |
| created_at | TIMESTAMP WITH TIME ZONE | Não | Data de cadastro |
| updated_at | TIMESTAMP WITH TIME ZONE | Não | Data de atualização |

*Regra de Integridade*: UNIQUE(email) global. Soft delete garante que mensagens enviadas pelo atendente continuem no histórico.

---

### 2.3. whatsapp_instances (Conexões Evolution API — Multi-Número)
| Campo | Tipo | Nulo? | Descrição |
| :--- | :--- | :--- | :--- |
| id | UUID (PK) | Não | ID da conexão |
| 	enant_id | UUID (FK) | Não | Vínculo com 	enants.id (ON DELETE CASCADE) |
| 
ame | VARCHAR(100) | Não | Nome amigável do canal (ex: "Vendas Matriz", "Suporte SAC") |
| instance_name | VARCHAR(100) | Não | Nome único no cluster Evolution (ex: 	enant_{uuid}_inst_{num}) |
| phone_number | VARCHAR(50) | Sim | Número do WhatsApp conectado |
| status | ENUM | Não | disconnected, connecting, connected |
| qrcode_base64 | TEXT | Sim | QR Code temporário para pareamento |
| webhook_secret| VARCHAR(100) | Não | Token de autenticação exigido no webhook de entrada |
| created_at | TIMESTAMP WITH TIME ZONE | Não | Data de criação |
| updated_at | TIMESTAMP WITH TIME ZONE | Não | Data de atualização |

---

### 2.4. contacts (Contatos / Leads do WhatsApp)
| Campo | Tipo | Nulo? | Descrição |
| :--- | :--- | :--- | :--- |
| id | UUID (PK) | Não | ID do contato |
| 	enant_id | UUID (FK) | Não | Vínculo com a empresa (ON DELETE CASCADE) |
| emote_jid | VARCHAR(100) | Não | Identificador WhatsApp (ex: 5511999999999@s.whatsapp.net) |
| phone | VARCHAR(50) | Não | Apenas dígitos do número de telefone |
| 
ame | VARCHAR(255) | Sim | Nome registrado ou obtido do perfil do WhatsApp |
| profile_pic_url | TEXT | Sim | Foto de perfil do contato sincronizada |
| current_stage_id| UUID (FK) | Sim | Vínculo com a etapa do Kanban (**ON DELETE SET NULL**) |
| ssigned_user_id| UUID (FK) | Sim | Atendente responsável (**ON DELETE SET NULL**) |
| custom_fields | JSONB | Sim | Dados extras flexíveis (CPF, cidade, observações) |
| deleted_at | TIMESTAMP WITH TIME ZONE | Sim | **Soft Delete**: Preserva o histórico caso o contato seja arquivado |
| created_at | TIMESTAMP WITH TIME ZONE | Não | Data do primeiro contato |
| updated_at | TIMESTAMP WITH TIME ZONE | Não | Data da última interação |

*Índice Composto*: UNIQUE(tenant_id, remote_jid) WHERE deleted_at IS NULL.

---

### 2.5. unnels & unnel_stages (Quadro Kanban Customizável)
- **unnels**:
  - id (UUID, PK)
  - 	enant_id (UUID, FK ➔ 	enants.id, ON DELETE CASCADE)
  - 
ame (VARCHAR(100)) — Ex: "Vendas", "Pós-Venda"
  - is_default (BOOLEAN)
  - deleted_at (TIMESTAMP WITH TIME ZONE, NULL)
- **unnel_stages**:
  - id (UUID, PK)
  - 	enant_id (UUID, FK ➔ 	enants.id, ON DELETE CASCADE)
  - unnel_id (UUID, FK ➔ unnels.id, ON DELETE CASCADE)
  - 
ame (VARCHAR(100)) — Ex: "Lead Novo", "Qualificação", "Proposta", "Fechado"
  - color (VARCHAR(20)) — Hexadecimal da coluna (ex: #9e8877)
  - order_position (INT) — Ordem visual das colunas no Kanban
  - deleted_at (TIMESTAMP WITH TIME ZONE, NULL) — **Soft Delete**: impede que a exclusão da coluna apague contatos nela presentes.

---

### 2.6. conversations (Sessões de Atendimento no Inbox)
| Campo | Tipo | Nulo? | Descrição |
| :--- | :--- | :--- | :--- |
| id | UUID (PK) | Não | ID da conversa |
| 	enant_id | UUID (FK) | Não | Isolamento do Workspace (ON DELETE CASCADE) |
| instance_id | UUID (FK) | Não | **Vínculo com a Instância/Número do WhatsApp** (ON DELETE RESTRICT) |
| contact_id | UUID (FK) | Não | Vínculo com contacts.id (ON DELETE RESTRICT) |
| ssigned_user_id| UUID (FK) | Sim | Atendente atribuído (**ON DELETE SET NULL**) |
| status | ENUM | Não | unassigned, open, pending, esolved |
| last_message_at | TIMESTAMP WITH TIME ZONE | Não | Timestamp para ordenação no Inbox |
| unread_count | INT | Não | Contador de mensagens não lidas pelo operador |
| deleted_at | TIMESTAMP WITH TIME ZONE | Sim | **Soft Delete**: Arquivamento sem perda física |

*Índice Composto de Performance*: CREATE INDEX idx_conv_tenant_inbox ON conversations(tenant_id, instance_id, status, last_message_at DESC) WHERE deleted_at IS NULL;

---

### 2.7. messages (Histórico de Mensagens WhatsApp)
| Campo | Tipo | Nulo? | Descrição |
| :--- | :--- | :--- | :--- |
| id | UUID (PK) | Não | ID único da mensagem |
| 	enant_id | UUID (FK) | Não | Vínculo com 	enants.id (ON DELETE CASCADE) |
| conversation_id | UUID (FK) | Não | Vínculo com conversations.id (ON DELETE CASCADE) |
| emote_msg_id | VARCHAR(150) | Sim | ID original da mensagem na Evolution/Baileys |
| sender_type | ENUM | Não | contact (cliente), ttendant (operador), ot (automação/IA) |
| user_id | UUID (FK) | Sim | Atendente que enviou manualmente (**ON DELETE SET NULL**) |
| content | TEXT | Sim | Conteúdo em texto ou legenda da mídia |
| media_type | ENUM | Não | 	ext, udio, image, ideo, document |
| media_url | TEXT | Sim | **URL no Bucket S3/Cloudflare R2** (armazenamento externo) |
| status | ENUM | Não | pending, sent, delivered, ead, ailed |
| deleted_at | TIMESTAMP WITH TIME ZONE | Sim | **Soft Delete** |
| created_at | TIMESTAMP WITH TIME ZONE | Não | Data e hora exata da mensagem |

---

### 2.8. internal_notes (Anotações Internas da Equipe)
| Campo | Tipo | Nulo? | Descrição |
| :--- | :--- | :--- | :--- |
| id | UUID (PK) | Não | ID da anotação |
| 	enant_id | UUID (FK) | Não | Vínculo do tenant (ON DELETE CASCADE) |
| conversation_id | UUID (FK) | Não | Conversa em que a nota foi inserida (ON DELETE CASCADE) |
| user_id | UUID (FK) | Sim | Atendente que redigiu a nota (**ON DELETE SET NULL**) |
| content | TEXT | Não | Conteúdo privado da equipe (destaque amarelo) |
| created_at | TIMESTAMP WITH TIME ZONE | Não | Data e hora |

---

### 2.9. quick_replies (Respostas Rápidas / Snippets)
| Campo | Tipo | Nulo? | Descrição |
| :--- | :--- | :--- | :--- |
| id | UUID (PK) | Não | ID da resposta rápida |
| 	enant_id | UUID (FK) | Não | Vínculo com 	enants.id (ON DELETE CASCADE) |
| shortcut | VARCHAR(50) | Não | Gatilho de teclado (ex: /pix, /horarios, /ola) |
| 	itle | VARCHAR(100) | Não | Título descritivo para busca no autocomplete |
| message | TEXT | Não | Mensagem com variáveis suportadas (ex: "Olá {{nome}}...") |
| media_url | TEXT | Sim | URL de imagem ou PDF anexado automaticamente no envio |
