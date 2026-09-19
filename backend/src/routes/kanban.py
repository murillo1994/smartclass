from flask import Blueprint, request, jsonify
from src.database import db, Funnel, FunnelStage, Contact
from src.middleware.auth import require_auth
from src.middleware.tenant import require_tenant, get_current_tenant_id
from src.services.event_dispatcher import EventDispatcher

kanban_bp = Blueprint('kanban', __name__)

@kanban_bp.route('/funnels', methods=['GET'])
@require_auth
@require_tenant
def get_funnels():
    tenant_id = get_current_tenant_id()
    funnel = Funnel.query.filter_by(tenant_id=tenant_id, is_default=True, deleted_at=None).first()
    if not funnel:
        funnel = Funnel.query.filter_by(tenant_id=tenant_id, deleted_at=None).first()
    
    if not funnel:
        return jsonify({'stages': []}), 200

    stages = FunnelStage.query.filter_by(funnel_id=funnel.id, deleted_at=None).order_by(FunnelStage.order_position.asc()).all()
    
    # Monta a estrutura de colunas com os contatos de cada etapa
    columns = []
    for stage in stages:
        contacts = Contact.query.filter_by(tenant_id=tenant_id, current_stage_id=stage.id, deleted_at=None).order_by(Contact.updated_at.desc()).all()
        columns.append({
            'id': stage.id,
            'name': stage.name,
            'color': stage.color,
            'order_position': stage.order_position,
            'contacts': [c.to_dict() for c in contacts]
        })

    return jsonify({
        'funnel_id': funnel.id,
        'funnel_name': funnel.name,
        'columns': columns
    }), 200

@kanban_bp.route('/cards/<contact_id>/move', methods=['PATCH'])
@require_auth
@require_tenant
def move_card(contact_id):
    tenant_id = get_current_tenant_id()
    contact = Contact.query.filter_by(id=contact_id, tenant_id=tenant_id, deleted_at=None).first()
    if not contact:
        return jsonify({'error': 'Contato não encontrado'}), 404

    data = request.get_json() or {}
    stage_id = data.get('stage_id')
    
    target_stage = FunnelStage.query.filter_by(id=stage_id, tenant_id=tenant_id, deleted_at=None).first()
    if not target_stage:
        return jsonify({'error': 'Etapa de destino inválida'}), 400

    old_stage_id = contact.current_stage_id
    contact.current_stage_id = target_stage.id
    db.session.commit()

    # Transmite evento em tempo real para todos os atendentes
    EventDispatcher.broadcast(tenant_id, 'kanban.card_moved', {
        'contact_id': contact.id,
        'from_stage_id': old_stage_id,
        'to_stage_id': target_stage.id,
        'contact': contact.to_dict()
    })

    return jsonify({'message': 'Card movido com sucesso', 'contact': contact.to_dict()}), 200
