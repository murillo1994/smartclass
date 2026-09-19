# Implementation Plan: Modo de Simulação IoT e Motor de Telemetria Autônomo

**Branch**: `004-classroom-dashboard` | **Date**: 2026-09-19 | **Spec**: [spec.md](file:///c:/Users/muril/unic_clinic/specs/004-classroom-dashboard/spec.md)
**Input**: User request adjusting the dashboard operation for the current demonstration stage where the physical ESP32 is not yet connected, making the system operate purely in realistic, automated simulation mode.

---

## Summary

Adequação da interface do SmartClass para operar com total clareza em **Modo de Simulação IoT**:
- **Comunicação Visual Clara**: Identificação no cabeçalho como `Simulação IoT Ativa 📡`, cards ajustados com textos de demonstração e nota explicativa na aba de Guia.
- **Motor de Simulação Autônomo (`frontend/js/simulation.js`)**: Gerador contínuo de telemetria com curvas térmicas orgânicas (inércia e variações graduais para *Sala 101, Sala 102, Lab 01, Lab 02, Auditório, Biblioteca*).
- **Auto-seed Histórico**: Geração automática de histórico recente caso o banco de dados esteja vazio ou com poucas medições, populando instantaneamente os gráficos e relatórios.
- **Controle de Simulação no Cabeçalho**: Botão para alternar a simulação contínua (*Ativa / Pausada*) e botão para disparo pontual de lote de leituras.

---

## Technical Context

**Language/Version**: JavaScript (ES6+ Modules), Python 3.11 (Flask RESTful), PostgreSQL 16  
**Primary Dependencies**: Tailwind CSS, Chart.js, Fetch API  
**Target Platform**: Web (Desktop, Tablet e Mobile)  
**Constraints**: O simulador deve consumir exclusivamente o endpoint oficial `POST /api/v1/medicoes`, garantindo paridade 100% com o firmware do ESP32 real.  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Princípio I (Fronteiras e Persistência)**: ✅ PASS — As leituras simuladas trafegam via HTTP POST padronizado e são salvas no PostgreSQL imutável com `CURRENT_TIMESTAMP`.
- **Princípio II (Estado e Reatividade)**: ✅ PASS — O motor de simulação roda no frontend desacoplado e interage apenas via API REST pública.
- **Princípio III (Qualidade e Resiliência)**: ✅ PASS — Tratamento de erros gracioso e geração de valores térmicos dentro de faixas físicas realistas (-40°C a 80°C).

---

## Project Structure

### Documentation (this feature)

```text
specs/004-classroom-dashboard/
├── plan.md              # Este plano de implementação
├── research.md          # Decisões do motor de simulação e rótulos da interface
├── data-model.md        # Entidades e modelo de telemetria
└── tasks.md             # Lista ordenada de tarefas
```

### Source Code (repository root)

```text
frontend/
├── dashboard.html       # Rótulos de 'Modo Simulação', controles de simulação contínua e notas informativas
└── js/
    ├── simulation.js    # Motor de simulação contínua com curvas térmicas e auto-seed
    ├── app.js           # Integração com o motor de simulação e atualização dos badges
    └── utils.js         # Textos de status adaptados para simulação
```

---

## Phases & Execution Plan

### Phase 1: Módulo de Simulação Contínua (`frontend/js/simulation.js`)
- Criar `simulation.js` com funções:
  - `startAutoSimulation(intervalMs)` / `stopAutoSimulation()`
  - `seedInitialDataIfEmpty()` (envio de lote com variação temporal se o banco tiver < 10 registros)
  - `generateRealisticReading(salaId)` (simula inércia térmica e variações graduais de 0.2°C a 0.5°C por ciclo)

### Phase 2: Atualização dos Textos e Badges (`frontend/dashboard.html`)
- Atualizar o badge de conexão do cabeçalho para `Simulação IoT Ativa 📡`.
- Atualizar o texto do card de ambientes para `Ambientes em simulação ativa`.
- Adicionar controle de alternância da simulação contínua no cabeçalho (*Simulação Automática: ON/OFF*).
- Atualizar a aba de Guia IoT informando que o sistema opera em simulação enquanto o hardware está em bancada.

### Phase 3: Integração no App (`frontend/js/app.js`)
- Integrar o motor de simulação no ciclo de vida do dashboard.
- Conectar o botão de alternância do simulador e exibir toasts informativos.

### Phase 4: Validação e Testes
- Testar auto-seeding em banco zerado ou com poucos dados.
- Verificar gráficos de linha atualizando continuamente de forma orgânica.
- Verificar relatórios PDF com dados simulados consistentes.
