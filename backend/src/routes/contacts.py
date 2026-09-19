from flask import Blueprint, request, jsonify
from src.database import db, Contact, Tag, contact_tags, FunnelStage
from src.middleware.auth import require_auth
from src.middleware.tenant import require_tenant, get_current_tenant_id

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('', methods=['GET'])
@require_auth
@require_tenant
def list_contacts():
    tenant_id = get_current_tenant_id()
    search = request.args.get('search', '').strip().lower()
    tag_id = request.args.get('tag_id')

    query = Contact.query.filter_by(tenant_id=tenant_id, deleted_at=None)

    if search:
        query = query.filter(
            db.or_(
                Contact.name.ilike(f'%{search}%'),
                Contact.phone.ilike(f'%{search}%')
            )
        )

    if tag_id:
        query = query.filter(Contact.tags.any(id=tag_id))

    contacts = query.order_by(Contact.updated_at.desc()).limit(200).all()
    return jsonify([c.to_dict() for c in contacts]), 200

@contacts_bp.route('', methods=['POST'])
@require_auth
@require_tenant
def create_contact():
    tenant_id = get_current_tenant_id()
    data = request.get_json() or {}
    phone = data.get('phone', '').strip().replace('+', '').replace('-', '').replace(' ', '')
    name = data.get('name', '').strip()

    if not phone:
        return jsonify({'error': 'Telefone é obrigatório'}), 400

    remote_jid = f'{phone}@s.whatsapp.net'
    
    # Verifica se já existe
    existing = Contact.query.filter_by(tenant_id=tenant_id, remote_jid=remote_jid, deleted_at=None).first()
    if existing:
        return jsonify({'error': 'Contato com este número já existe', 'contact': existing.to_dict()}), 409

    default_stage = FunnelStage.query.filter_by(tenant_id=tenant_id, deleted_at=None).order_by(FunnelStage.order_position.asc()).first()

    contact = Contact(
        tenant_id=tenant_id,
        remote_jid=remote_jid,
        phone=phone,
        name=name or phone,
        current_stage_id=default_stage.id if default_stage else None,
        custom_fields=data.get('custom_fields', {})
    )
    db.session.add(contact)
    db.session.commit()

    return jsonify(contact.to_dict()), 201

@contacts_bp.route('/<contact_id>', methods=['PATCH'])
@require_auth
@require_tenant
def update_contact(contact_id):
    tenant_id = get_current_tenant_id()
    contact = Contact.query.filter_by(id=contact_id, tenant_id=tenant_id, deleted_at=None).first()
    if not contact:
        return jsonify({'error': 'Contato não encontrado'}), 404

    data = request.get_json() or {}
    if 'name' in data:
        contact.name = data['name']
    if 'assigned_user_id' in data:
        contact.assigned_user_id = data['assigned_user_id']
    if 'current_stage_id' in data:
        contact.current_stage_id = data['current_stage_id']
    if 'custom_fields' in data:
        contact.custom_fields = data['custom_fields']

    db.session.commit()
    return jsonify(contact.to_dict()), 200

# ==========================================
# ETIQUETAS (TAGS)
# ==========================================

@contacts_bp.route('/tags', methods=['GET'])
@require_auth
@require_tenant
def list_tags():
    tenant_id = get_current_tenant_id()
    tags = Tag.query.filter_by(tenant_id=tenant_id).order_by(Tag.name.asc()).all()
    return jsonify([t.to_dict() for t in tags]), 200

@contacts_bp.route('/tags', methods=['POST'])
@require_auth
@require_tenant
def create_tag():
    tenant_id = get_current_tenant_id()
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    color = data.get('color', '#3b82f6')

    if not name:
        return jsonify({'error': 'Nome da etiqueta é obrigatório'}), 400

    tag = Tag(tenant_id=tenant_id, name=name, color=color)
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag.to_dict()), 201

@contacts_bp.route('/<contact_id>/tags', methods=['POST'])
@require_auth
@require_tenant
def add_tag_to_contact(contact_id):
    tenant_id = get_current_tenant_id()
    contact = Contact.query.filter_by(id=contact_id, tenant_id=tenant_id, deleted_at=None).first()
    if not contact:
        return jsonify({'error': 'Contato não encontrado'}), 404

    data = request.get_json() or {}
    tag_id = data.get('tag_id')
    tag = Tag.query.filter_by(id=tag_id, tenant_id=tenant_id).first()
    if not tag:
        return jsonify({'error': 'Etiqueta não encontrada'}), 404

    if tag not in contact.tags:
        contact.tags.append(tag)
        db.session.commit()

    return jsonify(contact.to_dict()), 200

@contacts_bp.route('/<contact_id>/tags/<tag_id>', methods=['DELETE'])
@require_auth
@require_tenant
def remove_tag_from_contact(contact_id, tag_id):
    tenant_id = get_current_tenant_id()
    contact = Contact.query.filter_by(id=contact_id, tenant_id=tenant_id, deleted_at=None).first()
    if not contact:
        return jsonify({'error': 'Contato não encontrado'}), 404

    tag = Tag.query.filter_by(id=tag_id, tenant_id=tenant_id).first()
    if tag and tag in contact.tags:
        contact.tags.remove(tag)
        db.session.commit()

    return jsonify(contact.to_dict()), 200
