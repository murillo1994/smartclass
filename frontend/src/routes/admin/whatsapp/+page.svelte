<script>
    import { onMount, onDestroy } from 'svelte';
    import Header from '../../../components/Header.svelte';
    import { api } from '../../services/api';

    let instances = [];
    let loading = true;
    let error = '';
    let selectedQrInstance = null;
    let qrModalOpen = false;
    let newNumberModalOpen = false;
    let newInstanceName = '';
    let actionLoading = false;
    let pollInterval = null;

    async function loadInstances() {
        loading = true;
        error = '';
        try {
            instances = await api.getWhatsAppInstances();
        } catch (err) {
            error = err.message || 'Erro ao carregar instâncias';
        } finally {
            loading = false;
        }
    }

    async function handleCreateInstance() {
        if (!newInstanceName.trim()) {
            alert('Dê um nome para o canal (ex: Vendas ou Suporte).');
            return;
        }
        actionLoading = true;
        try {
            const inst = await api.createWhatsAppInstance(newInstanceName.trim());
            newNumberModalOpen = false;
            newInstanceName = '';
            await loadInstances();
            if (inst.qrcode_base64) {
                selectedQrInstance = inst;
                qrModalOpen = true;
            }
        } catch (err) {
            alert(err.message);
        } finally {
            actionLoading = false;
        }
    }

    async function showQrCode(inst) {
        actionLoading = true;
        try {
            const res = await api.getInstanceQrCode(inst.id);
            selectedQrInstance = { ...inst, qrcode_base64: res.qrcode_base64, status: res.status };
            qrModalOpen = true;
        } catch (err) {
            alert('Erro ao carregar QR Code: ' + err.message);
        } finally {
            actionLoading = false;
        }
    }

    async function handleLogoutInstance(inst) {
        if (!confirm('Deseja realmente desconectar o número "' + inst.name + '"?')) return;
        try {
            await api.logoutInstance(inst.id);
            await loadInstances();
        } catch (err) {
            alert(err.message);
        }
    }

    onMount(() => {
        loadInstances();
        pollInterval = setInterval(loadInstances, 10000);
    });

    onDestroy(() => {
        if (pollInterval) clearInterval(pollInterval);
    });
</script>

<svelte:head>
    <title>Canais WhatsApp (Multi-Número) — Evolution CRM</title>
</svelte:head>

<Header adminMode={true} />

