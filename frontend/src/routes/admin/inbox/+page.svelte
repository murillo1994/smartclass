<script>
    import { onMount, onDestroy } from 'svelte';
    import { api } from '../../services/api';
    import { sse } from '../../services/sse';

    let currentTab = 'all'; // mine, unassigned, all, resolved
    let conversations = [];
    let selectedConversation = null;
    let messages = [];
    let teamUsers = [];
    let instances = [];
    let selectedInstanceId = '';
    let searchQuery = '';
    let messageText = '';
    let isInternalNoteMode = false;
    let loading = true;
    let sending = false;
    let quickReplies = [];
    let showQuickReplyMenu = false;
    let quickReplyFilter = '';

    // Usuário autenticado
    let currentUser = {};

    let unsubscribeSSE = [];

    async function loadInitialData() {
        loading = true;
        try {
            if (typeof window !== 'undefined') {
                currentUser = JSON.parse(localStorage.getItem('crm_user') || '{}');
            }
            const [instList, usersList, qrList] = await Promise.all([
                api.getWhatsAppInstances().catch(() => []),
                api.getTeamUsers().catch(() => []),
                api.getQuickReplies().catch(() => [])
            ]);
            instances = instList;
            teamUsers = usersList;
            quickReplies = qrList;

            await fetchConversations();
        } catch (err) {
            console.error('Erro ao carregar dados iniciais:', err);
        } finally {
            loading = false;
        }
    }

    async function fetchConversations() {
        try {
            conversations = await api.getInboxConversations(currentTab, selectedInstanceId, searchQuery);
            if (selectedConversation) {
                // Atualiza seleção se ainda existir
                const updated = conversations.find(c => c.id === selectedConversation.id);
                if (updated) selectedConversation = updated;
            } else if (conversations.length > 0 && !selectedConversation) {
                selectConversation(conversations[0]);
            }
        } catch (err) {
            console.error('Erro ao buscar conversas:', err);
        }
    }

    async function selectConversation(conv) {
        selectedConversation = conv;
        try {
            const data = await api.getConversationHistory(conv.id);
            messages = data.items;
            conv.unread_count = 0;
            // Scroll to bottom
            setTimeout(scrollToBottom, 50);
        } catch (err) {
            console.error('Erro ao abrir conversa:', err);
        }
    }

    function scrollToBottom() {
        const el = document.getElementById('chat-scroll-container');
        if (el) el.scrollTop = el.scrollHeight;
    }

    async function handleSendMessage() {
        if (!messageText.trim() || !selectedConversation) return;
        sending = true;
        const text = messageText.trim();
        messageText = '';
        showQuickReplyMenu = false;

        try {
            if (isInternalNoteMode) {
                const note = await api.addInternalNote(selectedConversation.id, text);
                messages = [...messages, note];
            } else {
                const msg = await api.sendMessage(selectedConversation.id, text);
                messages = [...messages, msg];
            }
            setTimeout(scrollToBottom, 50);
            await fetchConversations();
        } catch (err) {
            alert('Erro ao enviar mensagem: ' + err.message);
        } finally {
            sending = false;
        }
    }

    async function handleAssignUser(userId) {
        if (!selectedConversation) return;
        try {
            await api.assignConversation(selectedConversation.id, userId || null);
            await fetchConversations();
        } catch (err) {
            alert('Erro ao atribuir: ' + err.message);
        }
    }

    async function handleStatusChange(status) {
        if (!selectedConversation) return;
        try {
            await api.updateConversationStatus(selectedConversation.id, status);
            await fetchConversations();
        } catch (err) {
            alert('Erro ao mudar status: ' + err.message);
        }
    }

    function handleInputKeydown(e) {
        if (e.key === '/' && messageText === '') {
            showQuickReplyMenu = true;
        } else if (showQuickReplyMenu && e.key === 'Escape') {
            showQuickReplyMenu = false;
        } else if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    }

    function applyQuickReply(qr) {
        messageText = qr.message;
        showQuickReplyMenu = false;
    }

    onMount(() => {
        loadInitialData();

        // Conecta ao SSE em tempo real
        sse.connect();

        const unsubMsg = sse.on('message.created', (data) => {
            if (selectedConversation && data.conversation_id === selectedConversation.id) {
                messages = [...messages, data.message];
                setTimeout(scrollToBottom, 50);
            }
            fetchConversations();
        });

        const unsubNote = sse.on('note.created', (data) => {
            if (selectedConversation && data.conversation_id === selectedConversation.id) {
                messages = [...messages, data.note];
                setTimeout(scrollToBottom, 50);
            }
        });

        const unsubAssign = sse.on('conversation.assigned', () => fetchConversations());
        const unsubStatus = sse.on('conversation.status_changed', () => fetchConversations());

        unsubscribeSSE = [unsubMsg, unsubNote, unsubAssign, unsubStatus];
    });

    onDestroy(() => {
        unsubscribeSSE.forEach(u => u());
        sse.disconnect();
    });

    function formatTime(isoStr) {
        if (!isoStr) return '';
        const d = new Date(isoStr);
        return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    }
