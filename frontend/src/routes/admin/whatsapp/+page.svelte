<script>
    import { onMount, onDestroy } from 'svelte';
    import Header from '../../../components/Header.svelte';
    import { api } from '../../services/api';

    let status = "close"; // "open", "close", "connecting", "offline"
    let instanceName = "";
    let isMock = false;
    let qrCodeBase64 = null;
    let loading = true;
    let loadingAction = false;
    let error = "";
    let statusInterval = null;

    // Robot Sandbox / Beta Settings
    let betaModeEnabled = true;
    let betaAllowedNumbers = "";
    let autoActivateAiForNewLeads = false;
    let savingSettings = false;
    let settingsSuccess = "";

    // WhatsApp Chats History
    let whatsappChats = [];
    let loadingChats = false;
    let chatsError = "";
    let selectedStage = "lead_novo";

    async function checkStatus() {
        const previousStatus = status;
        try {
            const res = await api.getWhatsappStatus();
            status = res.status;
            instanceName = res.instance_name;
            isMock = res.is_mock;
            
            if (status === "open") {
                qrCodeBase64 = null;
                // If it just transitioned to connected, automatically fetch chats
                if (previousStatus !== "open") {
                    loadChats();
                }
            }
        } catch (err) {
            console.error(err);
            status = "offline";
            error = "Não foi possível se comunicar com o servidor da Evolution API.";
        } finally {
            loading = false;
        }
    }

    async function generateQRCode() {
        loadingAction = true;
        error = "";
        try {
            const res = await api.getWhatsappConnect();
            if (res.qrcode) {
                qrCodeBase64 = res.qrcode;
                status = "connecting";
            } else if (res.status === "open") {
                status = "open";
                qrCodeBase64 = null;
                loadChats();
            }
        } catch (err) {
            console.error(err);
            error = "Falha ao gerar o QR Code. Certifique-se de que a Evolution API está ativa.";
        } finally {
            loadingAction = false;
        }
    }

    async function handleDisconnect() {
        if (!confirm("Tem certeza que deseja desconectar o WhatsApp da empresa? O Robô Concierge deixará de responder às mensagens.")) return;
        loadingAction = true;
        error = "";
        try {
            await api.logoutWhatsapp();
            status = "close";
            qrCodeBase64 = null;
            whatsappChats = [];
        } catch (err) {
            console.error(err);
            error = "Falha ao desconectar a instância.";
        } finally {
            loadingAction = false;
        }
    }

    async function loadSettings() {
        try {
            const data = await api.getSettings();
            betaModeEnabled = data.beta_mode_enabled;
            betaAllowedNumbers = data.beta_allowed_numbers;
            autoActivateAiForNewLeads = data.auto_activate_ai_for_new_leads;
        } catch (err) {
            console.error("Erro ao carregar configurações:", err);
        }
    }

    async function saveSettings() {
        savingSettings = true;
        settingsSuccess = "";
        try {
            await api.updateSettings({
                beta_mode_enabled: betaModeEnabled,
                beta_allowed_numbers: betaAllowedNumbers,
                auto_activate_ai_for_new_leads: autoActivateAiForNewLeads
            });
            settingsSuccess = "Configurações salvas!";
            setTimeout(() => { settingsSuccess = ""; }, 3000);
        } catch (err) {
            console.error("Erro ao salvar configurações:", err);
            error = "Não foi possível salvar as configurações.";
        } finally {
            savingSettings = false;
        }
    }

    async function loadChats() {
        loadingChats = true;
        chatsError = "";
        try {
            whatsappChats = await api.getWhatsappChats();
        } catch (err) {
            console.error("Erro ao carregar conversas do WhatsApp:", err);
            chatsError = "Não foi possível obter a lista de conversas do aparelho.";
        } finally {
            loadingChats = false;
        }
    }

    async function handleImport(chat) {
        try {
            await api.importWhatsappChat(chat.phone, chat.name, selectedStage);
            loadChats();
        } catch (err) {
            console.error(err);
            alert("Falha ao importar contato para o CRM.");
        }
    }

    async function handleIgnore(phone) {
        if (!confirm("Deseja ignorar esta conversa? Ela será arquivada no CRM e o robô de IA nunca enviará mensagens automáticas a este número.")) return;
        try {
            await api.ignoreWhatsappChat(phone);
            loadChats();
        } catch (err) {
            console.error(err);
            alert("Falha ao ignorar contato.");
        }
    }

    onMount(() => {
        checkStatus();
        loadSettings();
        
        // Polling loop to check status every 3 seconds
        statusInterval = setInterval(() => {
            checkStatus();
        }, 3000);
    });

    onDestroy(() => {
        if (statusInterval) {
            clearInterval(statusInterval);
        }
    });
