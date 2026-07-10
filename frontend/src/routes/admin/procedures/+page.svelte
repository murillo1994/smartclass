<script>
    import { onMount } from 'svelte';
    import Header from '../../../components/Header.svelte';
    import { api } from '../../services/api';

    let procedures = [];
    let selectedProcedure = null;
    let loading = true;
    let saving = false;
    let error = "";
    let successMsg = "";

    // Form data for creating a new procedure
    let newProcName = "";
    let newProcDesc = "";
    let newProcDuration = 30;
    let newProcPrice = "";
    let addingProcedure = false;

    // Edit form fields
    let editName = "";
    let editDesc = "";
    let editDuration = 30;
    let editPrice = "";

    async function loadProcedures() {
        try {
            loading = true;
            procedures = await api.getProcedures();
            if (procedures.length > 0 && !selectedProcedure) {
                selectProcedure(procedures[0]);
            }
        } catch (err) {
            console.error(err);
            error = "Erro ao carregar procedimentos.";
        } finally {
            loading = false;
        }
    }

    function selectProcedure(proc) {
        selectedProcedure = proc;
        editName = proc.name;
        editDesc = proc.description || "";
        editDuration = proc.duration_minutes;
        editPrice = proc.price;
        successMsg = "";
        error = "";
    }

    async function handleAddProcedure(e) {
        e.preventDefault();
        if (!newProcName || !newProcDuration || !newProcPrice) return;
        addingProcedure = true;
        error = "";
        try {
            const res = await api.createProcedure(
                newProcName.trim(),
                newProcDesc.trim(),
                parseInt(newProcDuration),
                parseFloat(newProcPrice)
            );
            if (res.success) {
                newProcName = "";
                newProcDesc = "";
                newProcDuration = 30;
                newProcPrice = "";
                await loadProcedures();
                // Select new procedure
                const newProc = procedures.find(p => p.id === res.procedure.id);
                if (newProc) selectProcedure(newProc);
            }
        } catch (err) {
            console.error(err);
            error = "Falha ao cadastrar procedimento.";
        } finally {
            addingProcedure = false;
        }
    }

    async function handleUpdateProcedure(e) {
        e.preventDefault();
        if (!selectedProcedure || !editName || !editDuration || !editPrice) return;
        saving = true;
        successMsg = "";
        error = "";
        try {
            const payload = {
                name: editName.trim(),
                description: editDesc.trim(),
                duration_minutes: parseInt(editDuration),
                price: parseFloat(editPrice)
            };
            const res = await api.updateProcedure(selectedProcedure.id, payload);
            if (res.success) {
                successMsg = "Procedimento atualizado com sucesso!";
                await loadProcedures();
                // Maintain selected procedure state
                const updated = procedures.find(p => p.id === selectedProcedure.id);
                if (updated) selectProcedure(updated);
            }
        } catch (err) {
            console.error(err);
            error = "Erro ao atualizar dados do procedimento.";
        } finally {
            saving = false;
        }
    }

    async function handleDeleteProcedure(procId) {
        if (!confirm("Tem certeza que deseja excluir este procedimento?")) return;
        error = "";
        successMsg = "";
        try {
            await api.deleteProcedure(procId);
            if (selectedProcedure && selectedProcedure.id === procId) {
                selectedProcedure = null;
            }
            await loadProcedures();
            successMsg = "Procedimento removido com sucesso.";
        } catch (err) {
            console.error(err);
            error = err.message || "Erro ao excluir procedimento.";
        }
    }

    onMount(() => {
        loadProcedures();
    });
</script>

<svelte:head>
    <title>Unic Clinic — Procedimentos e Valores</title>
</svelte:head>

