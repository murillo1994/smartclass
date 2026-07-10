# Contrato de Rotas de API: Integração CRM Backend & Frontend

Este contrato detalha os endpoints expostos pelo backend em Python Flask para o consumo do painel administrativo SvelteKit.

## URL Base
`/api`

---

## 1. Gestão de Leads

### GET `/leads`
Retorna todos os pacientes/leads agrupados ou filtrados para a visualização no quadro Kanban do CRM.

**Resposta (200 OK):**
```json
[
  {
    "id": 1,
    "name": "João Silva",
    "phone": "5511999999999",
    "kanban_stage": "lead_novo",
    "ai_enabled": true,
    "created_at": "2026-07-10T12:00:00Z",
    "updated_at": "2026-07-10T12:05:00Z",
    "last_message": {
      "content": "Olá, gostaria de saber os preços de botox.",
      "created_at": "2026-07-10T12:05:00Z"
    }
  }
]
```

### PATCH `/leads/<id>`
Atualiza detalhes do perfil de um lead, altera a etapa do Kanban ou ativa/desativa o handoff da IA.

**Corpo da Requisição (Request Body):**
```json
{
  "name": "João Silva",
  "kanban_stage": "qualificacao",
  "ai_enabled": false
}
```

**Resposta (200 OK):**
```json
{
  "success": true,
  "lead": {
    "id": 1,
    "name": "João Silva",
    "phone": "5511999999999",
    "kanban_stage": "qualificacao",
    "ai_enabled": false,
    "updated_at": "2026-07-10T12:10:00Z"
  }
}
```

---

## 2. Histórico de Conversas e Mensagens

### GET `/leads/<id>/messages`
Recupera o histórico completo de conversas para um determinado lead.

**Resposta (200 OK):**
```json
[
  {
    "id": 101,
    "sender": "paciente",
    "content": "Olá, gostaria de saber os preços de botox.",
    "created_at": "2026-07-10T12:05:00Z"
  },
  {
    "id": 102,
    "sender": "bot",
    "content": "Olá! O procedimento de Toxina Botulínica (Botox) na Unic Clinic custa R$ 1.200,00...",
    "created_at": "2026-07-10T12:05:05Z"
  }
```

### POST `/leads/<id>/messages`
Envia uma mensagem manual através da recepção. Altera o campo `ai_enabled` do lead para `false` (handoff) e repassa a mensagem via Evolution API.

**Corpo da Requisição (Request Body):**
```json
{
  "content": "Olá, sou a recepcionista Maria. Vi que você tem interesse no Botox. Posso ajudar?"
}
```

**Resposta (201 Created):**
```json
{
  "success": true,
  "message": {
    "id": 103,
    "sender": "recepcao",
    "content": "Olá, sou a recepcionista Maria...",
    "created_at": "2026-07-10T12:15:00Z"
  }
}
```

---

## 3. Agendamentos e Calendário

### GET `/appointments`
Recupera todos os agendamentos registrados para exibição na grade do calendário. Parâmetros de consulta opcionais: `start_date`, `end_date`.

**Resposta (200 OK):**
```json
[
  {
    "id": 50,
    "patient": {
      "id": 1,
      "name": "João Silva",
      "phone": "5511999999999"
    },
    "procedure": {
      "id": 2,
      "name": "Toxina Botulínica",
      "duration_minutes": 30
    },
    "start_time": "2026-07-11T14:00:00Z",
    "end_time": "2026-07-11T14:30:00Z",
    "status": "confirmado"
  }
]
```

### POST `/appointments`
Cria manualmente um agendamento a partir do painel de recepção.

**Corpo da Requisição (Request Body):**
```json
{
  "patient_id": 1,
  "procedure_id": 2,
  "start_time": "2026-07-11T14:00:00Z"
}
```

**Resposta (201 Created):**
```json
{
  "success": true,
  "appointment": {
    "id": 51,
    "patient_id": 1,
    "procedure_id": 2,
    "start_time": "2026-07-11T14:00:00Z",
    "end_time": "2026-07-11T14:30:00Z",
    "status": "confirmado"
  }
}
```
