<script>
    import { onMount } from 'svelte';
    import Header from '../../../components/Header.svelte';
    import { api } from '../../services/api';

    let doctors = [];
    let selectedDoctor = null;
    let availability = [];
    let loading = true;
    let loadingSchedule = false;
    let error = "";
    let scheduleSuccess = "";
    let scheduleError = "";

    // Form data for creating a new doctor
    let newDocName = "";
    let newDocSpecialty = "";
    let addingDoctor = false;

    // Weekdays label map
    const WEEKDAYS = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"];

    async function loadDoctors() {
        try {
            loading = true;
            doctors = await api.getDoctors();
            if (doctors.length > 0 && !selectedDoctor) {
                await selectDoctor(doctors[0]);
            }
        } catch (err) {
            console.error(err);
            error = "Erro ao carregar médicos.";
        } finally {
            loading = false;
        }
    }

    async function selectDoctor(doc) {
        selectedDoctor = doc;
        loadingSchedule = true;
        scheduleSuccess = "";
        scheduleError = "";
        try {
            const rawAvail = await api.getDoctorAvailability(doc.id);
            
            // Map the raw availability list to a full 7-day array
            // filling missing days as inactive
            availability = Array.from({ length: 7 }, (_, i) => {
                const existing = rawAvail.find(a => a.day_of_week === i);
                return {
                    day_of_week: i,
                    active: !!existing,
                    start_time: existing ? existing.start_time : "09:00",
                    end_time: existing ? existing.end_time : "18:00"
                };
            });
        } catch (err) {
            console.error(err);
            scheduleError = "Erro ao carregar agenda.";
        } finally {
            loadingSchedule = false;
        }
    }

    async function handleAddDoctor(e) {
        e.preventDefault();
        if (!newDocName || !newDocSpecialty) return;
        addingDoctor = true;
        error = "";
        try {
            const res = await api.createDoctor(newDocName.trim(), newDocSpecialty.trim());
            if (res.success) {
                newDocName = "";
                newDocSpecialty = "";
                await loadDoctors();
                // Select the newly created doctor
                const newDoc = doctors.find(d => d.id === res.doctor.id);
                if (newDoc) selectDoctor(newDoc);
            }
        } catch (err) {
            console.error(err);
            error = "Falha ao cadastrar médico.";
        } finally {
            addingDoctor = false;
        }
    }

    async function handleDeleteDoctor(docId) {
        if (!confirm("Tem certeza que deseja remover este especialista? Todos os seus horários e agendamentos serão excluídos.")) return;
        try {
            const res = await api.deleteDoctor(docId);
            if (res.success) {
                if (selectedDoctor && selectedDoctor.id === docId) {
                    selectedDoctor = null;
                    availability = [];
                }
                await loadDoctors();
            }
        } catch (err) {
            console.error(err);
            error = "Erro ao deletar médico.";
        }
    }

    async function handleSaveSchedule() {
        if (!selectedDoctor) return;
        loadingSchedule = true;
        scheduleSuccess = "";
        scheduleError = "";
        
        // Filter only the active days to send to the backend
        const payload = availability
            .filter(a => a.active)
            .map(a => ({
                day_of_week: a.day_of_week,
                start_time: a.start_time,
                end_time: a.end_time
            }));

        try {
            const res = await api.updateDoctorAvailability(selectedDoctor.id, payload);
            if (res.success) {
                scheduleSuccess = "Agenda atualizada com sucesso!";
            }
        } catch (err) {
            console.error(err);
            scheduleError = "Falha ao salvar horários de atendimento.";
        } finally {
            loadingSchedule = false;
        }
    }

    onMount(() => {
        loadDoctors();
    });
</script>

<svelte:head>
    <title>Unic Clinic — Corpo Clínico e Agendas</title>
</svelte:head>

