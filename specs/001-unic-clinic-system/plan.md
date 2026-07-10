# Implementation Plan: Unic Clinic System Overview

**Branch**: `001-unic-clinic-system` | **Date**: 2026-07-10 | **Spec**: [spec.md](file:///c:/Users/muril/unic_clinic/specs/001-unic-clinic-system/spec.md)
**Input**: Feature specification from `/specs/001-unic-clinic-system/spec.md`

## Summary

The Unic Clinic system is a custom lead capture, scheduling, and CRM platform. The system uses a SvelteKit frontend for the premium client landing page and receptionist CRM panel, and a Python Flask backend to handle logic, database storage (PostgreSQL), and generative AI booking actions on WhatsApp (via Evolution API & OpenAI Function Calling).

## Technical Context

**Language/Version**: Python 3.11, Node.js 18+ (SvelteKit)  
**Primary Dependencies**: Flask, SQLAlchemy, openai, requests, SvelteKit, tailwindcss  
**Storage**: PostgreSQL  
**Testing**: pytest (backend), Vitest + Playwright (frontend)  
**Target Platform**: Linux Docker / VPS  
**Project Type**: web-service + web-app  
**Performance Goals**: Frontend landing page load < 1.5s, webhook turnaround < 3.0s  
**Constraints**: Zero-downtime webhook receiver, ACID scheduling transactions to prevent slot double-booking  
**Scale/Scope**: Boutique high-end clinic traffic scale (thousands of leads monthly, concurrent booking requests)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

No architectural gate violations detected. The structure uses standard, decoupled backend/frontend service containers in line with typical web applications.

## Project Structure

### Documentation (this feature)

```text
specs/001-unic-clinic-system/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── webhook-schema.json
│   └── api-routes.md
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   │   ├── openai_service.py
│   │   └── evolution_service.py
│   ├── routes/
│   │   ├── webhook.py
│   │   └── api.py
│   ├── app.py
│   ├── database.py
│   └── config.py
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   │   ├── KanbanColumn.svelte
│   │   ├── LeadCard.svelte
│   │   ├── ChatWindow.svelte
│   │   └── Header.svelte
│   ├── routes/
│   │   ├── +layout.svelte
│   │   ├── +page.svelte (Landing Page)
│   │   ├── admin/
│   │   │   ├── +layout.svelte
│   │   │   └── crm/
│   │   │       ├── +page.svelte (Kanban Dashboard)
│   │   │       └── [leadId]/
│   │   │           └── +page.svelte (Chat & Lead Detail)
│   │   └── services/
│   │       └── api.js
├── tailwind.config.js
├── svelte.config.js
├── Dockerfile
└── package.json

docker-compose.yml
```

**Structure Decision**: Option 2: Web application (decoupled backend & frontend directories orchestrated via root `docker-compose.yml`).

## Complexity Tracking

*No constitution violations or complex architectural overrides required.*

---

## Verification Plan

We will verify both components (backend & frontend) using automated test pipelines and manual inspection of flows.

### Automated Tests
- **Backend Unit Tests**: Run `pytest tests/unit` to test LLM tool calling parsing, webhook routing logic, and database operations.
- **Backend Integration Tests**: Run `pytest tests/integration` with a test database container to check appointment transaction isolation (double booking checks).
- **Frontend Unit Tests**: Run `npm run test:unit` inside `frontend/` to verify component rendering and state updates.

### Manual Verification
1. Spin up docker container stack using `docker-compose up`.
2. Access SvelteKit landing page, verify boutique aesthetic and smooth scrolling.
3. Access CRM dashboard admin panels, check Kanban visual hierarchy and layout responsiveness.
4. Send mock WhatsApp webhook payloads to backend, verify correct database inserts and AI message response generation.
