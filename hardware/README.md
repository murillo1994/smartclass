# 🛠️ SmartClass - Kit de Integração e Desenvolvimento de Hardware (ESP32)

Bem-vindo ao kit de desenvolvimento de hardware do **SmartClass**. Todos os recursos necessários para configurar, testar e conectar o microcontrolador ESP32 à nossa plataforma estão organizados aqui.

---

## 📁 Estrutura do Kit

| Arquivo / Pasta | Descrição |
| :--- | :--- |
| [`firmware_esp32/firmware_esp32.ino`](./firmware_esp32/firmware_esp32.ino) | **Código C++/Arduino pronto para gravação no ESP32** com reconexão Wi-Fi automática, leitura DHT e envio HTTP/HTTPS POST JSON para a VPS. |
| [`WIRING_GUIDE.md`](./WIRING_GUIDE.md) | **Esquemático e Pinout**: Tabela de ligação dos fios, resistores, pinos GPIO e cuidados elétricos. |
| [`NETWORK_GUIDE.md`](./NETWORK_GUIDE.md) | **Guia de Conectividade de Rede**: Como apontar o ESP32 diretamente para o IP/domínio da VPS em produção. |
| [`API_CONTRACT.md`](./API_CONTRACT.md) | **Contrato de API**: Especificação do payload JSON, códigos HTTP e comandos de teste com cURL. |
| [`wokwi_project/`](./wokwi_project/) | **Simulador Virtual Wokwi**: Teste o código e circuito no navegador sem precisar dos componentes físicos na hora. |

---

## ⚡ Guia Rápido (3 Passos)

1. **Montagem física**: Siga o [Guia de Ligação (`WIRING_GUIDE.md`)](./WIRING_GUIDE.md).
2. **Configuração de Rede**: Abra o [Guia de Rede (`NETWORK_GUIDE.md`)](./NETWORK_GUIDE.md) e insira o IP/domínio da sua VPS.
3. **Gravação**: Abra o arquivo [`firmware_esp32/firmware_esp32.ino`](./firmware_esp32/firmware_esp32.ino) na Arduino IDE, preencha o Wi-Fi e a URL da VPS, e grave na placa!
