# Tasks: Modo de Simulação IoT e Motor de Telemetria Autônomo

**Input**: Design documents from `specs/004-classroom-dashboard/`  
**Prerequisites**: [plan.md](file:///c:/Users/muril/unic_clinic/specs/004-classroom-dashboard/plan.md), [research.md](file:///c:/Users/muril/unic_clinic/specs/004-classroom-dashboard/research.md), [spec.md](file:///c:/Users/muril/unic_clinic/specs/004-classroom-dashboard/spec.md)

---

## Phase 1: Motor de Simulação Contínua (`frontend/js/simulation.js`)

- [X] T001 Implement `frontend/js/simulation.js` with realistic thermal variation algorithms, auto-streamer interval, and historical auto-seeding
- [X] T002 Update header connection badge to `Simulação IoT Ativa 📡` with indigo/emerald radar pulse in `frontend/dashboard.html`
- [X] T003 Update KPI card subtext to `Ambientes em simulação ativa` and add explanatory callout in Guide tab in `frontend/dashboard.html`
- [X] T004 Add simulation toggle control and quick burst generator button in header in `frontend/dashboard.html`
- [X] T005 Wire simulation engine into `SmartClassDashboard` lifecycle, handling auto-stream toggle and instant visual updates in `frontend/js/app.js`
- [X] T006 Verify continuous simulation streaming, chart curve evolution, history table refresh, and PDF export with simulated telemetry
