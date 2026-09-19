from datetime import datetime
from flask import Blueprint, request, jsonify, g
from src.database import db, Tenant, User, WhatsAppInstance
from src.middleware.auth import require_role
from src.middleware.tenant import require_tenant, get_current_tenant_id
from src.services.evolution_service import EvolutionService

tenant_admin_bp = Blueprint('tenant_admin', __name__)

# ==========================================
# GESTÃO MULTI-NÚMERO WHATSAPP
# ==========================================

@tenant_admin_bp.route('/whatsapp/instances', methods=['GET'])
@require_role(['admin', 'superadmin'])
@require_tenant
def list_instances():
    tenant_id = get_current_tenant_id()
    instances = WhatsAppInstance.query.filter_by(tenant_id=tenant_id).order_by(WhatsAppInstance.created_at.asc()).all()
    
    # Atualiza status em tempo real com a Evolution API
    results = []
    for inst in instances:
        live_state = EvolutionService.get_connection_status(inst.instance_name)
        inst.status = 'connected' if live_state in ['open', 'connected'] else 'disconnected'
        results.append(inst.to_dict())
    db.session.commit()
    return jsonify(results), 200

@tenant_admin_bp.route('/whatsapp/instances', methods=['POST'])
@require_role(['admin', 'superadmin'])
@require_tenant
def create_instance():
    tenant_id = get_current_tenant_id()
    tenant = Tenant.query.get(tenant_id)
    
    # Verifica limite contratado de instâncias
    current_count = WhatsAppInstance.query.filter_by(tenant_id=tenant_id).count()
    if current_count >= tenant.max_instances:
        return jsonify({'error': f'Limite de números atingido ({tenant.max_instances}). Faça upgrade do plano para conectar mais canais.'}), 400

    data = request.get_json() or {}
    name = data.get('name', f'WhatsApp #{current_count + 1}')
    
    # Gera nome único para a Evolution API
    instance_name = f'tenant_{tenant.slug}_{current_count + 1}'
    
    # Cria no banco local
    inst = WhatsAppInstance(
        tenant_id=tenant_id,
        name=name,
        instance_name=instance_name,
        status='connecting'
    )
    db.session.add(inst)
    db.session.flush()

    # Cria na Evolution API
    evo_res = EvolutionService.create_instance(instance_name)
    
    # Solicita QR Code
    qr_res = EvolutionService.get_qrcode(instance_name)
    qrcode_base64 = qr_res.get('qrcode', {}).get('base64') if isinstance(qr_res, dict) else None
    if qrcode_base64:
        inst.qrcode_base64 = qrcode_base64

    db.session.commit()
    return jsonify(inst.to_dict()), 201

@tenant_admin_bp.route('/whatsapp/instances/<instance_id>/qrcode', methods=['GET'])
@require_role(['admin', 'superadmin'])
@require_tenant
def get_instance_qrcode(instance_id):
    tenant_id = get_current_tenant_id()
    inst = WhatsAppInstance.query.filter_by(id=instance_id, tenant_id=tenant_id).first()
    if not inst:
        return jsonify({'error': 'Conexão não encontrada'}), 404

    qr_res = EvolutionService.get_qrcode(inst.instance_name)
    qrcode_base64 = qr_res.get('qrcode', {}).get('base64') or qr_res.get('base64')
    if qrcode_base64:
        inst.qrcode_base64 = qrcode_base64
        inst.status = 'connecting'
        db.session.commit()

    return jsonify({
        'status': inst.status,
        'qrcode_base64': inst.qrcode_base64
    }), 200

@tenant_admin_bp.route('/whatsapp/instances/<instance_id>/logout', methods=['POST'])
@require_role(['admin', 'superadmin'])
@require_tenant
def logout_instance(instance_id):
    tenant_id = get_current_tenant_id()
    inst = WhatsAppInstance.query.filter_by(id=instance_id, tenant_id=tenant_id).first()
    if not inst:
        return jsonify({'error': 'Conexão não encontrada'}), 404

    EvolutionService.logout_instance(inst.instance_name)
    inst.status = 'disconnected'
    inst.qrcode_base64 = None
    inst.phone_number = None
    db.session.commit()
    return jsonify({'message': 'WhatsApp desconectado com sucesso!'}), 200

# ==========================================
# GESTÃO DE EQUIPE (ATENDENTES)
# ==========================================

@tenant_admin_bp.route('/users', methods=['GET'])
@require_role(['admin', 'superadmin'])
@require_tenant
def list_team_users():
    tenant_id = get_current_tenant_id()
    users = User.query.filter_by(tenant_id=tenant_id, deleted_at=None).order_by(User.name.asc()).all()
    return jsonify([u.to_dict() for u in users]), 200

@tenant_admin_bp.route('/users', methods=['POST'])
@require_role(['admin', 'superadmin'])
@require_tenant
def create_team_user():
    tenant_id = get_current_tenant_id()
    tenant = Tenant.query.get(tenant_id)
    
    # Verifica limite contratado de atendentes
    active_users = User.query.filter_by(tenant_id=tenant_id, deleted_at=None).count()
    if active_users >= tenant.max_users:
        return jsonify({'error': f'Limite de usuários atingido ({tenant.max_users}). Atualize seu plano para convidar mais atendentes.'}), 400

    data = request.get_json() or {}
    name = data.get('name')
    email = (data.get('email') or '').strip().lower()
    password = data.get('password', '123456')
    role = data.get('role', 'attendant')

    if not name or not email:
        return jsonify({'error': 'Nome e e-mail são obrigatórios'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Este e-mail já está cadastrado no sistema'}), 409

    new_user = User(
        tenant_id=tenant_id,
        name=name,
        email=email,
        role=role,
        active=True
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

@tenant_admin_bp.route('/users/<user_id>', methods=['DELETE'])
@require_role(['admin', 'superadmin'])
@require_tenant
def delete_team_user(user_id):
    tenant_id = get_current_tenant_id()
    user = User.query.filter_by(id=user_id, tenant_id=tenant_id, deleted_at=None).first()
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    # Proteção: Soft delete para não perder histórico
    user.deleted_at = datetime.utcnow()
    user.active = False
    db.session.commit()

    return jsonify({'message': 'Usuário inativado com sucesso (histórico preservado)'}), 200