<div class="whatsapp-page">
    <div class="header-row">
        <div>
            <h1>Canais WhatsApp (Multi-Instância)</h1>
            <p class="subtitle">Conecte múltiplos números corporativos (ex: Vendas, SAC, Pós-Venda) à sua empresa</p>
        </div>
        <button class="btn-primary" on:click={() => newNumberModalOpen = true}>
            + Conectar Novo Número
        </button>
    </div>

    {#if error}
        <div class="error-banner">{error}</div>
    {/if}

    <div class="instances-grid">
        {#if loading && instances.length === 0}
            <div class="loading-state">Carregando canais conectados...</div>
        {:else if instances.length === 0}
            <div class="empty-state">
                <h3>Nenhum número conectado</h3>
                <p>Clique em "+ Conectar Novo Número" para escanear o QR Code pelo WhatsApp do seu celular.</p>
            </div>
        {:else}
            {#each instances as inst}
                <div class="instance-card">
                    <div class="card-top">
                        <div class="status-indicator" class:connected={inst.status === 'connected'}></div>
                        <div class="instance-details">
                            <h3>{inst.name}</h3>
                            <span class="instance-slug">{inst.instance_name}</span>
                        </div>
                        <span class="status-pill {inst.status}">
                            {inst.status === 'connected' ? 'Conectado' : inst.status === 'connecting' ? 'Aguardando Leitura' : 'Desconectado'}
                        </span>
                    </div>

                    <div class="card-meta">
                        <div class="meta-item">
                            <span class="meta-label">Número:</span>
                            <span class="meta-val">{inst.phone_number || 'Não identificado'}</span>
                        </div>
                    </div>

                    <div class="card-actions">
                        {#if inst.status !== 'connected'}
                            <button class="btn-action qr-btn" on:click={() => showQrCode(inst)} disabled={actionLoading}>
                                📷 Escanear QR Code
                            </button>
                        {:else}
                            <button class="btn-action logout-btn" on:click={() => handleLogoutInstance(inst)}>
                                Desconectar
                            </button>
                        {/if}
                    </div>
                </div>
            {/each}
        {/if}
    </div>
</div>

{#if qrModalOpen && selectedQrInstance}
    <div class="modal-backdrop">
        <div class="modal-box">
            <div class="modal-head">
                <h3>Escanear QR Code — {selectedQrInstance.name}</h3>
                <button class="close-x" on:click={() => qrModalOpen = false}>&times;</button>
            </div>
            <div class="modal-body-qr">
                {#if selectedQrInstance.qrcode_base64}
                    <img 
                        src={selectedQrInstance.qrcode_base64.startsWith('data:') ? selectedQrInstance.qrcode_base64 : 'data:image/png;base64,' + selectedQrInstance.qrcode_base64} 
                        alt="QR Code WhatsApp" 
                        class="qr-image"
                    />
                    <ol class="qr-instructions">
                        <li>Abra o WhatsApp no celular</li>
                        <li>Toque em <strong>Aparelhos Conectados</strong></li>
                        <li>Toque em <strong>Conectar um aparelho</strong> e aponte para a tela</li>
                    </ol>
                {:else}
                    <div class="loading-qr">Gerando QR Code pela Evolution API...</div>
                {/if}
            </div>
        </div>
    </div>
{/if}

{#if newNumberModalOpen}
    <div class="modal-backdrop">
        <div class="modal-box">
            <div class="modal-head">
                <h3>Conectar Novo Número WhatsApp</h3>
                <button class="close-x" on:click={() => newNumberModalOpen = false}>&times;</button>
            </div>
            <form on:submit|preventDefault={handleCreateInstance} class="modal-form">
                <label>Nome do Canal / Departamento</label>
                <input 
                    type="text" 
                    bind:value={newInstanceName} 
                    placeholder="ex: Comercial Matriz ou SAC" 
                    required 
                />
                <p class="modal-hint">Ao prosseguir, uma nova instância será criada na Evolution API e o QR Code gerado.</p>
                <div class="modal-actions">
                    <button type="button" class="btn-cancel" on:click={() => newNumberModalOpen = false}>Cancelar</button>
                    <button type="submit" class="btn-submit" disabled={actionLoading}>
                        {actionLoading ? 'Criando...' : 'Gerar QR Code'}
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}

<style>
    .whatsapp-page {
        max-width: 1100px;
        margin: 0 auto;
        padding: 30px 20px;
    }
    .header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }
    .header-row h1 {
        font-size: 1.8rem;
        font-weight: 800;
        color: #2c2523;
        margin: 0;
    }
    .subtitle {
        color: #7a6f68;
        font-size: 0.95rem;
        margin-top: 4px;
    }
    .btn-primary {
        background: #483d39;
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        cursor: pointer;
    }
    .instances-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 20px;
    }
    .instance-card {
        background: white;
        border: 1px solid #e8e2de;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .card-top {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }
    .status-indicator {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #ef4444;
    }
    .status-indicator.connected {
        background: #10b981;
    }
    .instance-details {
        flex: 1;
    }
    .instance-details h3 {
        margin: 0;
        font-size: 1.1rem;
        color: #2c2523;
    }
    .instance-slug {
        font-size: 0.75rem;
        color: #8c827c;
    }
    .status-pill {
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 700;
    }
    .status-pill.connected {
        background: #dcfce7;
        color: #15803d;
    }
    .status-pill.disconnected {
        background: #fee2e2;
        color: #b91c1c;
    }
    .status-pill.connecting {
        background: #fef3c7;
        color: #b45309;
    }
    .card-meta {
        background: #fbf9f8;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 16px;
        font-size: 0.85rem;
    }
    .meta-label {
        color: #7a6f68;
    }
    .meta-val {
        font-weight: 700;
        color: #2c2523;
        margin-left: 6px;
    }
    .card-actions {
        display: flex;
        justify-content: flex-end;
    }
    .btn-action {
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        border: none;
    }
    .qr-btn {
        background: #3b82f6;
        color: white;
    }
    .logout-btn {
        background: #fee2e2;
        color: #b91c1c;
    }
    .modal-backdrop {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }
    .modal-box {
        background: white;
        width: 100%;
        max-width: 460px;
        border-radius: 12px;
        overflow: hidden;
    }
    .modal-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 20px;
        background: #fbf9f8;
        border-bottom: 1px solid #e8e2de;
    }
    .modal-head h3 {
        margin: 0;
        font-size: 1.1rem;
    }
    .close-x {
        background: none;
        border: none;
        font-size: 1.4rem;
        cursor: pointer;
    }
    .modal-body-qr {
        padding: 24px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .qr-image {
        width: 240px;
        height: 240px;
        border: 1px solid #e8e2de;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .qr-instructions {
        font-size: 0.85rem;
        color: #5c4e47;
        line-height: 1.6;
        padding-left: 20px;
    }
    .modal-form {
        padding: 20px;
    }
    .modal-form label {
        display: block;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .modal-form input {
        width: 100%;
        padding: 9px 12px;
        border: 1px solid #d5ccc7;
        border-radius: 6px;
        box-sizing: border-box;
    }
    .modal-hint {
        font-size: 0.8rem;
        color: #8c827c;
        margin: 8px 0 16px 0;
    }
    .modal-actions {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
    }
    .btn-cancel {
        background: transparent;
        border: 1px solid #d5ccc7;
        padding: 8px 14px;
        border-radius: 6px;
        cursor: pointer;
    }
    .btn-submit {
        background: #483d39;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        cursor: pointer;
    }
</style>
