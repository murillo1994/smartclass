# 🌐 Guia de Rede e Conectividade para o ESP32

Como o **SmartClass estará hospedado em uma VPS (Servidor em Nuvem)**, a vida do desenvolvedor de hardware fica **100x mais fácil**!

---

## 🚀 Arquitetura Oficial: Servidor na VPS (Ambiente de Produção)

Com o backend rodando na sua VPS:
1. **O ESP32 pode estar em qualquer lugar**: na sua casa, na bancada da faculdade, no laboratório ou conectado ao 4G do celular.
2. **Não precisa estar na mesma rede Wi-Fi do seu computador pessoal**.
3. **Não precisa de ngrok nem de configuração de IP local**.

### Como configurar no ESP32 (`firmware_esp32.ino`):

Basta colocar o IP ou domínio da VPS na constante `SERVER_URL`:

```cpp
// Opção A: Se você configurou um domínio com HTTPS (Nginx / Let's Encrypt)
const char* SERVER_URL = "https://smartclass.seudominio.com/api/v1/medicoes";

// Opção B: Se estiver acessando direto pelo IP público da VPS
const char* SERVER_URL = "http://123.45.67.89:5000/api/v1/medicoes";
```

O firmware já está preparado com `WiFiClientSecure` e `setInsecure()` para aceitar conexões HTTPS com certificados SSL de forma totalmente automática.

---

## 🔒 Dicas para a VPS (Checklist de Portas e Firewall)

Para garantir que o ESP32 consiga enviar as requisições para a VPS:

1. **Liberar a Porta no Firewall da VPS (UFW / Security Group da AWS, Oracle Cloud, DigitalOcean, Hetzner, etc.)**:
   - Se estiver usando **Nginx** como Proxy Reverso: liberar portas **80 (HTTP)** e **443 (HTTPS)**.
   - Se estiver acessando o Flask diretamente: liberar a porta **5000 (TCP)**.
   ```bash
   # Exemplo no Ubuntu / Debian com UFW:
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 5000/tcp
   sudo ufw reload
   ```

2. **Garantir que o Flask escute em todas as interfaces (`0.0.0.0`)**:
   - O comando de inicialização na VPS deve ser:
   ```bash
   python backend/src/app.py
   # (Que internamente já roda com host="0.0.0.0" e port=5000)
   ```

---

## 🧪 Como Testar a VPS antes de Ligar o ESP32

Para ter certeza de que a VPS está recebendo dados da internet, teste no terminal do seu próprio computador ou no navegador:

### No navegador ou pelo celular (4G):
Acesse: `http://SEU_IP_VPS:5000/api/v1/health`  
*(Deve responder `{"service":"SmartClass IoT Telemetry Ingestion API","status":"healthy"}`)*

### Via cURL:
```bash
curl -X POST http://SEU_IP_VPS:5000/api/v1/medicoes \
  -H "Content-Type: application/json" \
  -d '{"sala_id": "Sala 101", "temperatura": 23.4, "umidade": 56.0}'
```

Se o teste acima funcionar, o ESP32 funcionará instantaneamente assim que for ligado na tomada!
