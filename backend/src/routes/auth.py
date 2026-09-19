from flask import Blueprint, request, jsonify, g
from src.database import db, User, Tenant
from src.middleware.auth import create_access_token, require_auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = (data.get('email') or data.get('username', '')).strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Informe e-mail e senha para acessar'}), 400

    # Busca usuário por e-mail (ativo e não deletado)
    user = User.query.filter_by(email=email).first()
    if not user or user.deleted_at is not None or not user.active:
        return jsonify({'error': 'Credenciais incorretas ou conta inativa'}), 401

    if not user.check_password(password):
        return jsonify({'error': 'Credenciais incorretas ou conta inativa'}), 401

    # Se for usuário de tenant, verifica se a empresa está ativa
    tenant_data = None
    if user.tenant_id:
        tenant = Tenant.query.get(user.tenant_id)
        if not tenant:
            return jsonify({'error': 'Empresa vinculada não encontrada'}), 403
        if tenant.status == 'suspended':
            return jsonify({'error': 'O acesso da sua empresa está suspenso. Entre em contato com o suporte.'}), 403
        tenant_data = tenant.to_dict()

    # Gera token JWT com claims completas
    token = create_access_token(
        user_id=user.id,
        role=user.role,
        tenant_id=user.tenant_id,
        email=user.email
    )

    return jsonify({
        'token': token,
        'user': user.to_dict(),
        'tenant': tenant_data
    }), 200

@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    tenant_data = None
    if g.current_user.tenant_id:
        tenant = Tenant.query.get(g.current_user.tenant_id)
        if tenant:
            tenant_data = tenant.to_dict()

    return jsonify({
        'user': g.current_user.to_dict(),
        'tenant': tenant_data
    }), 200
