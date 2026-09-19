from datetime import datetime
from flask import Blueprint, request, jsonify, g
from src.database import db, Conversation, Message, InternalNote, Contact, WhatsAppInstance
from src.middleware.auth import require_auth
from src.middleware.tenant import require_tenant, get_current_tenant_id
from src.services.evolution_service import EvolutionService
from src.services.event_dispatcher import EventDispatcher

inbox_bp = Blueprint('inbox', __name__)

@inbox_bp.route('/conversations', methods=['GET'])
@require_auth
@require_tenant
def list_conversations():
    tenant_id = get_current_tenant_id()
    tab = request.args.get('tab', 'all')
    instance_id = request.args.get('instance_id')
    search = request.args.get('search', '').strip().lower()

    query = Conversation.query.filter_by(tenant_id=tenant_id, deleted_at=None)

    # Filtro por instância/número
    if instance_id:
        query = query.filter_by(instance_id=instance_id)

    # Filtro por aba
    if tab == 'mine':
        query = query.filter_by(assigned_user_id=g.current_user.id)
    elif tab == 'unassigned':
        query = query.filter(Conversation.assigned_user_id.is_(None), Conversation.status != 'resolved')
    elif tab == 'resolved':
        query = query.filter_by(status='resolved')
    elif tab == 'all':
        query = query.filter(Conversation.status != 'resolved')

    # Busca por nome ou telefone do contato
    if search:
        query = query.join(Contact).filter(
            db.or_(
                Contact.name.ilike(f'%{search}%'),
                Contact.phone.ilike(f'%{search}%')
            )
        )

    conversations = query.order_by(Conversation.last_message_at.desc()).limit(100).all()
    return jsonify([c.to_dict(include_last_message=True) for c in conversations]), 200

@inbox_bp.route('/conversations/<conv_id>/messages', methods=['GET'])
@require_auth
@require_tenant
def get_conversation_history(conv_id):
    tenant_id = get_current_tenant_id()
    conv = Conversation.query.filter_by(id=conv_id, tenant_id=tenant_id, deleted_at=None).first()
    if not conv:
        return jsonify({'error': 'Conversa não encontrada'}), 404

    # Zera contagem de não lidas ao abrir a conversa
    if conv.unread_count > 0:
        conv.unread_count = 0
        db.session.commit()

    # Busca mensagens e notas internas
    messages = [m.to_dict() for m in conv.messages if not m.deleted_at]
    notes = [n.to_dict() for n in conv.internal_notes]

    # Mescla e ordena por data de criação
    combined = sorted(messages + notes, key=lambda x: x['created_at'])

    return jsonify({
        'conversation': conv.to_dict(include_last_message=False),
        'items': combined
    }), 200

@inbox_bp.route('/conversations/<conv_id>/messages', methods=['POST'])
@require_auth
@require_tenant
def send_message(conv_id):
    tenant_id = get_current_tenant_id()
    conv = Conversation.query.filter_by(id=conv_id, tenant_id=tenant_id, deleted_at=None).first()
    if not conv:
        return jsonify({'error': 'Conversa não encontrada'}), 404

    data = request.get_json() or {}
    content = data.get('content', '').strip()
    media_url = data.get('media_url')
    media_type = data.get('media_type', 'text')

    if not content and not media_url:
        return jsonify({'error': 'A mensagem não pode estar vazia'}), 400

    instance = conv.instance
    contact = conv.contact

    # 1. Envia via Evolution API v2
    if media_url:
        EvolutionService.send_media_message(
            instance_name=instance.instance_name,
            remote_jid=contact.remote_jid,
            media_url=media_url,
            media_type=media_type,
            caption=content
        )
    else:
        EvolutionService.send_text_message(
            instance_name=instance.instance_name,
            remote_jid=contact.remote_jid,
            text=content
        )

    # 2. Persiste no Banco de Dados
    new_msg = Message(
        tenant_id=tenant_id,
        conversation_id=conv.id,
        sender_type='attendant',
        user_id=g.current_user.id,
        content=content,
        media_type=media_type,
        media_url=media_url,
        status='sent'
    )
    conv.last_message_at = datetime.utcnow()
    conv.status = 'open'
    
    # Se a conversa não estiver atribuída a ninguém, atribui a quem respondeu
    if not conv.assigned_user_id:
        conv.assigned_user_id = g.current_user.id

    db.session.add(new_msg)
    db.session.commit()

    # 3. Transmite evento em tempo real via SSE
    msg_dict = new_msg.to_dict()
    EventDispatcher.broadcast(tenant_id, 'message.created', {
        'conversation_id': conv.id,
        'message': msg_dict,
        'last_message_at': conv.last_message_at.isoformat()
    })

    return jsonify(msg_dict), 201

@inbox_bp.route('/conversations/<conv_id>/notes', methods=['POST'])
@require_auth
@require_tenant
def add_internal_note(conv_id):
    tenant_id = get_current_tenant_id()
    conv = Conversation.query.filter_by(id=conv_id, tenant_id=tenant_id, deleted_at=None).first()
    if not conv:
        return jsonify({'error': 'Conversa não encontrada'}), 404

    data = request.get_json() or {}
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'error': 'O conteúdo da nota interna não pode ser vazio'}), 400

    note = InternalNote(
        tenant_id=tenant_id,
        conversation_id=conv.id,
        user_id=g.current_user.id,
        content=content
    )
    db.session.add(note)
    db.session.commit()

    note_dict = note.to_dict()
    EventDispatcher.broadcast(tenant_id, 'note.created', {
        'conversation_id': conv.id,
        'note': note_dict
    })

    return jsonify(note_dict), 201

@inbox_bp.route('/conversations/<conv_id>/assign', methods=['PATCH'])
@require_auth
@require_tenant
def assign_conversation(conv_id):
    tenant_id = get_current_tenant_id()
    conv = Conversation.query.filter_by(id=conv_id, tenant_id=tenant_id, deleted_at=None).first()
    if not conv:
        return jsonify({'error': 'Conversa não encontrada'}), 404

    data = request.get_json() or {}
    user_id = data.get('user_id') # Pode ser null para desatribuir

    conv.assigned_user_id = user_id
    db.session.commit()

    EventDispatcher.broadcast(tenant_id, 'conversation.assigned', {
        'conversation_id': conv.id,
        'assigned_user_id': user_id,
        'assigned_user_name': conv.assigned_user.name if conv.assigned_user else None
    })

    return jsonify({'message': 'Atribuição atualizada com sucesso', 'conversation': conv.to_dict()}), 200

@inbox_bp.route('/conversations/<conv_id>/status', methods=['PATCH'])
@require_auth
@require_tenant
def update_conversation_status(conv_id):
    tenant_id = get_current_tenant_id()
    conv = Conversation.query.filter_by(id=conv_id, tenant_id=tenant_id, deleted_at=None).first()
    if not conv:
        return jsonify({'error': 'Conversa não encontrada'}), 404

    data = request.get_json() or {}
    status = data.get('status')
    if status not in ['unassigned', 'open', 'pending', 'resolved']:
        return jsonify({'error': 'Status inválido'}), 400

    conv.status = status
    db.session.commit()

    EventDispatcher.broadcast(tenant_id, 'conversation.status_changed', {
        'conversation_id': conv.id,
        'status': status
    })

    return jsonify({'message': f'Status alterado para {status}', 'conversation': conv.to_dict()}), 200
