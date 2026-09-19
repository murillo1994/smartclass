# Pesquisa Técnica e Arquitetura Avançada: CRM WhatsApp SaaS Multi-Tenant

**Data**: 30-08-2026  
**Autor**: Arquiteto de Software & Full-Stack Sênior  
**Versão**: 2.1.0 (Refinada com Proteções de Produção: Soft Delete, SSE Real-Time, Storage S3/R2, Multi-Número e Segurança de Webhook)

---

## 1. Estratégia de Exclusão de Dados: Soft Deletes vs. ON DELETE CASCADE

### O Risco do CASCADE Cego:
Em ambientes de CRM e suporte, histórico de atendimento é patrimônio comercial e jurídico. Se a exclusão de um atendente ou de uma coluna do funil disparar ON DELETE CASCADE:
- Conversas ativas e históricas seriam deletadas permanentemente.
- Métricas de desempenho passadas seriam corrompidas.
- O cliente perderia dados de leads quentes, gerando cancelamento imediato (*churn*).

### Decisão Arquitetural:
- **Soft Deletes (Exclusão Lógica)** para todas as entidades operacionais: users, contacts, unnel_stages, conversations e messages.
  - Implementação via coluna deleted_at TIMESTAMP WITH TIME ZONE NULL.
  - Registros com deleted_at IS NOT NULL são omitidos das consultas operacionais através de filtros padrão no ORM/SQLAlchemy.
  - Permite restauração em caso de exclusão acidental por parte do cliente ("Lixeira do CRM").
- **ON DELETE CASCADE Restrito**:
  - Reservado **exclusivamente** para o nível raiz de 	enants(id). Se o Super Admin deliberadamente deletar e purgar a empresa cliente do sistema, todos os seus dados serão expurgados conforme a LGPD/GDPR.
- **ON DELETE SET NULL / RESTRICT**:
  - ssigned_user_id em conversations: se o atendente for inativado, a conversa vai para ssigned_user_id = NULL (não atribuída), mantendo todo o histórico intacto.
  - current_stage_id em contacts: se uma coluna for excluída logicamente, os leads são migrados para a primeira coluna padrão ou ficam em stage_id = NULL.

---

## 2. Camada de Tempo Real (Real-Time): SSE vs. WebSockets vs. Pusher

### Comparativo Técnico:

| Critério | Server-Sent Events (SSE) | Flask-SocketIO (WebSockets) | Pusher / Ably (Gerenciado) |
| :--- | :--- | :--- | :--- |
| **Complexidade no Flask** | 🟢 **Baixíssima** (endpoint nativo de streaming 	ext/event-stream) | 🔴 **Alta** (exige eventlet/gevent, conflita com workers sync do Gunicorn) | 🟡 **Baixa** (SDK HTTP), mas cria dependência externa paga |
| **Consumo de Recursos** | 🟢 **Levíssimo** (conexão HTTP padrão mantida aberta, nativa em HTTP/2) | 🟡 Médio/Alto por socket bidirecional | 🟢 Externo |
| **Suporte no Navegador** | 🟢 **Nativo** (EventSource API no SvelteKit sem libs pesadas) | 🟡 Exige biblioteca client-side socket.io | 🟡 Exige SDK proprietário |
| **Direção dos Dados** | 🟢 Unidirecional (Servidor ➔ Cliente): exatamente o que precisamos para novas mensagens, status e digitação | 🟡 Bidirecional (overkill, pois envios já são feitos via REST POST) | 🟢 Unidirecional |
| **Custo de Infraestrutura**| 🟢 **Zero custo adicional** (roda no próprio servidor) | 🟢 Roda no próprio servidor | 🔴 Custo por conexões simultâneas e volume de msgs |

### Decisão Arquitetural:
**Server-Sent Events (SSE) com Redis Pub/Sub**:
- O SvelteKit abre uma conexão persistente única para /api/v1/crm/events/stream?token=<jwt>.
- O backend Flask escuta o canal Redis 	enant:{tenant_id}.
- Quando a Evolution API bate no Webhook do Flask com uma nova mensagem, o Flask publica o evento no Redis (message.created, conversation.updated, stage.changed).
- A thread SSE entrega o evento JSON imediatamente ao navegador do atendente em **menos de 50 milissegundos**.
- Sem necessidade de F5, sem recarregar a tela, com reconexão automática nativa do navegador.

