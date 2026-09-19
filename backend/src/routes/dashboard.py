from flask import Blueprint, jsonify
from src.database import db, Contact, Conversation, Message, FunnelStage, User
from src.middleware.auth import require_auth
from src.middleware.tenant import require_tenant, get_current_tenant_id

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/metrics', methods=['GET'])
@require_auth
@require_tenant
def get_tenant_metrics():
    tenant_id = get_current_tenant_id()

    total_contacts = Contact.query.filter_by(tenant_id=tenant_id, deleted_at=None).count()
    open_conversations = Conversation.query.filter_by(tenant_id=tenant_id, status='open', deleted_at=None).count()
    unassigned_conversations = Conversation.query.filter(Conversation.tenant_id == tenant_id, Conversation.assigned_user_id.is_(None), Conversation.status != 'resolved', Conversation.deleted_at.is_(None)).count()
    resolved_conversations = Conversation.query.filter_by(tenant_id=tenant_id, status='resolved', deleted_at=None).count()

    # Contagem de mensagens enviadas por atendente
    attendants = User.query.filter_by(tenant_id=tenant_id, deleted_at=None).all()
    team_stats = []
    for att in attendants:
        msg_count = Message.query.filter_by(tenant_id=tenant_id, user_id=att.id, sender_type='attendant').count()
        conv_count = Conversation.query.filter_by(tenant_id=tenant_id, assigned_user_id=att.id, deleted_at=None).count()
        team_stats.append({
            'user_id': att.id,
            'name': att.name,
            'role': att.role,
            'messages_sent': msg_count,
            'active_conversations': conv_count
        })

    # Distribuição do Funil Kanban
    stages = FunnelStage.query.filter_by(tenant_id=tenant_id, deleted_at=None).order_by(FunnelStage.order_position.asc()).all()
    funnel_distribution = []
    for stg in stages:
        count = Contact.query.filter_by(tenant_id=tenant_id, current_stage_id=stg.id, deleted_at=None).count()
        funnel_distribution.append({
            'stage_id': stg.id,
            'name': stg.name,
            'color': stg.color,
            'contacts_count': count
        })

    return jsonify({
        'total_contacts': total_contacts,
        'open_conversations': open_conversations,
        'unassigned_conversations': unassigned_conversations,
        'resolved_conversations': resolved_conversations,
        'team_stats': team_stats,
        'funnel_distribution': funnel_distribution
    }), 200
