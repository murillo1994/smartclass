# Feature Specification: Unic Clinic System Overview

**Feature Branch**: `001-unic-clinic-system`  
**Created**: 2026-07-10  
**Status**: Draft  
**Input**: User description: "# 0. Visão Geral e Arquitetura (System Overview) ..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Autonomous WhatsApp Patient Capture & Scheduling (Priority: P1)

The system autonomously interacts with leads on WhatsApp, answers questions about clinic procedures, qualifies the patient's interests, checks the schedule grid, and inserts real bookings into the database.

**Why this priority**: It is the core value proposition of the system (digital concierge) which frees the human reception team from repetitive booking flows and converts visitors into scheduled patients.

**Independent Test**: Can be tested end-to-end by simulating incoming WhatsApp webhook messages for a mock patient, checking that the AI generates correct responses, checks availability, and creates an appointment in the database.

**Acceptance Scenarios**:

1. **Given** a new lead messages the clinic WhatsApp asking about a specific procedure (e.g., botox), **When** the message is processed, **Then** the digital concierge responds with context-aware information reflecting the clinic's premium aesthetic.
2. **Given** a patient asks to book an appointment for a specific day and time, **When** the digital concierge calls the check-availability tool and finds it free, **Then** it registers the appointment in the database and sends a WhatsApp confirmation.
3. **Given** a patient requests a time slot that is already booked, **When** the digital concierge checks availability, **Then** it politely informs the patient and suggests alternative slots.

---

### User Story 2 - Receptionist Dashboard & Kanban CRM (Priority: P2)

The receptionist uses a SvelteKit-based admin dashboard featuring a Kanban board to track leads through the sales pipeline, view chat histories, and manually intervene (toggle handoff) when necessary.

**Why this priority**: Required for receptionists to supervise the AI, manage lead progression, and handle exceptions where human intervention is needed.

**Independent Test**: Can be tested by loading the dashboard, dragging a lead card to another column, opening a chat view, and toggling the "Handoff" button.

**Acceptance Scenarios**:

1. **Given** a new lead initiates a conversation on WhatsApp, **When** the lead is registered, **Then** they appear in the first column ("Novo Lead") of the Kanban board in real time.
2. **Given** a lead requires personal attention, **When** the receptionist clicks "Handoff" in the chat view, **Then** the AI is paused for that lead, and all incoming/outgoing messages are flagged as human-managed.
3. **Given** the receptionist sends a message via the dashboard chat window, **When** submitted, **Then** the message is sent to the lead via the Evolution API WhatsApp instance.

---

### User Story 3 - Premium Institutional Website (Priority: P3)

A high-performance landing page representing the Unic Clinic boutique aesthetic, designed to capture visitor attention and direct them to start a conversation on WhatsApp.

**Why this priority**: The entry point for online traffic (paid ads), essential for converting visitors into leads.

**Independent Test**: Can be tested by loading the landing page and verifying its look-and-feel, performance, and the WhatsApp redirect.

**Acceptance Scenarios**:

1. **Given** a user opens the landing page URL, **When** the page loads, **Then** it displays high-quality styling, custom typography, and smooth micro-animations.
2. **Given** a user clicks the "Agendar Consulta" call-to-action button, **When** clicked, **Then** it redirects them to WhatsApp with a pre-configured welcoming message.

---

### Edge Cases

- **OpenAI API Downtime/Timeout**: If the OpenAI API fails, the backend must return a friendly default fallback message (e.g., "Desculpe, estou com uma instabilidade. Um de nossos atendentes irá falar com você em breve.") and flag the lead in the CRM for manual intervention.
- **Double Booking**: If two patients try to book the same slot at the same time, database transaction isolation or constraints must prevent double booking, showing the error gracefully to the second flow.
- **Media/Audio Messages**: If a patient sends an audio message or image, the system should either notify the receptionist for manual triage or attempt to transcribe it (if Whisper is enabled) or politely ask for text.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST process incoming WhatsApp webhooks from the Evolution API `unic_clinic` instance.
- **FR-002**: System MUST integrate with OpenAI API using Function Calling to allow the AI to read/write schedule slots and lead details.
- **FR-003**: System MUST expose a scheduling grid checking real-time availability in PostgreSQL.
- **FR-004**: System MUST provide a SvelteKit-based admin CRM panel with Kanban column stages for leads.
- **FR-005**: System MUST support a "Handoff" mechanism to pause the IA agent when a receptionist takes manual control.
- **FR-006**: System MUST persist all patient info, message history, procedures, and calendar schedules in PostgreSQL.
- **FR-007**: System MUST render a premium, minimalist institutional website optimized for fast loading and boutique branding.

### Key Entities *(include if feature involves data)*

- **Patient (Lead)**: Represents the client. Fields: ID, Name, Phone Number, Stage (New, Qualified, Scheduled, Lost), AI Status (Active/Paused).
- **Message**: Represents a chat message. Fields: ID, Patient ID, Sender (Patient, AI, Agent), Text Content, Timestamp.
- **Procedure**: Represents services offered. Fields: ID, Name, Description, Duration, Price.
- **Appointment**: Represents a booked slot. Fields: ID, Patient ID, Procedure ID, Start Time, End Time, Status (Scheduled, Completed, Canceled).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Patients can complete booking flows autonomously on WhatsApp in under 3 minutes.
- **SC-002**: SvelteKit dashboard updates in real-time when webhooks receive messages or leads change stages.
- **SC-003**: Website loads in under 1.5 seconds on standard mobile networks.
- **SC-004**: The system processes incoming WhatsApp webhooks and triggers AI response in under 3 seconds.

## Assumptions

- We have full access to a working Evolution API instance running on the same VPS or reachable locally.
- The PostgreSQL database will be run as a Docker container `unic_db` and will be persistent.
- OpenAI API credentials (API Key) are available and valid.
