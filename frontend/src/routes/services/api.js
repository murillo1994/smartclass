// Cliente HTTP REST para o Evolution CRM SaaS Multi-Tenant

const getBaseUrl = () => {
    if (typeof window !== 'undefined') {
        const hostname = window.location.hostname;
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:5010/api/v1';
        }
        if (hostname.endsWith('.mypaywise.cloud')) {
            return 'https://unic-api.mypaywise.cloud/api/v1';
        }
        const protocol = window.location.protocol;
        return protocol + '//' + hostname + ':5010/api/v1';
    }
    return 'http://localhost:5010/api/v1';
};

const BASE_URL = getBaseUrl();

export const getAuthToken = () => {
    if (typeof window !== 'undefined') {
        return localStorage.getItem('unic_admin_token');
    }
    return null;
};

const getHeaders = () => {
    const headers = { 'Content-Type': 'application/json' };
    const token = getAuthToken();
    if (token) {
        headers['Authorization'] = 'Bearer ' + token;
    }
    return headers;
};

export const api = {
    async login(email, password) {
        const res = await fetch(BASE_URL + '/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        });
        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.error || 'Credenciais inválidas');
        }
        const data = await res.json();
        if (typeof window !== 'undefined') {
            localStorage.setItem('unic_admin_token', data.token);
            localStorage.setItem('crm_user', JSON.stringify(data.user));
            if (data.tenant) {
                localStorage.setItem('crm_tenant', JSON.stringify(data.tenant));
            } else {
                localStorage.removeItem('crm_tenant');
            }
        }
        return data;
    },

    async getMe() {
        const res = await fetch(BASE_URL + '/auth/me', { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao autenticar usuário');
        return res.json();
    },

    logout() {
        if (typeof window !== 'undefined') {
            localStorage.removeItem('unic_admin_token');
            localStorage.removeItem('crm_user');
            localStorage.removeItem('crm_tenant');
            window.location.href = '/admin/login';
        }
    },

    async getSuperAdminMetrics() {
        const res = await fetch(BASE_URL + '/superadmin/metrics', { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao buscar métricas globais');
        return res.json();
    },

    async getSuperAdminTenants() {
        const res = await fetch(BASE_URL + '/superadmin/tenants', { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao listar empresas');
        return res.json();
    },

    async createTenant(data) {
        const res = await fetch(BASE_URL + '/superadmin/tenants', {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.error || 'Falha ao provisionar empresa');
        }
        return res.json();
    },

    async updateTenantStatus(tenantId, status) {
        const res = await fetch(BASE_URL + '/superadmin/tenants/' + tenantId + '/status', {
            method: 'PATCH',
            headers: getHeaders(),
            body: JSON.stringify({ status: status })
        });
        if (!res.ok) throw new Error('Falha ao atualizar status da empresa');
        return res.json();
    },

    async impersonateTenant(tenantId) {
        const res = await fetch(BASE_URL + '/superadmin/tenants/' + tenantId + '/impersonate', {
            method: 'POST',
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao iniciar sessão de suporte');
        const data = await res.json();
        if (typeof window !== 'undefined') {
            localStorage.setItem('unic_admin_token', data.token);
            localStorage.setItem('crm_user', JSON.stringify(data.user));
            localStorage.setItem('crm_tenant', JSON.stringify(data.tenant));
        }
        return data;
    },

    async getWhatsAppInstances() {
        const res = await fetch(BASE_URL + '/tenant/whatsapp/instances', { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao buscar instâncias de WhatsApp');
        return res.json();
    },

    async createWhatsAppInstance(name) {
        const res = await fetch(BASE_URL + '/tenant/whatsapp/instances', {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ name: name })
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.error || 'Falha ao criar canal de WhatsApp');
        }
        return res.json();
    },

    async getInstanceQrCode(instanceId) {
        const res = await fetch(BASE_URL + '/tenant/whatsapp/instances/' + instanceId + '/qrcode', { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao gerar QR Code');
        return res.json();
    },

    async logoutInstance(instanceId) {
        const res = await fetch(BASE_URL + '/tenant/whatsapp/instances/' + instanceId + '/logout', {
            method: 'POST',
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao desconectar canal');
        return res.json();
    },

    async getTeamUsers() {
        const res = await fetch(BASE_URL + '/tenant/users', { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao listar atendentes');
        return res.json();
    },

    async createTeamUser(data) {
        const res = await fetch(BASE_URL + '/tenant/users', {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.error || 'Falha ao convidar usuário');
        }
        return res.json();
    },

    async deleteTeamUser(userId) {
        const res = await fetch(BASE_URL + '/tenant/users/' + userId, {
            method: 'DELETE',
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao inativar usuário');
        return res.json();
    },

    async getInboxConversations(tab, instanceId, search) {
        let url = BASE_URL + '/crm/inbox/conversations?tab=' + (tab || 'all');
        if (instanceId) url += '&instance_id=' + instanceId;
        if (search) url += '&search=' + encodeURIComponent(search);
        const res = await fetch(url, { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao buscar conversas');
        return res.json();
    },

    async getConversationHistory(convId) {
        const res = await fetch(BASE_URL + '/crm/inbox/conversations/' + convId + '/messages', { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao carregar histórico da conversa');
        return res.json();
    },

    async sendMessage(convId, content, mediaUrl, mediaType) {
        const res = await fetch(BASE_URL + '/crm/inbox/conversations/' + convId + '/messages', {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({
                content: content,
                media_url: mediaUrl || null,
                media_type: mediaType || 'text'
            })
        });
        if (!res.ok) throw new Error('Falha ao enviar mensagem');
        return res.json();
    },

    async addInternalNote(convId, content) {
        const res = await fetch(BASE_URL + '/crm/inbox/conversations/' + convId + '/notes', {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ content: content })
        });
        if (!res.ok) throw new Error('Falha ao salvar anotação interna');
        return res.json();
    },

    async assignConversation(convId, userId) {
        const res = await fetch(BASE_URL + '/crm/inbox/conversations/' + convId + '/assign', {
            method: 'PATCH',
            headers: getHeaders(),
            body: JSON.stringify({ user_id: userId })
        });
        if (!res.ok) throw new Error('Falha ao atribuir conversa');
        return res.json();
    },

    async updateConversationStatus(convId, status) {
        const res = await fetch(BASE_URL + '/crm/inbox/conversations/' + convId + '/status', {
            method: 'PATCH',
            headers: getHeaders(),
            body: JSON.stringify({ status: status })
        });
        if (!res.ok) throw new Error('Falha ao atualizar status da conversa');
        return res.json();
    },

    async getKanbanFunnels() {
        const res = await fetch(BASE_URL + '/crm/kanban/funnels', { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao carregar funil Kanban');
        return res.json();
    },

    async moveKanbanCard(contactId, stageId) {
        const res = await fetch(BASE_URL + '/crm/kanban/cards/' + contactId + '/move', {
            method: 'PATCH',
            headers: getHeaders(),
            body: JSON.stringify({ stage_id: stageId })
        });
        if (!res.ok) throw new Error('Falha ao mover card');
        return res.json();
    },

    async getContacts(search, tagId) {
        let url = BASE_URL + '/crm/contacts?';
        if (search) url += 'search=' + encodeURIComponent(search) + '&';
        if (tagId) url += 'tag_id=' + tagId + '&';
        const res = await fetch(url, { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao carregar contatos');
        return res.json();
    },

    async getQuickReplies() {
        const res = await fetch(BASE_URL + '/crm/quick-replies', { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao carregar respostas rápidas');
        return res.json();
    },

    async createQuickReply(data) {
        const res = await fetch(BASE_URL + '/crm/quick-replies', {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Falha ao cadastrar resposta rápida');
        return res.json();
    },

    async getDashboardMetrics() {
        const res = await fetch(BASE_URL + '/crm/dashboard/metrics', { headers: getHeaders() });
        if (!res.ok) throw new Error('Falha ao buscar métricas do dashboard');
        return res.json();
    }
};
