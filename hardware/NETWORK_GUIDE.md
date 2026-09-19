# 🌐 Guia de Rede e Conectividade para o ESP32

O **SmartClass já está hospedado e rodando 24/7 na VPS do projeto**!

Isso significa que a integração do microcontrolador é direta: **basta conectar o ESP32 a qualquer rede Wi-Fi que tenha acesso à internet**.

---

## 🚀 Endpoints Oficiais em Produção (VPS)

| Finalidade | Endpoint Oficial na VPS | Método |
| :--- | :--- | :--- |
| **Ingestão de Telemetria** | `http://187.77.63.90/smartclass/api/v1/medicoes` | `POST` |
| **Health Check (Teste de Conexão)** | `http://187.77.63.90/smartclass/api/v1/health` | `GET` |
| **Dashboard Online** | `http://187.77.63.90/smartclass/dashboard` | `GET` |

---

## ⚡ Como Configurar o ESP32 (`firmware_esp32.ino`)

No arquivo [`firmware_esp32/firmware_esp32.ino`](./firmware_esp32/firmware_esp32.ino), as configurações já vêm prontas. Você só precisa preencher os dados da sua rede Wi-Fi:

```cpp
// 1. Coloque o nome e senha do seu Wi-Fi (2.4 GHz)
const char* WIFI_SSID     = "SUA_REDE_WIFI";
const char* WIFI_PASSWORD = "SUA_SENHA_WIFI";

// 2. URL Oficial da VPS (já pré-configurada)
const char* SERVER_URL    = "http://187.77.63.90/smartclass/api/v1/medicoes";

// 3. Nome da Sala monitorada
const char* SALA_ID       = "Sala 101";
```

O firmware inclui tratamento de reconexão automática (`WiFi.status() != WL_CONNECTED`) e temporização com `millis()`.

---

## 🧪 Teste Rápido de Conectividade com a VPS

Antes mesmo de ligar o ESP32, você pode validar a comunicação com a VPS pelo terminal do seu computador:

### 1. Teste de Saúde da API (Health Check)
```bash
curl -i http://187.77.63.90/smartclass/api/v1/health
```
**Resposta esperada (`200 OK`)**:
```json
{
  "service": "SmartClass IoT Telemetry Ingestion API",
  "status": "healthy"
}
```

### 2. Teste de Envio de Leitura (Telemetria)
```bash
curl -X POST http://187.77.63.90/smartclass/api/v1/medicoes \
  -H "Content-Type: application/json" \
  -d '{"sala_id": "Sala 101", "temperatura": 22.5, "umidade": 55.0}'
```

### 3. Teste via PowerShell (Windows):
```powershell
Invoke-RestMethod -Uri "http://187.77.63.90/smartclass/api/v1/medicoes" -Method Post -ContentType "application/json" -Body '{"sala_id":"Sala 101","temperatura":22.5,"umidade":55.0}'
```
