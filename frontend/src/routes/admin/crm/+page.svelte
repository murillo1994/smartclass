<script>
    import { onMount, onDestroy } from 'svelte';
    import Header from '../../../components/Header.svelte';
    import { api } from '../../services/api';
    import { sse } from '../../services/sse';

    let funnelData = { columns: [] };
    let loading = true;
    let error = null;
    let draggedContactId = null;
    let unsubscribeSSE = null;

    async function loadKanban() {
        try {
            funnelData = await api.getKanbanFunnels();
            error = null;
        } catch (err) {
            console.error(err);
            error = 'Não foi possível sincronizar os dados com o funil Kanban.';
        } finally {
            loading = false;
        }
    }

    function handleDragStart(e, contactId) {
        draggedContactId = contactId;
        e.dataTransfer.setData('text/plain', contactId);
    }

    async function handleDrop(e, targetStageId) {
        e.preventDefault();
        const contactId = e.dataTransfer.getData('text/plain') || draggedContactId;
        if (!contactId || !targetStageId) return;

        try {
            await api.moveKanbanCard(contactId, targetStageId);
            await loadKanban();
        } catch (err) {
            alert('Erro ao mover card: ' + err.message);
        }
    }

    function handleDragOver(e) {
        e.preventDefault();
    }

    onMount(() => {
        loadKanban();
        sse.connect();
        unsubscribeSSE = sse.on('kanban.card_moved', () => loadKanban());
    });

    onDestroy(() => {
        if (unsubscribeSSE) unsubscribeSSE();
    });
</script>

<svelte:head>
    <title>Funil de Vendas Kanban — Evolution CRM</title>
</svelte:head>

<Header adminMode={true} />

<div class="kanban-page">
    <div class="kanban-header">
        <div>
            <h1>Funil de Vendas (Kanban)</h1>
            <p class="subtitle">Arraste e solte os cards entre as etapas para gerenciar as oportunidades</p>
        </div>
        <button class="btn-refresh" on:click={loadKanban} disabled={loading}>
            {loading ? 'Sincronizando...' : 'Atualizar Funil'}
        </button>
    </div>

    {#if error}
        <div class="error-banner">{error}</div>
    {/if}

    <div class="kanban-board">
        {#each funnelData.columns as col}
            <div 
                class="kanban-col" 
                on:dragover={handleDragOver}
                on:drop={(e) => handleDrop(e, col.id)}
            >
                <div class="col-header" style="border-top: 4px solid {col.color};">
                    <span class="col-title">{col.name}</span>
                    <span class="col-count">{col.contacts.length}</span>
                </div>

                <div class="cards-list">
                    {#each col.contacts as contact}
                        <div 
                            class="kanban-card" 
                            draggable="true"
                            on:dragstart={(e) => handleDragStart(e, contact.id)}
                        >
                            <div class="card-name">{contact.name}</div>
                            <div class="card-phone">{contact.phone}</div>

                            {#if contact.tags && contact.tags.length > 0}
                                <div class="card-tags">
                                    {#each contact.tags as tag}
                                        <span class="tag-pill" style="background: {tag.color}20; color: {tag.color}; border: 1px solid {tag.color}40;">
                                            {tag.name}
                                        </span>
                                    {/each}
                                </div>
                            {/if}

                            {#if contact.assigned_user_name}
                                <div class="card-assignee">👤 {contact.assigned_user_name}</div>
                            {/if}
                        </div>
                    {/each}
                    {#if col.contacts.length === 0}
                        <div class="col-empty">Nenhum card aqui</div>
                    {/if}
                </div>
            </div>
        {/each}
    </div>
</div>

<style>
    .kanban-page {
        padding: 24px 30px;
        background: #f7f5f3;
        min-height: calc(100vh - 65px);
    }
    .kanban-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }
    .kanban-header h1 {
        font-size: 1.7rem;
        font-weight: 800;
        color: #2c2523;
        margin: 0;
    }
    .subtitle {
        color: #7a6f68;
        font-size: 0.9rem;
        margin-top: 4px;
    }
    .btn-refresh {
        background: #ffffff;
        border: 1px solid #d5ccc7;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
        color: #483d39;
        cursor: pointer;
    }
    .kanban-board {
        display: flex;
        gap: 20px;
        overflow-x: auto;
        padding-bottom: 20px;
        align-items: flex-start;
    }
    .kanban-col {
        background: #ece7e2;
        width: 300px;
        flex-shrink: 0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .col-header {
        background: #ffffff;
        padding: 14px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e0d8d2;
    }
    .col-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #2c2523;
    }
    .col-count {
        background: #f0eae6;
        color: #5c4e47;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 10px;
    }
    .cards-list {
        padding: 14px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        min-height: 250px;
    }
    .kanban-card {
        background: #ffffff;
        border: 1px solid #dfd7d0;
        border-radius: 8px;
        padding: 12px 14px;
        cursor: grab;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: transform 0.15s, box-shadow 0.15s;
    }
    .kanban-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    .card-name {
        font-weight: 700;
        font-size: 0.9rem;
        color: #2c2523;
        margin-bottom: 2px;
    }
    .card-phone {
        font-size: 0.8rem;
        color: #7a6f68;
        margin-bottom: 8px;
    }
    .card-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        margin-bottom: 8px;
    }
    .tag-pill {
        font-size: 0.7rem;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
    }
    .card-assignee {
        font-size: 0.75rem;
        color: #3b82f6;
        font-weight: 600;
    }
    .col-empty {
        text-align: center;
        color: #a89f98;
        font-size: 0.8rem;
        padding: 20px 0;
    }
</style>
