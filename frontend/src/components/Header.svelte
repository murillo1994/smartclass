<script>
    export let title = "UNIC CLINIC";
    export let logo = "";
    export let adminMode = false;
</script>

<header class="border-b border-luxury-border bg-luxury-dark/95 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
    <div class="flex items-center space-x-3">
        {#if logo}
            <a href="/" class="flex items-center">
                <img src={logo} alt="Unic Clinic Logo" class="h-8 md:h-10 object-contain" />
            </a>
        {:else}
            <span class="text-xl font-serif tracking-[0.2em] text-luxury-gold uppercase font-semibold">{title}</span>
        {/if}
        {#if adminMode}
            <span class="text-[10px] tracking-wider uppercase bg-luxury-gold/20 text-luxury-gold px-2 py-0.5 rounded border border-luxury-gold/30">CONCIERGE CRM</span>
        {/if}
    </div>
    
    <nav class="flex items-center space-x-6 text-xs tracking-widest uppercase">
        <a href="/" class="text-gray-400 hover:text-luxury-gold transition duration-200">Website</a>
        <a href="/admin/crm" class="px-4 py-2 rounded border border-luxury-gold/30 hover:border-luxury-gold text-luxury-gold transition duration-300 {adminMode ? 'bg-luxury-gold/10' : ''}">Painel CRM</a>
    </nav>
</header>
