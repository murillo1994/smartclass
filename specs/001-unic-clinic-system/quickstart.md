# Guia de Inicialização Rápida (Quickstart) — Evolution CRM SaaS

Este guia orienta como executar o ambiente localmente e testar o fluxo completo de multi-inquilino (Multi-Tenant).

---

## 1. Pré-requisitos
- **Python**: 3.10+ (com Flask, SQLAlchemy, psycopg2, pyjwt, bcrypt)
- **Node.js**: 18+ (com npm e SvelteKit)
- **PostgreSQL**: Rodando localmente ou via Docker
- **Evolution API v2**: Executando na porta 8080 ou 8081

---

## 2. Variáveis de Ambiente (.env)
`env
# Banco de Dados Multi-Tenant
DATABASE_URL=postgresql://unic_admin:unic_secure_pass@localhost:5433/unic_clinic_db

# Chave Criptográfica JWT
JWT_SECRET_KEY=sua_chave_mestra_ultra_secreta_jwt_2026
JWT_ACCESS_TOKEN_EXPIRES=86400

# Evolution API
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=admin123

# Servidor Flask
PORT=5010
FLASK_ENV=development

# Frontend SvelteKit
PUBLIC_API_URL=http://localhost:5010/api/v1
`

---

## 3. Inicialização e Migrações

### 3.1. Criar e Semear o Banco com Dados Iniciais SaaS
`ash
# Executa a criação das tabelas e o seed do SuperAdmin e de 2 Empresas de Teste
python backend/seed_saas.py
`
Isso criará:
1. **Super Admin**: super@crm.com / dmin123
2. **Empresa A**: dmin@clinicaalpha.com / dmin123 (2 atendentes + funil padrão)
3. **Empresa B**: dmin@clinicabeta.com / dmin123 (1 atendente + funil padrão)

---

## 4. Executando os Serviços

### Terminal 1 — Backend (Flask)
`ash
cd backend
python -m src.app
`
*API rodando em*: http://localhost:5010

### Terminal 2 — Frontend (SvelteKit)
`ash
cd frontend
npm run dev
`
*Interface rodando em*: http://localhost:5173

---

## 5. Roteiro de Teste do Isolamento Multi-Tenant

1. **Acesse** http://localhost:5173/admin/login.
2. **Faça login como SuperAdmin** (super@crm.com):
   - Visualize a lista de todas as empresas cadastradas (Clínica Alpha, Clínica Beta).
   - Teste suspender e reativar uma empresa.
3. **Abra uma janela anônima e faça login na Empresa A** (dmin@clinicaalpha.com):
   - Verifique que **apenas** os contatos e conversas da Clínica Alpha são exibidos.
   - Conecte o WhatsApp via QR Code da instância 	enant_alpha.
4. **Abra outra janela e faça login na Empresa B** (dmin@clinicabeta.com):
   - Confirme o isolamento rigoroso: nenhuma mensagem, tag ou lead da Empresa A aparece aqui.
5. **Faça login como Atendente da Empresa A**:
   - Responda mensagens em tempo real no Inbox compartilhado.
   - Mova cards de leads no quadro Kanban.
   - Adicione anotações internas amarelas.
