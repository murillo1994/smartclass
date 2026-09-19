import logging
import requests
from src.config import Config

logger = logging.getLogger(__name__)

class EvolutionService:
    @staticmethod
    def _headers():
        return {
            'apikey': Config.EVOLUTION_API_KEY,
            'Content-Type': 'application/json'
        }

    @classmethod
    def create_instance(cls, instance_name: str):
        """Cria uma nova instância no cluster da Evolution API v2"""
        url = f'{Config.EVOLUTION_API_URL}/instance/create'
        payload = {
            'instanceName': instance_name,
            'token': '',
            'qrcode': True,
            'integration': 'WHATSAPP-BAILEYS',
            'webhook': f'http://localhost:{Config.PORT}/api/v1/webhooks/evolution',
            'webhook_by_events': False,
            'events': [
                'MESSAGES_UPSERT',
                'MESSAGES_UPDATE',
                'CONNECTION_UPDATE',
                'QRCODE_UPDATED'
            ]
        }
        try:
            res = requests.post(url, json=payload, headers=cls._headers(), timeout=10)
            return res.json()
        except Exception as e:
            logger.error(f'Erro ao criar instância {instance_name} na Evolution API: {e}')
            return {'error': str(e)}

    @classmethod
    def get_qrcode(cls, instance_name: str):
        """Solicita conexão e retorno do QR Code"""
        url = f'{Config.EVOLUTION_API_URL}/instance/connect/{instance_name}'
        try:
            res = requests.get(url, headers=cls._headers(), timeout=10)
            return res.json()
        except Exception as e:
            logger.error(f'Erro ao obter QR Code de {instance_name}: {e}')
            return {'error': str(e)}

    @classmethod
    def get_connection_status(cls, instance_name: str):
        """Verifica o status atual da conexão"""
        url = f'{Config.EVOLUTION_API_URL}/instance/connectionState/{instance_name}'
        try:
            res = requests.get(url, headers=cls._headers(), timeout=5)
            if res.ok:
                data = res.json()
                return data.get('instance', {}).get('state', 'disconnected')
            return 'disconnected'
        except Exception as e:
            logger.error(f'Erro ao verificar status de {instance_name}: {e}')
            return 'disconnected'

    @classmethod
    def logout_instance(cls, instance_name: str):
        """Desconecta o WhatsApp da instância"""
        url = f'{Config.EVOLUTION_API_URL}/instance/logout/{instance_name}'
        try:
            res = requests.delete(url, headers=cls._headers(), timeout=10)
            return res.json()
        except Exception as e:
            logger.error(f'Erro ao desconectar {instance_name}: {e}')
            return {'error': str(e)}

    @classmethod
    def send_text_message(cls, instance_name: str, remote_jid: str, text: str):
        """Envia mensagem de texto via Evolution API"""
        url = f'{Config.EVOLUTION_API_URL}/message/sendText/{instance_name}'
        # Normaliza número
        number = remote_jid.split('@')[0] if '@' in remote_jid else remote_jid
        payload = {
            'number': number,
            'options': {
                'delay': 1200,
                'presence': 'composing',
                'linkPreview': True
            },
            'text': text
        }
        try:
            res = requests.post(url, json=payload, headers=cls._headers(), timeout=10)
            return res.json()
        except Exception as e:
            logger.error(f'Erro ao enviar mensagem para {remote_jid} via {instance_name}: {e}')
            return {'error': str(e)}

    @classmethod
    def send_media_message(cls, instance_name: str, remote_jid: str, media_url: str, media_type: str, caption: str = ''):
        """Envia áudio/imagem/documento via Evolution API"""
        url = f'{Config.EVOLUTION_API_URL}/message/sendMedia/{instance_name}'
        number = remote_jid.split('@')[0] if '@' in remote_jid else remote_jid
        payload = {
            'number': number,
            'media': media_url,
            'mediatype': media_type,
            'caption': caption
        }
        try:
            res = requests.post(url, json=payload, headers=cls._headers(), timeout=15)
            return res.json()
        except Exception as e:
            logger.error(f'Erro ao enviar mídia para {remote_jid} via {instance_name}: {e}')
            return {'error': str(e)}
