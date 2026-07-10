<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import Header from '../../../../components/Header.svelte';
    import ChatWindow from '../../../../components/ChatWindow.svelte';
    import { api } from '../../../services/api';

    const leadId = $page.params.leadId;
    
    let lead = null;
    let messages = [];
    let procedures = [];
    let loading = true;
    let error = null;

    // Manual appointment form data
    let selectedProcedureId = "";
    let appointmentTime = "";
    let schedulingMsg = "";
    let schedulingError = "";

    async function loadLeadData() {
        try {
            loading = true;
            // Fetch lead details, messages, and procedures in parallel
            const [leadsList, msgsList, procsList] = await Promise.all([
                api.getLeads(),
                api.getMessages(leadId),
                api.getProcedures()
            ]);
            
            lead = leadsList.find(l => l.id === parseInt(leadId));
            messages = msgsList;
            procedures = procsList;
            
            if (!lead) {
                error = "Paciente não encontrado no banco de dados.";
            }
        } catch (err) {
            console.error(err);
            error = "Erro ao carregar dados do paciente.";
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        loadLeadData();
        
        // Auto-poll message thread every 5 seconds for live text updates
        const interval = setInterval(async () => {
            if (lead) {
                try {
                    messages = await api.getMessages(leadId);
                } catch (e) {
                    console.error("Erro no polling de mensagens", e);
                }
            }
        }, 5000);

        return () => clearInterval(interval);
    });

    async function updateLeadProfile() {
        try {
            const res = await api.updateLead(lead.id, {
                name: lead.name,
                kanban_stage: lead.kanban_stage,
                ai_enabled: lead.ai_enabled
            });
            if (res.success) {
                lead = res.lead;
            }
        } catch (e) {
            alert("Erro ao salvar perfil");
        }
    }

    async function toggleAI() {
        lead.ai_enabled = !lead.ai_enabled;
        await updateLeadProfile();
    }

    function handleNewMessage(msg) {
        messages = [...messages, msg];
        // Outgoing manual message auto-disables AI (triggers handoff)
        lead.ai_enabled = false;
    }

    async function scheduleAppointment(e) {
        e.preventDefault();
        schedulingMsg = "";
        schedulingError = "";

        if (!selectedProcedureId || !appointmentTime) {
            schedulingError = "Escolha o procedimento e o horário.";
            return;
        }

        try {
            const res = await api.createAppointment(
                lead.id, 
                parseInt(selectedProcedureId), 
                appointmentTime
            );
            if (res.success) {
                schedulingMsg = "Consulta agendada com sucesso!";
                lead.kanban_stage = "agendado";
                selectedProcedureId = "";
                appointmentTime = "";
                // Refresh messages for the confirmation message log
                messages = await api.getMessages(leadId);
            }
        } catch (err) {
            console.error(err);
            schedulingError = "Conflito de horários ou falha no servidor.";
        }
    }
</script>

