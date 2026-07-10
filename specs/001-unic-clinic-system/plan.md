# Plano de Implementação: Visão Geral do Sistema Unic Clinic

**Branch**: `001-unic-clinic-system` | **Data**: 10-07-2026 | **Especificação**: [spec.md](file:///c:/Users/muril/unic_clinic/specs/001-unic-clinic-system/spec.md)
**Entrada**: Especificação da funcionalidade em `/specs/001-unic-clinic-system/spec.md`

## Resumo

O sistema Unic Clinic é uma plataforma personalizada de captação de leads, agendamento e CRM. O sistema utiliza um frontend em SvelteKit para a landing page institucional de alto padrão e o painel CRM dos recepcionistas, e um backend em Python Flask para gerenciar a lógica de negócios, o armazenamento no banco de dados (PostgreSQL) e as ações automatizadas de agendamento no WhatsApp (via Evolution API e OpenAI Function Calling).

## Contexto Técnico

**Linguagem/Versão**: Python 3.11, Node.js 18+ (SvelteKit)  
**Dependências Principais**: Flask, SQLAlchemy, openai, requests, SvelteKit, tailwindcss  
**Armazenamento**: PostgreSQL  
**Testes**: pytest (backend), Vitest + Playwright (frontend)  
**Plataforma Alvo**: Docker em Linux / VPS  
**Tipo de Projeto**: web-service + web-app  
**Metas de Desempenho**: Carregamento da landing page < 1.5s, tempo de resposta do webhook do WhatsApp < 3.0s  
**Restrições**: Tratamento seguro da chave da API da OpenAI, isolamento de credenciais do banco de dados  
**Escopo/Escala**: Fluxo de funil de leads para clínica boutique de alto padrão (milhares de leads mensais, requisições de agendamento concorrentes)

## Verificação da Constituição

*PORTAL: Deve passar antes da pesquisa da Fase 0. Verificar novamente após o design da Fase 1.*

Nenhuma violação de diretrizes arquiteturais foi detectada. A estrutura utiliza contêineres de serviços desacoplados padrão (backend e frontend), em linha com as práticas recomendadas para aplicações web modernas.

## Estrutura do Projeto

### Documentação (desta funcionalidade)

```text
specs/001-unic-clinic-system/
├── plan.md              # Este arquivo (plano de implementação)
├── research.md          # Saída da Fase 0 (pesquisa e decisões)
├── data-model.md        # Saída da Fase 1 (modelo de dados)
├── quickstart.md        # Saída da Fase 1 (guia de início rápido)
├── contracts/           # Saída da Fase 1 (contratos e esquemas de integração)
│   ├── webhook-schema.json
│   └── api-routes.md
└── tasks.md             # Saída da Fase 2 (lista de tarefas de execução)
```

### Código Fonte (raiz do repositório)

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
│   │   │       ├── +page.svelte (Dashboard Kanban)
│   │   │       └── [leadId]/
│   │   │           └── +page.svelte (Visualização de Chat e Lead)
│   │   └── services/
│   │       └── api.js
├── tailwind.config.js
├── svelte.config.js
├── Dockerfile
└── package.json

docker-compose.yml
```

**Decisão de Estrutura**: Opção 2: Aplicação Web (diretórios desacoplados de backend e frontend orquestrados via `docker-compose.yml` na raiz).

## Rastreamento de Complexidade

*Nenhuma violação ou ajuste complexo de arquitetura foi necessário.*

---

## Plano de Verificação

Iremos verificar ambos os componentes (backend e frontend) usando pipelines de testes automatizados e inspeção visual dos fluxos.

### Testes Automatizados
- **Testes Unitários do Backend**: Rodar `pytest tests/unit` para testar o parseamento de chamadas de funções da LLM, rotas de webhook e operações do banco.
- **Testes de Integração do Backend**: Rodar `pytest tests/integration` com um banco de dados de teste para validar o isolamento de transações de agendamento (bloqueio de reserva dupla).
- **Testes Unitários do Frontend**: Rodar `npm run test:unit` dentro de `frontend/` para verificar a renderização de componentes e atualizações de estados.

### Verificação Manual
1. Iniciar a pilha de contêineres Docker usando `docker-compose up`.
2. Acessar a landing page do SvelteKit no navegador, validando a estética boutique e transições.
3. Acessar o dashboard do CRM, arrastar os cards na coluna Kanban, alterar o handoff e verificar se o status atualiza imediatamente.
4. Disparar payloads de webhook de simulação de mensagens da Evolution API para o backend e verificar as atualizações correspondentes no PostgreSQL (tabelas `patients`, `messages`, `appointments`).
