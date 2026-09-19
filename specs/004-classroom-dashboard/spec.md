# Feature Specification: Dashboard Web de Monitoramento das Salas de Aula (Módulo 2)

**Feature Branch**: `004-classroom-dashboard`  
**Created**: 2026-09-13  
**Status**: Draft  
**Input**: User description: "Dashboard Web de Monitoramento das Salas de Aula (Módulo 2) - Interface web moderna, estática e desacoplada para visualização em tempo real e análise histórica das medições de temperatura e umidade das salas escolares."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Monitoramento em Tempo Real com Cards de Ambientes (Priority: P1) 🎯 MVP

Como gestor escolar ou professor em sala,
Quero acessar uma página web limpa e responsiva que exiba cards com a temperatura atual, umidade e índice de conforto térmico de cada sala monitorada,
Para avaliar imediatamente se o ambiente de aula está dentro dos parâmetros ideais de conforto e produtividade dos alunos.

**Why this priority**: É o valor central para o usuário final. Permite saber o estado climático de todas as salas sem depender de comandos técnicos ou consultas ao banco de dados.

**Independent Test**: Abrir o dashboard no navegador, verificar a renderização dos cards para as salas com telemetria (ex: "Sala 101", "Lab 02"), checar se a temperatura e a umidade refletem os últimos dados persistidos e se a badge de status de conforto térmico (ex: "Ideal 🟢", "Atenção: Quente 🔴", "Atenção: Frio 🔵") é calculada corretamente.

**Acceptance Scenarios**:

1. **Given** que existem medições recentes na API,
   **When** o usuário abre a página do dashboard,
   **Then** o sistema deve carregar os dados via requisição assíncrona e apresentar um card para cada sala com a temperatura mais recente, umidade (se disponível), horário da última atualização e tag de conforto.

2. **Given** uma sala com temperatura entre 20°C e 24°C,
   **When** o card é renderizado,
   **Then** o indicador visual deve exibir status "Confortável / Ideal" com destaque visual positivo (verde).

3. **Given** uma sala com temperatura superior a 24.5°C ou inferior a 19.5°C,
   **When** o card é renderizado,
   **Then** o indicador deve alertar visualmente sobre ambiente quente (vermelho/laranja) ou frio (azul).

---

### User Story 2 - Gráfico Interativo de Tendência Temporal (Priority: P2)

Como coordenador de infraestrutura escolar,
Quero visualizar a evolução térmica das salas ao longo do tempo em gráficos de linha dinâmicos,
Para identificar picos de calor durante o período letivo e otimizar o acionamento de climatizadores e ventiladores.

**Why this priority**: Oferece percepção visual rápida da dinâmica de aquecimento e resfriamento da sala de aula ao longo das horas.

**Independent Test**: Observar a seção de gráficos do dashboard e verificar a plotagem de curvas de temperatura e umidade com pontos cronológicos ordenados no tempo.

**Acceptance Scenarios**:

1. **Given** múltiplas leituras temporais de uma sala,
   **When** o gráfico é renderizado,
   **Then** a linha do tempo deve exibir no eixo horizontal os horários das medições e no eixo vertical os valores de temperatura (°C) e umidade (%).

2. **Given** a seleção de uma sala específica no seletor do dashboard,
   **When** o usuário troca de sala,
   **Then** o gráfico deve atualizar seus dados e curvas instantaneamente sem recarregar a página inteira.

---

### User Story 3 - Histórico Analítico em Tabela e Atualização Automática (Priority: P3)

Como mantenedor do sistema IoT,
Quero visualizar a tabela com o histórico cronológico de todas as telemetrias e poder ativar/desativar atualização automática (polling),
Para acompanhar as leituras à medida que chegam do ESP32 sem precisar pressionar F5 manualmente.

**Why this priority**: Facilita a auditoria de leituras do hardware, inspeção de falhas e monitoramento contínuo em painéis ou TVs de monitoramento da escola.

**Independent Test**: Ativar o botão de "Auto-refresh" (ex: a cada 10s), disparar uma nova medição simulada na API e confirmar que a tabela e os cards atualizam seus valores automaticamente.

**Acceptance Scenarios**:

1. **Given** o dashboard aberto na tela,
   **When** o auto-refresh está habilitado,
   **Then** o frontend deve buscar periodicamente as novas medições no endpoint `/api/v1/medicoes/recent` via `Fetch API` e atualizar os componentes na tela sem piscar ou rolar a página.

