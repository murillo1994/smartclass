# 🕹️ Simulação Virtual no Wokwi (ESP32 + DHT22)

Você pode simular todo o circuito e código sem ter o ESP32 físico em mãos utilizando o simulador gratuito [Wokwi](https://wokwi.com).

---

## 🚀 Como Executar a Simulação Online

1. Acesse: [https://wokwi.com/projects/new/esp32](https://wokwi.com/projects/new/esp32)
2. No editor de código principal (`sketch.ino`), cole o conteúdo do arquivo:
   `hardware/firmware_esp32/firmware_esp32.ino`
3. Na aba `diagram.json`, substitua o conteúdo pelo arquivo:
   `hardware/wokwi_project/diagram.json`
4. Na aba `Library Manager` (ícone de pastinha/livro na esquerda), adicione as bibliotecas:
   - `DHT sensor library for ESPx` ou `DHT sensor library`
   - `ArduinoJson`
5. Altere a constante `WIFI_SSID` para `"Wokwi-GUEST"` e `WIFI_PASSWORD` para `""` (vazio), que é a rede Wi-Fi virtual que o Wokwi disponibiliza.
6. Clique no botão verde de **Play / Simular**.
7. Durante a simulação, você pode clicar em cima do sensor DHT22 virtual para alterar a temperatura e umidade com um slider interativo e ver as leituras saindo no Monitor Serial!
