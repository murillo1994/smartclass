# 🌡️ SmartClass - Monitoramento Inteligente de Conforto Térmico Escolar

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![ESP32](https://img.shields.io/badge/ESP32-IoT_Hardware-E7352C?style=for-the-badge&logo=espressif&logoColor=white)](https://www.espressif.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Projeto Integrador em Computação — Universidade Virtual do Estado de São Paulo (UNIVESP)**  
*Uma solução aberta de Internet das Coisas (IoT) e Inteligência de Dados para transformar a qualidade ambiental em salas de aula e espaços pedagógicos.*

<br/>

> 🌐 **Acesse a Demonstração Online em Produção:**  
> **[http://187.77.63.90/smartclass/login](http://187.77.63.90/smartclass/login)**  
> *(Usuário: `univesp` \| Senha: `p4univesp`)*

<br/>

[🚀 Guia de Instalação Rápida](./INSTALL.md) • [🔌 Kit de Hardware ESP32](./hardware/README.md) • [📜 Contrato de API](./hardware/API_CONTRACT.md) • [🕹️ Simulação Wokwi](./hardware/wokwi_project/README.md)

</div>

---

## 📖 Visão Geral e Propósito Humano

Em ambientes educacionais, a temperatura e a umidade do ar não são apenas métricas físicas — são **fatores determinantes para a capacidade de concentração, o bem-estar psicológico e a saúde de alunos e educadores**.

Estudos pedagógicos e normas de ergonomia comprovam que o estresse térmico em salas de aula:
- Reduz em até **30% a retenção de conteúdo e a velocidade de raciocínio**.
- Aumenta a fadiga, irritabilidade e sonolência de estudantes e professores.
- Eleva o risco de propagação de doenças respiratórias devido à ventilação inadequada.
- Provoca desperdício de energia por climatização desregulada.

O **SmartClass** foi concebido para fechar a lacuna entre a engenharia eletrônica e a gestão escolar, entregando uma plataforma de fácil operação que coleta, audita e apresenta dados climáticos contínuos para embasar decisões humanas e administrativas com rigor científico.

---

## 🏗️ Arquitetura do Sistema

A solução foi projetada de forma modular e resiliente, integrando nós sensores de baixo custo com microsserviços modernos:

```
  ┌──────────────────────┐          HTTP POST JSON           ┌─────────────────────────┐
  │   ESP32 + DHT22/11   │ ─────────────────────────────────▶│   Backend RESTful       │
  │   (Bancada / Sala)   │        (Wi-Fi 2.4GHz)             │   Flask / Python 3.11   │
  └──────────────────────┘                                   └────────────┬────────────┘
             │                                                            │
             │ (Ou Modo de Simulação Autônomo)                            │ SQL Ingestion
             ▼                                                            ▼
  ┌──────────────────────┐                                   ┌─────────────────────────┐
  │  Dashboard Web       │◀──────────────────────────────────│   Banco de Dados        │
  │  (SPA Vanilla + CDN) │        GET /api/v1/medicoes       │   PostgreSQL 16         │
  └──────────────────────┘                                   └─────────────────────────┘
```

### Componentes da Arquitetura:
1. **Nó de Coleta IoT (ESP32)**: Coleta temperatura e umidade a intervalos regulares, trata exceções com `millis()` e transmite via HTTP/HTTPS com `WiFiClientSecure`.
2. **Backend de Ingestão (Python / Flask)**: Valida esquemas, executa regras de negócio e classifica o conforto térmico no momento da persistência.
3. **Persistência Estruturada (PostgreSQL)**: Armazena o histórico imutável das medições com carimbo de tempo (*timestamp*) e chave de sala.
4. **Dashboard Web Interativo**: Interface Single-Page Application (SPA) com gráficos dinâmicos (*Chart.js*), modo escuro, motor de simulação integrado e exportação de relatórios (*jsPDF* e *CSV*).

---

## ✨ Funcionalidades Principais

- 📊 **Painel de Monitoramento em Tempo Real**: Indicadores de Salas Monitoradas, Temperatura Média, Umidade Média e Salas em Alerta.
- 📡 **Modo de Simulação IoT Autônomo**: Permite testar e demonstrar o sistema 100% funcional mesmo sem o hardware físico ESP32 conectado.
- 📈 **Análise Gráfica com Curvas Spline**: Gráficos temporais com faixas de referência ideais e comparativos entre múltiplos ambientes.
- 📋 **Tabela Histórica com Filtros Dinâmicos**: Busca textual instantânea e filtros rápidos por status (*Confortável*, *Alerta*, *Crítico*).
- 📄 **Exportação de Relatórios de Auditoria**: Emissão de relatórios em **PDF formatado** (com cabeçalhos institucionais e metadados) e **CSV para planilhas**.
- 🌓 **Suporte a Dark Mode**: Alternância suave entre tema Claro e Escuro com persistência em `localStorage`.
- 🔐 **Autenticação Segura de Operadores**: Controle de acesso por sessão autenticada com credenciais parametrizáveis via `.env`.

---

## 🎯 Parâmetros de Conforto Térmico Escolar

O sistema implementa faixas de conformidade inspiradas em diretrizes ergonômicas para ambientes de trabalho e aprendizado:

| Classificação | Faixa de Temperatura | Faixa de Umidade | Diagnóstico e Impacto no Ambiente |
| :--- | :--- | :--- | :--- |
| 🟢 **Confortável** | **20.0 °C a 23.0 °C** | **40% a 60%** | **Zona Ideal**: Máxima concentração, conforto respiratório e disposição física. |
| 🟡 **Alerta** | **18.0 °C a 19.9 °C**<br>**23.1 °C a 26.0 °C** | **30% a 39%**<br>**61% a 70%** | **Atenção**: Início de desconforto, sonolência leve ou ressecamento das vias aéreas. |
| 🔴 **Crítico** | **< 18.0 °C** ou **> 26.0 °C** | **< 30%** ou **> 70%** | **Inadequado**: Queda acentuada de rendimento cognitivo e risco ao bem-estar. |

---

## 🚀 Como Executar o Projeto Localmente (Guia Rápido)

> Para um passo a passo detalhado voltado para iniciantes, consulte o [📖 Guia de Instalação Completo](./INSTALL.md).

### Opção 1: Execução com Python e PostgreSQL

1. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/murillo1994/smartclass.git
   cd smartclass
   ```

2. **Criar o Ambiente Virtual e Instalar Dependências**:
   ```bash
   python -m venv venv
   # Ativação no Windows:
   .\venv\Scripts\activate
   # Ativação no Linux/macOS:
   source venv/bin/activate

   pip install -r backend/requirements.txt
   ```

3. **Configurar as Variáveis de Ambiente**:
   ```bash
   # Copie o arquivo de exemplo:
   cp .env.example .env
   # Edite o .env com suas configurações de banco e credenciais de login
   ```

4. **Executar a Aplicação**:
   ```bash
   python backend/src/app.py
   ```

5. **Acessar no Navegador**:
   - Painel: [http://localhost:5000](http://localhost:5000)

---

### Opção 2: Execução em 1 Comando com Docker Compose

```bash
docker compose up -d
```
O Docker inicializará o banco PostgreSQL e a API Flask automaticamente.

---

## 🛠️ Kit de Hardware ESP32

O repositório conta com uma pasta dedicada [`hardware/`](./hardware/README.md) com tudo pronto para quem for montar a bancada física:
- [`hardware/firmware_esp32/firmware_esp32.ino`](./hardware/firmware_esp32/firmware_esp32.ino): Código C++/Arduino pronto para gravação.
- [`hardware/WIRING_GUIDE.md`](./hardware/WIRING_GUIDE.md): Diagrama de fios, pinagem do ESP32 e resistor de pull-up.
- [`hardware/NETWORK_GUIDE.md`](./hardware/NETWORK_GUIDE.md): Guia de conexão do ESP32 com a nuvem / VPS.
- [`hardware/wokwi_project/`](./hardware/wokwi_project/README.md): Simulação virtual do ESP32 + DHT22 no navegador pelo [Wokwi](https://wokwi.com).

---

## 📁 Estrutura de Pastas do Repositório

```
smartclass/
├── backend/                  # Servidor Backend em Python / Flask
│   ├── src/
│   │   ├── models/           # Entidades e modelos de dados
│   │   ├── repositories/     # Camada de acesso ao banco PostgreSQL
│   │   ├── routes/           # Rotas RESTful (Auth, Telemetria, Health)
│   │   ├── config.py         # Carregamento seguro de variáveis de ambiente
│   │   └── app.py            # Inicializador e fábrica da aplicação Flask
│   ├── requirements.txt      # Dependências Python (Flask, psycopg2, gunicorn, etc.)
│   └── Dockerfile            # Imagem Docker do backend
├── frontend/                 # Interface Web do Dashboard (SPA)
│   ├── js/
│   │   ├── api.js            # Cliente HTTP REST
│   │   ├── app.js            # Controlador principal e ciclo de vida
│   │   ├── charts.js         # Configurações do Chart.js
│   │   ├── simulation.js     # Motor de telemetria IoT simulada
│   │   ├── pdf_export.js     # Geração de relatórios em PDF
│   │   └── auth.js           # Gerenciamento de sessão do operador
│   ├── dashboard.html        # Página principal com abas e gráficos
│   └── login.html            # Tela de autenticação institucional
├── hardware/                 # Kit de Desenvolvimento ESP32
│   ├── firmware_esp32/       # Sketch Arduino C++ completo
│   ├── WIRING_GUIDE.md       # Diagrama de ligação elétrica
│   ├── NETWORK_GUIDE.md      # Guia de conectividade e VPS
│   ├── API_CONTRACT.md       # Especificação técnica dos endpoints
│   └── wokwi_project/        # Simulação virtual no Wokwi
├── .env.example              # Modelo seguro de variáveis de ambiente
├── docker-compose.yml        # Orquestração de containers para produção/teste
├── INSTALL.md                # Guia pedagógico de instalação para estudantes
├── LICENSE                   # Licença MIT
└── README.md                 # Este documento
```

---

## 👥 Equipe do Projeto

Projeto desenvolvido como parte do **Projeto Integrador em Computação — UNIVESP**:

| Integrante | Função Principal |
| :--- | :--- |
| **Murillo Augusto** | Arquitetura de Software, Backend & Frontend Web |
| **Desenvolvimento de Hardware** | Montagem de Bancada IoT, Firmware ESP32 & Sensores |
| **Pesquisa Pedagógica e Normativa** | Levantamento de Parâmetros Térmicos e Documentação |

---

## 📄 Licença

Este projeto está licenciado sob os termos da **[Licença MIT](./LICENSE)** — permitindo livre uso, modificação e distribuição para fins acadêmicos e profissionais.