<div class="min-h-screen bg-luxury-black text-white flex flex-col h-screen">
    <Header adminMode={true} />
    
    {#if loading && !lead}
        <div class="flex-1 flex items-center justify-center">
            <span class="text-xs uppercase tracking-widest text-gray-500 animate-pulse">Carregando painel de atendimento...</span>
        </div>
    {:else if error}
        <div class="flex-1 flex flex-col items-center justify-center p-6 space-y-4">
            <p class="text-sm text-red-400">{error}</p>
            <a href="/admin/crm" class="text-xs text-luxury-gold uppercase tracking-wider underline">Voltar para o Kanban</a>
        </div>
    {:else}
        <div class="flex-1 flex overflow-hidden">
            <!-- Left Panel: Chat Transcript -->
            <div class="flex-1 p-6 flex flex-col h-full overflow-hidden">
                <div class="mb-4 flex items-center justify-between">
                    <a href="/admin/crm" class="text-xs text-gray-400 hover:text-luxury-gold flex items-center space-x-2 transition duration-200">
                        <span>←</span>
                        <span>Voltar ao Kanban</span>
                    </a>
                </div>
                
                <div class="flex-1 overflow-hidden">
                    <ChatWindow 
                        {leadId} 
                        {messages} 
                        onNewMessage={handleNewMessage} 
                    />
                </div>
            </div>

            <!-- Right Panel: Lead details and scheduler -->
            <div class="w-[380px] border-l border-luxury-border bg-luxury-dark/40 p-6 flex flex-col space-y-6 overflow-y-auto h-full">
                <!-- Section 1: Lead Profile info -->
                <div class="space-y-4 pb-6 border-b border-luxury-border/40">
                    <h2 class="font-serif text-lg text-luxury-accent">Detalhes do Paciente</h2>
                    
                    <div class="space-y-3">
                        <div>
                            <label class="text-[10px] uppercase text-gray-500 block mb-1">Nome</label>
                            <input 
                                type="text" 
                                bind:value={lead.name} 
                                on:change={updateLeadProfile}
                                class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                                placeholder="Nome não cadastrado"
                            />
                        </div>
                        
                        <div>
                            <label class="text-[10px] uppercase text-gray-500 block mb-1">Telefone WhatsApp</label>
                            <div class="w-full bg-luxury-black border border-luxury-border/30 rounded px-3 py-2 text-xs text-gray-400 font-mono">
                                +{lead.phone}
                            </div>
                        </div>

                        <div>
                            <label class="text-[10px] uppercase text-gray-500 block mb-1">Fase do Funil</label>
                            <select 
                                bind:value={lead.kanban_stage} 
                                on:change={updateLeadProfile}
                                class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                            >
                                <option value="novo_lead">Novos Contatos</option>
                                <option value="qualificado">Interessados</option>
                                <option value="agendado">Consultas Agendadas</option>
                                <option value="sem_interesse">Sem Interesse</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- Section 2: Handoff Controller -->
                <div class="space-y-3 pb-6 border-b border-luxury-border/40">
                    <h3 class="font-serif text-sm text-luxury-accent">Modo de Atendimento</h3>
                    <div class="bg-luxury-card border border-luxury-border p-4 rounded-xl flex items-center justify-between">
                        <div>
                            <p class="text-xs font-semibold {lead.ai_enabled ? 'text-emerald-400' : 'text-amber-400'}">
                                {lead.ai_enabled ? 'Robô Concierge Ativo' : 'Atendimento Humano'}
                            </p>
                            <p class="text-[10px] text-gray-400 mt-0.5">
                                {lead.ai_enabled ? 'IA responde no WhatsApp' : 'IA pausada para você digitar'}
                            </p>
                        </div>
                        <button 
                            on:click={toggleAI}
                            class="px-3 py-1.5 rounded text-[10px] font-bold uppercase tracking-wider border transition duration-200
                                {lead.ai_enabled 
                                    ? 'bg-amber-500/10 border-amber-500/30 text-amber-400 hover:bg-amber-500/20' 
                                    : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20'}"
                        >
                            {lead.ai_enabled ? 'Pausar' : 'Ativar'}
                        </button>
                    </div>
                </div>

                <!-- Section 3: Manual Scheduling form -->
                <div class="space-y-4">
                    <h3 class="font-serif text-sm text-luxury-accent">Agendar Consulta</h3>
                    <form on:submit={scheduleAppointment} class="space-y-3 bg-luxury-card/30 border border-luxury-border/50 p-4 rounded-xl">
                        <div>
                            <label class="text-[10px] uppercase text-gray-500 block mb-1">Procedimento</label>
                            <select 
                                bind:value={selectedProcedureId} 
                                class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                            >
                                <option value="">Selecione...</option>
                                {#each procedures as proc (proc.id)}
                                    <option value={proc.id}>{proc.name} (R$ {proc.price})</option>
                                {/each}
                            </select>
                        </div>

                        <div>
                            <label class="text-[10px] uppercase text-gray-500 block mb-1">Data e Hora</label>
                            <input 
                                type="datetime-local" 
                                bind:value={appointmentTime}
                                class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                            />
                        </div>

                        {#if schedulingMsg}
                            <p class="text-[11px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 p-2 rounded">{schedulingMsg}</p>
                        {/if}
                        {#if schedulingError}
                            <p class="text-[11px] text-red-400 bg-red-500/10 border border-red-500/20 p-2 rounded">{schedulingError}</p>
                        {/if}

                        <button 
                            type="submit" 
                            class="w-full bg-luxury-gold text-luxury-black font-bold py-2 px-3 rounded hover:bg-luxury-gold/90 transition duration-200 text-xs uppercase tracking-wider"
                        >
                            Confirmar Agendamento
                        </button>
                    </form>
                </div>
            </div>
        </div>
    {/if}
</div>