---

## 3. Gestão de Mídias (Áudios, Imagens e Documentos): S3 / Cloudflare R2

### O Risco do Armazenamento Local ou Base64:
- Mensagens de voz (PTT), fotos de comprovantes e documentos em PDF pesam em média 500 KB a 5 MB cada.
- Se salvos em base64 no PostgreSQL: o banco incha centenas de gigabytes em meses, estourando custos de backup e travando consultas.
- Se salvos no disco local da VPS: inviabiliza balanceamento de carga, migração de servidor e Docker efêmero.

### Decisão Arquitetural:
**Offloading Nativo da Evolution API v2 para Object Storage (S3 / Cloudflare R2 / MinIO)**:
- A Evolution API v2 possui suporte nativo a S3/R2 (S3_ENABLED=true, S3_BUCKET, S3_ACCESS_KEY, S3_ENDPOINT).
- Fluxo de Entrada:
  1. O cliente envia uma mensagem de áudio ou foto no WhatsApp.
  2. A Evolution API processa o arquivo, faz o upload direto para o bucket S3/R2 e gera a URL pública ou assinada.
  3. No payload do Webhook para o Flask, a Evolution envia apenas o campo data.message.audioMessage.url ou mediaUrl.
  4. O PostgreSQL armazena apenas a string da URL (media_url TEXT) e o tipo MIME (media_type).
- O banco de dados armazena apenas metadados ultraleves, garantindo escalabilidade infinita com custo baixíssimo (Cloudflare R2 tem custo zero de transferência de dados/egress).

---

## 4. Multi-Instâncias por Tenant (Future-Proofing Multi-Número)

### O Problema do Vínculo Direto Tenant ── Conversa:
Clientes maiores do CRM frequentemente utilizam:
- Número 1: Equipe de Vendas (WhatsApp Comercial)
- Número 2: Equipe de Suporte / SAC
- Número 3: Cobrança / Financeiro

Se a conversa não sabe por qual número o cliente chamou, atendentes de suporte responderão conversas de vendas e vice-versa.

### Decisão Arquitetural:
**Modelo whatsapp_instances ──1:N──> conversations**:
- A tabela whatsapp_instances pertence a um 	enant_id e possui:
  - id (UUID, PK)
  - 	enant_id (UUID, FK)
  - 
ame (VARCHAR) — Ex: "Vendas Matriz", "SAC Suporte"
  - phone_number (VARCHAR)
  - instance_name (VARCHAR) — Identificador único na Evolution API
- A tabela conversations possui obrigatoriamente:
  - instance_id (UUID, FK ➔ whatsapp_instances.id)
  - 	enant_id (UUID, FK ➔ 	enants.id para conferência rápida de isolamento)
- A Caixa de Entrada no SvelteKit ganha um filtro por número de WhatsApp:
  - *"Exibindo conversas de: [Todos os Números ▼] ou [Vendas Matriz (5511...)]"*
- O envio de mensagens pelo atendente direciona a requisição da Evolution API especificamente para a instância instance.instance_name vinculada àquela conversa.

---

## 5. Segurança Rigorosa do Webhook

### O Risco de Endpoints Abertos:
A rota /api/v1/webhooks/evolution fica exposta à internet para receber os disparos da Evolution API. Sem proteção:
- Invasores poderiam forjar mensagens falsas e injetar contatos fictícios no CRM.
- Ataques de DoS poderiam sobrecarregar o processamento do backend.

### Decisão Arquitetural:
**Autenticação Dupla por Header de Assinatura (X-Webhook-Secret ou Bearer Token)**:
- Na configuração do webhook na Evolution API, registra-se um segredo seguro (UUID v4 ou hash SHA-256) em webhook_secret.
- O decorator @require_webhook_token no Flask:
  1. Inspeciona o header X-Webhook-Secret (ou Authorization: Bearer <token>).
  2. Valida se o token confere com o EVOLUTION_WEBHOOK_SECRET global ou com o segredo registrado da instância correspondente.
  3. Se inválido ou ausente: rejeita imediatamente com HTTP 401 Unauthorized e bloqueia a execução.
