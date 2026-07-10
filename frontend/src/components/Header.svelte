<script>
    export let logo = "";
    export let adminMode = false;

    let menuOpen = false;

    const whatsappUrl = `https://api.whatsapp.com/send?phone=5511999999999&text=${encodeURIComponent("Olá! Vim do site da Unic Clinic e gostaria de mais informações.")}`;

    function logout() {
        if (typeof window !== 'undefined') {
            localStorage.removeItem('unic_admin_token');
            window.location.href = '/admin/login';
        }
    }
</script>

<header style="
    background: rgba(250, 248, 245, 0.95);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid #ddd5c8;
    position: sticky;
    top: 0;
    z-index: 50;
    padding: 0 2rem;
    height: 65px;
    display: flex;
    align-items: center;
    justify-content: space-between;
">
    <!-- Logo -->
    <a href="/" style="display: flex; align-items: center;">
        {#if logo}
            <img src={logo} alt="Unic Clinic" style="width: 160px; height: auto; object-fit: contain; display: block;" />
        {:else}
            <span style="font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 1.1rem; letter-spacing: 0.15em; color: #483d39; text-transform: uppercase;">
                UNIC CLINIC
            </span>
        {/if}
    </a>

    <!-- Desktop Nav -->
    {#if !adminMode}
        <nav style="display: flex; align-items: center; gap: 2.5rem;" class="desktop-nav">
            <a href="#tratamentos" style="font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6b5446; font-weight: 500; text-decoration: none; transition: color 0.2s;" 
               onmouseenter={e => e.target.style.color='#483d39'}
               onmouseleave={e => e.target.style.color='#6b5446'}>
                Tratamentos
            </a>
            <a href="#sobre" style="font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6b5446; font-weight: 500; text-decoration: none; transition: color 0.2s;"
               onmouseenter={e => e.target.style.color='#483d39'}
               onmouseleave={e => e.target.style.color='#6b5446'}>
                Sobre
            </a>
            <a href="#contato" style="font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; color: #6b5446; font-weight: 500; text-decoration: none; transition: color 0.2s;"
               onmouseenter={e => e.target.style.color='#483d39'}
               onmouseleave={e => e.target.style.color='#6b5446'}>
                Contato
            </a>
            <a href={whatsappUrl} target="_blank" rel="noopener noreferrer" style="
                font-size: 0.72rem;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                font-weight: 600;
                color: #483d39;
                text-decoration: none;
                border: 1.5px solid #483d39;
                padding: 0.55rem 1.4rem;
                border-radius: 2px;
                transition: all 0.25s;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            "
            onmouseenter={e => { e.currentTarget.style.background='#483d39'; e.currentTarget.style.color='#faf8f5'; }}
            onmouseleave={e => { e.currentTarget.style.background='transparent'; e.currentTarget.style.color='#483d39'; }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.553 4.116 1.522 5.855L.057 24l6.305-1.654A11.954 11.954 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 01-5.013-1.372l-.36-.213-3.724.976 1-3.635-.234-.374A9.818 9.818 0 0112 2.182c5.42 0 9.818 4.399 9.818 9.818 0 5.42-4.399 9.818-9.818 9.818z"/></svg>
                Agende uma consulta
            </a>
        </nav>
    {:else}
        <nav style="display: flex; align-items: center; gap: 1.5rem;">
            <a href="/" style="font-size: 0.75rem; color: #6b5446; text-decoration: none;">Website</a>
            <a href="/admin/crm" style="font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 600; color: #483d39; text-decoration: none; border: 1px solid #483d39; padding: 0.4rem 1rem; border-radius: 2px;">Painel CRM</a>
            <button on:click={logout} style="font-size: 0.75rem; color: #9c4c4c; background: none; border: none; font-weight: 600; cursor: pointer; transition: color 0.2s;"
                    onmouseenter={e => e.target.style.color='#7f3232'}
                    onmouseleave={e => e.target.style.color='#9c4c4c'}>
                Sair
            </button>
        </nav>
    {/if}
</header>

<style>
    @media (max-width: 768px) {
        .desktop-nav { display: none !important; }
    }
</style>
