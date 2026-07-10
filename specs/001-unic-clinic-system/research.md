# Pesquisas e Decisões Técnicas: Sistema Unic Clinic

Este documento descreve as pesquisas técnicas, o processo de tomada de decisão e a lógica arquitetural do ecossistema da Unic Clinic.

## 1. Integração com Evolution API (Serviço de WhatsApp)

### Decisão
Integrar com a Evolution API através de webhooks HTTP para receber mensagens recebidas no WhatsApp e utilizar sua API HTTP para enviar mensagens de resposta.

### Lógica
A Evolution API é uma API de alto desempenho que abstrai os protocolos internos do WhatsApp Web/Cloud. Ela é executada na mesma VPS, permitindo uma comunicação local e de baixíssima latência entre ela e o backend Flask.

### Detalhes do Evento do Webhook
- Escutaremos especificamente os eventos do tipo `MESSAGES_UPSERT`.
- O payload de entrada contém detalhes do remetente (`remoteJid`), tipo da mensagem (ex: texto, áudio, imagem) e o conteúdo de texto.
- Endpoint de envio: `POST /message/sendText/{instanceName}` com os headers `apikey` e corpo JSON contendo `{"number": "...", "text": "..."}`.

### Alternativas Consideradas
- *API Oficial do WhatsApp Cloud*: Rejeitada devido à alta fricção de configuração inicial, cobrança por sessão de conversa e necessidade estrita de modelos de templates pré-aprovados para mensagens ativas, o que inviabilizaria a conversa fluida com a IA.

---

## 2. Orquestração de LLM e Function Calling

### Decisão
Utilizar o backend Flask em Python com o SDK oficial da OpenAI (`openai`). O agente executará com o modelo GPT-4o (ou GPT-4o-mini para economia de custos) usando chamadas de funções (**Chat Completions com Function Calling**) em um loop de conversação.
Definiremos as seguintes funções para a IA:
1. `check_available_slots(date: str)`: Retorna os horários livres na grade de agendamentos para uma determinada data.
2. `book_appointment(patient_name: str, phone: str, procedure_id: int, start_time: str)`: Efetua a reserva do horário no banco de dados.
3. `get_procedures()`: Retorna a lista de procedimentos disponíveis na clínica com preços e durações.

### Lógica
O Function Calling permite que a LLM aja como um controlador de dados estruturado e seguro. O modelo gera os argumentos JSON, e o backend em Python executa as consultas no banco de dados. Isso previne injeção direta de SQL e permite validação rigorosa dos parâmetros pelo backend.

---

## 3. Modelo de Banco de Dados (PostgreSQL)

### Decisão
Criar um banco de dados relacional PostgreSQL com tabelas dedicadas para:
- `patients` (leads): rastreia contatos e a etapa ativa no Kanban.
- `messages`: armazena o histórico do chat para visualização no CRM e envio de contexto para a IA.
- `procedures`: lista de procedimentos estéticos oferecidos pela clínica.
- `appointments`: agendamentos com associação a paciente e procedimento.

### Lógica
O PostgreSQL garante consistência transacional ACID, o que é fundamental para evitar a reserva dupla (concorrência no mesmo horário de agendamento).

---

## 4. Framework Frontend (SvelteKit + Tailwind CSS)

### Decisão
Implementar SvelteKit tanto para a landing page institucional pública quanto para o painel CRM administrativo da clínica.

### Lógica
- **Desempenho**: SvelteKit suporta geração de páginas estáticas (SSG) e renderização no servidor (SSR), o que garante carregamentos instantâneos cruciais para campanhas de tráfego pago.
- **Reatividade**: Gerenciamento de estado direto e transições nativas eficientes do Svelte, ideais para o comportamento dinâmico do Kanban do CRM.
- **Tailwind CSS**: Agiliza a criação de uma interface premium e minimalista de clínica-boutique.
