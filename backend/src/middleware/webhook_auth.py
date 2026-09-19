from functools import wraps
from flask import request, jsonify
from src.config import Config
from src.database import WhatsAppInstance

def require_webhook_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 1. Verifica token via header X-Webhook-Secret ou Authorization
        token = request.headers.get('X-Webhook-Secret') or request.headers.get('apikey')
        if not token:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split()[1]
                
        # 2. Se bater com o segredo global do cluster
        if token and Config.EVOLUTION_WEBHOOK_SECRET and token == Config.EVOLUTION_WEBHOOK_SECRET:
            return f(*args, **kwargs)

        # 3. Se vier da Evolution API local sem segredo no header em ambiente de desenvolvimento
        payload = request.get_json(silent=True) or {}
        instance_name = payload.get('instance')
        
        if instance_name:
            instance = WhatsAppInstance.query.filter_by(instance_name=instance_name).first()
            if instance and token and instance.webhook_secret == token:
                return f(*args, **kwargs)
                
        # Se for desenvolvimento local e nenhum segredo estiver configurado estritamente
        if Config.FLASK_ENV == 'development' and not Config.EVOLUTION_WEBHOOK_SECRET:
            return f(*args, **kwargs)
            
        if not token or (token != Config.EVOLUTION_WEBHOOK_SECRET):
            return jsonify({'error': 'Webhook não autorizado: token de assinatura inválido'}), 401
            
        return f(*args, **kwargs)
    return decorated