<div class="min-h-screen bg-luxury-black text-white flex flex-col h-screen">
    <Header adminMode={true} />

    {#if loading}
        <div class="flex-1 flex items-center justify-center">
            <span class="text-xs uppercase tracking-widest text-gray-500 animate-pulse">Carregando corpo clínico...</span>
        </div>
    {:else}
        <div class="flex-1 flex overflow-hidden main-layout">
            <!-- Left Column: Doctors List & Form -->
            <div class="w-[360px] border-r border-luxury-border/40 p-6 flex flex-col space-y-6 h-full overflow-y-auto left-panel">
                <div>
                    <h2 class="font-serif text-lg text-luxury-accent">Médicos &amp; Especialistas</h2>
                    <p class="text-[10px] text-gray-400 mt-1">Gerenciamento do corpo clínico ativo na unidade</p>
                </div>

                {#if error}
                    <div class="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-lg text-xs">
                        {error}
                    </div>
                {/if}

                <!-- Add Doctor Form -->
                <form on:submit={handleAddDoctor} class="bg-luxury-card/30 border border-luxury-border/50 p-4 rounded-xl space-y-3">
                    <span class="text-[10px] uppercase font-bold text-luxury-gold tracking-wider block">Novo Especialista</span>
                    
                    <div class="space-y-2">
                        <input 
                            type="text" 
                            bind:value={newDocName} 
                            placeholder="Nome completo (Ex: Dra. Ana Paula)" 
                            required
                            disabled={addingDoctor}
                            class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                        />
                        <input 
                            type="text" 
                            bind:value={newDocSpecialty} 
                            placeholder="Especialidade (Ex: Dermatologista)" 
                            required
                            disabled={addingDoctor}
                            class="w-full bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-2 text-xs text-white outline-none"
                        />
                    </div>

                    <button 
                        type="submit" 
                        disabled={addingDoctor}
                        class="w-full bg-luxury-gold text-luxury-black font-bold py-2 rounded hover:bg-luxury-gold/90 transition text-xs uppercase tracking-wider"
                    >
                        {addingDoctor ? 'Cadastrando...' : 'Cadastrar'}
                    </button>
                </form>

                <!-- Doctors List -->
                <div class="flex-1 space-y-2">
                    <span class="text-[10px] uppercase font-bold text-gray-500 tracking-wider block">Profissionais Cadastrados ({doctors.length})</span>
                    
                    {#each doctors as doc (doc.id)}
                        <button 
                            on:click={() => selectDoctor(doc)}
                            class="w-full flex items-center justify-between p-3.5 rounded-xl border text-left transition-all duration-200 group
                                {selectedDoctor && selectedDoctor.id === doc.id 
                                    ? 'bg-luxury-card border-luxury-gold' 
                                    : 'bg-luxury-card/10 border-luxury-border/40 hover:border-luxury-border hover:bg-luxury-card/20'}"
                        >
                            <div>
                                <p class="text-xs font-semibold text-white group-hover:text-luxury-gold transition duration-200">{doc.name}</p>
                                <p class="text-[10px] text-gray-400 mt-0.5">{doc.specialty}</p>
                            </div>
                            <button 
                                on:click|stopPropagation={() => handleDeleteDoctor(doc.id)}
                                class="text-gray-500 hover:text-red-400 p-1 rounded transition duration-200"
                                title="Excluir profissional"
                            >
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                            </button>
                        </button>
                    {/each}

                    {#if doctors.length === 0}
                        <div class="text-center py-8 text-gray-500 border border-dashed border-luxury-border/20 rounded-xl">
                            <span class="text-[11px]">Nenhum médico cadastrado.</span>
                        </div>
                    {/if}
                </div>
            </div>

            <!-- Right Column: Selected Doctor's availability details -->
            <div class="flex-1 p-6 flex flex-col h-full overflow-y-auto right-panel">
                {#if selectedDoctor}
                    <div class="mb-6 flex justify-between items-start">
                        <div>
                            <h2 class="font-serif text-lg text-luxury-accent">Horários de Atendimento</h2>
                            <p class="text-[10px] text-gray-400 mt-1">Definição dos dias e faixas horárias de trabalho para: <strong class="text-luxury-gold">{selectedDoctor.name}</strong></p>
                        </div>
                        
                        <button 
                            on:click={handleSaveSchedule}
                            disabled={loadingSchedule}
                            class="bg-luxury-gold text-luxury-black font-bold py-2 px-5 rounded hover:bg-luxury-gold/90 transition text-xs uppercase tracking-wider"
                        >
                            {loadingSchedule ? 'Salvando...' : 'Salvar Agenda'}
                        </button>
                    </div>

                    {#if scheduleSuccess}
                        <div class="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 p-3 rounded-lg text-xs mb-4">
                            {scheduleSuccess}
                        </div>
                    {/if}
                    {#if scheduleError}
                        <div class="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-lg text-xs mb-4">
                            {scheduleError}
                        </div>
                    {/if}

                    {#if loadingSchedule && availability.length === 0}
                        <div class="flex-1 flex items-center justify-center">
                            <span class="text-xs uppercase tracking-widest text-gray-500 animate-pulse">Buscando horários da agenda...</span>
                        </div>
                    {:else}
                        <!-- Availability Form Rows -->
                        <div class="space-y-3 bg-luxury-dark/40 border border-luxury-border/50 p-6 rounded-2xl">
                            {#each availability as item (item.day_of_week)}
                                <div class="flex items-center justify-between p-4 rounded-xl border border-luxury-border/30 bg-luxury-card/20 hover:bg-luxury-card/45 transition duration-150 schedule-row">
                                    
                                    <!-- Day selector checkbox -->
                                    <div class="flex items-center space-x-3 w-[180px]">
                                        <input 
                                            type="checkbox" 
                                            id={`day-${item.day_of_week}`}
                                            bind:checked={item.active}
                                            class="w-4 h-4 rounded border-luxury-border text-luxury-gold bg-luxury-card focus:ring-0 outline-none"
                                        />
                                        <label for={`day-${item.day_of_week}`} class="text-xs font-semibold select-none cursor-pointer {item.active ? 'text-white' : 'text-gray-500'}">
                                            {WEEKDAYS[item.day_of_week]}
                                        </label>
                                    </div>

                                    <!-- Hours inputs -->
                                    <div class="flex items-center space-x-3">
                                        <span class="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Entrada</span>
                                        <input 
                                            type="text" 
                                            bind:value={item.start_time}
                                            placeholder="09:00"
                                            disabled={!item.active}
                                            class="w-[75px] bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-1.5 text-xs text-white text-center outline-none disabled:opacity-30 transition duration-150"
                                        />

                                        <span class="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Saída</span>
                                        <input 
                                            type="text" 
                                            bind:value={item.end_time}
                                            placeholder="18:00"
                                            disabled={!item.active}
                                            class="w-[75px] bg-luxury-card border border-luxury-border/80 focus:border-luxury-gold rounded px-3 py-1.5 text-xs text-white text-center outline-none disabled:opacity-30 transition duration-150"
                                        />
                                    </div>
                                </div>
                            {/each}
                        </div>
                    {/if}
                {:else}
                    <div class="flex-1 flex flex-col items-center justify-center text-gray-500 py-24 space-y-2">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="opacity-40"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                        <span class="text-xs uppercase tracking-widest opacity-60">Selecione um profissional para configurar sua agenda</span>
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

        .schedule-row {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 1rem !important;
        }
    }
</style>
