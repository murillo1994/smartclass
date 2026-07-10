# Research & Technical Decisions: Unic Clinic System

This document outlines the technical research, decision-making process, and architectural rationale for the Unic Clinic system.

## 1. Evolution API Integration (WhatsApp Service)

### Decision
Integrate with Evolution API via HTTP webhooks for receiving incoming WhatsApp messages, and use its HTTP API for sending outgoing messages.

### Rationale
Evolution API is an enterprise-grade, high-performance API that abstracts the underlying WhatsApp Web/Cloud protocols. It is running on the same VPS, allowing local, low-latency API communication.

### Webhook Event Details
- We will listen specifically to `MESSAGES_UPSERT` webhook events.
- Incoming payload structure contains message sender details (`remoteJid`), message type (e.g., text, audio, image), and text content.
- Response payload for sending message: `POST /message/sendText/{instanceName}` with headers `apikey` and JSON body `{"number": "...", "text": "..."}`.

### Alternatives Considered
- *Official WhatsApp Cloud API*: Rejected due to high startup friction, pricing per conversation, and strict template requirements for outbound messaging, which restricts natural conversational flows.

---

## 2. LLM Orchestration & Database Function Calling

### Decision
Use Python Flask backend with the official `openai` Python SDK. The agent is run with GPT-4o (or GPT-4o-mini for cost-efficiency) using the **Assistant API** or standard **Chat Completions with Function Calling (Tools)** in a loop.
We will define tools:
1. `check_available_slots(date: str)`: Returns list of free time slots for a given date.
2. `book_appointment(patient_name: str, phone: str, procedure_id: int, start_time: str)`: Books the slot in the database.
3. `get_procedures()`: Lists available procedures with prices and durations.

### Rationale
Function Calling allows the model to act as a database controller in a structured, safe manner. The LLM generates the JSON arguments, and our Python backend executes the database queries, preventing direct SQL injection by the LLM.

---

## 3. Database Schema (PostgreSQL)

### Decision
Create a relational PostgreSQL database with tables for:
- `patients` (leads): tracks contact info and active stage in Kanban.
- `messages`: tracks full chat history for CRM visibility and LLM context.
- `procedures`: pre-seeded clinic services.
- `appointments`: schedules associated with a patient and procedure.

### Rationale
PostgreSQL ensures ACID transactional consistency, which is vital for preventing double-booking of appointment slots.

---

## 4. Frontend Framework (SvelteKit + Tailwind CSS)

### Decision
Implement SvelteKit for both the public-facing landing page and the CRM admin dashboard. 

### Rationale
- **Performance**: SvelteKit supports static site generation (SSG) and server-side rendering (SSR), enabling lightning-fast loads for public marketing pages.
- **Reactivity**: SvelteKit provides clean state management and simple transitions, making the Kanban CRM interface highly responsive.
- **Tailwind CSS**: Ideal for building the premium boutique clinic UI with minimal styling overhead.
