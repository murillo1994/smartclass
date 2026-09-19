# 🛠️ SmartClass - Kit de Integração e Desenvolvimento de Hardware (ESP32)

Bem-vindo ao kit de desenvolvimento de hardware do **SmartClass**.

O backend do projeto já está **hospedado e ativo em produção na VPS**:
- **Servidor Ativo**: `https://smartclass.mypaywise.cloud/api/v1`
- **Dashboard Online**: `https://smartclass.mypaywise.cloud/dashboard`

---

## 📁 Estrutura do Kit

| Arquivo / Pasta | Descrição |
| :--- | :--- |
| [`firmware_esp32/firmware_esp32.ino`](./firmware_esp32/firmware_esp32.ino) | **Código C++/Arduino pré-configurado com a URL da VPS**, reconexão Wi-Fi automática, leitura DHT e envio HTTP POST JSON. |
| [`WIRING_GUIDE.md`](./WIRING_GUIDE.md) | **Esquemático e Pinout**: Tabela de ligação dos fios, resistores, pinos GPIO e cuidados elétricos. |
| [`NETWORK_GUIDE.md`](./NETWORK_GUIDE.md) | **Guia de Conectividade de Rede**: Instruções para conectar o ESP32 ao servidor em produção na VPS. |
| [`API_CONTRACT.md`](./API_CONTRACT.md) | **Contrato de API**: Especificação do payload JSON, códigos HTTP e comandos de teste com cURL. |
| [`wokwi_project/`](./wokwi_project/) | **Simulador Virtual Wokwi**: Teste o código e circuito no navegador sem precisar dos componentes físicos na hora. |

---

## ⚡ Guia Rápido de Gravação (3 Passos)

1. **Montagem física**: Conecte o sensor DHT ao ESP32 seguindo o [Guia de Ligação (`WIRING_GUIDE.md`)](./WIRING_GUIDE.md).
2. **Preencher Wi-Fi**: Abra o arquivo [`firmware_esp32/firmware_esp32.ino`](./firmware_esp32/firmware_esp32.ino) na Arduino IDE e coloque o nome e senha do seu Wi-Fi.
3. **Gravar**: Conecte o ESP32 na porta USB do computador e clique em **Carregar (Upload)**! As medições começarão a aparecer no dashboard online instantaneamente!
