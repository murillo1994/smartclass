<script>
    import LeadCard from './LeadCard.svelte';
    export let title;
    export let stage;
    export let leads = [];
    
    // Automatically re-filter leads when the database list updates
    $: filteredLeads = leads.filter(l => l.kanban_stage === stage);
</script>

<div class="flex-1 min-w-[280px] bg-luxury-dark/40 border border-luxury-border/50 rounded-2xl p-4 flex flex-col h-full max-h-[75vh]">
    <div class="flex items-center justify-between mb-4 pb-2 border-b border-luxury-border/30">
        <h3 class="font-serif tracking-wider text-luxury-gold uppercase text-xs font-semibold">{title}</h3>
        <span class="text-[10px] bg-luxury-card px-2.5 py-0.5 rounded border border-luxury-border text-gray-400 font-mono">
            {filteredLeads.length}
        </span>
    </div>
    
    <!-- Leads container with vertical scroll overflow -->
    <div class="flex-1 overflow-y-auto space-y-3 pr-1">
        {#each filteredLeads as lead (lead.id)}
            <LeadCard {lead} />
        {/each}
        
        {#if filteredLeads.length === 0}
            <div class="flex flex-col items-center justify-center py-12 text-gray-500 border border-dashed border-luxury-border/20 rounded-xl bg-luxury-card/5">
                <span class="text-[11px] uppercase tracking-wider">Sem leads</span>
            </div>
        {/if}
    </div>
</div>
