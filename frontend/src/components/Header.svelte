<script>
    import { onMount } from 'svelte';
    import { api } from '../routes/services/api';
    
    export let logo = "";
    export let adminMode = true;

    let isLightMode = false;
    let currentUser = null;
    let currentTenant = null;

    onMount(() => {
        if (typeof window !== 'undefined') {
            isLightMode = localStorage.getItem('admin_theme') === 'light';
            applyTheme();
            
            try {
                currentUser = JSON.parse(localStorage.getItem('crm_user') || 'null');
                currentTenant = JSON.parse(localStorage.getItem('crm_tenant') || 'null');
            } catch (e) {
                console.error(e);
            }
        }
    });

    function toggleTheme() {
        isLightMode = !isLightMode;
        if (typeof window !== 'undefined') {
            localStorage.setItem('admin_theme', isLightMode ? 'light' : 'dark');
            applyTheme();
        }
    }

    function applyTheme() {
        if (typeof window !== 'undefined') {
            if (isLightMode) {
                document.documentElement.classList.add('theme-light');
            } else {
                document.documentElement.classList.remove('theme-light');
            }
        }
    }

    function handleLogout() {
        api.logout();
    }
</script>

<header class="main-header">
    <!-- Brand / Tenant Info -->
    <div class="brand-wrap">
        <a href={currentUser?.role === 'superadmin' ? '/admin/superadmin' : '/admin/inbox'} class="logo-link">
            <span class="logo-text">EVOLUTION CRM</span>
            {#if currentTenant}
                <span class="tenant-tag">{currentTenant.name}</span>
            {:else if currentUser?.role === 'superadmin'}
                <span class="tenant-tag super">SUPER ADMIN</span>
            {/if}
        </a>
    </div>

    <!-- Navegação Adaptativa por Papel -->
    <nav class="nav-links">
        {#if currentUser?.role === 'superadmin'}
            <a href="/admin/superadmin" class="nav-item">🏢 Painel Mestre</a>
        {:else}
            <a href="/admin/inbox" class="nav-item">📥 Inbox WhatsApp</a>
            <a href="/admin/crm" class="nav-item">📊 Funil Kanban</a>
            {#if currentUser?.role === 'admin'}
                <a href="/admin/whatsapp" class="nav-item">📱 Canais WhatsApp</a>
            {/if}
        {/if}

        <div class="user-profile">
            {#if currentUser}
                <div class="user-details">
                    <span class="user-name">{currentUser.name}</span>
                    <span class="user-role">{currentUser.role === 'superadmin' ? 'Master' : currentUser.role === 'admin' ? 'Gestor' : 'Atendente'}</span>
                </div>
            {/if}

            <button on:click={handleLogout} class="btn-logout" title="Sair da Conta">
                Sair
            </button>
        </div>
    </nav>
</header>

<style>
    .main-header {
        background: #ffffff;
        border-bottom: 1px solid #e8e2de;
        position: sticky;
        top: 0;
        z-index: 50;
        padding: 0 24px;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .brand-wrap {
        display: flex;
        align-items: center;
    }
    .logo-link {
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
    }
    .logo-text {
        font-family: inherit;
        font-weight: 800;
        font-size: 1.15rem;
        letter-spacing: -0.01em;
        color: #2c2523;
    }
    .tenant-tag {
        font-size: 0.75rem;
        background: #f0eae6;
        color: #5c4e47;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
    }
    .tenant-tag.super {
        background: #e0e7ff;
        color: #3730a3;
    }
    .nav-links {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .nav-item {
        font-size: 0.88rem;
        font-weight: 600;
        color: #5c4e47;
        text-decoration: none;
        padding: 6px 12px;
        border-radius: 6px;
        transition: all 0.15s;
    }
    .nav-item:hover {
        background: #f8f6f4;
        color: #2c2523;
    }
    .user-profile {
        display: flex;
        align-items: center;
        gap: 14px;
        border-left: 1px solid #e8e2de;
        padding-left: 16px;
    }
    .user-details {
        display: flex;
        flex-direction: column;
        text-align: right;
    }
    .user-name {
        font-size: 0.85rem;
        font-weight: 700;
        color: #2c2523;
    }
    .user-role {
        font-size: 0.7rem;
        color: #8c827c;
        text-transform: uppercase;
    }
    .btn-logout {
        font-size: 0.8rem;
        color: #dc2626;
        background: #fef2f2;
        border: 1px solid #fee2e2;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.15s;
    }
    .btn-logout:hover {
        background: #fee2e2;
    }
</style>
