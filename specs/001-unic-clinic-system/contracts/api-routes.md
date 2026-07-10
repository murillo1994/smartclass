# API Routes Contract: CRM Backend & Frontend Integration

This contract details the endpoints exposed by the Python Flask backend for the SvelteKit admin panel.

## Base URL
`/api`

---

## 1. Leads Management

### GET `/leads`
Retrieve all patients/leads grouped or filtered for the CRM Kanban board.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "João Silva",
    "phone": "5511999999999",
    "kanban_stage": "novo_lead",
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
Update a lead's profile details or Kanban stage, or toggle the AI handoff.

**Request Body:**
```json
{
  "name": "João Silva",
  "kanban_stage": "qualificado",
  "ai_enabled": false
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "lead": {
    "id": 1,
    "name": "João Silva",
    "phone": "5511999999999",
    "kanban_stage": "qualificado",
    "ai_enabled": false,
    "updated_at": "2026-07-10T12:10:00Z"
  }
}
```

---

## 2. Chat & Message History

### GET `/leads/<id>/messages`
Fetch complete conversation transcript for a specific lead.

**Response (200 OK):**
```json
[
  {
    "id": 101,
    "sender": "patient",
    "content": "Olá, gostaria de saber os preços de botox.",
    "created_at": "2026-07-10T12:05:00Z"
  },
  {
    "id": 102,
    "sender": "ai",
    "content": "Olá! O procedimento de Toxina Botulínica (Botox) na Unic Clinic custa R$ 1.200,00...",
    "created_at": "2026-07-10T12:05:05Z"
  }
]
```

### POST `/leads/<id>/messages`
Send a manual message from a receptionist. Toggles `ai_enabled` to false (handoff) and sends via Evolution API.

**Request Body:**
```json
{
  "content": "Olá, sou a recepcionista Maria. Vi que você tem interesse no Botox. Posso te ajudar?"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": {
    "id": 103,
    "sender": "agent",
    "content": "Olá, sou a recepcionista Maria...",
    "created_at": "2026-07-10T12:15:00Z"
  }
}
```

---

## 3. Appointments & Schedule Grid

### GET `/appointments`
Fetch all appointments for calendar display. Optional query params: `start_date`, `end_date`.

**Response (200 OK):**
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
    "status": "confirmed"
  }
]
```

### POST `/appointments`
Manually create an appointment from the receptionist panel.

**Request Body:**
```json
{
  "patient_id": 1,
  "procedure_id": 2,
  "start_time": "2026-07-11T14:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "appointment": {
    "id": 51,
    "patient_id": 1,
    "procedure_id": 2,
    "start_time": "2026-07-11T14:00:00Z",
    "end_time": "2026-07-11T14:30:00Z",
    "status": "confirmed"
  }
}
```
