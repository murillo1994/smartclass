import json
import queue
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class EventDispatcher:
    # Mapeia tenant_id -> lista de queues de clientes conectados
    _subscribers: Dict[str, List[queue.Queue]] = {}

    @classmethod
    def subscribe(cls, tenant_id: str) -> queue.Queue:
        q = queue.Queue(maxsize=100)
        if tenant_id not in cls._subscribers:
            cls._subscribers[tenant_id] = []
        cls._subscribers[tenant_id].append(q)
        logger.info(f'Novo assinante SSE conectado ao tenant {tenant_id}. Total: {len(cls._subscribers[tenant_id])}')
        return q

    @classmethod
    def unsubscribe(cls, tenant_id: str, q: queue.Queue):
        if tenant_id in cls._subscribers:
            if q in cls._subscribers[tenant_id]:
                cls._subscribers[tenant_id].remove(q)
            if not cls._subscribers[tenant_id]:
                del cls._subscribers[tenant_id]
        logger.info(f'Assinante SSE desconectado do tenant {tenant_id}')

    @classmethod
    def broadcast(cls, tenant_id: str, event: str, data: dict):
        if not tenant_id or tenant_id not in cls._subscribers:
            return

        payload = f'event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n'
        dead_queues = []
        
        for q in cls._subscribers[tenant_id]:
            try:
                q.put_nowait(payload)
            except queue.Full:
                dead_queues.append(q)
                
        for dead_q in dead_queues:
            cls.unsubscribe(tenant_id, dead_q)
