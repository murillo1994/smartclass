/*
 * =========================================================================================
 * SmartClass - Firmware de Telemetria IoT para ESP32
 * =========================================================================================
 * Projeto: SmartClass - Monitoramento de Conforto Térmico Escolar
 * Microcontrolador: ESP32 DevKit V1 (30 ou 38 pinos)
 * Sensor: DHT11 ou DHT22 (Temperatura e Umidade)
 * Comunicação: Wi-Fi 2.4GHz + HTTP REST Client (POST JSON)
 *
 * Bibliotecas Necessárias (instalar pelo Gerenciador de Bibliotecas da Arduino IDE):
 * 1. "DHT sensor library" by Adafruit (ou "DHTesp" by beegee-tokyo)
 *    -> Requer também "Adafruit Unified Sensor"
 * 2. "ArduinoJson" by Benoit Blanchon (versão 6 ou 7)
 * =========================================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <DHT.h>
#include <ArduinoJson.h>

// =========================================================================================
// 1. CONFIGURAÇÕES PRINCIPAIS (AJUSTE AQUI CONFORME SEU AMBIENTE)
// =========================================================================================

// Credenciais da Rede Wi-Fi (o ESP32 suporta apenas redes 2.4 GHz)
// Pode ser o Wi-Fi de casa, da faculdade ou o 4G roteado pelo celular.
const char* WIFI_SSID     = "SUA_REDE_WIFI";
const char* WIFI_PASSWORD = "SUA_SENHA_WIFI";

// URL da API Backend do SmartClass na sua VPS
// Exemplos:
// - Com domínio e HTTPS: "https://smartclass.seudominio.com/api/v1/medicoes"
// - Com IP direto da VPS: "http://SEU_IP_VPS:5000/api/v1/medicoes"
// - Em teste local:       "http://192.168.1.100:5000/api/v1/medicoes"
const char* SERVER_URL    = "http://SEU_IP_VPS:5000/api/v1/medicoes";

// Identificador da Sala / Ambiente monitorado por este ESP32
const char* SALA_ID       = "Sala 101";

// Intervalo de envio das medições (em milissegundos) -> 10000 ms = 10 segundos
const unsigned long INTERVALO_ENVIO_MS = 10000;

// =========================================================================================
// 2. PINAGEM E SENSORES
// =========================================================================================

#define DHT_PIN 4        // Pino GPIO do ESP32 conectado à perna de DATA do DHT
#define DHT_TYPE DHT22   // Troque para DHT11 se estiver usando o sensor azul

#define LED_STATUS_PIN 2 // LED onboard do ESP32 (GPIO 2 na maioria das placas)

// Instância do sensor
DHT dht(DHT_PIN, DHT_TYPE);

// Controle de tempo não-bloqueante (evita travar o ESP32 com delay)
unsigned long ultimaLeituraMs = 0;

// =========================================================================================
// 3. FUNÇÕES AUXILIARES
// =========================================================================================

// Função para piscar o LED indicador
void piscarLed(int vezes, int tempoMs) {
  for (int i = 0; i < vezes; i++) {
    digitalWrite(LED_STATUS_PIN, HIGH);
    delay(tempoMs);
    digitalWrite(LED_STATUS_PIN, LOW);
    delay(tempoMs);
  }
}

// Conexão e manutenção do Wi-Fi
void conectarWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;

  Serial.println();
  Serial.print("[WiFi] Conectando a: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 25) {
    delay(500);
    Serial.print(".");
    digitalWrite(LED_STATUS_PIN, !digitalRead(LED_STATUS_PIN));
    tentativas++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(LED_STATUS_PIN, HIGH);
    Serial.println();
    Serial.println("[WiFi] Conectado com sucesso!");
    Serial.print("[WiFi] Endereço IP do ESP32: ");
    Serial.println(WiFi.localIP());
    Serial.print("[WiFi] Sinal RSSI: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    digitalWrite(LED_STATUS_PIN, LOW);
    Serial.println();
    Serial.println("[WiFi] Falha ao conectar. Tentando novamente no próximo ciclo...");
  }
}

// Envio da medição via HTTP / HTTPS POST JSON
bool enviarMedicao(float temperatura, float umidade) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[HTTP] Wi-Fi desconectado. Abortando envio.");
    return false;
  }

  HTTPClient http;
  WiFiClientSecure *clientSecure = nullptr;
  WiFiClient *clientInsecure = nullptr;

  if (String(SERVER_URL).startsWith("https://")) {
    clientSecure = new WiFiClientSecure;
    clientSecure->setInsecure(); // Permite certificados SSL sem necessidade de gravar CA root no chip
    http.begin(*clientSecure, SERVER_URL);
  } else {
    clientInsecure = new WiFiClient;
    http.begin(*clientInsecure, SERVER_URL);
  }

  http.addHeader("Content-Type", "application/json");
  http.addHeader("Accept", "application/json");
  http.setTimeout(7000); // 7 segundos de timeout

  // Montagem do documento JSON
  StaticJsonDocument<200> doc;
  doc["sala_id"] = SALA_ID;
  doc["temperatura"] = serialized(String(temperatura, 2));
  doc["umidade"] = serialized(String(umidade, 2));

  String requestBody;
  serializeJson(doc, requestBody);

  Serial.print("[HTTP] Enviando POST para: ");
  Serial.println(SERVER_URL);
  Serial.print("[HTTP] Payload: ");
  Serial.println(requestBody);

  int httpResponseCode = http.POST(requestBody);

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.print("[HTTP] Código de Resposta: ");
    Serial.println(httpResponseCode);
    Serial.print("[HTTP] Retorno do Servidor: ");
    Serial.println(response);

    if (httpResponseCode == 200 || httpResponseCode == 201) {
      piscarLed(2, 80); // Pisca rápido 2x indicando sucesso
      http.end();
      if (clientSecure) delete clientSecure;
      if (clientInsecure) delete clientInsecure;
      return true;
    }
  } else {
    Serial.print("[HTTP] Erro na requisição: ");
    Serial.println(http.errorToString(httpResponseCode).c_str());
  }

  http.end();
  if (clientSecure) delete clientSecure;
  if (clientInsecure) delete clientInsecure;
  return false;
}

// =========================================================================================
// 4. SETUP INICIAL
// =========================================================================================
void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(LED_STATUS_PIN, OUTPUT);
  digitalWrite(LED_STATUS_PIN, LOW);

  Serial.println("\n==================================================");
  Serial.println("   SmartClass - Inicializando Módulo ESP32 IoT   ");
  Serial.println("==================================================");

  // Inicializa o sensor DHT
  Serial.println("[Sensor] Inicializando sensor DHT...");
  dht.begin();

  // Conecta ao Wi-Fi
  conectarWiFi();

  Serial.println("[Sistema] Configuração concluída. Iniciando loop de telemetria.\n");
}

// =========================================================================================
// 5. LOOP PRINCIPAL
// =========================================================================================
void loop() {
  // Garante que o Wi-Fi permaneça conectado
  if (WiFi.status() != WL_CONNECTED) {
    conectarWiFi();
  }

  unsigned long agora = millis();

  // Dispara a leitura e envio no intervalo configurado
  if (agora - ultimaLeituraMs >= INTERVALO_ENVIO_MS) {
    ultimaLeituraMs = agora;

    Serial.println("--------------------------------------------------");
    Serial.println("[Sensor] Efetuando leitura do ambiente...");

    float temp = dht.readTemperature();
    float hum  = dht.readHumidity();

    // Verificação de integridade da leitura (evita enviar NaN/lixo)
    if (isnan(temp) || isnan(hum)) {
      Serial.println("[Sensor] ⚠️ AVISO: Falha ao ler do sensor DHT! Verifique fios e resistor.");
      piscarLed(5, 50); // Pisca 5x rápido indicando alerta no sensor
      return;
    }

    Serial.print("[Sensor] Temperatura: ");
    Serial.print(temp, 2);
    Serial.print(" °C | Umidade: ");
    Serial.print(hum, 2);
    Serial.println(" %");

    // Envia para o backend
    bool sucesso = enviarMedicao(temp, hum);

    if (sucesso) {
      Serial.println("[Status] ✅ Medição registrada no SmartClass com sucesso!");
    } else {
      Serial.println("[Status] ❌ Falha na transmissão de telemetria.");
    }
  }

  // Pequeno delay para aliviar o watchdog do ESP32
  delay(10);
}
