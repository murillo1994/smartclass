import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
from src.config import Config
from src.database import User

def create_access_token(user_id: str, role: str, tenant_id: str = None, email: str = None) -> str:
    payload = {
        'sub': user_id,
        'role': role,
        'tenant_id': tenant_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token de autorização não fornecido'}), 401
            
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Formato de token inválido (use Bearer <token>)'}), 401
            
        token = parts[1]
        
        # Suporte a token mestre de admin configurado no .env
        if token == Config.ADMIN_API_TOKEN:
            g.current_user = User.query.filter_by(role='superadmin').first()
            g.current_tenant_id = None
            g.user_role = 'superadmin'
            return f(*args, **kwargs)

        payload = decode_access_token(token)
        if not payload:
            return jsonify({'error': 'Token inválido ou expirado'}), 401
            
        user = User.query.filter_by(id=payload['sub']).first()
        if not user or not user.active or user.deleted_at is not None:
            return jsonify({'error': 'Usuário inexistente ou inativo'}), 403

        # Injeta o contexto na requisição
        g.current_user = user
        g.current_tenant_id = user.tenant_id
        g.user_role = user.role
        
        return f(*args, **kwargs)
    return decorated

def require_role(allowed_roles):
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated(*args, **kwargs):
            if g.user_role not in allowed_roles:
                return jsonify({'error': 'Acesso negado: privilégios insuficientes'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