<div class="min-h-screen bg-luxury-black text-white flex flex-col h-screen">
    <Header adminMode={true} />

    {#if loading}
        <div class="flex-1 flex items-center justify-center">
            <span class="text-xs uppercase tracking-widest text-gray-500 animate-pulse">Carregando catálogo...</span>
        </div>
    {:else}
        <div class="flex-1 flex overflow-hidden main-layout">
            <!-- Left Panel: Procedures List & Create Form -->
            <div class="w-[360px] border-r border-luxury-border/40 p-6 flex flex-col space-y-6 h-full overflow-y-auto left-panel">
                <div>
                    <h2 class="font-serif text-lg text-luxury-accent">Catálogo</h2>
                    <p class="text-[10px] text-gray-400 mt-1">Procedimentos ativos e valores cobrados</p>
                </div>

                {#if error && !selectedProcedure}
                    <div class="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-lg text-xs">
                        {error}
                    </div>
                {/if}

                <!-- Add Procedure Form -->
                <form on:submit={handleAddProcedure} class="bg-luxury-card/30 border border-luxury-border/50 p-4 rounded-xl space-y-3">
                    <span class="text-[10px] uppercase font-bold text-luxury-gold tracking-wider block">Novo Procedimento</span>
                    
                    <div class="space-y-2">
                        <input 
                            type="text" 
                            bind:value={newProcName} 
                            placeholder="Nome do procedimento" 
                            required
                            disabled={addingProcedure}
                            class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                        />
                        <textarea 
                            bind:value={newProcDesc} 
                            placeholder="Descrição breve do procedimento"
                            disabled={addingProcedure}
                            rows="2"
                            class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none resize-none"
                        ></textarea>
                        
                        <div class="flex space-x-2">
                            <div class="flex-1">
                                <label class="text-[9px] uppercase text-gray-500 block mb-1">Duração (min)</label>
                                <input 
                                    type="number" 
                                    bind:value={newProcDuration} 
                                    placeholder="30"
                                    min="5"
                                    required
                                    disabled={addingProcedure}
                                    class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                                />
                            </div>
                            <div class="flex-1">
                                <label class="text-[9px] uppercase text-gray-500 block mb-1">Preço (R$)</label>
                                <input 
                                    type="number" 
                                    step="0.01"
                                    bind:value={newProcPrice} 
                                    placeholder="1200.00" 
                                    required
                                    disabled={addingProcedure}
                                    class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                                />
                            </div>
                        </div>
                    </div>

                    <button 
                        type="submit" 
                        disabled={addingProcedure}
                        class="w-full bg-luxury-gold text-luxury-black font-bold py-2 rounded hover:bg-luxury-gold/90 transition text-xs uppercase tracking-wider"
                    >
                        {addingProcedure ? 'Cadastrando...' : 'Cadastrar'}
                    </button>
                </form>

                <!-- Procedures list -->
                <div class="flex-1 space-y-2">
                    <span class="text-[10px] uppercase font-bold text-gray-500 tracking-wider block">Tratamentos ({procedures.length})</span>
                    
                    {#each procedures as proc (proc.id)}
                        <button 
                            on:click={() => selectProcedure(proc)}
                            class="w-full flex items-center justify-between p-3.5 rounded-xl border text-left transition-all duration-200 group
                                {selectedProcedure && selectedProcedure.id === proc.id 
                                    ? 'bg-luxury-card border-luxury-gold' 
                                    : 'bg-luxury-card/10 border-luxury-border/40 hover:border-luxury-border hover:bg-luxury-card/20'}"
                        >
                            <div class="flex-1 mr-2">
                                <p class="text-xs font-semibold text-white group-hover:text-luxury-gold transition duration-200">{proc.name}</p>
                                <p class="text-[10px] text-gray-400 mt-0.5">{proc.duration_minutes} min • R$ {parseFloat(proc.price).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</p>
                            </div>
                            <button 
                                on:click|stopPropagation={() => handleDeleteProcedure(proc.id)}
                                class="text-gray-500 hover:text-red-400 p-1 rounded transition duration-200"
                                title="Excluir procedimento"
                            >
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                            </button>
                        </button>
                    {/each}

                    {#if procedures.length === 0}
                        <div class="text-center py-8 text-gray-500 border border-dashed border-luxury-border/20 rounded-xl">
                            <span class="text-[11px]">Nenhum procedimento cadastrado.</span>
                        </div>
                    {/if}
                </div>
            </div>

            <!-- Right Panel: Edit Selected Procedure -->
            <div class="flex-1 p-6 flex flex-col h-full overflow-y-auto right-panel">
                {#if selectedProcedure}
                    <div class="mb-6 flex justify-between items-start">
                        <div>
                            <h2 class="font-serif text-lg text-luxury-accent">Detalhes do Tratamento</h2>
                            <p class="text-[10px] text-gray-400 mt-1">Configure o valor comercial e tempo de sala para: <strong class="text-luxury-gold">{selectedProcedure.name}</strong></p>
                        </div>
                    </div>

                    {#if successMsg}
                        <div class="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 p-3 rounded-lg text-xs mb-4">
                            {successMsg}
                        </div>
                    {/if}
                    {#if error && selectedProcedure}
                        <div class="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-lg text-xs mb-4">
                            {error}
                        </div>
                    {/if}

                    <form on:submit={handleUpdateProcedure} class="space-y-4 bg-luxury-dark/40 border border-luxury-border/50 p-6 rounded-2xl">
                        <div class="space-y-2">
                            <div>
                                <label class="text-[10px] uppercase text-gray-500 block mb-1">Nome do Procedimento</label>
                                <input 
                                    type="text" 
                                    bind:value={editName}
                                    required
                                    disabled={saving}
                                    class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                                />
                            </div>

                            <div>
                                <label class="text-[10px] uppercase text-gray-500 block mb-1">Descrição</label>
                                <textarea 
                                    bind:value={editDesc}
                                    rows="4"
                                    disabled={saving}
                                    class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none resize-none"
                                ></textarea>
                            </div>

                            <div class="flex space-x-4">
                                <div class="flex-1">
                                    <label class="text-[10px] uppercase text-gray-500 block mb-1">Duração (minutos)</label>
                                    <input 
                                        type="number" 
                                        bind:value={editDuration}
                                        min="5"
                                        required
                                        disabled={saving}
                                        class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                                    />
                                </div>
                                <div class="flex-1">
                                    <label class="text-[10px] uppercase text-gray-500 block mb-1">Preço Cobrado (R$)</label>
                                    <input 
                                        type="number" 
                                        step="0.01"
                                        bind:value={editPrice}
                                        required
                                        disabled={saving}
                                        class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                                    />
                                </div>
                            </div>
                        </div>

                        <button 
                            type="submit" 
                            disabled={saving}
                            class="bg-luxury-gold text-luxury-black font-bold py-2 px-6 rounded hover:bg-luxury-gold/90 transition text-xs uppercase tracking-wider"
                        >
                            {saving ? 'Salvando...' : 'Salvar Alterações'}
                        </button>
                    </form>
                {:else}
                    <div class="flex-1 flex flex-col items-center justify-center text-gray-500 py-24 space-y-2">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="opacity-40"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                        <span class="text-xs uppercase tracking-widest opacity-60">Selecione um procedimento para editar seus detalhes</span>
                    </div>
                {/if}
            </div>
        </div>
    {/if}
</div>

<style>
    .main-layout {
        display: flex;
        flex: 1;
        overflow: hidden;
    }

    .left-panel {
        height: 100%;
        overflow-y: auto;
    }

    .right-panel {
        height: 100%;
        overflow-y: auto;
    }

    @media (max-width: 768px) {
        .main-layout {
            flex-direction: column !important;
            overflow-y: auto !important;
            height: auto !important;
        }

        .left-panel {
            width: 100% !important;
            border-right: none !important;
            border-bottom: 1px solid rgba(42, 50, 61, 0.2) !important;
            height: auto !important;
            flex: none !important;
            padding: 1rem !important;
        }

        .right-panel {
            width: 100% !important;
            height: auto !important;
            flex: none !important;
            padding: 1rem !important;
        }
    }
</style>
