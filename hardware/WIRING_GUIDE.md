# 🔌 Guia de Ligação e Hardware (ESP32 + DHT11 / DHT22)

Este guia contém todas as instruções práticas, pinagem e diagrama de conexão para montar a bancada física do projeto **SmartClass**.

---

## 📋 Lista de Componentes Necessários

| Componente | Quantidade | Observação |
| :--- | :--- | :--- |
| **ESP32 DevKit V1** (30 ou 38 pinos) | 1 un. | Microcontrolador com Wi-Fi 2.4GHz integrado |
| **Sensor de Temperatura/Umidade** | 1 un. | **DHT22** (branco, maior precisão) ou **DHT11** (azul, básico) |
| **Resistor de 10kΩ** | 1 un. | **Apenas se o DHT for o sensor solto de 4 pinos** (dispensável se for módulo de 3 pinos) |
| **Protoboard (Matriz de Contato)** | 1 un. | Tamanho médio (400 ou 830 furos) |
| **Jumpers Macho-Macho / Macho-Fêmea** | 3 a 5 un. | Para ligar o ESP32 ao sensor |
| **Cabo Micro-USB ou USB-C** | 1 un. | Para alimentação e gravação via computador |

---

## 📌 Tabela de Conexões (Pinout)

### Opção A: Módulo DHT de 3 Pinos (comum em kits de robótica)
Geralmente possui a placa PCB com o resistor pull-up já embutido.

| Pino do Módulo DHT | Descrição | Conectar no ESP32 | Cor recomendada do jumper |
| :--- | :--- | :--- | :--- |
| **VCC** (ou `+`) | Alimentação 3.3V ~ 5V | **3V3** (ou **VIN**) | Vermelho |
| **DATA** (ou `out` / `S`) | Sinal Digital | **GPIO 4** (D4) | Amarelo / Verde |
| **GND** (ou `-`) | Terra / Referência | **GND** | Preto / Azul |

---

### Opção B: Sensor DHT Avulso de 4 Pinos
Requer um resistor pull-up de **10kΩ** entre o pino de dados e o pino positivo.

```
       +-----------------+
       |  DHT11 / DHT22  |
       |  [ Frente ]     |
       +-----------------+
         |   |   |   |
       Pin 1 2   3   4
         |   |       |
         |   +-------+----[ Resistor 10kΩ ]----+
         |   |                                 |
        VCC DATA    NC                        GND
         |   |                                 |
         |   +--------> Conectar ao GPIO 4    |
         +------------> Conectar ao 3V3       |
         +------------------------------------+
```

- **Pino 1 (Esquerda):** VCC $\rightarrow$ Conectar ao **3V3** do ESP32.
- **Pino 2:** DATA $\rightarrow$ Conectar ao **GPIO 4 (D4)** do ESP32 + uma perna do resistor de 10kΩ.
- **Pino 3:** Não Conectado (NC).
- **Pino 4 (Direita):** GND $\rightarrow$ Conectar ao **GND** do ESP32.
- **Resistor 10kΩ:** Ligar entre o **Pino 1 (VCC)** e o **Pino 2 (DATA)**.

---

## 💻 Como Gravar o ESP32 na Arduino IDE (Passo a Passo)

1. **Instalar a Arduino IDE** (versão 2.x recomendada).
2. **Adicionar o suporte à placa ESP32**:
   - Vá em `Arquivo -> Preferências` (`File -> Preferences`).
   - No campo *URLs Adicionais do Gerenciador de Placas*, adicione:
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Vá em `Ferramentas -> Placa -> Gerenciador de Placas`, busque por `esp32` (da Espressif Systems) e clique em **Instalar**.
3. **Instalar as Bibliotecas Necessárias**:
   - Vá em `Ferramentas -> Gerenciar Bibliotecas...` (`Ctrl + Shift + I`).
   - Busque e instale:
     - `DHT sensor library` (por Adafruit) — instale as dependências que ele pedir (`Adafruit Unified Sensor`).
     - `ArduinoJson` (por Benoit Blanchon).
4. **Abrir o Firmware**:
   - Abra o arquivo [`hardware/firmware_esp32/firmware_esp32.ino`](./firmware_esp32/firmware_esp32.ino).
   - Altere as constantes:
     ```cpp
     const char* WIFI_SSID     = "SEU_WIFI";
     const char* WIFI_PASSWORD = "SUA_SENHA";
     const char* SERVER_URL    = "http://192.168.1.100:5000/api/v1/medicoes";
     const char* SALA_ID       = "Sala 101";
     ```
5. **Gravação**:
   - Selecione a placa: `DOIT ESP32 DEVKIT V1` (ou `ESP32 Dev Module`).
   - Selecione a Porta COM correspondente.
   - Clique em **Carregar (Upload)**.
   - Abra o **Monitor Serial** em `115200 baud` para acompanhar os logs em tempo real.

---

## 🛠️ Diagnóstico e Resolução de Problemas (Troubleshooting)

| Sintoma | Causa Mais Provável | Solução |
| :--- | :--- | :--- |
| `Falha ao ler do sensor DHT!` | Fio solto, pino incorreto ou ausência do resistor de 10kΩ. | Verifique se o pino de dados está no GPIO 4 e se o sensor está bem encaixado na protoboard. |
| `WiFi: Falha ao conectar` | Wi-Fi em 5GHz (o ESP32 só opera em 2.4GHz) ou senha errada. | Conecte no ponto de acesso 2.4GHz ou roteie o 4G do celular. |
| `HTTP: Código -1 ou Connection Refused` | O ESP32 está tentando acessar `localhost` ou o Firewall do Windows bloqueou a porta 5000. | Siga as instruções do [`hardware/NETWORK_GUIDE.md`](./NETWORK_GUIDE.md). |
