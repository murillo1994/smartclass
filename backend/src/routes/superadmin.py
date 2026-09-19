from flask import Blueprint, request, jsonify
from src.database import db, Tenant, User, WhatsAppInstance, Contact, Funnel, FunnelStage
from src.middleware.auth import require_role, create_access_token

superadmin_bp = Blueprint('superadmin', __name__)

@superadmin_bp.route('/metrics', methods=['GET'])
@require_role(['superadmin'])
def get_global_metrics():
    total_tenants = Tenant.query.count()
    active_tenants = Tenant.query.filter_by(status='active').count()
    total_users = User.query.filter(User.role != 'superadmin', User.deleted_at.is_(None)).count()
    total_instances = WhatsAppInstance.query.count()
    connected_instances = WhatsAppInstance.query.filter_by(status='connected').count()
    total_contacts = Contact.query.filter(Contact.deleted_at.is_(None)).count()

    return jsonify({
        'total_tenants': total_tenants,
        'active_tenants': active_tenants,
        'total_users': total_users,
        'total_instances': total_instances,
        'connected_instances': connected_instances,
        'total_contacts': total_contacts
    }), 200

@superadmin_bp.route('/tenants', methods=['GET'])
@require_role(['superadmin'])
def list_tenants():
    tenants = Tenant.query.order_by(Tenant.created_at.desc()).all()
    results = []
    for t in tenants:
        t_dict = t.to_dict()
        t_dict['users_count'] = User.query.filter_by(tenant_id=t.id, deleted_at=None).count()
        t_dict['instances_count'] = WhatsAppInstance.query.filter_by(tenant_id=t.id).count()
        t_dict['contacts_count'] = Contact.query.filter_by(tenant_id=t.id, deleted_at=None).count()
        # Admin info
        admin_user = User.query.filter_by(tenant_id=t.id, role='admin', deleted_at=None).first()
        t_dict['admin_name'] = admin_user.name if admin_user else None
        t_dict['admin_email'] = admin_user.email if admin_user else None
        results.append(t_dict)
    return jsonify(results), 200

@superadmin_bp.route('/tenants', methods=['POST'])
@require_role(['superadmin'])
def create_tenant():
    data = request.get_json() or {}
    name = data.get('name')
    slug = (data.get('slug') or '').strip().lower()
    admin_email = (data.get('admin_email') or '').strip().lower()
    admin_name = data.get('admin_name', 'Administrador')
    admin_password = data.get('admin_password', 'admin123')
    plan_name = data.get('plan_name', 'starter')
    max_users = int(data.get('max_users', 3))
    max_instances = int(data.get('max_instances', 1))

    if not name or not slug or not admin_email:
        return jsonify({'error': 'Nome da empresa, slug e e-mail do admin são obrigatórios'}), 400

    if Tenant.query.filter_by(slug=slug).first():
        return jsonify({'error': 'Este slug de empresa já está em uso'}), 409

    if User.query.filter_by(email=admin_email).first():
        return jsonify({'error': 'Este e-mail de usuário já está cadastrado'}), 409

    # 1. Cria Workspace (Tenant)
    tenant = Tenant(
        name=name,
        slug=slug,
        document=data.get('document'),
        status='active',
        plan_name=plan_name,
        max_users=max_users,
        max_instances=max_instances
    )
    db.session.add(tenant)
    db.session.flush()

    # 2. Cria Usuário Admin Titular
    admin_user = User(
        tenant_id=tenant.id,
        name=admin_name,
        email=admin_email,
        role='admin',
        active=True
    )
    admin_user.set_password(admin_password)
    db.session.add(admin_user)

    # 3. Cria Funil Padrão e Etapas Kanban
    funnel = Funnel(
        tenant_id=tenant.id,
        name='Funil de Vendas Padrão',
        is_default=True
    )
    db.session.add(funnel)
    db.session.flush()

    default_stages = [
        FunnelStage(tenant_id=tenant.id, funnel_id=funnel.id, name='Lead Novo', color='#3b82f6', order_position=0),
        FunnelStage(tenant_id=tenant_id if (tenant_id := tenant.id) else tenant.id, funnel_id=funnel.id, name='Qualificação', color='#eab308', order_position=1),
        FunnelStage(tenant_id=tenant.id, funnel_id=funnel.id, name='Proposta Enviada', color='#8b5cf6', order_position=2),
        FunnelStage(tenant_id=tenant.id, funnel_id=funnel.id, name='Fechado / Ganho', color='#10b981', order_position=3)
    ]
    db.session.add_all(default_stages)

    # 4. Cria instância inicial do WhatsApp
    initial_instance = WhatsAppInstance(
        tenant_id=tenant.id,
        name='WhatsApp Principal',
        instance_name=f'tenant_{tenant.slug}_p1',
        status='disconnected'
    )
    db.session.add(initial_instance)

    db.session.commit()
    return jsonify({
        'message': 'Empresa provisionada com sucesso!',
        'tenant': tenant.to_dict(),
        'admin_user': admin_user.to_dict()
    }), 201

@superadmin_bp.route('/tenants/<tenant_id>/status', methods=['PATCH'])
@require_role(['superadmin'])
def update_tenant_status(tenant_id):
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        return jsonify({'error': 'Empresa não encontrada'}), 404

    data = request.get_json() or {}
    new_status = data.get('status')
    if new_status not in ['active', 'suspended', 'trial', 'cancelled']:
        return jsonify({'error': 'Status inválido'}), 400

    tenant.status = new_status
    db.session.commit()
    return jsonify({'message': f'Status da empresa atualizado para {new_status}', 'tenant': tenant.to_dict()}), 200

@superadmin_bp.route('/tenants/<tenant_id>/impersonate', methods=['POST'])
@require_role(['superadmin'])
def impersonate_tenant(tenant_id):
    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        return jsonify({'error': 'Empresa não encontrada'}), 404

    admin_user = User.query.filter_by(tenant_id=tenant.id, role='admin', deleted_at=None).first()
    if not admin_user:
        return jsonify({'error': 'Nenhum administrador encontrado nesta empresa'}), 404

    # Gera token de suporte em nome do admin da empresa
    token = create_access_token(
        user_id=admin_user.id,
        role='admin',
        tenant_id=tenant.id,
        email=admin_user.email
    )
    return jsonify({
        'token': token,
        'message': f'Sessão de suporte iniciada para {tenant.name}',
        'user': admin_user.to_dict(),
        'tenant': tenant.to_dict()
    }), 200
