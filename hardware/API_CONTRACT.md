# 📜 Contrato de API & Especificação de Telemetria

Este documento define o contrato oficial de comunicação entre o hardware (ESP32) e o backend do **SmartClass**.

---

## 🌐 Endpoints Oficiais em Produção (VPS)

- **Base URL Oficial**: `http://187.77.63.90/smartclass/api/v1`
- **Base URL Local (Desenvolvimento)**: `http://localhost:5070/api/v1`

---

## 📡 1. Ingestão de Telemetria

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
```json
{
  "status": "success",
  "message": "Medição registrada com sucesso.",
  "data": {
    "id": 1,
    "sala_id": "Sala 101",
    "temperatura": 22.5,
    "umidade": 58.2,
    "data_registro": "2026-09-19T13:15:24.421213+00:00"
  }
}
```

#### 2. Erro de Validação: `400 Bad Request`
```json
{
  "status": "error",
  "message": "Campo 'sala_id' é obrigatório e não pode ser vazio."
}
```

---

## 🔍 2. Health Check (Verificação de Status)

### `GET /api/v1/health`

- **Método**: `GET`
- **Resposta `200 OK`**:
```json
{
  "service": "SmartClass IoT Telemetry Ingestion API",
  "status": "healthy"
}
```

---

## 🧪 Comandos de Teste com a VPS

### Teste via cURL:
```bash
curl -X POST http://187.77.63.90/smartclass/api/v1/medicoes \
  -H "Content-Type: application/json" \
  -d '{"sala_id": "Sala 101", "temperatura": 21.8, "umidade": 52.0}'
```

### Teste via PowerShell (Windows):
```powershell
Invoke-RestMethod -Uri "http://187.77.63.90/smartclass/api/v1/medicoes" -Method Post -ContentType "application/json" -Body '{"sala_id":"Sala 101","temperatura":21.8,"umidade":52.0}'
```
