import time
from flask import Blueprint, request, Response, stream_with_context
from src.middleware.auth import decode_access_token
from src.services.event_dispatcher import EventDispatcher
from src.database import User

sse_bp = Blueprint('sse', __name__)

@sse_bp.route('/events/stream', methods=['GET'])
def event_stream():
    token = request.args.get('token')
    if not token:
        return {'error': 'Token não fornecido'}, 401

    payload = decode_access_token(token)
    if not payload:
        return {'error': 'Token inválido ou expirado'}, 401

    tenant_id = payload.get('tenant_id')
    if not tenant_id:
        return {'error': 'Usuário não vinculado a um tenant'}, 400

    q = EventDispatcher.subscribe(tenant_id)

    def event_generator():
        # Evento de conexão inicial bem-sucedida
        yield f'event: connected\ndata: {{\"status\": \"connected\", \"tenant_id\": \"{tenant_id}\"}}\n\n'
        
        last_ping = time.time()
        try:
            while True:
                try:
                    # Aguarda nova mensagem com timeout para permitir ping de keep-alive
                    msg = q.get(timeout=15.0)
                    yield msg
                except Exception:
                    # Timeout natural: envia comentário de keepalive para evitar timeout de proxy
                    now = time.time()
                    if now - last_ping >= 20.0:
                        yield ': ping\n\n'
                        last_ping = now
        except GeneratorExit:
            EventDispatcher.unsubscribe(tenant_id, q)

    return Response(
        stream_with_context(event_generator()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*'
        }
    )
