# Quickstart: Dashboard Web de Monitoramento das Salas de Aula (Módulo 2)

Guia de inicialização rápida e teste da interface visual do SmartClass.

---

## 1. Pré-Requisitos

1. **Backend Flask em Execução**:
   Certifique-se de que o backend está ativo na porta `5000`:
   ```bash
   curl http://localhost:5000/api/v1/health
   ```
2. **Navegador Web Moderno** (Google Chrome, Firefox, Edge, Safari).

---

## 2. Acessar o Dashboard

Como o frontend é uma aplicação **100% estática e desacoplada**:

### Opção A: Abrir diretamente no navegador
Abra o arquivo [`frontend/dashboard.html`](file:///c:/Users/muril/unic_clinic/frontend/dashboard.html) no seu navegador.

### Opção B: Servir via servidor estático Python
```bash
python -m http.server 8080 --directory frontend
```
Em seguida, acesse no navegador: `http://localhost:8080/dashboard.html`

---

## 3. Fluxo de Validação Visual

1. **Conectividade**:
   - Observe o badge no topo: deve exibir `Conectado 🟢`.
2. **Cards de Salas**:
   - Devem listar as salas que já enviaram medições (`Sala 101`, `Lab 02`), com temperatura, umidade e tag de conforto térmico.
3. **Gráficos em Tempo Real**:
   - O gráfico de linha exibe a variação de temperatura e umidade ao longo do tempo.
4. **Tabela de Histórico e Filtros**:
   - Filtre por sala ou pesquise por termo no campo de busca.
5. **Auto-Refresh**:
   - Alterne o seletor para `5s` ou `10s` e dispare o script de simulação:
   ```bash
   python backend/scripts/simulate_sensor.py
   ```
   - Veja os cards, gráficos e tabela atualizando automaticamente a cada nova medição do sensor.
