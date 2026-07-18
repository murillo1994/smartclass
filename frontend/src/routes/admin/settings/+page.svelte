<script>
    import { onMount } from 'svelte';
    import Header from '../../../components/Header.svelte';
    import { api } from '../../services/api';

    let settings = {
        clinic_name: "Unic Clinic",
        clinic_responsible: "",
        clinic_address: "",
        clinic_phones: "",
        clinic_addresses: "[]",
        clinic_phones_list: "[]",
        clinic_instagram: "",
        clinic_working_hours: "Segunda a Sexta, das 09:00 às 18:00",
        clinic_custom_notes: "",
        beta_mode_enabled: true,
        beta_allowed_numbers: "",
        auto_activate_ai_for_new_leads: false
    };

    // Reactively managed arrays for the form UI
    let addresses = [{ label: "Unidade Principal", address: "" }];
    let phones = [{ label: "Contato Principal", phone: "" }];

    let loading = true;
    let saving = false;
    let successMsg = "";
    let errorMsg = "";

    async function loadSettings() {
        try {
            loading = true;
            const res = await api.getSettings();
            if (res) {
                settings = {
                    clinic_name: res.clinic_name || "Unic Clinic",
                    clinic_responsible: res.clinic_responsible || "",
                    clinic_address: res.clinic_address || "",
                    clinic_phones: res.clinic_phones || "",
                    clinic_addresses: res.clinic_addresses || "[]",
                    clinic_phones_list: res.clinic_phones_list || "[]",
                    clinic_instagram: res.clinic_instagram || "",
                    clinic_working_hours: res.clinic_working_hours || "Segunda a Sexta, das 09:00 às 18:00",
                    clinic_custom_notes: res.clinic_custom_notes || "",
                    beta_mode_enabled: res.beta_mode_enabled !== undefined ? res.beta_mode_enabled : true,
                    beta_allowed_numbers: res.beta_allowed_numbers || "",
                    auto_activate_ai_for_new_leads: res.auto_activate_ai_for_new_leads !== undefined ? res.auto_activate_ai_for_new_leads : false
                };

                // Parse addresses JSON list
                try {
                    const parsedAddrs = JSON.parse(settings.clinic_addresses);
                    if (Array.isArray(parsedAddrs) && parsedAddrs.length > 0) {
                        addresses = parsedAddrs;
                    } else if (settings.clinic_address) {
                        addresses = [{ label: "Unidade Principal", address: settings.clinic_address }];
                    }
                } catch (e) {
                    console.error("Erro ao fazer parse dos endereços", e);
                }

                // Parse phones JSON list
                try {
                    const parsedPhones = JSON.parse(settings.clinic_phones_list);
                    if (Array.isArray(parsedPhones) && parsedPhones.length > 0) {
                        phones = parsedPhones;
                    } else if (settings.clinic_phones) {
                        phones = [{ label: "Contato Principal", phone: settings.clinic_phones }];
                    }
                } catch (e) {
                    console.error("Erro ao fazer parse dos telefones", e);
                }
            }
        } catch (err) {
            console.error(err);
            errorMsg = "Erro ao carregar dados da clínica.";
        } finally {
            loading = false;
        }
    }

    function addAddress() {
        addresses = [...addresses, { label: "", address: "" }];
    }

    function removeAddress(index) {
        addresses = addresses.filter((_, i) => i !== index);
        if (addresses.length === 0) {
            addresses = [{ label: "", address: "" }];
        }
    }

    function addPhone() {
        phones = [...phones, { label: "", phone: "" }];
    }

    function removePhone(index) {
        phones = phones.filter((_, i) => i !== index);
        if (phones.length === 0) {
            phones = [{ label: "", phone: "" }];
        }
    }

    async function handleSave(e) {
        e.preventDefault();
        saving = true;
        successMsg = "";
        errorMsg = "";

        // Sync arrays back to settings object payload
        settings.clinic_addresses = addresses.filter(a => a.address.trim());
        settings.clinic_phones_list = phones.filter(p => p.phone.trim());

        // Keep fallbacks updated for safety
        if (settings.clinic_addresses.length > 0) {
            settings.clinic_address = settings.clinic_addresses[0].address;
        }
        if (settings.clinic_phones_list.length > 0) {
            settings.clinic_phones = settings.clinic_phones_list[0].phone;
        }

        try {
            const res = await api.updateSettings(settings);
            if (res.success) {
                successMsg = "Dados salvos e atualizados no cérebro da IA com sucesso!";
                if (res.settings) {
                    settings = { ...settings, ...res.settings };
                }
            } else {
                errorMsg = "Ocorreu um erro ao salvar as configurações.";
            }
        } catch (err) {
            console.error(err);
            errorMsg = "Falha ao conectar ao servidor.";
        } finally {
            saving = false;
        }
    }

    onMount(() => {
        loadSettings();
    });