2. **Given** a tabela de histórico de leituras,
   **When** o usuário digita no campo de busca ou filtra por sala,
   **Then** as linhas da tabela devem ser filtradas em tempo real exibindo ID, Sala, Temperatura, Umidade e Data/Hora formatada.

---

### Edge Cases

- **Falha de Conexão com o Backend**: Se a API estiver inacessível ou o backend estiver desligado, o frontend deve exibir um banner discreto de advertência ("Servidor de telemetria indisponível. Tentando reconectar...") sem quebrar a interface com telas em branco.
- **Nenhuma Leitura Cadastrada (Estado Vazio)**: Se o banco estiver vazio, o dashboard deve exibir mensagem amigável convidando ao envio da primeira leitura IoT.
- **Hardware sem Sensor de Umidade**: Quando a umidade for `null`, o card e a tabela devem exibir um traço indicativo (`—` ou `N/A`) sem quebrar cálculos ou gráficos.
- **Visualização Mobile**: A interface deve se adaptar fluidamente a telas pequenas (smartphones de professores) e grandes (telas da diretoria).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O frontend DEVE ser implementado como uma aplicação web estática (HTML5, JavaScript moderno e Tailwind CSS).
- **FR-002**: O frontend DEVE ser 100% desacoplado do backend, comunicando-se exclusivamente através da API REST pública via `Fetch API` assíncrona.
- **FR-003**: O dashboard DEVE consumir o endpoint `GET /api/v1/medicoes/recent` (ou endpoints específicos de agregação) para obter as leituras.
- **FR-004**: O dashboard DEVE apresentar cards de resumo por sala de aula destacando: nome da sala, temperatura atual, umidade atual, status de conforto e horário da última leitura.
- **FR-005**: O dashboard DEVE calcular o status de conforto térmico com base em faixas parametrizadas (ex: Confortável: 20°C a 24°C; Atenção Calor: >24°C; Atenção Frio: <20°C).
- **FR-006**: O dashboard DEVE conter gráficos interativos de linha (usando Chart.js via CDN) demonstrando a variação temporal de temperatura e umidade.
- **FR-007**: O dashboard DEVE conter tabela cronológica das últimas medições com identificador, sala, temperatura, umidade e data formatada no padrão brasileiro (`DD/MM/AAAA HH:mm:ss`).
- **FR-008**: O dashboard DEVE disponibilizar botão manual de "Atualizar Dados" e alternador de "Auto-refresh" periódico configurável (ex: a cada 5s ou 10s).
- **FR-009**: A construção visual e estilização DEVE ser resolvida integralmente com classes utilitárias do Tailwind CSS, sem CSS global customizado arbitrário.
- **FR-010**: O frontend DEVE tratar falhas de rede de forma resiliente, notificando o usuário sem travar a interface.

### Key Entities

- **ResumoSala**:
  - `sala_id`: Nome identificador do ambiente escolar.
  - `ultima_temperatura`: Valor numérico da última leitura (°C).
  - `ultima_umidade`: Valor numérico da última umidade relativa (%), ou null.
  - `data_ultima_leitura`: Timestamp formatado da última captura.
  - `status_conforto`: Categoria semântica ("ideal", "quente", "frio").
  - `total_leituras`: Quantidade de leituras registradas para aquela sala.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O dashboard é carregado e renderiza o primeiro lote de dados em menos de 1 segundo em conexões locais padrão.
- **SC-002**: A alternância de filtros por sala ou atualização via auto-refresh reflete novos dados na tela em menos de 200ms após o retorno da API.
- **SC-003**: 100% das páginas e componentes são responsivos, adaptando-se sem quebra de layout de telas de 360px (mobile) até 1920px+ (desktop/TV).
- **SC-004**: Zero dependência de renderização no servidor (SSR) ou dependência de banco de dados no frontend.

## Assumptions

- A API Flask está rodando na mesma máquina ou rede (`http://localhost:5000`) com headers CORS devidamente habilitados para permitir requisições assíncronas do frontend.
- O navegador do usuário suporta JavaScript ES6+ e Fetch API nativa.
- Bibliotecas visuais utilitárias (Tailwind CSS e Chart.js) são carregadas de forma leve via CDN confiável para prototipagem rápida e visualização instantânea.
