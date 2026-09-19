from flask import Blueprint, request, jsonify
from src.database import db, QuickReply
from src.middleware.auth import require_auth
from src.middleware.tenant import require_tenant, get_current_tenant_id

quick_replies_bp = Blueprint('quick_replies', __name__)

@quick_replies_bp.route('', methods=['GET'])
@require_auth
@require_tenant
def list_quick_replies():
    tenant_id = get_current_tenant_id()
    items = QuickReply.query.filter_by(tenant_id=tenant_id).order_by(QuickReply.shortcut.asc()).all()
    return jsonify([i.to_dict() for i in items]), 200

@quick_replies_bp.route('', methods=['POST'])
@require_auth
@require_tenant
def create_quick_reply():
    tenant_id = get_current_tenant_id()
    data = request.get_json() or {}
    shortcut = (data.get('shortcut') or '').strip()
    title = data.get('title', '').strip()
    message = data.get('message', '').strip()

    if not shortcut or not message:
        return jsonify({'error': 'Atalho (ex: /pix) e mensagem são obrigatórios'}), 400

    if not shortcut.startswith('/'):
        shortcut = f'/{shortcut}'

    reply = QuickReply(
        tenant_id=tenant_id,
        shortcut=shortcut,
        title=title or shortcut,
        message=message,
        media_url=data.get('media_url')
    )
    db.session.add(reply)
    db.session.commit()
    return jsonify(reply.to_dict()), 201

@quick_replies_bp.route('/<reply_id>', methods=['DELETE'])
@require_auth
@require_tenant
def delete_quick_reply(reply_id):
    tenant_id = get_current_tenant_id()
    reply = QuickReply.query.filter_by(id=reply_id, tenant_id=tenant_id).first()
    if not reply:
        return jsonify({'error': 'Resposta rápida não encontrada'}), 404

    db.session.delete(reply)
    db.session.commit()
    return jsonify({'message': 'Resposta rápida removida com sucesso'}), 200
