<script>
    import { onMount } from 'svelte';
    import Header from '../../../components/Header.svelte';
    import KanbanColumn from '../../../components/KanbanColumn.svelte';
    import { api } from '../../services/api';

    let leads = [];
    let loading = true;
    let error = null;

    async function loadLeads() {
        try {
            leads = await api.getLeads();
            error = null;
        } catch (err) {
            console.error(err);
            error = "Não foi possível sincronizar os dados com o servidor CRM.";
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        loadLeads();
        
        // Auto-refresh lead board every 10 seconds to show active customer arrivals
        const interval = setInterval(loadLeads, 10000);
        return () => clearInterval(interval);
    });
</script>

<div class="min-h-screen bg-luxury-black text-white flex flex-col">
    <Header adminMode={true} />
    
    <main class="flex-1 p-6 flex flex-col space-y-6">
        <!-- Subheader layout -->
        <div class="flex items-center justify-between">
            <div>
                <h1 class="text-xl font-serif tracking-wide text-luxury-accent">Fluxo de Captação</h1>
                <p class="text-[11px] text-gray-400 mt-1">Supervisão de pacientes cadastrados e triagem de atendimentos</p>
            </div>
            
            <button 
                on:click={loadLeads}
                class="px-4 py-2 border border-luxury-border hover:border-luxury-gold text-[10px] uppercase tracking-wider font-bold rounded bg-luxury-card/30 hover:bg-luxury-card/60 transition duration-200"
                disabled={loading}
            >
                {loading ? 'Carregando...' : 'Atualizar Kanban'}
            </button>
        </div>

        {#if error}
            <div class="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-xl text-xs">
                {error}
            </div>
        {/if}

        {#if loading && leads.length === 0}
            <div class="flex-1 flex items-center justify-center py-24">
                <span class="text-xs uppercase tracking-widest text-gray-500 animate-pulse">Buscando leads ativos...</span>
            </div>
        {:else}
            <!-- Kanban Columns Container -->
            <div class="flex-1 flex overflow-x-auto gap-4 items-start pb-6">
                <KanbanColumn title="Novos Contatos" stage="lead_novo" {leads} />
                <KanbanColumn title="Qualificação" stage="qualificacao" {leads} />
                <KanbanColumn title="Agenda Pendente" stage="agendamento_pendente" {leads} />
                <KanbanColumn title="Agendados" stage="agendado" {leads} />
                <KanbanColumn title="Perdidos" stage="perdido" {leads} />
                <KanbanColumn title="Concluídos" stage="concluido" {leads} />
            </div>
        {/if}
    </main>
</div>
