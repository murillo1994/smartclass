// Cliente Server-Sent Events (SSE) para tempo real no SvelteKit

import { getAuthToken } from './api';

class SSEClient {
    constructor() {
        this.eventSource = null;
        this.listeners = new Map();
        this.reconnectTimeout = null;
    }

    connect() {
        if (typeof window === 'undefined') return;

        const token = getAuthToken();
        if (!token) return;

        this.disconnect();

        const streamUrl = 'http://localhost:5010/api/v1/crm/events/stream?token=' + encodeURIComponent(token);
        this.eventSource = new EventSource(streamUrl);

        this.eventSource.onopen = () => {
            console.log('SSE Conexao em tempo real estabelecida com sucesso');
        };

        this.eventSource.onerror = (err) => {
            console.warn('SSE Conexao interrompida. Tentando reconectar em 3s...', err);
            this.disconnect();
            this.reconnectTimeout = setTimeout(() => this.connect(), 3000);
        };

        const events = [
            'message.created',
            'conversation.assigned',
            'conversation.status_changed',
            'note.created',
            'kanban.card_moved',
            'instance.status_changed',
            'instance.qrcode_updated'
        ];

        events.forEach(eventName => {
            this.eventSource.addEventListener(eventName, (e) => {
                try {
                    const data = JSON.parse(e.data);
                    const cbs = this.listeners.get(eventName) || [];
                    cbs.forEach(cb => cb(data));
                } catch (err) {
                    console.error('Erro ao processar evento SSE', err);
                }
            });
        });
    }

    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);

        return () => {
            const list = this.listeners.get(event) || [];
            this.listeners.set(event, list.filter(cb => cb !== callback));
        };
    }

    disconnect() {
        if (this.reconnectTimeout) {
            clearTimeout(this.reconnectTimeout);
            this.reconnectTimeout = null;
        }
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }
}

export const sse = new SSEClient();
