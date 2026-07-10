import requests
import logging
from src.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)

class EvolutionService:
    @staticmethod
    def send_message(phone: str, text: str):
        """
        Envia uma mensagem de texto para o número especificado via Evolution API.
        """
        # Limpa o número de telefone (remove sufixo de JID do whatsapp caso esteja presente)
        clean_phone = phone.split('@')[0]
        
        url = f"{Config.EVOLUTION_API_URL}/message/sendText/{Config.EVOLUTION_INSTANCE_NAME}"
        headers = {
            "Content-Type": "application/json",
            "apikey": Config.EVOLUTION_API_KEY
        }
        payload = {
            "number": clean_phone,
            "text": text,
            "delay": 1000,  # 1 segundo de atraso de digitação simulado
            "linkPreview": False
        }
        
        # Ignora envio real se o host padrão não estiver configurado para evitar quebras locais de teste
        if not Config.EVOLUTION_API_KEY or "your_evolution" in Config.EVOLUTION_API_KEY:
            logging.warning(f"[Evolution API mock] Enviando mensagem para {clean_phone}: {text}")
            return True

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code in [200, 201]:
                logging.info(f"Mensagem enviada com sucesso para {clean_phone}")
                return True
            else:
                logging.error(f"Erro ao enviar mensagem para {clean_phone}: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logging.error(f"Erro de conexão com Evolution API: {e}")
            return False
