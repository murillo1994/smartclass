# Research: Modo de Simulação Contínua IoT e Identificação Visual (SmartClass)

## Context & Objectives
O usuário pontuou que, no momento presente, o hardware físico ESP32 não está conectado à bancada/sala de aula, operando exclusivamente em **Modo de Simulação**.

O objetivo é:
1. **Adequar a Interface e Comunicação**: Deixar explícito e transparente em toda a interface que o sistema está operando em **"Modo Simulação / Demonstração IoT"**, ajustando os badges de status, rótulos e cards informativos.
2. **Motor de Simulação Autônomo e Realista**: Prover um gerador de telemetria contínuo (opcional/automático) e auto-seeding inicial, permitindo que os gráficos, tabelas e relatórios PDF apresentem curvas térmicas dinâmicas e realistas sem depender de cliques manuais repetitivos.
3. **Preservação Total da Arquitetura**: Manter o fluxo real de ingestão via `POST /api/v1/medicoes` e persistência no PostgreSQL, garantindo que o acoplamento do ESP32 físico no futuro ocorra sem qualquer alteração no backend ou frontend.

---

## Research Findings & Architectural Decisions

### 1. Adequação da Identidade e Badges de Status
- **Decisão**: 
  - **Badge do Cabeçalho**: Atualizar para `Modo Simulação IoT 📡` com radar pulsante em azul/índigo (ou verde esmeralda translúcido), sinalizando que o pipeline de telemetria está ativo via simulação.
  - **Rótulos dos Cards**: Substituir "Microcontroladores ESP32 online" por "Ambientes em simulação ativa".
  - **Banner de Guia**: Adicionar nota explicativa na aba de Guia IoT informando que as medições atuais são geradas pelo simulador de telemetria enquanto o microcontrolador físico está em fase de bancada.

---

### 2. Motor de Simulação Contínua (Continuous Simulation Engine)
- **Decisão**: 
  - Adicionar um controlador no frontend `js/simulation.js` com:
    - **Auto-geração periódica**: Envio assíncrono de medições a cada intervalo (com variação térmica natural com inércia, simulando a ocupação da sala: 21°C a 26°C com umidade entre 45% e 65%).
    - **Controle Rápido**: Interruptor no cabeçalho ou menu de ações: `Simulador Automático: Ativo/Pausado`.
    - **Carga Inicial Inteligente (Auto-seed)**: Ao carregar o dashboard pela primeira vez, se houver poucos registros, gerar um lote histórico inicial de medições para que os gráficos e tabelas fiquem ricos e prontos para demonstração imediata.

---

### 3. Preservação da Paridade com o ESP32 Real
- **Decisão**: 
  - O simulador envia exatamente o mesmo payload JSON (`sala_id`, `temperatura`, `umidade`) para `POST /api/v1/medicoes` que o firmware C++/Arduino do ESP32 transmite.
  - Quando o ESP32 real for ligado na rede Wi-Fi, o simulador pode ser pausado com 1 clique, sem necessidade de refatorar nenhuma rota ou tabela de banco.
