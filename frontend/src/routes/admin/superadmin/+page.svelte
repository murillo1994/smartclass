<script>
    import { onMount } from 'svelte';
    import { api } from '../../services/api';
    import { goto } from '/navigation';

    let metrics = {
        total_tenants: 0,
        active_tenants: 0,
        total_users: 0,
        total_instances: 0,
        connected_instances: 0,
        total_contacts: 0
    };
    let tenants = [];
    let loading = true;
    let error = '';
    let showModal = false;
    let actionLoading = false;

    let newTenant = {
        name: '',
        slug: '',
        document: '',
        admin_name: '',
        admin_email: '',
        admin_password: 'admin123',
        plan_name: 'starter',
        max_users: 3,
        max_instances: 1
    };

    async function loadData() {
        loading = true;
        error = '';
        try {
            const [m, t] = await Promise.all([
                api.getSuperAdminMetrics(),
                api.getSuperAdminTenants()
            ]);
            metrics = m;
            tenants = t;
        } catch (err) {
            error = err.message || 'Erro ao carregar dados do Super Admin';
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        loadData();
    });

    async function handleCreateTenant() {
        if (!newTenant.name || !newTenant.slug || !newTenant.admin_email) {
            alert('Preencha os campos obrigatórios: Nome da Empresa, Slug e E-mail do Administrador.');
            return;
        }
        actionLoading = true;
        try {
            await api.createTenant(newTenant);
            showModal = false;
            newTenant = {
                name: '',
                slug: '',
                document: '',
                admin_name: '',
                admin_email: '',
                admin_password: 'admin123',
                plan_name: 'starter',
                max_users: 3,
                max_instances: 1
            };
            await loadData();
        } catch (err) {
            alert('Erro ao criar empresa: ' + err.message);
        } finally {
            actionLoading = false;
        }
    }

    async function toggleStatus(tenant) {
        const nextStatus = tenant.status === 'active' ? 'suspended' : 'active';
        if (!confirm('Deseja alterar o status de ' + tenant.name + ' para ' + nextStatus.toUpperCase() + '?')) return;
        try {
            await api.updateTenantStatus(tenant.id, nextStatus);
            await loadData();
        } catch (err) {
            alert('Erro ao alterar status: ' + err.message);
        }
    }

    async function handleImpersonate(tenant) {
        if (!confirm('Deseja entrar no CRM corporativo da empresa "' + tenant.name + '" como Suporte Técnico?')) return;
        try {
            await api.impersonateTenant(tenant.id);
            goto('/admin/inbox');
        } catch (err) {
            alert('Erro ao iniciar suporte: ' + err.message);
        }
    }
</script>

<svelte:head>
    <title>Painel Mestre Super Admin — Evolution CRM</title>
</svelte:head>

