<script>
    import { onMount, afterUpdate } from 'svelte';
    import { api } from '../routes/services/api';
    
    export let leadId;
    export let messages = [];
    export let onNewMessage = () => {};
    
    let newMessage = '';
    let chatContainer;
    let sending = false;

    // Helper to snap scrollbar to bottom of chat
    function scrollToBottom() {
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }

    onMount(() => {
        scrollToBottom();
    });

    afterUpdate(() => {
        scrollToBottom();
    });

    async function handleSend(e) {
        e.preventDefault();
        if (!newMessage.trim() || sending) return;
        
        sending = true;
        const msgText = newMessage.trim();
        newMessage = '';
        
        try {
            const res = await api.sendManualMessage(leadId, msgText);
            if (res.success) {
                // Callback parent to append message
                onNewMessage(res.message);
            }
        } catch (err) {
            console.error(err);
            alert('Falha ao enviar mensagem de chat');
        } finally {
            sending = false;
        }
    }
</script>

<div class="flex flex-col h-full bg-luxury-dark/60 border border-luxury-border/50 rounded-2xl overflow-hidden">
    <!-- Chat Header -->
    <div class="px-6 py-4 border-b border-luxury-border/40 bg-luxury-card/30 flex items-center justify-between">
        <span class="text-xs font-semibold tracking-wider uppercase text-luxury-gold">Histórico de Mensagens</span>
        <span class="text-[10px] text-gray-400 bg-luxury-black px-2 py-0.5 rounded border border-luxury-border">WHATSAPP</span>
    </div>
    
    <!-- Messages Scroll Area -->
    <div bind:this={chatContainer} class="flex-1 overflow-y-auto p-6 space-y-4">
        {#each messages as msg (msg.id)}
            <div class="flex {msg.sender === 'patient' ? 'justify-start' : 'justify-end'}">
                <div class="max-w-[75%] rounded-2xl px-4 py-3 text-xs shadow-md leading-relaxed
                    {msg.sender === 'patient' 
                        ? 'bg-luxury-card border border-luxury-border/80 text-white rounded-tl-none' 
                        : msg.sender === 'ai' 
                            ? 'bg-luxury-gold/5 border border-luxury-gold/30 text-luxury-accent rounded-tr-none'
                            : 'bg-luxury-gold text-luxury-black font-medium rounded-tr-none'}"
                >
                    <div class="flex items-center space-x-2 mb-1 text-[9px] opacity-60">
                        <span class="font-bold uppercase tracking-wider">
                            {msg.sender === 'patient' ? 'Paciente' : msg.sender === 'ai' ? 'IA Concierge' : 'Atendente'}
                        </span>
                        <span>•</span>
                        <span>
                            {new Date(msg.created_at).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
                        </span>
                    </div>
                    
                    <p class="whitespace-pre-wrap">{msg.content}</p>
                </div>
            </div>
        {/each}
        
        {#if messages.length === 0}
            <div class="flex flex-col items-center justify-center h-full text-gray-500 py-12">
                <p class="text-xs uppercase tracking-widest text-gray-600">Sem histórico de mensagens</p>
            </div>
        {/if}
    </div>
    
    <!-- Input Form -->
    <form on:submit={handleSend} class="p-4 border-t border-luxury-border/40 bg-luxury-card/25 flex items-center space-x-3">
        <input 
            type="text" 
            bind:value={newMessage}
            placeholder="Digite uma mensagem... (Isso pausará o Concierge IA e ativará o Handoff)" 
            class="flex-1 bg-luxury-black border border-luxury-border/60 focus:border-luxury-gold rounded-xl px-4 py-3 text-xs text-white placeholder-gray-500 outline-none transition duration-200"
            disabled={sending}
        />
        <button 
            type="submit" 
            class="bg-luxury-gold text-luxury-black font-bold px-5 py-3 rounded-xl hover:bg-luxury-gold/90 transition duration-200 text-xs uppercase tracking-wider disabled:opacity-50"
            disabled={sending || !newMessage.trim()}
        >
            {sending ? 'Enviando...' : 'Enviar'}
        </button>
    </form>
</div>
