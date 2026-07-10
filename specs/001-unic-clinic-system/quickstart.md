# Quickstart Guide: Unic Clinic System Setup

This guide walks you through setting up and running the Unic Clinic ecosystem locally using Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- An active OpenAI API key
- An instance running on Evolution API (e.g., `unic_clinic`)

---

## 1. Environment Configurations

Create a `.env` file in the root of the project with the following properties:

```env
# Database Settings
POSTGRES_USER=unic_admin
POSTGRES_PASSWORD=unic_secure_pass
POSTGRES_DB=unic_clinic_db
DATABASE_URL=postgresql://unic_admin:unic_secure_pass@unic_db:5432/unic_clinic_db

# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Evolution API Settings
EVOLUTION_API_URL=http://your-evolution-api-host:8080
EVOLUTION_API_KEY=your_evolution_global_key_here
EVOLUTION_INSTANCE_NAME=unic_clinic
EVOLUTION_WEBHOOK_SECRET=your_optional_secret

# Flask Settings
FLASK_ENV=development
PORT=5000

# Frontend Settings (SvelteKit)
PUBLIC_API_URL=http://localhost:5000/api
```

---

## 2. Running the Application

To start the database, backend, and frontend containers in the correct order, run:

```bash
docker-compose up --build
```

This will spin up:
1. **`unic_db`** (PostgreSQL) on port 5432 (internal only).
2. **`unic_backend`** (Flask API) on port 5000.
3. **`unic_frontend`** (SvelteKit CRM & Site) on port 5173.

---

## 3. Pre-seeding Database Procedures

Once the containers are up, database migrations will run automatically. You can seed the clinic procedures with a backend helper endpoint or database script:

```bash
# Example command to run database seed script (detailed in implementation plan)
docker-compose exec unic_backend python seed_db.py
```

---

## 4. Setting up WhatsApp Webhook in Evolution API

Point the webhook in Evolution API to your backend endpoint:
- **Webhook URL**: `http://<your-vps-ip>:5000/webhook/evolution`
- **Events**: Select `MESSAGES_UPSERT`
- **Status**: Enabled
