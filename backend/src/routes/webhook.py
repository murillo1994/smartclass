import logging
from datetime import datetime
from flask import Blueprint, request, jsonify
from src.database import db, Tenant, WhatsAppInstance, Contact, Conversation, Message, Funnel, FunnelStage
from src.middleware.webhook_auth import require_webhook_token
from src.services.event_dispatcher import EventDispatcher

logger = logging.getLogger(__name__)
webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/evolution', methods=['POST'])
@require_webhook_token
def handle_evolution_webhook():
    payload = request.get_json(silent=True) or {}
    event = payload.get('event')
    instance_name = payload.get('instance')

    if not instance_name:
        return jsonify({'status': 'ignored', 'reason': 'instance_missing'}), 200

    # Localiza o canal/instância no banco
    instance = WhatsAppInstance.query.filter_by(instance_name=instance_name).first()
    if not instance:
        logger.warning(f'Webhook recebido para instância desconhecida: {instance_name}')
        return jsonify({'status': 'ignored', 'reason': 'instance_not_registered'}), 200

    tenant_id = instance.tenant_id

    # 1. ATUALIZAÇÃO DE CONEXÃO
    if event == 'connection.update':
        state = payload.get('data', {}).get('state')
        if state in ['open', 'connected']:
            instance.status = 'connected'
            instance.qrcode_base64 = None
        elif state in ['close', 'disconnected']:
            instance.status = 'disconnected'
        db.session.commit()
        
        EventDispatcher.broadcast(tenant_id, 'instance.status_changed', {
            'instance_id': instance.id,
            'status': instance.status
        })
        return jsonify({'status': 'processed', 'event': event}), 200

    # 2. ATUALIZAÇÃO DE QR CODE
    if event == 'qrcode.updated':
        qrcode_b64 = payload.get('data', {}).get('qrcode', {}).get('base64')
        if qrcode_b64:
            instance.qrcode_base64 = qrcode_b64
            instance.status = 'connecting'
            db.session.commit()
            
            EventDispatcher.broadcast(tenant_id, 'instance.qrcode_updated', {
                'instance_id': instance.id,
                'qrcode': qrcode_b64
            })
        return jsonify({'status': 'processed', 'event': event}), 200

    # 3. MENSAGEM RECEBIDA OU ENVIADA (messages.upsert)
    if event in ['messages.upsert', 'messages.update']:
        data = payload.get('data', {})
        key = data.get('key', {})
        remote_jid = key.get('remoteJid', '')
        from_me = key.get('fromMe', False)
        msg_id = key.get('id')

        # Ignora mensagens de grupos ou transmissões de status
        if not remote_jid or '@g.us' in remote_jid or 'status@broadcast' in remote_jid:
            return jsonify({'status': 'ignored', 'reason': 'group_or_status'}), 200

        # Extrai telefone puro
        phone = remote_jid.split('@')[0]
        push_name = data.get('pushName') or phone

        # 3.1. Localiza ou Cria o Contato
        contact = Contact.query.filter_by(tenant_id=tenant_id, remote_jid=remote_jid, deleted_at=None).first()
        if not contact:
            # Encontra primeira etapa do funil padrão
            default_stage = FunnelStage.query.filter_by(tenant_id=tenant_id, deleted_at=None).order_by(FunnelStage.order_position.asc()).first()
            contact = Contact(
                tenant_id=tenant_id,
                remote_jid=remote_jid,
                phone=phone,
                name=push_name,
                current_stage_id=default_stage.id if default_stage else None
            )
            db.session.add(contact)
            db.session.flush()

        # 3.2. Localiza ou Cria a Conversa vinculada a esta Instância específica
        conv = Conversation.query.filter_by(
            tenant_id=tenant_id,
            instance_id=instance.id,
            contact_id=contact.id,
            deleted_at=None
        ).first()

        if not conv:
            conv = Conversation(
                tenant_id=tenant_id,
                instance_id=instance.id,
                contact_id=contact.id,
                status='open' if not from_me else 'pending',
                unread_count=1 if not from_me else 0
            )
            db.session.add(conv)
            db.session.flush()
        else:
            if not from_me:
                conv.unread_count = (conv.unread_count or 0) + 1
                if conv.status == 'resolved':
                    conv.status = 'open' # Reabre automaticamente se o cliente mandar mensagem
            conv.last_message_at = datetime.utcnow()

        # 3.3. Extrai Conteúdo e Mídia (Suporte a S3/R2 nativo)
        msg_obj = data.get('message', {})
        content = ''
        media_type = 'text'
        media_url = None

        if 'conversation' in msg_obj:
            content = msg_obj['conversation']
        elif 'extendedTextMessage' in msg_obj:
            content = msg_obj['extendedTextMessage'].get('text', '')
        elif 'audioMessage' in msg_obj:
            media_type = 'audio'
            media_url = msg_obj['audioMessage'].get('url') or data.get('mediaUrl')
            content = '[Nota de Voz]'
        elif 'imageMessage' in msg_obj:
            media_type = 'image'
            media_url = msg_obj['imageMessage'].get('url') or data.get('mediaUrl')
            content = msg_obj['imageMessage'].get('caption', '[Imagem]')
        elif 'videoMessage' in msg_obj:
            media_type = 'video'
            media_url = msg_obj['videoMessage'].get('url') or data.get('mediaUrl')
            content = msg_obj['videoMessage'].get('caption', '[Vídeo]')
        elif 'documentMessage' in msg_obj:
            media_type = 'document'
            media_url = msg_obj['documentMessage'].get('url') or data.get('mediaUrl')
            content = msg_obj['documentMessage'].get('title', '[Documento]')

        # 3.4. Cria a Mensagem
        new_msg = Message(
            tenant_id=tenant_id,
            conversation_id=conv.id,
            remote_msg_id=msg_id,
            sender_type='contact' if not from_me else 'attendant',
            content=content,
            media_type=media_type,
            media_url=media_url,
            status='delivered' if not from_me else 'sent'
        )
        db.session.add(new_msg)
        db.session.commit()

        # 3.5. Transmite evento SSE em Tempo Real para todos os atendentes conectados
        EventDispatcher.broadcast(tenant_id, 'message.created', {
            'conversation_id': conv.id,
            'message': new_msg.to_dict(),
            'contact': contact.to_dict(),
            'unread_count': conv.unread_count,
            'last_message_at': conv.last_message_at.isoformat() if conv.last_message_at else None
        })

        return jsonify({'status': 'processed', 'message_id': new_msg.id}), 200

    return jsonify({'status': 'received'}), 200