</script>

<svelte:head>
    <title>Caixa de Entrada Compartilhada — Evolution CRM</title>
</svelte:head>

<div class="inbox-container">
    <!-- COLUNA 1: LISTA DE CONVERSAS -->
    <div class="conversations-sidebar">
        <div class="sidebar-header">
            <h2>Caixa de Entrada</h2>
            <!-- Seletor de Instância (Multi-Número) -->
            {#if instances.length > 1}
                <select class="instance-select" bind:value={selectedInstanceId} on:change={fetchConversations}>
                    <option value="">Todos os Números</option>
                    {#each instances as inst}
                        <option value={inst.id}>{inst.name}</option>
                    {/each}
                </select>
            {/if}

            <!-- Campo de Busca -->
            <input 
                type="text" 
                class="search-input" 
                placeholder="Buscar contato ou número..." 
                bind:value={searchQuery}
                on:input={fetchConversations}
            />

            <!-- Abas do Inbox -->
            <div class="inbox-tabs">
                <button class="tab-btn" class:active={currentTab === 'all'} on:click={() => { currentTab = 'all'; fetchConversations(); }}>
                    Todas
                </button>
                <button class="tab-btn" class:active={currentTab === 'mine'} on:click={() => { currentTab = 'mine'; fetchConversations(); }}>
                    Minhas
                </button>
                <button class="tab-btn" class:active={currentTab === 'unassigned'} on:click={() => { currentTab = 'unassigned'; fetchConversations(); }}>
                    Fila
                </button>
                <button class="tab-btn" class:active={currentTab === 'resolved'} on:click={() => { currentTab = 'resolved'; fetchConversations(); }}>
                    Resolvidas
                </button>
            </div>
        </div>

        <!-- Lista de Conversas -->
        <div class="conversation-list">
            {#if loading && conversations.length === 0}
                <div class="empty-text">Carregando conversas...</div>
            {:else if conversations.length === 0}
                <div class="empty-text">Nenhuma conversa encontrada nesta aba.</div>
            {:else}
                {#each conversations as conv}
                    <div 
                        class="conv-card" 
                        class:selected={selectedConversation && selectedConversation.id === conv.id}
                        on:click={() => selectConversation(conv)}
                    >
                        <div class="avatar-circle">
                            {(conv.contact && conv.contact.name ? conv.contact.name[0] : 'C').toUpperCase()}
                        </div>
                        <div class="conv-info">
                            <div class="conv-top">
                                <span class="contact-name">{conv.contact ? conv.contact.name : 'Desconhecido'}</span>
                                <span class="conv-time">{formatTime(conv.last_message_at)}</span>
                            </div>
                            <div class="conv-bottom">
                                <span class="last-msg-snippet">
                                    {conv.last_message ? conv.last_message.content : 'Sem mensagens'}
                                </span>
                                {#if conv.unread_count > 0}
                                    <span class="unread-badge">{conv.unread_count}</span>
                                {/if}
                            </div>
                            <div class="conv-meta">
                                <span class="channel-tag">{conv.instance_name || 'WhatsApp'}</span>
                                {#if conv.assigned_user_name}
                                    <span class="assigned-tag">👤 {conv.assigned_user_name}</span>
                                {:else}
                                    <span class="unassigned-tag">⚠️ Não atribuída</span>
                                {/if}
                            </div>
                        </div>
                    </div>
                {/each}
            {/if}
        </div>
    </div>

    <!-- COLUNA 2: CHAT ATIVO -->
    <div class="chat-main">
        {#if selectedConversation}
            <!-- CABEÇALHO DO CHAT -->
            <div class="chat-header">
                <div class="chat-header-info">
                    <h3>{selectedConversation.contact ? selectedConversation.contact.name : ''}</h3>
                    <span class="phone-number">{selectedConversation.contact ? selectedConversation.contact.phone : ''}</span>
                </div>

                <div class="chat-header-actions">
                    <!-- Atribuir Atendente -->
                    <select 
                        class="select-action" 
                        value={selectedConversation.assigned_user_id || ''} 
                        on:change={(e) => handleAssignUser(e.target.value)}
                    >
                        <option value="">Atribuir: Ninguém</option>
                        {#each teamUsers as u}
                            <option value={u.id}>Atendente: {u.name}</option>
                        {/each}
                    </select>

                    <!-- Mudar Status -->
                    <select 
                        class="select-action" 
                        value={selectedConversation.status} 
                        on:change={(e) => handleStatusChange(e.target.value)}
                    >
                        <option value="open">Em Aberto</option>
                        <option value="pending">Pendente</option>
                        <option value="resolved">Resolvida</option>
                    </select>
                </div>
            </div>

            <!-- CORPO DAS MENSAGENS -->
            <div class="chat-messages" id="chat-scroll-container">
                {#each messages as item}
                    {#if item.is_internal_note}
                        <!-- NOTA INTERNA AMARELA -->
                        <div class="internal-note-wrapper">
                            <div class="internal-note-box">
                                <div class="note-header">
                                    <span>🔒 NOTA INTERNA • {item.author_name}</span>
                                    <span>{formatTime(item.created_at)}</span>
                                </div>
                                <div class="note-content">{item.content}</div>
                            </div>
                        </div>
                    {:else}
                        <!-- MENSAGEM WHATSAPP -->
                        <div class="message-row" class:mine={item.sender_type === 'attendant'}>
                            <div class="bubble" class:mine={item.sender_type === 'attendant'}>
                                {#if item.sender_type === 'attendant'}
                                    <div class="sender-tag">{item.sender_name || 'Você'}</div>
                                {/if}
                                <div class="bubble-text">{item.content}</div>
                                <div class="bubble-time">{formatTime(item.created_at)}</div>
                            </div>
                        </div>
                    {/if}
                {/each}
            </div>

            <!-- POPUP DE RESPOSTAS RÁPIDAS (AO DIGITAR /) -->
            {#if showQuickReplyMenu && quickReplies.length > 0}
                <div class="quick-reply-popup">
                    <div class="qr-title">Respostas Rápidas (Pressione Enter para inserir)</div>
                    {#each quickReplies as qr}
                        <div class="qr-item" on:click={() => applyQuickReply(qr)}>
                            <code>{qr.shortcut}</code> — <strong>{qr.title}</strong>
                            <div class="qr-snippet">{qr.message}</div>
                        </div>
                    {/each}
                </div>
            {/if}

            <!-- RODAPÉ DE ENVIO DE MENSAGENS -->
            <div class="chat-footer">
                <div class="mode-toggle-bar">
                    <label class="switch-label">
                        <input type="checkbox" bind:checked={isInternalNoteMode} />
                        <span class="mode-indicator" class:note-active={isInternalNoteMode}>
                            {isInternalNoteMode ? '🔒 MODO NOTA INTERNA (Amarela — invisível ao cliente)' : '💬 MENSAGEM WHATSAPP (Será entregue ao cliente)'}
                        </span>
                    </label>
                    <span class="tip-shortcut">Dica: Digite <code>/</code> para respostas rápidas</span>
                </div>

                <div class="input-row">
                    <textarea 
                        rows="2" 
                        class="chat-input" 
                        class:note-mode={isInternalNoteMode}
                        placeholder={isInternalNoteMode ? 'Escreva uma anotação privada para sua equipe...' : 'Digite sua resposta... (Pressione Enter para enviar)'}
                        bind:value={messageText}
                        on:keydown={handleInputKeydown}
                    ></textarea>
                    <button class="btn-send" class:note-send={isInternalNoteMode} on:click={handleSendMessage} disabled={sending}>
                        {sending ? '...' : (isInternalNoteMode ? 'Anotar' : 'Enviar')}
                    </button>
                </div>
            </div>
        {:else}
            <div class="no-selection">
                <div class="empty-icon">💬</div>
                <h3>Selecione uma conversa ao lado</h3>
                <p>Gerencie atendimentos simultâneos, envie mensagens ou adicione anotações internas.</p>
            </div>
        {/if}
    </div>
</div>

<style>
    .inbox-container {
        display: flex;
        height: calc(100vh - 65px);
        background: #f4f0eb;
        overflow: hidden;
    }
    .conversations-sidebar {
        width: 360px;
        background: #ffffff;
        border-right: 1px solid #e8e2de;
        display: flex;
        flex-direction: column;
    }
    .sidebar-header {
        padding: 16px;
        border-bottom: 1px solid #e8e2de;
    }
    .sidebar-header h2 {
        margin: 0 0 12px 0;
        font-size: 1.3rem;
        font-weight: 800;
        color: #2c2523;
    }
    .instance-select, .search-input {
        width: 100%;
        padding: 8px 12px;
        border: 1px solid #d5ccc7;
        border-radius: 6px;
        font-size: 0.85rem;
        margin-bottom: 10px;
        box-sizing: border-box;
    }
    .inbox-tabs {
        display: flex;
        gap: 6px;
        background: #f8f6f4;
        padding: 4px;
        border-radius: 8px;
    }
    .tab-btn {
        flex: 1;
        background: none;
        border: none;
        padding: 6px 4px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #7a6f68;
        border-radius: 6px;
        cursor: pointer;
    }
    .tab-btn.active {
        background: #ffffff;
        color: #2c2523;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .conversation-list {
        flex: 1;
        overflow-y: auto;
    }
    .conv-card {
        display: flex;
        gap: 12px;
        padding: 14px 16px;
        border-bottom: 1px solid #f2ede9;
        cursor: pointer;
        transition: background 0.15s;
    }
    .conv-card:hover {
        background: #fcfbfa;
    }
    .conv-card.selected {
        background: #f5ede6;
        border-left: 4px solid #483d39;
    }
    .avatar-circle {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: #e2dad4;
        color: #483d39;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .conv-info {
        flex: 1;
        min-width: 0;
    }
    .conv-top {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }
    .contact-name {
        font-weight: 700;
        font-size: 0.9rem;
        color: #2c2523;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .conv-time {
        font-size: 0.75rem;
        color: #9c918a;
    }
    .conv-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .last-msg-snippet {
        font-size: 0.8rem;
        color: #655953;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 200px;
    }
    .unread-badge {
        background: #10b981;
        color: white;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 10px;
    }
    .conv-meta {
        display: flex;
        gap: 6px;
        font-size: 0.7rem;
    }
    .channel-tag {
        background: #e8e2de;
        color: #483d39;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
    }
    .assigned-tag {
        color: #3b82f6;
        font-weight: 600;
    }
    .unassigned-tag {
        color: #f59e0b;
        font-weight: 600;
    }
    .chat-main {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: #efeae2;
        position: relative;
    }
    .chat-header {
        background: #ffffff;
        padding: 12px 20px;
        border-bottom: 1px solid #e8e2de;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .chat-header h3 {
        margin: 0;
        font-size: 1.1rem;
        color: #2c2523;
    }
    .phone-number {
        font-size: 0.8rem;
        color: #7a6f68;
    }
    .chat-header-actions {
        display: flex;
        gap: 10px;
    }
    .select-action {
        padding: 6px 12px;
        border: 1px solid #d5ccc7;
        border-radius: 6px;
        font-size: 0.85rem;
        background: white;
    }
    .chat-messages {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .message-row {
        display: flex;
        width: 100%;
    }
    .message-row.mine {
        justify-content: flex-end;
    }
    .bubble {
        max-width: 65%;
        padding: 10px 14px;
        border-radius: 12px;
        background: #ffffff;
        box-shadow: 0 1px 2px rgba(0,0,0,0.08);
        font-size: 0.9rem;
        color: #2c2523;
    }
    .bubble.mine {
        background: #d9fdd3;
    }
    .sender-tag {
        font-size: 0.75rem;
        font-weight: 700;
        color: #0f766e;
        margin-bottom: 4px;
    }
    .bubble-time {
        font-size: 0.7rem;
        color: #8c827c;
        text-align: right;
        margin-top: 4px;
    }
    /* NOTA INTERNA AMARELA */
    .internal-note-wrapper {
        display: flex;
        justify-content: center;
        margin: 8px 0;
    }
    .internal-note-box {
        background: #fef08a;
        border: 1px solid #facc15;
        color: #713f12;
        padding: 10px 16px;
        border-radius: 10px;
        width: 80%;
        max-width: 500px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .note-header {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        font-weight: 800;
        margin-bottom: 4px;
        letter-spacing: 0.03em;
    }
    .note-content {
        font-size: 0.9rem;
        line-height: 1.4;
    }
    .chat-footer {
        background: #ffffff;
        border-top: 1px solid #e8e2de;
        padding: 12px 20px;
    }
    .mode-toggle-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .mode-indicator {
        font-size: 0.8rem;
        font-weight: 700;
        color: #059669;
        margin-left: 6px;
    }
    .mode-indicator.note-active {
        color: #b45309;
    }
    .tip-shortcut {
        font-size: 0.75rem;
        color: #8c827c;
    }
    .input-row {
        display: flex;
        gap: 10px;
    }
    .chat-input {
        flex: 1;
        padding: 10px 14px;
        border: 1px solid #d5ccc7;
        border-radius: 8px;
        font-family: inherit;
        font-size: 0.9rem;
        resize: none;
    }
    .chat-input.note-mode {
        background: #fffbeb;
        border-color: #fcd34d;
    }
    .btn-send {
        background: #483d39;
        color: white;
        border: none;
        padding: 0 22px;
        border-radius: 8px;
        font-weight: 700;
        cursor: pointer;
    }
    .btn-send.note-send {
        background: #eab308;
        color: #451a03;
    }
    .quick-reply-popup {
        position: absolute;
        bottom: 120px;
        left: 20px;
        right: 20px;
        background: white;
        border: 1px solid #e8e2de;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        max-height: 200px;
        overflow-y: auto;
        z-index: 100;
    }
    .qr-title {
        background: #fbf9f8;
        padding: 8px 14px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #7a6f68;
        border-bottom: 1px solid #e8e2de;
    }
    .qr-item {
        padding: 10px 14px;
        border-bottom: 1px solid #f2ede9;
        cursor: pointer;
    }
    .qr-item:hover {
        background: #f5ede6;
    }
    .qr-snippet {
        font-size: 0.8rem;
        color: #7a6f68;
        margin-top: 2px;
    }
    .no-selection {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #8c827c;
    }
    .empty-icon {
        font-size: 3rem;
        margin-bottom: 12px;
    }
</style>
