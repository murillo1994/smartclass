# 📘 Guia Prático de Instalação e Utilização — SmartClass

Este guia foi elaborado especialmente para que **colegas de curso, professores e avaliadores** consigam clonar, instalar e rodar o projeto **SmartClass** em seus computadores de forma simples, rápida e sem complicação técnica.

> 🌐 **Dica**: Se você deseja apenas testar e utilizar o sistema sem instalar nada localmente, o SmartClass já está disponível online na VPS em:  
> **[http://187.77.63.90/smartclass/login](http://187.77.63.90/smartclass/login)** *(Usuário: `univesp` \| Senha: `p4univesp`)*

---

## 📋 Pré-requisitos Básicos

Antes de começar, verifique se você tem instalado no seu computador:
1. **Git**: Para baixar o código ([git-scm.com](https://git-scm.com/)).
2. **Python 3.10 ou superior**: ([python.org](https://www.python.org/)). *Lembre-se de marcar a opção "Add Python to PATH" durante a instalação no Windows.*
3. **PostgreSQL** (instalado localmente) **OU Docker Desktop** (para subir o banco com 1 comando).

---

## 🛠️ Passo a Passo de Instalação (Método Padrão)

### Passo 1: Clonar o Repositório
Abra o seu terminal (Prompt de Comando, PowerShell ou Terminal do Linux/macOS) e execute:

```bash
git clone https://github.com/murillo1994/smartclass.git
cd smartclass
```

---

### Passo 2: Criar e Ativar o Ambiente Virtual (Virtualenv)
O ambiente virtual isola as bibliotecas do projeto para não misturar com outros programas do seu computador.

**No Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(Se o PowerShell der erro de permissão de script, execute: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e tente ativar novamente).*

**No Linux ou macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Passo 3: Instalar as Dependências do Backend
Com o ambiente virtual ativado (você verá `(venv)` no início da linha do terminal):

```bash
pip install -r backend/requirements.txt
```

---

### Passo 4: Configurar as Variáveis de Ambiente (`.env`)

Copie o arquivo de exemplo `.env.example` criando o seu arquivo local `.env`:

**No Windows PowerShell:**
```powershell
Copy-Item .env.example .env
```

**No Linux/macOS:**
```bash
cp .env.example .env
```

Abra o arquivo `.env` em um editor de texto (como VS Code ou Bloco de Notas) e configure suas preferências:
- Defina a senha do seu PostgreSQL (`POSTGRES_PASSWORD`).
- Defina o usuário e senha que **você** deseja usar para fazer login no painel (`SMARTCLASS_USER` e `SMARTCLASS_PASS`).

---

### Passo 5: Iniciar o Servidor Flask

Execute o comando principal:
```bash
python backend/src/app.py
```

Você verá uma mensagem informando que o servidor está rodando:
```text
 * Running on http://127.0.0.1:5000
 * Servidor SmartClass iniciado com sucesso!
```

---

### Passo 6: Acessar a Aplicação

1. Abra o navegador e acesse: **[http://localhost:5000](http://localhost:5000)**
2. Você será direcionado para a tela de login.
3. Digite o usuário e a senha que você configurou no seu `.env` (ou os valores padrão).
4. Pronto! Você está dentro do **SmartClass Dashboard**.

---

## 📡 Como Testar Sem ter o ESP32 Físico (Modo de Simulação IoT)

Não tem um microcontrolador ESP32 ou sensores de temperatura com você? **Sem problemas!**

O SmartClass possui um **Motor de Simulação Autônomo** integrado no próprio frontend:
1. Ao acessar o painel, o sistema detecta se o banco possui poucos registros e **popula dados históricos automaticamente**.
2. No cabeçalho, você verá o badge **`Simulação IoT Ativa 📡`**.
3. O sistema gera variações térmicas e de umidade contínuas e realistas para as salas cadastradas (*Sala 101, Sala 102, Lab 01, Lab 02, Auditório, Biblioteca*).
4. Você pode clicar no botão **`+ Leitura`** no cabeçalho a qualquer momento para disparar uma nova medição pontual e ver os gráficos se atualizarem em tempo real.
5. Se quiser pausar a geração, basta clicar no botão **`Simulador Ativo`** para alternar para **`Simulador Pausado`**.

---

## 🐳 Método Alternativo: Execução Completa com Docker (1 Comando)

Se você já usa o **Docker Desktop**:

1. Na raiz do projeto, execute:
   ```bash
   docker compose up -d
   ```
2. O Docker criará automaticamente:
   - O container do banco PostgreSQL com o esquema de tabelas criado.
   - O container do backend Flask pronto para receber conexões.
3. Acesse diretamente: [http://localhost:5000](http://localhost:5000).

Para encerrar os containers:
```bash
docker compose down
```

---

## ❓ Perguntas Frequentes & Resolução de Problemas (FAQ)

### 1. O backend não conecta ao PostgreSQL (`Connection refused`)
- Verifique se o serviço do PostgreSQL está iniciado no seu computador (no Windows: abra `services.msc` e confira se `postgresql-x64-XX` está em Execução).
- Verifique se a porta e a senha no seu arquivo `.env` correspondem à senha que você definiu ao instalar o PostgreSQL.

### 2. O comando `python` não é reconhecido no terminal
- Certifique-se de que o Python está instalado e marcado na variável de ambiente PATH do sistema.

### 3. Como testar o envio de dados via terminal (cURL)?
Você pode simular o envio de um sensor a qualquer momento executando:
```bash
curl -X POST http://localhost:5000/api/v1/medicoes \
  -H "Content-Type: application/json" \
  -d "{\"sala_id\": \"Laboratorio 01\", \"temperatura\": 21.5, \"umidade\": 50.0}"
```

---

## 🤝 Dúvidas ou Sugestões?
Sinta-se à vontade para abrir uma **Issue** ou enviar um **Pull Request** no repositório do GitHub!
