# Implementation Plan: CRM & Concierge da Unic Clinic

**Branch**: `001-unic-clinic-system` | **Date**: 10-07-2026 | **Spec**: [spec.md](file:///C:/Users/muril/unic_clinic/specs/001-unic-clinic-system/spec.md)
**Input**: Feature specification from `/specs/001-unic-clinic-system/spec.md`

## Summary

O sistema é uma plataforma completa e exclusiva de captação, atendimento e gestão de clientes para a **Unic Clinic**, consistindo em:
1. **Landing Page Premium:** Um site institucional minimalista com estética boutique para atrair e direcionar tráfego qualificado para o WhatsApp.
2. **Concierge Digital (IA):** Integração com a API da OpenAI (GPT-4o/GPT-3.5) usando *Function Calling* para tirar dúvidas, qualificar leads e realizar agendamentos diretamente no banco.
3. **Painel CRM Kanban & Chat:** Interface de recepção humana baseada em SvelteKit para supervisão, com controle de *handoff* e chat em tempo real.
4. **Infraestrutura Docker:** Banco de dados PostgreSQL com enums nativos, backend Flask exposto na porta 5010 e frontend SvelteKit na porta 5173.

## Technical Context

**Language/Version**: Python 3.10 (Backend) / Node.js 20+ (Frontend)  
**Primary Dependencies**: Flask, SQLAlchemy, OpenAI SDK, SvelteKit, TailwindCSS  
**Storage**: PostgreSQL 15 (Docker container `unic_db`)  
**Testing**: Pytest (Backend) / Vitest & Playwright (Frontend)  
**Target Platform**: VPS Linux (Docker Compose Stack behind Nginx Proxy Manager)  
**Project Type**: Web Application (Frontend SvelteKit + Backend Flask + PostgreSQL)  
**Performance Goals**: Processamento de webhooks do WhatsApp em < 3 segundos; Carregamento do site em < 1.5s.  
**Constraints**: Sem overbooking; Conformidade estrita com a LGPD; Handoff imediato ao solicitar humano.  
**Scale/Scope**: Inquilino único (Single-Tenant), projetado para atender leads e consultas de alta performance da clínica.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Princípio I (Identidade):** O Concierge usará linguagem requintada, frases curtas, sem gírias e no máximo 1 emoji por mensagem. ✅ *Passa*
- **Princípio II (Hard Boundaries):** Proibido diagnósticos remotos, prescrições de dosagem de toxina ou concessão de descontos e pacotes customizados. ✅ *Passa*
- **Princípio III (Mídias):** Resposta automática padrão para recusa de imagens e direcionamento a consulta presencial. ✅ *Passa*
- **Princípio IV (Objeções):** Contorno elegante para preço ("insumos premium e excelência") e dor ("técnicas de conforto avançadas"). ✅ *Passa*
- **Princípio V (Handoff):** Desativação automática da IA (`ai_enabled = false`) em reclamações, pedidos expressos de humanos ou perguntas sobre contraindicações de medicamentos. ✅ *Passa*

## Project Structure

```text
backend/
├── src/
│   ├── models/           # database.py (Modelos SQLAlchemy e Enums)
│   ├── services/         # openai_service.py (Integração LLM e Functions)
│   └── routes/           # api.py, webhook.py (Endpoints da stack e WhatsApp)
└── tests/

frontend/
├── src/
│   ├── components/       # Header.svelte e componentes comuns
│   └── routes/           # Rotas do SvelteKit (+page.svelte e admin/crm)
└── static/               # Imagens e logotipos reais da clínica
```

**Structure Decision**: Web application layout com separação clara de responsabilidades (Backend Flask em `backend/` e Frontend SvelteKit em `frontend/`).

## Complexity Tracking

*Sem violações ativas na constituição.*

## Proposed Changes

### Backend

#### [MODIFY] [database.py](file:///c:/Users/muril/unic_clinic/backend/src/database.py)
- Modelos contendo tipos Enums nativos do PostgreSQL (`enum_fase_funil`, `enum_origem_msg`, `enum_status_agenda`, `enum_tipo_midia`).

#### [MODIFY] [api.py](file:///c:/Users/muril/unic_clinic/backend/src/routes/api.py)
- Sincronização dos endpoints REST com as novas definições de enums em português.

#### [MODIFY] [webhook.py](file:///c:/Users/muril/unic_clinic/backend/src/routes/webhook.py)
- Tratamento de mensagens complexas e regras de handoff com transbordo imediato.

#### [MODIFY] [openai_service.py](file:///c:/Users/muril/unic_clinic/backend/src/services/openai_service.py)
- Injeção das diretrizes de persona e function calling de agendamento.

### Frontend

#### [MODIFY] [+page.svelte](file:///c:/Users/muril/unic_clinic/frontend/src/routes/+page.svelte)
- Novo design premium baseado na referência `clinicaromana.com.br` integrado com as imagens reais da pasta `FOTOS` e logos da pasta `LOGO`.

#### [MODIFY] [Header.svelte](file:///c:/Users/muril/unic_clinic/frontend/src/components/Header.svelte)
- Renderização condicional do logotipo institucional com transparência no topo.

#### [MODIFY] [+page.svelte (CRM)](file:///c:/Users/muril/unic_clinic/frontend/src/routes/admin/crm/+page.svelte)
- Layout Kanban expandido para as 6 fases em português.

#### [MODIFY] [+page.svelte (Chat)](file:///c:/Users/muril/unic_clinic/frontend/src/routes/admin/crm/[leadId]/+page.svelte)
- Atualização do painel lateral de prontuário, sincronizando as opções de etapa de leads e status de consultas com os novos enums de banco.

## Verification Plan

### Automated Tests
- Execução de testes de integração e unitários no backend:
  ```bash
  docker compose exec unic_backend pytest
  ```

### Manual Verification
- Verificação visual da Landing Page no navegador: `http://187.77.63.90:5173/`
- Verificação funcional das transições Kanban e Handoff no CRM: `http://187.77.63.90:5173/admin/crm`