<div class="superadmin-page">
    <div class="page-header">
        <div>
            <h1>Painel Mestre (Super Admin)</h1>
            <p class="subtitle">Gestão global de empresas clientes, limites contratados e suporte direto</p>
        </div>
        <button class="btn-primary" on:click={() => showModal = true}>
            + Nova Empresa Cliente
        </button>
    </div>

    {#if error}
        <div class="error-banner">{error}</div>
    {/if}

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="label">Empresas Ativas</div>
            <div class="value">{metrics.active_tenants} <span class="subval">/ {metrics.total_tenants}</span></div>
        </div>
        <div class="metric-card">
            <div class="label">Total de Atendentes</div>
            <div class="value">{metrics.total_users}</div>
        </div>
        <div class="metric-card">
            <div class="label">Canais WhatsApp Conectados</div>
            <div class="value">{metrics.connected_instances} <span class="subval">/ {metrics.total_instances}</span></div>
        </div>
        <div class="metric-card">
            <div class="label">Total de Contatos na Base</div>
            <div class="value">{metrics.total_contacts}</div>
        </div>
    </div>

    <div class="table-container">
        <div class="table-header">
            <h2>Empresas Licenciadas</h2>
            <button class="btn-secondary" on:click={loadData} disabled={loading}>
                {loading ? 'Atualizando...' : 'Recarregar'}
            </button>
        </div>

        {#if loading && tenants.length === 0}
            <div class="loading-state">Carregando empresas...</div>
        {:else if tenants.length === 0}
            <div class="empty-state">Nenhuma empresa cliente cadastrada ainda.</div>
        {:else}
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Empresa</th>
                        <th>Slug</th>
                        <th>Admin Titular</th>
                        <th>Plano</th>
                        <th>Usuários</th>
                        <th>WhatsApp</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {#each tenants as t}
                        <tr>
                            <td>
                                <strong>{t.name}</strong>
                                {#if t.document}<div class="doc-text">{t.document}</div>{/if}
                            </td>
                            <td><code>{t.slug}</code></td>
                            <td>
                                <div>{t.admin_name || '—'}</div>
                                <div class="sub-email">{t.admin_email || '—'}</div>
                            </td>
                            <td><span class="badge-plan">{t.plan_name.toUpperCase()}</span></td>
                            <td>{t.users_count} / {t.max_users}</td>
                            <td>{t.instances_count} / {t.max_instances}</td>
                            <td>
                                <span class="status-badge {t.status}">
                                    {t.status === 'active' ? 'Ativa' : t.status === 'suspended' ? 'Suspensa' : t.status}
                                </span>
                            </td>
                            <td>
                                <div class="action-buttons">
                                    <button class="btn-action support" title="Acessar conta para suporte" on:click={() => handleImpersonate(t)}>
                                        Suporte
                                    </button>
                                    <button class="btn-action toggle" on:click={() => toggleStatus(t)}>
                                        {t.status === 'active' ? 'Suspender' : 'Reativar'}
                                    </button>
                                </div>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        {/if}
    </div>
</div>

{#if showModal}
    <div class="modal-backdrop">
        <div class="modal-card">
            <div class="modal-header">
                <h3>Provisionar Nova Empresa Cliente</h3>
                <button class="close-btn" on:click={() => showModal = false}>&times;</button>
            </div>
            <form on:submit|preventDefault={handleCreateTenant} class="modal-form">
                <div class="form-row">
                    <div class="form-group">
                        <label>Nome da Empresa *</label>
                        <input type="text" bind:value={newTenant.name} placeholder="ex: Clínica Bella Vita" required />
                    </div>
                    <div class="form-group">
                        <label>Slug URL (único) *</label>
                        <input type="text" bind:value={newTenant.slug} placeholder="ex: bella-vita" required />
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label>CNPJ / CPF</label>
                        <input type="text" bind:value={newTenant.document} placeholder="00.000.000/0001-00" />
                    </div>
                    <div class="form-group">
                        <label>Plano Contratado</label>
                        <select bind:value={newTenant.plan_name}>
                            <option value="starter">Starter (3 Usuários, 1 WhatsApp)</option>
                            <option value="pro">Pro (10 Usuários, 3 WhatsApps)</option>
                            <option value="enterprise">Enterprise (Ilimitado)</option>
                        </select>
                    </div>
                </div>

                <hr class="divider" />
                <h4 style="margin: 0 0 10px 0; color: #483d39;">Dados do Administrador da Empresa</h4>

                <div class="form-row">
                    <div class="form-group">
                        <label>Nome do Responsável *</label>
                        <input type="text" bind:value={newTenant.admin_name} placeholder="ex: Roberto Carlos" required />
                    </div>
                    <div class="form-group">
                        <label>E-mail de Login *</label>
                        <input type="email" bind:value={newTenant.admin_email} placeholder="admin@bellavita.com" required />
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label>Senha Provisória</label>
                        <input type="password" bind:value={newTenant.admin_password} required />
                    </div>
                    <div class="form-group">
                        <label>Limite de Atendentes</label>
                        <input type="number" bind:value={newTenant.max_users} min="1" max="100" />
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn-secondary" on:click={() => showModal = false}>Cancelar</button>
                    <button type="submit" class="btn-primary" disabled={actionLoading}>
                        {actionLoading ? 'Provisionando...' : 'Criar Empresa & Ativar'}
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}

<style>
    .superadmin-page {
        max-width: 1200px;
        margin: 0 auto;
        padding: 30px 20px;
        font-family: inherit;
    }
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }
    .page-header h1 {
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
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-bottom: 30px;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e8e2de;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .metric-card .label {
        font-size: 0.85rem;
        color: #7a6f68;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .metric-card .value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #2c2523;
        margin-top: 8px;
    }
    .metric-card .subval {
        font-size: 1rem;
        color: #a89f98;
        font-weight: 500;
    }
    .table-container {
        background: #ffffff;
        border: 1px solid #e8e2de;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        overflow: hidden;
    }
    .table-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 24px;
        border-bottom: 1px solid #e8e2de;
    }
    .table-header h2 {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2c2523;
        margin: 0;
    }
    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
        text-align: left;
    }
    .data-table th {
        background: #fbf9f8;
        padding: 12px 18px;
        color: #655953;
        font-weight: 600;
        border-bottom: 1px solid #e8e2de;
    }
    .data-table td {
        padding: 14px 18px;
        border-bottom: 1px solid #f0eae6;
        vertical-align: middle;
    }
    .doc-text, .sub-email {
        font-size: 0.8rem;
        color: #8c827c;
        margin-top: 2px;
    }
    .badge-plan {
        background: #f0eae6;
        color: #5c4e47;
        font-size: 0.75rem;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
    }
    .status-badge {
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 700;
    }
    .status-badge.active {
        background: #dcfce7;
        color: #15803d;
    }
    .status-badge.suspended {
        background: #fee2e2;
        color: #b91c1c;
    }
    .action-buttons {
        display: flex;
        gap: 8px;
    }
    .btn-action {
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
        border: none;
        transition: all 0.15s;
    }
    .btn-action.support {
        background: #3b82f6;
        color: white;
    }
    .btn-action.support:hover {
        background: #2563eb;
    }
    .btn-action.toggle {
        background: #f0eae6;
        color: #483d39;
    }
    .btn-action.toggle:hover {
        background: #e4dcda;
    }
    .btn-primary {
        background: #483d39;
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
    }
    .btn-primary:hover {
        background: #362c28;
    }
    .btn-secondary {
        background: transparent;
        border: 1px solid #d5ccc7;
        color: #5c4e47;
        padding: 8px 14px;
        border-radius: 6px;
        font-size: 0.85rem;
        cursor: pointer;
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
    .modal-card {
        background: white;
        width: 100%;
        max-width: 580px;
        border-radius: 14px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        overflow: hidden;
    }
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 24px;
        background: #fbf9f8;
        border-bottom: 1px solid #e8e2de;
    }
    .modal-header h3 {
        margin: 0;
        font-size: 1.15rem;
        color: #2c2523;
    }
    .close-btn {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: #7a6f68;
    }
    .modal-form {
        padding: 20px 24px;
    }
    .form-row {
        display: flex;
        gap: 16px;
        margin-bottom: 14px;
    }
    .form-group {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    .form-group label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #483d39;
        margin-bottom: 6px;
    }
    .form-group input, .form-group select {
        padding: 9px 12px;
        border: 1px solid #d5ccc7;
        border-radius: 6px;
        font-size: 0.9rem;
    }
    .divider {
        border: none;
        border-top: 1px solid #e8e2de;
        margin: 16px 0;
    }
    .modal-footer {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        margin-top: 20px;
    }
</style>