</script>

<svelte:head>
    <title>Unic Clinic — Conexão WhatsApp</title>
</svelte:head>

<div class="min-h-screen bg-luxury-black text-white flex flex-col">
    <Header adminMode={true} />

    <div class="flex-1 w-full max-w-7xl mx-auto p-6 space-y-8">
        <!-- Dashboard Header -->
        <div class="space-y-1 relative">
            <h2 class="font-serif text-3xl text-luxury-accent">Canal WhatsApp & Central de IA</h2>
            <p class="text-xs text-gray-400">Conecte o número da clínica, configure o Sandbox de testes e gerencie conversas do celular.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Side: Status & Settings (lg:col-span-5) -->
            <div class="lg:col-span-5 space-y-8">
                
                <!-- Status Card -->
                <div class="w-full bg-luxury-dark/40 border border-luxury-border/50 rounded-2xl p-6 space-y-6 backdrop-blur-md shadow-2xl relative">
                    <h3 class="font-serif text-lg text-luxury-accent border-b border-luxury-border/30 pb-3">Status da Conexão</h3>
                    
                    {#if error}
                        <div class="bg-red-500/10 border border-red-500/20 text-red-400 p-3.5 rounded-xl text-xs text-center">
                            {error}
                        </div>
                    {/if}

                    {#if loading}
                        <div class="py-12 flex flex-col items-center justify-center space-y-3">
                            <div class="spinner"></div>
                            <span class="text-[10px] uppercase tracking-widest text-gray-500">Verificando conexão...</span>
                        </div>
                    {:else}
                        <div class="flex items-center justify-between p-5 bg-luxury-card/25 border border-luxury-border/30 rounded-xl">
                            <div class="space-y-1">
                                <span class="text-[10px] uppercase text-gray-500 block">Conectividade</span>
                                <div class="flex items-center space-x-2">
                                    <span class="w-2.5 h-2.5 rounded-full block
                                        {status === 'open' ? 'bg-emerald-400 animate-pulse shadow-[0_0_8px_rgba(52,211,153,0.5)]' : ''}
                                        {status === 'connecting' ? 'bg-amber-400 animate-pulse shadow-[0_0_8px_rgba(251,191,36,0.5)]' : ''}
                                        {status === 'close' ? 'bg-gray-500' : ''}
                                        {status === 'offline' ? 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.5)]' : ''}
                                    "></span>
                                    <strong class="text-sm font-semibold capitalize text-white">
                                        {status === 'open' ? 'Conectado' : ''}
                                        {status === 'connecting' ? 'Aguardando Leitura' : ''}
                                        {status === 'close' ? 'Desconectado' : ''}
                                        {status === 'offline' ? 'Offline' : ''}
                                    </strong>
                                </div>
                            </div>

                            <div class="text-right space-y-0.5">
                                <span class="text-[10px] uppercase text-gray-500 block">Instância</span>
                                <span class="text-xs text-white font-mono">{instanceName || 'unic_clinic'}</span>
                                {#if isMock}
                                    <span class="block text-[9px] text-luxury-gold uppercase tracking-wider font-bold mt-0.5">Modo Simulador</span>
                                {/if}
                            </div>
                        </div>

                        <!-- Actions block -->
                        <div class="space-y-4">
                            {#if status === 'open'}
                                <div class="p-5 border border-emerald-500/20 bg-emerald-500/5 rounded-xl text-center space-y-3">
                                    <div class="mx-auto w-10 h-10 bg-emerald-500/10 rounded-full flex items-center justify-center text-emerald-400">
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                                    </div>
                                    <div>
                                        <h4 class="text-xs font-semibold text-white">Canal Ativo</h4>
                                        <p class="text-[10px] text-gray-400 mt-0.5">O robô está conectado no WhatsApp de forma síncrona com o CRM.</p>
                                    </div>
                                </div>

                                <button 
                                    on:click={handleDisconnect}
                                    disabled={loadingAction}
                                    class="w-full bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20 font-bold py-3 rounded-xl transition text-xs uppercase tracking-wider"
                                >
                                    {loadingAction ? 'Desconectando...' : 'Desconectar WhatsApp'}
                                </button>

                            {:else if status === 'connecting' && qrCodeBase64}
                                <div class="flex flex-col items-center justify-center space-y-5">
                                    <div class="bg-white p-4 rounded-xl shadow-xl border border-luxury-border/40 relative">
                                        <img src={qrCodeBase64} alt="WhatsApp QR Code" class="w-44 h-44 block" />
                                        {#if loadingAction}
                                            <div class="absolute inset-0 bg-white/80 flex items-center justify-center rounded-xl">
                                                <div class="spinner"></div>
                                            </div>
                                        {/if}
                                    </div>

                                    <div class="w-full space-y-2 bg-luxury-card/30 border border-luxury-border/40 p-4 rounded-xl text-left">
                                        <span class="text-[10px] uppercase font-bold text-luxury-gold tracking-widest block mb-1.5 text-center">Como Parear</span>
                                        <ol class="text-[11px] text-gray-400 space-y-1.5 list-decimal list-inside leading-relaxed">
                                            <li>Abra o <strong>WhatsApp</strong> no seu celular.</li>
                                            <li>Toque em <strong>Aparelhos conectados</strong> e depois em <strong>Conectar aparelho</strong>.</li>
                                            <li>Aponte a câmera para ler o QR Code acima.</li>
                                        </ol>
                                    </div>

                                    {#if isMock}
                                        <div class="w-full bg-luxury-gold/5 border border-luxury-gold/20 p-2.5 rounded-lg text-center">
                                            <p class="text-[9px] text-luxury-gold uppercase tracking-widest font-bold animate-pulse">Mock: Pareamento simulado em 3 segundos...</p>
                                        </div>
                                    {/if}
                                </div>

                            {:else}
                                <div class="p-5 border border-luxury-border/30 bg-luxury-card/5 rounded-xl text-center space-y-3">
                                    <div class="mx-auto w-10 h-10 bg-luxury-border/30 rounded-full flex items-center justify-center text-gray-400">
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="9" x2="15" y2="15"></line><line x1="15" y1="9" x2="9" y2="15"></line></svg>
                                    </div>
                                    <div>
                                        <h4 class="text-xs font-semibold text-white">Sessão Inativa</h4>
                                        <p class="text-[10px] text-gray-400 mt-0.5">Nenhum aparelho conectado a esta instância da Evolution API.</p>
                                    </div>
                                </div>

                                <button 
                                    on:click={generateQRCode}
                                    disabled={loadingAction || status === 'offline'}
                                    class="w-full bg-luxury-gold text-luxury-black font-bold py-3 rounded-xl hover:bg-luxury-gold/90 transition text-xs uppercase tracking-wider disabled:opacity-40"
                                >
                                    {loadingAction ? 'Gerando...' : 'Gerar QR Code de Conexão'}
                                </button>
                            {/if}
                        </div>
                    {/if}
                </div>

                <!-- AI Settings / Sandbox Card -->
                <div class="w-full bg-luxury-dark/40 border border-luxury-border/50 rounded-2xl p-6 space-y-6 backdrop-blur-md shadow-2xl relative">
                    <h3 class="font-serif text-lg text-luxury-accent border-b border-luxury-border/30 pb-3">Sandbox e Configurações da IA</h3>
                    
                    <!-- Restricted Beta Whitelist Toggle -->
                    <div class="flex items-start justify-between p-4 bg-luxury-card/20 border border-luxury-border/30 rounded-xl space-x-4">
                        <div class="space-y-1">
                            <span class="text-xs font-semibold text-white block">Modo Beta Restrito (Sandbox)</span>
                            <p class="text-[10px] text-gray-400 leading-relaxed">
                                Se ativado, a IA responderá **apenas** aos números cadastrados na whitelist de teste. Perfeito para validação sem incomodar clientes reais.
                            </p>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer mt-1">
                            <input type="checkbox" bind:checked={betaModeEnabled} class="sr-only peer">
                            <div class="w-10 h-5.5 bg-luxury-border/40 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-gray-300 after:rounded-full after:h-4.5 after:w-4.5 after:transition-all peer-checked:bg-luxury-gold peer-checked:after:bg-luxury-black"></div>
                        </label>
                    </div>

                    <!-- Whitelist Allowed Numbers -->
                    {#if betaModeEnabled}
                        <div class="space-y-2 animate-fade-in">
                            <label class="text-[10px] uppercase text-gray-400 block font-semibold">Números Autorizados (DDI + DDD + Telefone separados por vírgula)</label>
                            <textarea 
                                bind:value={betaAllowedNumbers} 
                                placeholder="Ex: 5512999999999, 5511988888888" 
                                rows="3"
                                class="w-full bg-luxury-black/60 border border-luxury-border/40 rounded-xl p-3 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-luxury-gold transition resize-none font-mono leading-relaxed"
                            ></textarea>
                        </div>
                    {/if}

                    <!-- Auto-activate AI Toggle -->
                    <div class="flex items-start justify-between p-4 bg-luxury-card/20 border border-luxury-border/30 rounded-xl space-x-4">
                        <div class="space-y-1">
                            <span class="text-xs font-semibold text-white block">Ativação Automática para Novos Leads</span>
                            <p class="text-[10px] text-gray-400 leading-relaxed">
                                Se desativado, qualquer novo contato iniciará no modo **Humano (IA Pausada)**. O atendente terá que ativar a IA manualmente na ficha técnica.
                            </p>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer mt-1">
                            <input type="checkbox" bind:checked={autoActivateAiForNewLeads} class="sr-only peer">
                            <div class="w-10 h-5.5 bg-luxury-border/40 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-gray-300 after:rounded-full after:h-4.5 after:w-4.5 after:transition-all peer-checked:bg-luxury-gold peer-checked:after:bg-luxury-black"></div>
                        </label>
                    </div>

                    <!-- Action Buttons -->
                    <div class="space-y-2">
                        <button 
                            on:click={saveSettings}
                            disabled={savingSettings}
                            class="w-full bg-luxury-gold/10 border border-luxury-gold/30 hover:bg-luxury-gold/25 text-luxury-gold font-bold py-2.5 rounded-xl transition text-xs uppercase tracking-wider disabled:opacity-40"
                        >
                            {savingSettings ? 'Salvando...' : 'Salvar Configurações'}
                        </button>
                        {#if settingsSuccess}
                            <p class="text-[10px] text-emerald-400 text-center animate-pulse">{settingsSuccess}</p>
                        {/if}
                    </div>

                </div>

            </div>

            <!-- Right Side: Active Device Chats (History Import) (lg:col-span-7) -->
            <div class="lg:col-span-7">
                <div class="w-full bg-luxury-dark/40 border border-luxury-border/50 rounded-2xl p-6 space-y-6 backdrop-blur-md shadow-2xl relative min-h-[500px] flex flex-col">
                    
                    <div class="flex items-center justify-between border-b border-luxury-border/30 pb-3">
                        <h3 class="font-serif text-lg text-luxury-accent">Conversas no Aparelho</h3>
                        
                        {#if status === 'open'}
                            <button 
                                on:click={loadChats} 
                                disabled={loadingChats}
                                class="text-[10px] bg-luxury-gold/10 hover:bg-luxury-gold/20 text-luxury-gold border border-luxury-gold/20 font-bold py-1 px-3.5 rounded-lg transition disabled:opacity-50"
                            >
                                {loadingChats ? 'Buscando...' : 'Atualizar Conversas'}
                            </button>
                        {/if}
                    </div>

                    {#if status !== 'open'}
                        <div class="flex-1 flex flex-col items-center justify-center text-center p-8 space-y-3">
                            <div class="w-12 h-12 bg-luxury-border/20 rounded-full flex items-center justify-center text-gray-500">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                            </div>
                            <div>
                                <h4 class="text-sm font-semibold text-white">Dispositivo Desconectado</h4>
                                <p class="text-xs text-gray-400 max-w-sm mx-auto mt-1">Conecte um telefone no painel lateral esquerdo para puxar as conversas existentes no celular e importá-las para o CRM.</p>
                            </div>
                        </div>
                    {:else if loadingChats}
                        <div class="flex-1 flex flex-col items-center justify-center py-20 space-y-3">
                            <div class="spinner"></div>
                            <span class="text-[10px] uppercase tracking-widest text-gray-500">Buscando histórico do aparelho...</span>
                        </div>
                    {:else if chatsError}
                        <div class="flex-1 flex flex-col items-center justify-center p-8 text-center text-red-400 space-y-2">
                            <p class="text-xs">{chatsError}</p>
                            <button on:click={loadChats} class="text-[10px] text-luxury-gold hover:underline">Tentar novamente</button>
                        </div>
                    {:else if whatsappChats.length === 0}
                        <div class="flex-1 flex flex-col items-center justify-center text-center p-8 space-y-3">
                            <p class="text-xs text-gray-400">Nenhuma conversa recente encontrada no aparelho.</p>
                        </div>
                    {:else}
                        <!-- Chats Grid / List -->
                        <div class="space-y-4 flex-1 overflow-y-auto max-h-[550px] pr-2">
                            
                            <!-- Global stage selector for imports -->
                            <div class="flex items-center justify-between p-3.5 bg-luxury-card/25 border border-luxury-border/30 rounded-xl">
                                <span class="text-xs text-gray-300 font-semibold">Coluna padrão para novos imports:</span>
                                <select 
                                    bind:value={selectedStage}
                                    class="bg-luxury-black border border-luxury-border/40 text-xs text-white rounded-lg px-2.5 py-1 focus:outline-none focus:border-luxury-gold"
                                >
                                    <option value="lead_novo">Novo Lead</option>
                                    <option value="qualificacao">Qualificação</option>
                                    <option value="agendado">Agendado</option>
                                </select>
                            </div>

                            <div class="space-y-2.5">
                                {#each whatsappChats as chat}
                                    <div class="flex items-center justify-between p-4 bg-luxury-card/15 border border-luxury-border/20 rounded-xl hover:border-luxury-border/40 transition">
                                        
                                        <!-- Contact details -->
                                        <div class="flex items-center space-x-3.5">
                                            <!-- Initials Icon -->
                                            <div class="w-9 h-9 bg-luxury-gold/10 border border-luxury-gold/30 rounded-full flex items-center justify-center text-luxury-gold text-xs font-bold font-serif relative">
                                                {chat.name ? chat.name.charAt(0).toUpperCase() : '?'}
                                                {#if chat.unread > 0}
                                                    <span class="absolute -top-1 -right-1 bg-luxury-gold text-luxury-black text-[9px] font-bold rounded-full w-4.5 h-4.5 flex items-center justify-center">{chat.unread}</span>
                                                {/if}
                                            </div>
                                            <div class="space-y-0.5">
                                                <span class="text-xs font-semibold text-white block">{chat.name}</span>
                                                <span class="text-[10px] text-gray-400 block font-mono">+{chat.phone}</span>
                                            </div>
                                        </div>

                                        <!-- Status Badge or Action Buttons -->
                                        <div>
                                            {#if chat.already_exists}
                                                <span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-3 py-1 rounded-full text-[9px] font-bold uppercase tracking-wider">No CRM</span>
                                            {:else if chat.ignored}
                                                <span class="bg-gray-500/10 text-gray-400 border border-gray-500/30 px-3 py-1 rounded-full text-[9px] font-bold uppercase tracking-wider">Ignorado</span>
                                            {:else}
                                                <div class="flex items-center space-x-2">
                                                    <button 
                                                        on:click={() => handleImport(chat)}
                                                        class="bg-luxury-gold text-luxury-black hover:bg-luxury-gold/90 px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-wider transition"
                                                    >
                                                        Importar
                                                    </button>
                                                    <button 
                                                        on:click={() => handleIgnore(chat.phone)}
                                                        class="bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20 px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-wider transition"
                                                    >
                                                        Ignorar
                                                    </button>
                                                </div>
                                            {/if}
                                        </div>

                                    </div>
                                {/each}
                            </div>
                        </div>
                    {/if}

                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .spinner {
        width: 32px;
        height: 32px;
        border: 2px solid #ddd5c8;
        border-top-color: #9e8877;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