</script>

<div class="min-h-screen bg-luxury-black text-white flex flex-col h-screen overflow-y-auto">
    <Header adminMode={true} />

    {#if loading}
        <div class="flex-1 flex items-center justify-center">
            <span class="text-xs uppercase tracking-widest text-gray-500 animate-pulse">Carregando dados da clínica...</span>
        </div>
    {:else}
        <div class="max-w-4xl mx-auto w-full p-6 md:p-12 space-y-8">
            <!-- Header Section -->
            <div class="flex items-center justify-between border-b border-luxury-border/30 pb-6">
                <div>
                    <h1 class="font-serif text-2xl text-luxury-accent">Dados da Clínica</h1>
                    <p class="text-xs text-gray-400 mt-1">Gerencie múltiplos endereços, contatos e parametrizações do Concierge de IA</p>
                </div>
            </div>

            <!-- Form -->
            <form on:submit={handleSave} class="space-y-6">
                {#if successMsg}
                    <div class="bg-luxury-gold/10 border border-luxury-gold/40 text-luxury-accent p-4 rounded-xl text-xs flex items-center space-x-2 animate-fade-in">
                        <span>✨</span>
                        <span>{successMsg}</span>
                    </div>
                {/if}

                {#if errorMsg}
                    <div class="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl text-xs flex items-center space-x-2 animate-fade-in">
                        <span>⚠️</span>
                        <span>{errorMsg}</span>
                    </div>
                {/if}

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    
                    <!-- Left Column: Branches details -->
                    <div class="space-y-6">
                        
                        <!-- General Info -->
                        <div class="space-y-4 bg-luxury-card/20 border border-luxury-border/30 p-6 rounded-2xl">
                            <h2 class="text-xs font-bold uppercase text-luxury-gold tracking-widest border-b border-luxury-border/20 pb-2">Informações Gerais</h2>
                            
                            <div class="space-y-1">
                                <label class="text-[10px] uppercase text-gray-400 block font-semibold">Nome da Empresa/Clínica</label>
                                <input 
                                    type="text" 
                                    bind:value={settings.clinic_name} 
                                    placeholder="Ex: Unic Clinic"
                                    required
                                    class="w-full bg-luxury-black border border-luxury-border/60 focus:border-luxury-gold rounded-xl px-4 py-2.5 text-xs text-white outline-none transition"
                                />
                            </div>

                            <div class="space-y-1">
                                <label class="text-[10px] uppercase text-gray-400 block font-semibold">Responsável Técnico / Direção</label>
                                <input 
                                    type="text" 
                                    bind:value={settings.clinic_responsible} 
                                    placeholder="Ex: Dra. Mariana Rocha"
                                    class="w-full bg-luxury-black border border-luxury-border/60 focus:border-luxury-gold rounded-xl px-4 py-2.5 text-xs text-white outline-none transition"
                                />
                            </div>

                            <div class="grid grid-cols-2 gap-4">
                                <div class="space-y-1">
                                    <label class="text-[10px] uppercase text-gray-400 block font-semibold">Instagram da Clínica</label>
                                    <input 
                                        type="text" 
                                        bind:value={settings.clinic_instagram} 
                                        placeholder="Ex: @unic.clinic"
                                        class="w-full bg-luxury-black border border-luxury-border/60 focus:border-luxury-gold rounded-xl px-4 py-2.5 text-xs text-white outline-none transition"
                                    />
                                </div>
                                <div class="space-y-1">
                                    <label class="text-[10px] uppercase text-gray-400 block font-semibold">Horário de Funcionamento</label>
                                    <input 
                                        type="text" 
                                        bind:value={settings.clinic_working_hours} 
                                        placeholder="Ex: Segunda a Sexta das 9h às 18h"
                                        class="w-full bg-luxury-black border border-luxury-border/60 focus:border-luxury-gold rounded-xl px-4 py-2.5 text-xs text-white outline-none transition"
                                    />
                                </div>
                            </div>
                        </div>

                        <!-- Structured Addresses List -->
                        <div class="space-y-4 bg-luxury-card/20 border border-luxury-border/30 p-6 rounded-2xl">
                            <div class="flex items-center justify-between border-b border-luxury-border/20 pb-2">
                                <h2 class="text-xs font-bold uppercase text-luxury-gold tracking-widest">Endereços / Unidades</h2>
                                <button 
                                    type="button" 
                                    on:click={addAddress} 
                                    class="text-[9px] uppercase tracking-wider text-luxury-accent border border-luxury-accent/30 hover:border-luxury-accent px-2 py-1 rounded bg-luxury-black transition"
                                >
                                    + Adicionar Unidade
                                </button>
                            </div>

                            <div class="space-y-3 max-h-[300px] overflow-y-auto pr-1">
                                {#each addresses as addr, index}
                                    <div class="p-3 bg-luxury-black/40 border border-luxury-border/40 rounded-xl space-y-2 relative">
                                        <button 
                                            type="button" 
                                            on:click={() => removeAddress(index)} 
                                            class="absolute right-3 top-3 text-[10px] text-red-400 hover:text-red-300 font-bold"
                                            title="Excluir Unidade"
                                        >
                                            ✕
                                        </button>
                                        
                                        <div class="space-y-1 pr-6">
                                            <input 
                                                type="text" 
                                                bind:value={addr.label} 
                                                placeholder="Identificação (Ex: Unidade Paulista)" 
                                                required
                                                class="w-full bg-luxury-black border border-luxury-border/50 focus:border-luxury-gold rounded-lg px-3 py-1.5 text-[11px] font-semibold text-luxury-accent outline-none"
                                            />
                                        </div>
                                        <div class="space-y-1">
                                            <input 
                                                type="text" 
                                                bind:value={addr.address} 
                                                placeholder="Endereço completo (Ex: Av. Paulista, 1000 - Cj 52)" 
                                                required
                                                class="w-full bg-luxury-black border border-luxury-border/50 focus:border-luxury-gold rounded-lg px-3 py-1.5 text-[11px] text-white outline-none"
                                            />
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </div>

                    </div>

                    <!-- Right Column: Phones & AI parameters -->
                    <div class="space-y-6">

                        <!-- Structured Phones List -->
                        <div class="space-y-4 bg-luxury-card/20 border border-luxury-border/30 p-6 rounded-2xl">
                            <div class="flex items-center justify-between border-b border-luxury-border/20 pb-2">
                                <h2 class="text-xs font-bold uppercase text-luxury-gold tracking-widest">Telefones para Contato</h2>
                                <button 
                                    type="button" 
                                    on:click={addPhone} 
                                    class="text-[9px] uppercase tracking-wider text-luxury-accent border border-luxury-accent/30 hover:border-luxury-accent px-2 py-1 rounded bg-luxury-black transition"
                                >
                                    + Adicionar Telefone
                                </button>
                            </div>

                            <div class="space-y-3 max-h-[300px] overflow-y-auto pr-1">
                                {#each phones as ph, index}
                                    <div class="p-3 bg-luxury-black/40 border border-luxury-border/40 rounded-xl space-y-2 relative">
                                        <button 
                                            type="button" 
                                            on:click={() => removePhone(index)} 
                                            class="absolute right-3 top-3 text-[10px] text-red-400 hover:text-red-300 font-bold"
                                            title="Excluir Contato"
                                        >
                                            ✕
                                        </button>
                                        
                                        <div class="space-y-1 pr-6">
                                            <input 
                                                type="text" 
                                                bind:value={ph.label} 
                                                placeholder="Identificação (Ex: WhatsApp Unidade Paulista)" 
                                                required
                                                class="w-full bg-luxury-black border border-luxury-border/50 focus:border-luxury-gold rounded-lg px-3 py-1.5 text-[11px] font-semibold text-luxury-accent outline-none"
                                            />
                                        </div>
                                        <div class="space-y-1">
                                            <input 
                                                type="text" 
                                                bind:value={ph.phone} 
                                                placeholder="Telefone (Ex: 11 99999-9999)" 
                                                required
                                                class="w-full bg-luxury-black border border-luxury-border/50 focus:border-luxury-gold rounded-lg px-3 py-1.5 text-[11px] text-white outline-none"
                                            />
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </div>

                        <!-- AI Instructions -->
                        <div class="space-y-4 bg-luxury-card/20 border border-luxury-border/30 p-6 rounded-2xl">
                            <h2 class="text-xs font-bold uppercase text-luxury-gold tracking-widest border-b border-luxury-border/20 pb-2">Instruções para o Robô</h2>
                            
                            <div class="space-y-1">
                                <label class="text-[10px] uppercase text-gray-400 block font-semibold">Observações Customizadas da Clínica</label>
                                <textarea 
                                    bind:value={settings.clinic_custom_notes} 
                                    placeholder="Ex: Dispomos de manobrista no local. Recomendamos suspender anticoagulantes antes do microagulhamento..."
                                    rows="4"
                                    class="w-full bg-luxury-black border border-luxury-border/60 focus:border-luxury-gold rounded-xl px-4 py-3 text-xs text-white outline-none transition resize-none"
                                ></textarea>
                                <span class="text-[9px] text-gray-500 block">Essas anotações complementam a base de conhecimento do robô em tempo real.</span>
                            </div>
                        </div>

                        <!-- Sandbox / Security parameters -->
                        <div class="bg-luxury-card/20 border border-luxury-border/30 p-6 rounded-2xl space-y-4">
                            <h2 class="text-xs font-bold uppercase text-luxury-gold tracking-widest border-b border-luxury-border/20 pb-2">Segurança do Robô (Sandbox & IA)</h2>

                            <div class="flex items-center justify-between">
                                <div>
                                    <span class="text-[11px] font-semibold block">Modo Beta Restrito (Whitelist)</span>
                                    <span class="text-[9px] text-gray-400">A IA responderá apenas para os números autorizados.</span>
                                </div>
                                <input 
                                    type="checkbox" 
                                    bind:checked={settings.beta_mode_enabled} 
                                    class="w-4 h-4 accent-luxury-gold"
                                />
                            </div>

                            <div class="flex items-center justify-between">
                                <div>
                                    <span class="text-[11px] font-semibold block">Auto-ativar IA para Novos Leads</span>
                                    <span class="text-[9px] text-gray-400">Novos contatos começam com robô ativo automaticamente.</span>
                                </div>
                                <input 
                                    type="checkbox" 
                                    bind:checked={settings.auto_activate_ai_for_new_leads} 
                                    class="w-4 h-4 accent-luxury-gold"
                                />
                            </div>

                            {#if settings.beta_mode_enabled}
                                <div class="space-y-1 pt-2 border-t border-luxury-border/10">
                                    <label class="text-[10px] uppercase text-gray-400 block font-semibold">Números de Telefone Autorizados</label>
                                    <textarea 
                                        bind:value={settings.beta_allowed_numbers} 
                                        placeholder="Ex: 5511999999999, 5511988888888"
                                        rows="2"
                                        class="w-full bg-luxury-black border border-luxury-border/60 focus:border-luxury-gold rounded-xl px-4 py-2 text-xs text-white outline-none transition resize-none"
                                    ></textarea>
                                </div>
                            {/if}
                        </div>

                    </div>

                </div>

                <!-- Save button -->
                <div class="flex justify-end pt-4">
                    <button 
                        type="submit" 
                        disabled={saving}
                        class="bg-luxury-gold text-luxury-black font-bold px-8 py-3.5 rounded-xl hover:bg-luxury-gold/90 transition duration-200 text-xs uppercase tracking-wider disabled:opacity-50"
                    >
                        {saving ? 'Salvando Configurações...' : 'Salvar Alterações'}
                    </button>
                </div>
            </form>
        </div>
    {/if}
</div>
