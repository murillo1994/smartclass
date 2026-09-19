# 📜 Contrato de API & Especificação de Telemetria

Este documento define o contrato oficial de comunicação entre o hardware (ESP32) e o backend do **SmartClass**.

---

## 📡 Endpoint Principal de Ingestão de Telemetria

### `POST /api/v1/medicoes`

Registra uma nova leitura climática realizada pelo sensor no ambiente escolar.

- **Método**: `POST`
- **Headers**:
  - `Content-Type: application/json`
  - `Accept: application/json`

---

### 📥 Formato do Payload (JSON Enviado pelo ESP32)

```json
{
  "sala_id": "Sala 101",
  "temperatura": 22.50,
  "umidade": 58.20
}
```

#### Dicionário de Campos:

| Campo | Tipo | Obrigatório? | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `sala_id` | `String` | **Sim** | Identificador textual da sala ou laboratório monitorado. | `"Sala 101"`, `"Lab 01"`, `"Auditório"` |
| `temperatura` | `Float` | **Sim** | Temperatura lida em Graus Celsius (°C). | `22.5` |
| `umidade` | `Float` | Não | Umidade relativa do ar em percentual (%). | `58.2` |

---

### 📤 Respostas do Servidor (Códigos HTTP)

#### 1. Sucesso: `201 Created`
Retornado quando a medição foi validada, classificada e salva no banco de dados com sucesso.
```json
{
  "status": "success",
  "message": "Medição registrada com sucesso.",
  "data": {
    "id": 142,
    "sala_id": "Sala 101",
    "temperatura": 22.5,
    "umidade": 58.2,
    "data_registro": "2026-09-19T09:20:00.000000-03:00"
  }
}
```

#### 2. Erro de Validação: `400 Bad Request`
Retornado se faltar `sala_id`, `temperatura` ou se os valores forem inválidos.
```json
{
  "status": "error",
  "message": "Campo 'sala_id' é obrigatório e não pode ser vazio."
}
```

---

## 🔍 Endpoint de Health Check

### `GET /api/v1/health`
Útil para o ESP32 ou desenvolvedor testar se a API está online e respondendo antes de começar a enviar dados.

- **Método**: `GET`
- **Resposta `200 OK`**:
```json
{
  "service": "SmartClass IoT Telemetry Ingestion API",
  "status": "healthy"
}
```

---

## 🧪 Comandos de Teste Rápido no Computador

### Teste via cURL (Linux / macOS / Git Bash / PowerShell):
```bash
curl -X POST http://localhost:5000/api/v1/medicoes \
  -H "Content-Type: application/json" \
  -d '{"sala_id": "Sala 101", "temperatura": 21.8, "umidade": 52.0}'
```

### Teste via PowerShell nativo (Windows):
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/medicoes" -Method Post -ContentType "application/json" -Body '{"sala_id":"Sala 101","temperatura":21.8,"umidade":52.0}'
```
