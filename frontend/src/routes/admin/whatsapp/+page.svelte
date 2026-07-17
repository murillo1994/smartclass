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

    async function checkStatus() {
        try {
            const res = await api.getWhatsappStatus();
            status = res.status;
            instanceName = res.instance_name;
            isMock = res.is_mock;
            
            // If it becomes connected, we can clear the qr code
            if (status === "open") {
                qrCodeBase64 = null;
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
        } catch (err) {
            console.error(err);
            error = "Falha ao desconectar a instância.";
        } finally {
            loadingAction = false;
        }
    }

    onMount(() => {
        checkStatus();
        
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

    <div class="flex-1 flex flex-col items-center justify-center p-6">
        <div class="w-full max-w-lg bg-luxury-dark/40 border border-luxury-border/50 rounded-2xl p-8 space-y-8 backdrop-blur-md shadow-2xl relative overflow-hidden">
            <!-- Glow background decor -->
            <div class="absolute -top-24 -right-24 w-48 h-48 bg-luxury-gold/10 rounded-full blur-3xl pointer-events-none"></div>
            
            <!-- Title -->
            <div class="text-center space-y-2 relative">
                <h2 class="font-serif text-2xl text-luxury-accent">Integração WhatsApp</h2>
                <p class="text-xs text-gray-400">Conecte o número de telefone da clínica ao Robô Concierge</p>
            </div>

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
                <!-- Status Card -->
                <div class="flex items-center justify-between p-5 bg-luxury-card/20 border border-luxury-border/30 rounded-2xl relative">
                    <div class="space-y-1">
                        <span class="text-[10px] uppercase text-gray-500 block">Status da Instância</span>
                        <div class="flex items-center space-x-2">
                            <!-- Indicator Light -->
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

                <!-- Action / Details Area -->
                <div class="space-y-6">
                    {#if status === 'open'}
                        <div class="p-6 border border-emerald-500/20 bg-emerald-500/5 rounded-2xl text-center space-y-4">
                            <div class="mx-auto w-12 h-12 bg-emerald-500/10 rounded-full flex items-center justify-center text-emerald-400">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                            </div>
                            <div class="space-y-1">
                                <h4 class="text-sm font-semibold text-white">Pronto para Atendimento</h4>
                                <p class="text-xs text-gray-400">O robô está ativamente capturando mensagens e classificando contatos no funil.</p>
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
                        <!-- QR Code Reader Screen -->
                        <div class="flex flex-col items-center justify-center space-y-6">
                            <div class="bg-white p-4 rounded-2xl shadow-xl border border-luxury-border/40 relative">
                                <img src={qrCodeBase64} alt="WhatsApp QR Code" class="w-48 h-48 block" />
                                {#if loadingAction}
                                    <div class="absolute inset-0 bg-white/80 flex items-center justify-center rounded-2xl">
                                        <div class="spinner"></div>
                                    </div>
                                {/if}
                            </div>

                            <div class="w-full space-y-3 bg-luxury-card/30 border border-luxury-border/40 p-5 rounded-2xl text-left">
                                <span class="text-[10px] uppercase font-bold text-luxury-gold tracking-widest block mb-2 text-center">Instruções de Conexão</span>
                                <ol class="text-xs text-gray-400 space-y-2 list-decimal list-inside leading-relaxed">
                                    <li>Abra o <strong>WhatsApp</strong> no seu aparelho celular.</li>
                                    <li>Toque em <strong>Menu (três pontos)</strong> ou <strong>Configurações</strong>.</li>
                                    <li>Selecione <strong>Aparelhos conectados</strong> e depois <strong>Conectar um aparelho</strong>.</li>
                                    <li>Aponte a câmera para a tela para ler o QR Code acima.</li>
                                </ol>
                            </div>

                            {#if isMock}
                                <div class="w-full bg-luxury-gold/5 border border-luxury-gold/20 p-3 rounded-xl text-center">
                                    <p class="text-[10px] text-luxury-gold uppercase tracking-widest font-bold animate-pulse">Aguarde 3 segundos para simular a leitura do QR Code...</p>
                                </div>
                            {/if}
                        </div>

                    {:else}
                        <!-- Disconnected Screen / Offline -->
                        <div class="p-6 border border-luxury-border/30 bg-luxury-card/5 rounded-2xl text-center space-y-4">
                            <div class="mx-auto w-12 h-12 bg-luxury-border/30 rounded-full flex items-center justify-center text-gray-400">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="9" x2="15" y2="15"></line><line x1="15" y1="9" x2="9" y2="15"></line></svg>
                            </div>
                            <div class="space-y-1">
                                <h4 class="text-sm font-semibold text-white">Instância Inativa</h4>
                                <p class="text-xs text-gray-400">Gere um novo QR code para sincronizar a sessão de WhatsApp da empresa.</p>
                            </div>
                        </div>

                        <button 
                            on:click={generateQRCode}
                            disabled={loadingAction || status === 'offline'}
                            class="w-full bg-luxury-gold text-luxury-black font-bold py-3.5 rounded-xl hover:bg-luxury-gold/90 transition text-xs uppercase tracking-wider disabled:opacity-40"
                        >
                            {loadingAction ? 'Gerando...' : 'Gerar QR Code de Conexão'}
                        </button>
                    {/if}
                </div>
            {/if}
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
