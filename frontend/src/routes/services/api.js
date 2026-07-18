// HTTP client to interface SvelteKit with Flask API endpoints.
// Utilizes fallback to localhost:5000 if no dynamic environment is set.

const getBaseUrl = () => {
    if (typeof window !== 'undefined') {
        const hostname = window.location.hostname;
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:5010/api';
        }
        if (hostname.endsWith('.mypaywise.cloud')) {
            // Secure connection when using the custom domain
            return `https://unic-api.mypaywise.cloud/api`;
        }
        // Fallback to the same IP but on port 5010 (external backend port)
        const protocol = window.location.protocol;
        return `${protocol}//${hostname}:5010/api`;
    }
    return 'http://localhost:5010/api';
};

const BASE_URL = getBaseUrl();

const getHeaders = () => {
    const headers = { 'Content-Type': 'application/json' };
    if (typeof window !== 'undefined') {
        const token = localStorage.getItem('unic_admin_token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }
    return headers;
};

export const api = {
    async login(username, password) {
        const res = await fetch(`${BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.error || 'Credenciais inválidas');
        }
        const data = await res.json();
        if (typeof window !== 'undefined') {
            localStorage.setItem('unic_admin_token', data.token);
        }
        return data;
    },

    async getLeads() {
        const res = await fetch(`${BASE_URL}/leads`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao buscar leads');
        return res.json();
    },
    
    async updateLead(id, data) {
        const res = await fetch(`${BASE_URL}/leads/${id}`, {
            method: 'PATCH',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Falha ao atualizar lead');
        return res.json();
    },
    
    async getMessages(leadId) {
        const res = await fetch(`${BASE_URL}/leads/${leadId}/messages`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao obter mensagens');
        return res.json();
    },
    
    async sendManualMessage(leadId, content) {
        const res = await fetch(`${BASE_URL}/leads/${leadId}/messages`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ content })
        });
        if (!res.ok) throw new Error('Falha ao enviar mensagem manual');
        return res.json();
    },
    
    async getAppointments() {
        const res = await fetch(`${BASE_URL}/appointments`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao obter agendamentos');
        return res.json();
    },
    
    async createAppointment(patientId, procedureId, startTime) {
        const res = await fetch(`${BASE_URL}/appointments`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({
                patient_id: patientId,
                procedure_id: procedureId,
                start_time: startTime
            })
        });
        if (!res.ok) throw new Error('Falha ao registrar agendamento');
        return res.json();
    },
    
    async getProcedures() {
        const res = await fetch(`${BASE_URL}/procedures`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao obter procedimentos');
        return res.json();
    },

    async getDoctors() {
        const res = await fetch(`${BASE_URL}/doctors`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao obter médicos');
        return res.json();
    },

    async createDoctor(name, specialty) {
        const res = await fetch(`${BASE_URL}/doctors`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ name, specialty })
        });
        if (!res.ok) throw new Error('Falha ao cadastrar médico');
        return res.json();
    },

    async deleteDoctor(id) {
        const res = await fetch(`${BASE_URL}/doctors/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao excluir médico');
        return res.json();
    },

    async getDoctorAvailability(id) {
        const res = await fetch(`${BASE_URL}/doctors/${id}/availability`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao obter agenda do médico');
        return res.json();
    },

    async updateDoctorAvailability(id, availabilities) {
        const res = await fetch(`${BASE_URL}/doctors/${id}/availability`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(availabilities)
        });
        if (!res.ok) throw new Error('Falha ao atualizar agenda do médico');
        return res.json();
    },

    async createProcedure(name, description, duration_minutes, price) {
        const res = await fetch(`${BASE_URL}/procedures`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ name, description, duration_minutes, price })
        });
        if (!res.ok) throw new Error('Falha ao cadastrar procedimento');
        return res.json();
    },

    async updateProcedure(id, data) {
        const res = await fetch(`${BASE_URL}/procedures/${id}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Falha ao atualizar procedimento');
        return res.json();
    },

    async deleteProcedure(id) {
        const res = await fetch(`${BASE_URL}/procedures/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.error || 'Falha ao excluir procedimento');
        }
        return res.json();
    },

    async getWhatsappStatus() {
        const res = await fetch(`${BASE_URL}/whatsapp/status`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao obter status do WhatsApp');
        return res.json();
    },

    async getWhatsappConnect() {
        const res = await fetch(`${BASE_URL}/whatsapp/connect`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao obter QR Code de conexão');
        return res.json();
    },

    async logoutWhatsapp() {
        const res = await fetch(`${BASE_URL}/whatsapp/logout`, {
            method: 'POST',
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao desconectar o WhatsApp');
        return res.json();
    },

    async getSettings() {
        const res = await fetch(`${BASE_URL}/settings`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao obter configurações');
        return res.json();
    },

    async updateSettings(data) {
        const res = await fetch(`${BASE_URL}/settings`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Falha ao atualizar configurações');
        return res.json();
    },

    async getWhatsappChats() {
        const res = await fetch(`${BASE_URL}/whatsapp/chats`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('Falha ao obter conversas do aparelho');
        return res.json();
    },

    async importWhatsappChat(phone, name, kanban_stage) {
        const res = await fetch(`${BASE_URL}/whatsapp/import-chat`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ phone, name, kanban_stage })
        });
        if (!res.ok) throw new Error('Falha ao importar conversa');
        return res.json();
    },

    async ignoreWhatsappChat(phone) {
        const res = await fetch(`${BASE_URL}/whatsapp/ignore-chat`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ phone })
        });
        if (!res.ok) throw new Error('Falha ao ignorar conversa');
        return res.json();
    }
};
