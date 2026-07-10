<script>
    export let lead;
    
    // Formats clean number to +XX (XX) XXXXX-XXXX
    function formatPhone(phone) {
        if (!phone) return '';
        // If it already has formatting, return as is
        if (phone.includes('(') || phone.includes('-')) return phone;
        
        if (phone.length === 13) {
            return `+${phone.substring(0, 2)} (${phone.substring(2, 4)}) ${phone.substring(4, 9)}-${phone.substring(9)}`;
        } else if (phone.length === 11) {
            return `(${phone.substring(0, 2)}) ${phone.substring(2, 7)}-${phone.substring(7)}`;
        }
        return phone;
    }
</script>

<a href="/admin/crm/{lead.id}" class="block bg-luxury-card border border-luxury-border/60 hover:border-luxury-gold p-4 rounded-xl shadow-lg transition-all duration-300 hover:-translate-y-0.5 group">
    <div class="flex items-center justify-between mb-2">
        <span class="font-medium text-white group-hover:text-luxury-gold transition duration-200">
            {lead.name || 'Lead sem nome'}
        </span>
        
        <!-- Status indicator showing if AI chatbot or human receptionist is handling conversations -->
        <span class="text-[9px] px-2 py-0.5 rounded border tracking-wider uppercase font-semibold
            {lead.ai_enabled 
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' 
                : 'bg-amber-500/10 text-amber-400 border-amber-500/20'}"
            title={lead.ai_enabled ? 'IA está respondendo automaticamente' : 'Recepcionista assumiu o controle manual'}>
            {lead.ai_enabled ? 'IA ATIVA' : 'HUMANO'}
        </span>
    </div>
    
    <div class="text-[11px] text-gray-400 mb-3 font-mono">
        {formatPhone(lead.phone)}
    </div>
    
    {#if lead.last_message}
        <p class="text-xs text-gray-400 line-clamp-2 italic bg-luxury-black/40 p-2 rounded border border-luxury-border/30">
            "{lead.last_message.content}"
        </p>
    {:else}
        <p class="text-xs text-gray-500 italic">Nenhuma mensagem registrada</p>
    {/if}
</a>
