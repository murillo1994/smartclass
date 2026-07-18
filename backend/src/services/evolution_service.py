import requests
import logging
import time
from src.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)

class EvolutionService:
    _mock_state = "close"  # "open", "close", "connecting"
    _mock_connect_time = None

    @staticmethod
    def is_mock_enabled():
        return not Config.EVOLUTION_API_KEY or "your_evolution" in Config.EVOLUTION_API_KEY

    @staticmethod
    def create_instance():
        """
        Cria a instância na Evolution API.
        """
        if EvolutionService.is_mock_enabled():
            return True

        url = f"{Config.EVOLUTION_API_URL}/instance/create"
        headers = {
            "Content-Type": "application/json",
            "apikey": Config.EVOLUTION_API_KEY
        }
        payload = {
            "instanceName": Config.EVOLUTION_INSTANCE_NAME,
            "qrcode": True,
            "integration": "WHATSAPP-BAILEYS"
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            if response.status_code in [200, 201]:
                logging.info(f"Instância {Config.EVOLUTION_INSTANCE_NAME} criada com sucesso.")
                return True
            else:
                logging.error(f"Erro ao criar instância {Config.EVOLUTION_INSTANCE_NAME}: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logging.error(f"Erro de conexão ao criar instância: {e}")
            return False

    @staticmethod
    def get_connection_state():
        """
        Retorna o estado da conexão da instância.
        Retornos possíveis: "open", "close", "connecting", "offline"
        """
        if EvolutionService.is_mock_enabled():
            if EvolutionService._mock_state == "connecting":
                if EvolutionService._mock_connect_time and time.time() - EvolutionService._mock_connect_time > 3:
                    EvolutionService._mock_state = "open"
            return EvolutionService._mock_state

        url = f"{Config.EVOLUTION_API_URL}/instance/connectionState/{Config.EVOLUTION_INSTANCE_NAME}"
        headers = {
            "apikey": Config.EVOLUTION_API_KEY
        }
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 404:
                logging.info(f"Instância {Config.EVOLUTION_INSTANCE_NAME} não encontrada. Criando...")
                if EvolutionService.create_instance():
                    return "close"
            if response.status_code == 200:
                data = response.json()
                state = data.get("instance", {}).get("state", "close")
                return state
            return "offline"
        except Exception as e:
            logging.error(f"Erro ao obter estado da conexão: {e}")
            return "offline"

    @staticmethod
    def get_qrcode():
        """
        Gera e retorna o QR code de conexão.
        Retorno: string em Base64 ("data:image/png;base64,...") ou None
        """
        if EvolutionService.is_mock_enabled():
            EvolutionService._mock_state = "connecting"
            EvolutionService._mock_connect_time = time.time()
            return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QcJDQ4oB5mHzwAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAABXUlEQVR42u3cQUpDMRSE4Y9Lu/EC3oIbL+A1vID34NJ16UZwpxDSpknMTKbIfF8g2Drw85K0aVvbtn1lWZa/13gD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13AD13ADv9sPH92FD/d9m2sAAAAASUVORK5CYII="

        url = f"{Config.EVOLUTION_API_URL}/instance/connect/{Config.EVOLUTION_INSTANCE_NAME}"
        headers = {
            "apikey": Config.EVOLUTION_API_KEY
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 404:
                logging.info(f"Instância {Config.EVOLUTION_INSTANCE_NAME} não encontrada ao obter QR. Criando...")
                if EvolutionService.create_instance():
                    response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                qrcode_data = data.get("qrcode", {})
                if isinstance(qrcode_data, dict):
                    return qrcode_data.get("base64")
                return data.get("base64")
            return None
        except Exception as e:
            logging.error(f"Erro ao obter QR Code: {e}")
            return None

    @staticmethod
    def logout():
        """
        Encerra a sessão da instância.
        """
        if EvolutionService.is_mock_enabled():
            EvolutionService._mock_state = "close"
            EvolutionService._mock_connect_time = None
            return True

        url = f"{Config.EVOLUTION_API_URL}/instance/logout/{Config.EVOLUTION_INSTANCE_NAME}"
        headers = {
            "apikey": Config.EVOLUTION_API_KEY
        }
        try:
            response = requests.post(url, headers=headers, timeout=10)
            return response.status_code in [200, 201]
        except Exception as e:
            logging.error(f"Erro ao fazer logout da instância: {e}")
            return False

    @staticmethod
    def send_message(phone: str, text: str):
        """
        Envia uma mensagem de texto para o número especificado via Evolution API.
        """
        clean_phone = phone.split('@')[0]
        
        url = f"{Config.EVOLUTION_API_URL}/message/sendText/{Config.EVOLUTION_INSTANCE_NAME}"
        headers = {
            "Content-Type": "application/json",
            "apikey": Config.EVOLUTION_API_KEY
        }
        payload = {
            "number": clean_phone,
            "text": text,
            "delay": 1000,
            "linkPreview": False
        }
        
        if EvolutionService.is_mock_enabled():
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
