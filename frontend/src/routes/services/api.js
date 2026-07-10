// HTTP client to interface SvelteKit with Flask API endpoints.
// Utilizes fallback to localhost:5000 if no dynamic environment is set.

const getBaseUrl = () => {
    if (typeof window !== 'undefined') {
        // Can be overridden at runtime
        return window.__env__?.PUBLIC_API_URL || 'http://localhost:5000/api';
    }
    return 'http://localhost:5000/api';
};

const BASE_URL = getBaseUrl();

export const api = {
    async getLeads() {
        const res = await fetch(`${BASE_URL}/leads`);
        if (!res.ok) throw new Error('Falha ao buscar leads');
        return res.json();
    },
    
    async updateLead(id, data) {
        const res = await fetch(`${BASE_URL}/leads/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Falha ao atualizar lead');
        return res.json();
    },
    
    async getMessages(leadId) {
        const res = await fetch(`${BASE_URL}/leads/${leadId}/messages`);
        if (!res.ok) throw new Error('Falha ao obter mensagens');
        return res.json();
    },
    
    async sendManualMessage(leadId, content) {
        const res = await fetch(`${BASE_URL}/leads/${leadId}/messages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content })
        });
        if (!res.ok) throw new Error('Falha ao enviar mensagem manual');
        return res.json();
    },
    
    async getAppointments() {
        const res = await fetch(`${BASE_URL}/appointments`);
        if (!res.ok) throw new Error('Falha ao obter agendamentos');
        return res.json();
    },
    
    async createAppointment(patientId, procedureId, startTime) {
        const res = await fetch(`${BASE_URL}/appointments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
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
        const res = await fetch(`${BASE_URL}/procedures`);
        if (!res.ok) throw new Error('Falha ao obter procedimentos');
        return res.json();
    }
};
